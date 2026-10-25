import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { readFileSync } from "node:fs";

test("Sprint 12 import history, freeze dataset, reproduce CPU baseline and withdraw", async ({
  page,
}) => {
  test.setTimeout(180000);
  page.setDefaultTimeout(20000);
  test.skip(!process.env.PPM_IDENTITY_FIXTURE, "Use isolated browser runner");
  const f = JSON.parse(readFileSync(process.env.PPM_IDENTITY_FIXTURE!, "utf8"));
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto("/login");
  await page.getByLabel("Email address", { exact: true }).fill(f.agent_email);
  await page.getByLabel("Password", { exact: true }).fill(f.password);
  await page.getByRole("button", { name: "Sign in", exact: true }).click();
  await expect(
    page.getByRole("button", { name: "Sign out", exact: true }),
  ).toBeVisible();
  await page.goto("/ml");
  await expect(
    page.getByRole("heading", { name: "History & baseline lab" }),
  ).toBeVisible();
  await page
    .getByRole("combobox", { name: "History project", exact: true })
    .selectOption(f.agent_project);
  await page
    .getByRole("button", { name: "Load synthetic example", exact: true })
    .click();
  await expect(
    page.getByLabel("History import JSON", { exact: true }),
  ).toHaveValue(/synthetic/, { timeout: 20000 });
  await page
    .getByRole("button", { name: "Import history version", exact: true })
    .click();
  await expect(
    page.getByRole("status").filter({ hasText: "Imported version" }),
  ).toBeVisible();
  await page
    .getByRole("button", { name: "Build dataset version", exact: true })
    .click();
  await expect(
    page.getByRole("status").filter({ hasText: "Dataset frozen: demo_only" }),
  ).toBeVisible();
  await page
    .getByRole("button", { name: "Run CPU baseline", exact: true })
    .click();
  const card = page.getByRole("region", { name: "Model card", exact: true });
  await expect(
    card.getByRole("heading", { name: "Model card · succeeded" }),
  ).toBeVisible({ timeout: 60000 });
  await expect(card).toContainText("SYNTHETIC DEMO ONLY");
  await expect(card).toContainText("BLOCKED");
  await page
    .getByRole("button", { name: "Run CPU baseline", exact: true })
    .click();
  await expect(card).toContainText(
    "Reproduction matches previous result: true",
    { timeout: 60000 },
  );
  const downloadPromise = page.waitForEvent("download");
  await page
    .getByRole("button", {
      name: "Download model card & artifacts",
      exact: true,
    })
    .click();
  expect((await downloadPromise).suggestedFilename()).toMatch(
    /^baseline-.+\.json$/,
  );
  for (const width of [1440, 768, 360]) {
    await page.setViewportSize({ width, height: 1000 });
    expect(
      (
        await new AxeBuilder({ page })
          .withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"])
          .analyze()
      ).violations,
    ).toEqual([]);
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    ).toBe(true);
    await page.screenshot({
      path: `test-results/sprint12-lab-${width}.png`,
      fullPage: true,
    });
  }
  await page
    .getByRole("button", { name: /^Withdraw Synthetic delay history v/ })
    .first()
    .click();
  await expect(
    page.getByRole("status").filter({ hasText: "History withdrawn" }),
  ).toBeVisible();
  expect(errors).toEqual([]);
});

test("connector authority, local edit conflict and reviewed resolution are usable", async ({
  page,
}) => {
  test.setTimeout(120000);
  page.setDefaultTimeout(20000);
  test.skip(!process.env.PPM_IDENTITY_FIXTURE, "Use isolated browser runner");
  const f = JSON.parse(readFileSync(process.env.PPM_IDENTITY_FIXTURE!, "utf8"));
  await page.goto("/login");
  await page.getByLabel("Email address", { exact: true }).fill(f.agent_email);
  await page.getByLabel("Password", { exact: true }).fill(f.password);
  await page.getByRole("button", { name: "Sign in", exact: true }).click();
  await expect(
    page.getByRole("button", { name: "Sign out", exact: true }),
  ).toBeVisible();
  const csrf = (await page.context().cookies()).find(
    (c) => c.name === "ppm_csrf",
  )!.value;
  const headers = {
    origin: process.env.PPM_WEB_URL!,
    "x-csrf-token": csrf,
    "x-organization-id": f.agent_org,
    "idempotency-key": crypto.randomUUID(),
  };
  // Derive active tenant from the existing authenticated account, never a guessed fixture field.
  const account = await (await page.request.get("/api/v1/auth/me")).json();
  headers["x-organization-id"] = account.organization_id;
  const created = await page.request.post("/api/v1/integrations", {
    headers,
    data: {
      name: "Sprint12 source review",
      provider: "csv",
      project_id: f.agent_project,
      source_namespace: "sprint12-browser",
      mapping: {
        external_id: "id",
        name: "name",
        source_updated_at: "updated_at",
      },
    },
  });
  expect(created.status(), await created.text()).toBe(201);
  const integration = await created.json();
  await page.goto("/integrations");
  await page
    .getByRole("combobox", { name: "Connection", exact: true })
    .selectOption(integration.id);
  await page
    .getByRole("button", {
      name: "Approve / rotate connector authority",
      exact: true,
    })
    .click();
  await expect(
    page.getByRole("status").filter({ hasText: "authority approved" }),
  ).toBeVisible();
  async function sync(text: string) {
    const result = await page.request.post(
      `/api/v1/integrations/${integration.id}/sync`,
      {
        headers: { ...headers, "idempotency-key": crypto.randomUUID() },
        data: { csv_text: text },
      },
    );
    expect(result.status(), await result.text()).toBe(202);
    const job = await result.json();
    await expect
      .poll(
        async () =>
          (
            await (
              await page.request.get(
                `/api/v1/integrations/activity/jobs/${job.id}`,
              )
            ).json()
          ).status,
        { timeout: 45000 },
      )
      .toMatch(/succeeded/);
  }
  await sync(
    "id,name,updated_at\nreview-1,Upstream original,2026-10-01T00:00:00Z",
  );
  const evidence = await (
    await page.request.get(`/api/v1/integrations/${integration.id}/sources`)
  ).json();
  const work = await (
    await page.request.get(
      `/api/v1/delivery/work_items/${evidence[0].target_id}`,
    )
  ).json();
  const edited = await page.request.patch(
    `/api/v1/delivery/work_items/${work.id}`,
    {
      headers: { ...headers, "if-match": String(work.revision) },
      data: { ...work.data, name: "Protected local edit" },
    },
  );
  expect(edited.status(), await edited.text()).toBe(200);
  await sync(
    "id,name,updated_at\nreview-1,Upstream proposed,2026-10-02T00:00:00Z",
  );
  await page
    .getByRole("button", { name: "Refresh source conflicts", exact: true })
    .click();
  await expect(
    page.getByRole("table", {
      name: "Current saved local values and proposed source values",
    }),
  ).toContainText("Protected local edit");
  await page.screenshot({
    path: "test-results/sprint12-source-conflict.png",
    fullPage: true,
  });
  expect(
    (
      await new AxeBuilder({ page })
        .withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"])
        .analyze()
    ).violations,
  ).toEqual([]);
  await page
    .getByRole("button", { name: "Keep local edits", exact: true })
    .click();
  await expect(
    page.getByRole("status").filter({ hasText: "Reviewed conflict resolved" }),
  ).toBeVisible();
  await page
    .getByRole("button", { name: "Revoke connector authority", exact: true })
    .click();
  await expect(
    page.getByRole("status").filter({ hasText: "Connector revoked" }),
  ).toBeVisible();
});
