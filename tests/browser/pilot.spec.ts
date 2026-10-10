import { test, expect, type Page } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { readFileSync } from "node:fs";
import { spawnSync } from "node:child_process";

function fixture() {
  test.skip(!process.env.PPM_IDENTITY_FIXTURE, "Use isolated browser runner");
  return JSON.parse(readFileSync(process.env.PPM_IDENTITY_FIXTURE!, "utf8"));
}
async function login(page: Page, email: string, password: string) {
  await page.goto("/login");
  await page.getByLabel("Email address", { exact: true }).fill(email);
  await page.getByLabel("Password", { exact: true }).fill(password);
  await page.getByRole("button", { name: "Sign in", exact: true }).click();
  await expect(
    page.getByRole("button", { name: "Sign out", exact: true }),
  ).toBeVisible();
}
function mail(email: string): { link: string }[] {
  const r = spawnSync(
    "docker",
    [
      "compose",
      "-f",
      "compose.yaml",
      "-f",
      "compose.identity-test.yaml",
      "exec",
      "-T",
      "api",
      "python",
      "scripts/pilot_browser_mail.py",
      email,
    ],
    { encoding: "utf8", env: process.env },
  );
  expect(r.status).toBe(0);
  return JSON.parse(r.stdout);
}
async function accessible(page: Page) {
  const result = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"])
    .analyze();
  expect(
    result.violations.map((v) => ({
      id: v.id,
      nodes: v.nodes.map((n) => n.target),
    })),
  ).toEqual([]);
}
test("verified signup, setup, profile and cancelled invitations", async ({
  page,
}) => {
  test.setTimeout(120000);
  const f = fixture();
  const email = `signup-${crypto.randomUUID()}@example.com`;
  await page.goto("/signup");
  await page.getByLabel("Email address", { exact: true }).fill(email);
  await page
    .getByLabel("Organization name", { exact: true })
    .fill("Fictional Northstar");
  await page
    .getByRole("button", { name: "Send verification instructions" })
    .click();
  await expect(page.getByRole("status")).toContainText("If eligible");
  const link = mail(email)[0].link;
  await page.goto(link);
  await page
    .getByLabel("Display name", { exact: true })
    .fill("Fictional Admin");
  await page
    .getByLabel("Password (12–72 bytes)", { exact: true })
    .fill(f.password);
  await page.getByRole("button", { name: "Verify and continue" }).click();
  await expect(page.getByRole("status")).toContainText("Account verified");
  await login(page, email, f.password);
  await page.getByRole("button", { name: "Edit name", exact: true }).click();
  await page
    .getByLabel("Organization name", { exact: true })
    .fill("Fictional Northstar renamed");
  await page.getByRole("button", { name: "Save organization name" }).click();
  await expect(
    page.getByRole("status").filter({ hasText: "Organization name saved." }),
  ).toBeVisible();
  await page.reload();
  await expect(
    page.getByRole("heading", {
      name: "Fictional Northstar renamed",
      exact: true,
    }),
  ).toBeVisible();
  const recipient = `invite-${crypto.randomUUID()}@example.com`;
  await page.getByLabel("Email address", { exact: true }).fill(recipient);
  await page
    .getByRole("button", { name: "Create invitation", exact: true })
    .click();
  await expect(
    page.getByText(recipient, { exact: false }).first(),
  ).toBeVisible();
  const inviteLink = mail(recipient)[0].link;
  await page
    .getByRole("button", { name: "Resend invitation", exact: true })
    .click();
  await expect(
    page.getByRole("button", { name: "Cancel invitation", exact: true }),
  ).toBeVisible();
  await page
    .getByRole("button", { name: "Cancel invitation", exact: true })
    .click();
  await expect(
    page.getByText("No pending invitations.", { exact: true }),
  ).toBeVisible();
  await page.goto("/");
  await expect(
    page.getByRole("heading", { name: "Getting started" }),
  ).toBeVisible();
  for (const width of [1440, 768, 360]) {
    await page.setViewportSize({ width, height: 1000 });
    expect(
      await page.evaluate(() => document.documentElement.scrollWidth),
    ).toBeLessThanOrEqual(width);
    await accessible(page);
    await page.screenshot({
      path: `docs/verification/sprint81-setup-${width}.png`,
      fullPage: true,
    });
  }
  await page.goto(inviteLink);
  await page
    .getByLabel("Display name", { exact: true })
    .fill("Cancelled invite");
  await page
    .getByLabel("Password (12–72 bytes)", { exact: true })
    .fill(f.password);
  await page.getByRole("button", { name: "Verify and continue" }).click();
  await expect(
    page
      .getByRole("alert")
      .filter({ hasText: "invalid, expired or already used" }),
  ).toContainText("invalid, expired or already used");
  await expect(
    page.getByRole("link", { name: "request verification again" }),
  ).toBeVisible();
  await expect(
    page.getByRole("link", { name: "request a password reset" }),
  ).toBeVisible();
});

