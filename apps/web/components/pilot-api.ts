"use client";
import { useCallback } from "react";
import { apiError } from "./api-error";
export function usePilotApi(transport: typeof fetch) {
  return useCallback(
    async <T>(
      path: string,
      method = "GET",
      body?: unknown,
      revision?: number,
    ): Promise<T> => {
      const r = await transport(
        new Request(window.location.origin + "/api/v1/" + path, {
          method,
          headers: {
            "content-type": "application/json",
            "idempotency-key": crypto.randomUUID(),
            ...(revision == null ? {} : { "if-match": String(revision) }),
          },
          body: body === undefined ? undefined : JSON.stringify(body),
        }),
      );
      if (!r.ok)
        throw new Error(apiError(await r.json().catch(() => null), r.status));
      return r.json();
    },
    [transport],
  );
}
