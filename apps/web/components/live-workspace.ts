"use client";
import { useEffect, useRef, useState } from "react";

export function useLiveWorkspace(
  transport: typeof fetch,
  organization: string,
  refresh: () => Promise<void>,
) {
  const callback = useRef(refresh);
  const [status, setStatus] = useState("Connecting to saved changes…");
  useEffect(() => {
    callback.current = refresh;
  }, [refresh]);
  useEffect(() => {
    const abort = new AbortController();
    let last = "";
    let timer: ReturnType<typeof setTimeout> | undefined;
    let retry: ReturnType<typeof setTimeout> | undefined;
    function changed() {
      if (timer) return;
      timer = setTimeout(() => {
        timer = undefined;
        void callback
          .current()
          .catch(() => setStatus("Refresh failed. Use Refresh to retry."));
      }, 300);
    }
    async function connect() {
      try {
        const r = await transport(
          new Request(window.location.origin + "/api/v1/workspace/events", {
            signal: abort.signal,
            headers: { "last-event-id": last },
          }),
        );
        if (!r.ok || !r.body) throw new Error("Stream unavailable");
        setStatus("Listening for saved changes");
        const reader = r.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";
        while (!abort.signal.aborted) {
          const { value, done } = await reader.read();
          if (done) break;
          buffer += decoder.decode(value, { stream: true });
          let split;
          while ((split = buffer.indexOf("\n\n")) >= 0) {
            const frame = buffer.slice(0, split);
            buffer = buffer.slice(split + 2);
            if (frame.includes("event: access_revoked")) {
              setStatus("Access changed. Sign in again.");
              abort.abort();
              return;
            }
            const id = frame.match(/^id: (.+)$/m)?.[1];
            if (frame.includes("event: changed") && id && id !== last) {
              const alreadyConnected = !!last;
              last = id;
              if (alreadyConnected)
                setStatus(
                  "Saved change received " + new Date().toLocaleTimeString(),
                );
              if (alreadyConnected) changed();
            }
          }
        }
      } catch {
        if (abort.signal.aborted) return;
      }
      if (!abort.signal.aborted) {
        setStatus("Reconnecting; snapshot may be stale");
        retry = setTimeout(() => void connect(), 3000);
      }
    }
    void connect();
    return () => {
      abort.abort();
      clearTimeout(timer);
      clearTimeout(retry);
    };
  }, [transport, organization]);
  return status;
}
