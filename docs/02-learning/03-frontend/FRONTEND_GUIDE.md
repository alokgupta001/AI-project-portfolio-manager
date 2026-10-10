# The frontend: forms, requests and screen updates

[Learning roadmap](../00-getting-started/README.md) Â· Next: [backend](../02-backend/BACKEND_GUIDE.md)

## React and Next.js

**What are they?** React turns component code and current state into a screen. Next.js supplies the page routing, server features and build process around React.

**Why here?** AI-PPM needs forms, project lists, account screens and dashboards. It also needs a server route that forwards browser requests to the Python backend.

**Where?** Pages live under `apps/web/app`. For example, `projects/page.tsx` opens the project workspace and `command-center/page.tsx` opens the dashboards. `app/layout.tsx` supplies the root layout. Interactive components live under `apps/web/components`.

**Real example:** `RecordEditor` in [`delivery.tsx`](../../../apps/web/components/delivery.tsx) contains:

```typescript
const [values, setValues] = useState(initial);
const [error, setError] = useState("");
const [busy, setBusy] = useState(false);
const [command] = useState(() => crypto.randomUUID());
```

`values` holds the current form fields; `setValues` changes them. `error` holds a message shown when saving fails. `busy` tells the UI a request is running. `command` is created once for this editor instance and identifies the create request on retries.

**Internally:** changing state asks React to render again. Submitting calls `save`, which makes an HTTP request. On success, `onSaved` changes the parent's refresh state and its effect reloads server records. React state by itself does not update PostgreSQL.

**If something goes wrong:** `save` catches the request error and updates `error`. The form keeps the fields the user entered. The backend still checks permissions even if someone manually calls an action hidden by the UI.

**Remember:** React displays state; Next.js selects pages and forwards API requests; PostgreSQL remains the stored source of records. Read [the complete flow](../02-backend/REQUEST_LIFECYCLE.md) for the actual POST call.

## TypeScript and the generated API client

**What?** TypeScript checks JavaScript types during development. A contract describes which paths, fields and response types an API uses.

**Why here?** The frontend and Python backend should agree about names such as `revision`, `portfolio_id` and `ProjectInput`. Generating types avoids maintaining a second handwritten definition for every backend schema.

**Where?** Backend schemas produce `packages/contracts/openapi.json`; `scripts/contracts.mjs` produces `packages/contracts/src/schema.d.ts`. [`client.ts`](../../../packages/contracts/src/client.ts) uses those types:

```typescript
export function createApiClient(baseUrl: string, transport?: typeof fetch) {
  return createClient<paths>({ baseUrl, fetch: transport });
}
```

The function accepts the website URL and an optional fetch function. `<paths>` connects the client methods to generated route types. The returned client offers typed methods such as `GET`, `POST` and `PATCH`.

**Internally:** types catch many wrong calls before the app runs. They disappear from the running JavaScript. Pydantic performs runtime validation on the backend. A TypeScript cast such as `body as DeliveryInput` does not check an actual JSON object.

**If something goes wrong:** an unregenerated schema can leave frontend types behind backend changes. `npm run contracts:check` detects generated-contract drift. A correctly typed call may still receive 401, 403, 409 or another runtime error.

**Remember:** generated types help developers; server checks protect runtime operations; regenerate contracts after changing backend request or response schemas.

## Shared transport and the Next.js proxy

`transport` in [`identity-client.tsx`](../../../apps/web/app/account/identity-client.tsx) is the actual shared fetch function. It obtains a CSRF token, adds the active organization header and retries an eligible 401 after one shared refresh attempt within that page. The account's organization comes from `/auth/me`, not an arbitrary form field. Login credentials stay in cookies.

The proxy in [`app/api/v1/[...path]/route.ts`](../apps/web/app/api/v1/[...path]/route.ts) reads its configured `API_ORIGIN`, forwards a fixed list of headers, bounds the body size and waits at most 15 seconds for the backend. It forwards cookies returned by login or refresh individually. If the upstream request fails, it returns 503 with a safe message.

Assessment and command-center components also have local API wrappers over the shared transport. Do not assume every request uses the generated client merely because the component imports generated response types.

## Which component should I open?

| Screen | Main component | Where its displayed data comes from |
| --- | --- | --- |
| Projects and delivery | `components/delivery.tsx:Delivery`, `RecordEditor`; `delivery-fields.ts` | Delivery list/detail/summary routes |
| Resource planning | `components/capacity.tsx:Capacity` | Delivery resource records and calculated capacity routes |
| Assessments | `components/assessments.tsx:Assessments` | Framework, answer and review routes |
| Dashboards | `components/command-center.tsx:CommandCenter` | One `/api/v1/command/snapshot` response |
| Login and account | `app/account/identity-client.tsx:IdentityClient` | Authentication and organization routes |
| Shared layout | `components/shell.tsx`, `ui.tsx` | Account/navigation state and component props |

Styling uses `app/globals.css`, Tailwind/PostCSS and shared UI components. `ui.tsx:Modal` uses a native dialog, opens it on state change and restores focus on cleanup. The existing app uses local React state; no Redux or React Query layer needs to be imagined.

**Try reading:** find `RecordEditor.save`, then find its `onSaved` caller. Explain why a second fetch happens. `tests/browser/delivery.spec.ts` checks the real browser workflow; `shell.spec.ts` covers shared UI behavior. Read [verification limits](../08-deployment-and-operations/OPERATIONS_AND_LIMITS.md) before treating those tests as proof of universal accessibility.


## Source-reviewed Sprint 8.1 update — 9 October 2026

Open `apps/web/components/pilot.tsx` for setup/My work, `pilot-api.ts` for transport, `shell.tsx` for the record palette, and `record-select.tsx` for paged selectors. Input changes request a server page; a result carries its authorized destination. Selection opens the owning page, which fetches the record again. Empty results mean no permitted matches; a 401 or changed organization must not reuse another scope’s records. Debug Network requests, active organization and component error state; reproduce two profiles with `tests/browser/pilot.spec.ts`.

Status: **IMPLEMENTED AND VERIFIED** within retained local evidence; external gates stay **BLOCKED** or **IMPLEMENTED BUT UNVERIFIED**. See [current status](../../00-overview/CURRENT_STATUS.md), [8.1 evidence](../../03-sprints/active/sprint-8.1/SPRINT_REPORT.md), [future concept and documentation map](../../09-planning/FEATURE_DOCUMENT_MAPPING.md) and [PLANNED work](../../09-planning/FUTURE_SPRINT_ROADMAP.md).

## Verified Gmail and access update — 10 October 2026

`identity-client.tsx` reads the private fragment token, masks it in the completion form and removes it from the address. The nonsecret action hint selects Reset your password or invitation instructions; it does not authorize the backend operation. Reset success now says Password reset. `pilot.tsx` renders queued/provider-accepted/local/failure labels and browser framework/result Access panels. Role selectors change membership, not record grants. Follow [account email and role access](../05-security/ACCOUNT_EMAIL_AND_ROLE_ACCESS.md).
