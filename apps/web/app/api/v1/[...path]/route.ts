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
  ]) {
    const value = request.headers.get(name);
    if (value) headers.set(name, value);
  }
  const body = ["GET", "HEAD"].includes(request.method)
    ? undefined
    : await request.text();
  if (body && body.length > 16384) return new Response(null, { status: 413 });
  try {
    const result = await fetch(
      `${origin}/api/v1/${path.join("/")}${request.nextUrl.search}`,
      {
        method: request.method,
        headers,
        body,
        cache: "no-store",
        redirect: "error",
        signal: AbortSignal.timeout(15000),
      },
    );
    const output = new Headers({
      "Content-Type": "application/json",
      "Cache-Control": "no-store",
    });
    for (const name of ["x-request-id", "retry-after"]) {
      const value = result.headers.get(name);
      if (value) output.set(name, value);
    }
    for (const value of result.headers.getSetCookie())
      output.append("Set-Cookie", value);
    return new Response(await result.text(), {
      status: result.status,
      headers: output,
    });
  } catch {
    return Response.json(
      { error: { message: "API unavailable. Try again shortly." } },
      { status: 503 },
    );
  }
}

export { proxy as GET, proxy as POST, proxy as PATCH, proxy as DELETE };