test("older records, selectors, full cohorts and browser result grants", async ({
  page,
  browser,
}) => {
  test.setTimeout(180000);
  page.setDefaultTimeout(15000);
  const f = fixture();
  await login(page, f.pilot_email, f.password);
  await page.goto("/");
  await page.getByRole("button", { name: "Search workspace commands" }).click();
  await expect(
    page.getByRole("dialog", { name: "Workspace commands" }),
  ).toBeVisible();
  await page
    .getByLabel("Find a record", { exact: true })
    .fill("Pilot project 124");
  await expect(
    page
      .getByRole("navigation", { name: "Matching records" })
      .getByRole("link", { name: /Pilot project 124/ }),
  ).toBeVisible();
  await page
    .getByRole("navigation", { name: "Matching records" })
    .getByRole("link")
    .click();
  await expect(
    page.getByRole("heading", { name: "Pilot project 124", exact: true }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Edit project", exact: true }).click();
  const dialog = page.getByRole("dialog", { name: "Edit Projects" });
  await dialog
    .getByRole("combobox", { name: "Project priority (optional)", exact: true })
    .selectOption("high");
  await dialog
    .getByRole("combobox", { name: "Methodology (optional)", exact: true })
    .selectOption("hybrid");
  await dialog
    .getByRole("button", { name: "Save record", exact: true })
    .click();
  await expect(dialog).not.toBeVisible();
  await page.goto("/projects");
  await page
    .getByRole("searchbox", { name: "Search records", exact: true })
    .fill("Pilot project 124");
  await page
    .getByRole("combobox", { name: "Industry filter", exact: true })
    .selectOption("fintech");
  await expect(
    page.getByRole("link", { name: "Pilot project 124", exact: true }),
  ).toBeVisible();
  await page.goto("/resources");
  await page
    .getByLabel("Find resource profile", { exact: true })
    .fill("Pilot resource 124");
  await page
    .getByRole("combobox", { name: "Resource profile", exact: true })
    .selectOption({ label: "Pilot resource 124" });
  await expect(
    page.getByRole("heading", {
      name: "Pilot resource 124: capacity heatmap",
      exact: true,
    }),
  ).toBeVisible();
  await page.goto("/integrations");
  await page
    .getByLabel("Find project", { exact: true })
    .fill("Pilot project 124");
  await page
    .getByRole("combobox", { name: "Project", exact: true })
    .selectOption(f.pilot_project);
  await page.goto("/assessments");
  await page
    .getByLabel("Find assessments", { exact: true })
    .fill("Pilot assessment 124");
  await page
    .getByRole("button", { name: "Open Pilot assessment 124", exact: true })
    .click();
  await expect(page.getByText(/125 completed records/)).toBeVisible();
  await expect(
    page.getByRole("button", { name: /^Open Pilot assessment / }),
  ).toHaveCount(1);
  await expect(
    page.getByRole("table").filter({
      has: page.getByText("Compatible departmental scores", { exact: true }),
    }),
  ).toContainText("75");
  const access = page.locator('section[aria-label="Assessment access"]').last();
  await access.getByLabel("Find member", { exact: true }).fill("Pilot viewer");
  await access
    .getByRole("combobox", { name: "Member", exact: true })
    .selectOption(f.pilot_viewer);
  await access
    .getByRole("button", { name: "Grant result access", exact: true })
    .click();
  await expect(
    access.getByRole("button", { name: "Revoke access", exact: true }),
  ).toBeVisible();
  const viewerContext = await browser.newContext();
  const viewer = await viewerContext.newPage();
  await login(viewer, f.pilot_viewer_email, f.password);
  await viewer.goto(`/assessments?assessment=${f.pilot_assessment}`);
  await expect(
    viewer
      .getByRole("heading", { name: "Pilot assessment 124", exact: true })
      .last(),
  ).toBeVisible();
  await expect(
    viewer.getByRole("button", { name: "Grant result access" }),
  ).toHaveCount(0);
  await access
    .getByRole("button", { name: "Revoke access", exact: true })
    .click();
  await expect(
    access.getByRole("button", { name: "Revoke access", exact: true }),
  ).toHaveCount(0);
  await viewer.reload();
  await expect(
    viewer
      .getByRole("alert")
      .filter({ hasText: /unavailable|failed|Could not|not found|access/i })
      .first(),
  ).toBeVisible();
  await expect(
    viewer.getByText("Pilot assessment 124", { exact: true }),
  ).toHaveCount(0);
  await viewerContext.close();
  await accessible(page);
  await page.screenshot({
    path: "docs/verification/sprint81-assessment-access.png",
    fullPage: true,
  });
});

test("My Work, persistent notifications and manual changes refresh a second session", async ({
  page,
  browser,
}) => {
  test.setTimeout(180000);
  page.setDefaultTimeout(15000);
  const f = fixture();
  await login(page, f.pilot_pm_email, f.password);
  await page.goto("/");
  await expect(
    page.getByRole("link", { name: "Pilot assigned work", exact: true }),
  ).toBeVisible();
  const adminContext = await browser.newContext();
  const admin = await adminContext.newPage();
  await login(admin, f.pilot_email, f.password);
  const csrf = (await adminContext.cookies()).find(
    (c) => c.name === "ppm_csrf",
  )!.value;
  const headers = {
    origin: process.env.PPM_WEB_URL!,
    "x-csrf-token": csrf,
    "x-organization-id": f.pilot_org,
    "idempotency-key": crypto.randomUUID(),
  };
  const assigned = await admin.request.post("/api/v1/delivery/work_items", {
    headers,
    data: {
      kind: "work_items",
      name: "Pilot new assignment",
      project_id: f.pilot_project,
      owner_id: f.pilot_pm,
    },
  });
  expect(assigned.status()).toBe(201);
  await page
    .getByRole("button", { name: "Open notifications", exact: true })
    .click();
  await expect(
    page.getByRole("link", { name: "Pilot new assignment", exact: true }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Mark read", exact: true }).click();
  await expect(
    page.getByRole("button", { name: "Read", exact: true }),
  ).toBeDisabled();
  await page.keyboard.press("Escape");
  await page.goto("/command-center");
  await expect(
    page.getByText("Listening for saved changes", { exact: true }),
  ).toBeVisible();
  const baseline = await page.request.get(
    "/api/v1/command/snapshot?start=2026-10-01&end=2026-11-01",
    { headers: { "x-organization-id": f.pilot_org } },
  );
  expect(baseline.status()).toBe(200);
  const refreshed = page.waitForResponse(
    (r) => r.url().includes("/command/snapshot") && r.status() === 200,
  );
  const milestone = await admin.request.post("/api/v1/delivery/milestones", {
    headers: { ...headers, "idempotency-key": crypto.randomUUID() },
    data: {
      kind: "milestones",
      name: "Pilot saved milestone",
      project_id: f.pilot_project,
      due_date: "2026-11-01",
      critical: true,
    },
  });
  expect(milestone.status()).toBe(201);
  await expect(page.getByText(/Saved change received/)).toBeVisible();
  expect((await refreshed).status()).toBe(200);
  await page.goto("/");
  await page
    .getByRole("button", { name: "Open notifications", exact: true })
    .click();
  await expect(
    page.getByRole("button", { name: "Read", exact: true }),
  ).toBeDisabled();
  await page.keyboard.press("Escape");
  const grant = await admin.request.get(
    `/api/v1/delivery/grants/${f.pilot_grant}`,
    { headers },
  );
  const g = await grant.json();
  expect(
    (
      await admin.request.patch(`/api/v1/delivery/grants/${f.pilot_grant}`, {
        headers: { ...headers, "if-match": String(g.revision) },
        data: { ...g.data, archived: true },
      })
    ).status(),
  ).toBe(200);
  await page.reload();
  await expect(
    page.getByRole("link", { name: "Pilot assigned work", exact: true }),
  ).toHaveCount(0);
  await page
    .getByRole("button", { name: "Open notifications", exact: true })
    .click();
  await expect(
    page.getByRole("link", { name: "Pilot new assignment", exact: true }),
  ).toHaveCount(0);
  await adminContext.close();
});
