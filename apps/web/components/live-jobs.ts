"use client";
import { useEffect, useState } from "react";
import type { components } from "@ppm/contracts/schema";

type Job = components["schemas"]["JobView"];
type Stage = components["schemas"]["StageView"];
const terminal = new Set([
  "succeeded",
  "partially_succeeded",
  "failed",
  "cancelled",
]);

/** Poll for authorized run discovery; SSE is persisted progress, snapshots remain authoritative. */
export function useLiveJobs(
  onChange: () => Promise<void>,
  transport: typeof fetch,
) {
  const [status, setStatus] = useState("Checking sync activity…");
  useEffect(() => {
    const controller = new AbortController();
    const cursors = new Map<string, number>();
    const subscriptions = new Set<string>();
    const seen = new Map<string, string>();
    let initialized = false;
    async function subscribe(id: string) {
      subscriptions.add(id);
      try {
        const response = await transport(
          new Request(
            window.location.origin +
              `/api/v1/integrations/activity/jobs/${id}/events`,
            {
              headers: { "last-event-id": String(cursors.get(id) || 0) },
              signal: controller.signal,
            },
          ),
        );
        if (!response.ok || !response.body)
          throw new Error("Sync progress unavailable");
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";
        setStatus("Listening to authorized sync progress");
        while (!controller.signal.aborted) {
          const next = await reader.read();
          if (next.done) break;
          buffer += decoder.decode(next.value, { stream: true });
          let boundary;
          while ((boundary = buffer.indexOf("\n\n")) >= 0) {
            const block = buffer.slice(0, boundary);
            buffer = buffer.slice(boundary + 2);
            if (block.includes("event: access_revoked"))
              throw new Error("Sync access changed; refresh scope");
            if (block.includes("event: resync_required")) {
              const snapshotResponse = await transport(
                new Request(
                  window.location.origin +
                    `/api/v1/integrations/activity/jobs/${id}`,
                  { signal: controller.signal },
                ),
              );
              if (!snapshotResponse.ok)
                throw new Error("Sync scope unavailable");
              const snapshot: Job = await snapshotResponse.json();
              cursors.set(id, snapshot.sequence);
              await onChange();
            }
            if (block.includes("event: stage")) {
              const data = block
                .split("\n")
                .find((line) => line.startsWith("data: "));
              if (!data) continue;
              const event: Stage = JSON.parse(data.slice(6));
              cursors.set(id, event.sequence);
              if (["completed", "degraded"].includes(event.stage)) {
                await onChange();
                setStatus("Dashboard refreshed after sync");
              }
            }
          }
        }
      } catch {
        if (!controller.signal.aborted)
          setStatus("Live progress interrupted; checking current activity");
      } finally {
        subscriptions.delete(id);
      }
    }
    void (async () => {
      while (!controller.signal.aborted) {
        try {
          const response = await transport(
            new Request(
              window.location.origin + "/api/v1/integrations/activity/jobs",
              { signal: controller.signal },
            ),
          );
          if (!response.ok) throw new Error();
          const jobs: Job[] = await response.json();
          for (const job of jobs) {
            const version = `${job.status}:${job.sequence}`;
            if (
              initialized &&
              seen.get(job.id) !== version &&
              terminal.has(job.status)
            )
              await onChange();
            seen.set(job.id, version);
            if (
              !terminal.has(job.status) &&
              !subscriptions.has(job.id) &&
              subscriptions.size < 5
            )
              void subscribe(job.id);
          }
          initialized = true;
          if (!jobs.some((job) => !terminal.has(job.status)))
            setStatus("No active sync jobs; checking for changes");
        } catch {
          if (!controller.signal.aborted)
            setStatus("Sync activity unavailable; dashboard snapshot retained");
        }
        await new Promise((resolve) => setTimeout(resolve, 3000));
      }
    })();
    return () => controller.abort();
  }, [onChange, transport]);
  return status;
}
