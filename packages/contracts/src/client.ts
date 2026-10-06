import createClient from "openapi-fetch";
import type { paths } from "./schema";

/** Runtime transport typed directly from the committed backend OpenAPI schema. */
export function createApiClient(baseUrl: string, transport?: typeof fetch) {
  return createClient<paths>({ baseUrl, fetch: transport });
}
