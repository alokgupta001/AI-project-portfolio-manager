import { NextRequest } from "next/server";

async function proxy(
  request: NextRequest,
  context: { params: Promise<{ path: string[] }> },
) {
  const { path } = await context.params;
  const origin = process.env.API_ORIGIN;
  if (!origin)
    return Response.json(
      { error: { message: "API unavailable." } },
      { status: 503 },
    );
  if (path.some((part) => !/^[a-zA-Z0-9_-]+$/.test(part)))
    return new Response(null, { status: 400 });
  const headers = new Headers();
  for (const name of [
    "cookie",
    "content-type",
    "origin",
    "x-csrf-token",
    "if-match",
    "x-organization-id",
    "idempotency-key",
    "x-change-reason",
    "last-event-id",
    "x-hub-signature-256",
    "x-github-delivery",
    "x-github-event",
  ]) {
    const value = request.headers.get(name);
    if (value) headers.set(name, value);
  }
  let body: string | undefined;
  if (!["GET", "HEAD"].includes(request.method) && path[0] === "integrations") {
    const reader = request.body?.getReader();
    const decoder = new TextDecoder();
    let size = 0;
    body = "";
    if (reader) {
      while (true) {
        const next = await reader.read();
        if (next.done) break;
        size += next.value.byteLength;
        if (size > 650000) {
          await reader.cancel();
          return new Response(null, { status: 413 });
        }
        body += decoder.decode(next.value, { stream: true });
      }
      body += decoder.decode();
    }
  } else {
    body = ["GET", "HEAD"].includes(request.method)
      ? undefined
      : await request.text();
    if (
      body &&
      body.length >
        (path[0] === "assessment"
          ? 2097152
          : path[0] === "integrations"
            ? 650000
            : 16384)
    )
      return new Response(null, { status: 413 });
  }
  try {
    const result = await fetch(
      `${origin}/api/v1/${path.join("/")}${request.nextUrl.search}`,
      {
        method: request.method,
        headers,
        body,
        cache: "no-store",
        redirect: "error",
        signal:
          path.at(-1) === "events"
            ? request.signal
            : AbortSignal.timeout(15000),
      },
    );
    const output = new Headers({
      "Content-Type": result.headers.get("content-type") || "application/json",
      "Cache-Control": "no-store",
    });
    for (const name of [
      "x-request-id",
      "retry-after",
      "content-disposition",
      "x-content-type-options",
    ]) {
      const value = result.headers.get(name);
      if (value) output.set(name, value);
    }
    for (const value of result.headers.getSetCookie())
      output.append("Set-Cookie", value);
    return new Response(
      result.headers.get("content-type")?.includes("text/event-stream")
        ? result.body
        : await result.text(),
      {
        status: result.status,
        headers: output,
      },
    );
  } catch {
    return Response.json(
      { error: { message: "API unavailable. Try again shortly." } },
      { status: 503 },
    );
  }
}

export {
  proxy as GET,
  proxy as POST,
  proxy as PATCH,
  proxy as PUT,
  proxy as DELETE,
};
