import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { mkdirSync, readFileSync } from "node:fs";
import { resolve } from "node:path";

test("page guides: every workspace page has first-visit tips, route reset and replay", async ({
  page,
}) => {
  test.setTimeout(180000);
  test.skip(!process.env.PPM_IDENTITY_FIXTURE, "Use isolated browser runner");
  const fixture = JSON.parse(
    readFileSync(process.env.PPM_IDENTITY_FIXTURE!, "utf8"),
  );
  await page.addInitScript(() => {
    const read = Storage.prototype.getItem;
    Storage.prototype.getItem = function (key) {
      return key.startsWith("ppm-tutorial-v1:")
        ? JSON.stringify({ version: 1, status: "completed", step: 7 })
        : read.call(this, key);
    };
  });
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.goto("/login");
  await page
    .getByLabel("Email address", { exact: true })
    .fill(fixture.command_email);
  await page.getByLabel("Password", { exact: true }).fill(fixture.password);
  await page.getByRole("button", { name: "Sign in", exact: true }).click();
  await page
    .getByRole("combobox", { name: "Organization", exact: true })
    .selectOption(fixture.command_org);
  await expect(
    page.getByRole("heading", { name: "Organization members" }),
  ).toBeVisible();
  const errors: string[] = [];
  page.on("pageerror", (error) => errors.push(error.message));
  const csrf = (await page.context().cookies()).find(
    (cookie) => cookie.name === "ppm_csrf",
  )!.value;
  const headers = {
    origin: process.env.PPM_WEB_URL!,
    "x-csrf-token": csrf,
    "x-organization-id": fixture.command_org,
  };
  const settings = await page.request.get("/api/v1/delivery/settings", {
    headers,
  });
  expect(settings.ok()).toBeTruthy();
  if (!(await settings.json()).items.length) {
    const response = await page.request.post("/api/v1/delivery/settings", {
      headers: { ...headers, "idempotency-key": crypto.randomUUID() },
      data: {
        kind: "settings",
        name: "Guide settings",
        timezone: "Asia/Kolkata",
        currency: "INR",
      },
    });
    expect(response.status()).toBe(201);
  }
  const portfolioResponse = await page.request.post(
    "/api/v1/delivery/portfolios",
    {
      headers: { ...headers, "idempotency-key": crypto.randomUUID() },
      data: { kind: "portfolios", name: "Page guide portfolio" },
    },
  );
  expect(portfolioResponse.status()).toBe(201);
  const portfolio = await portfolioResponse.json();
  const created = await page.request.post("/api/v1/delivery/projects", {
    headers: { ...headers, "idempotency-key": crypto.randomUUID() },
    data: {
      kind: "projects",
      name: "Page guide verification",
      portfolio_id: portfolio.id,
      currency: "INR",
      status: "active",
    },
  });
  expect(created.status()).toBe(201);
  const project = await created.json();
  const routes = [
    ["/", "Workspace overview"],
    ["/projects", "Projects"],
    [`/projects/${project.id}`, "Project details"],
    ["/portfolios", "Portfolios"],
    ["/resources", "Resource planning"],
    ["/assessments", "Maturity assessments"],
    ["/command-center", "Command center"],
    ["/documents", "Document library"],
    ["/integrations", "Integrations & jobs"],
    ["/ai", "AI operations & evidence"],
    ["/agents", "Agents & recommendations"],
    ["/ml", "History & baselines"],
    ["/organization", "Organization setup"],
    ["/account", "Account & access"],
    ["/design-system", "Component gallery"],
  ];
  const evidence = resolve("..", "output", "frontend-redesign");
  mkdirSync(evidence, { recursive: true });
  for (const [route, title] of routes) {
    await page.goto(route);
    const guide = page.getByRole("region", {
      name: `${title} page guide`,
      exact: true,
    });
    // Account was already visited during sign-in; its replay is the entry point.
    if (route === "/account")
      await page
        .getByRole("button", { name: "Page guide", exact: true })
        .click();
    await expect(guide).toBeVisible();
    await expect(guide).toContainText("1 / 3");
    if (title === "Project details") {
      await expect(
        page.getByRole("heading", { name: "Project overview", exact: true }),
      ).toBeVisible();
    }
    await guide
      .getByRole("button", { name: "Show section", exact: false })
      .click();
    await expect(page.locator(".page-guide-highlight")).toBeVisible();
    await guide.getByRole("button", { name: "Next tip", exact: true }).click();
    await expect(guide).toContainText("2 / 3");
    if (route === "/organization") {
      await guide.getByRole("button", { name: "Show section" }).click();
      await expect(page.locator(".page-guide-highlight")).toBeVisible();
    }
    await guide.getByRole("button", { name: "Next tip", exact: true }).click();
    await expect(guide).toContainText("3 / 3");
    if (route === "/ai") {
      await page.evaluate(() => window.scrollTo(0, 0));
      await page.screenshot({
        path: resolve(evidence, "ai-page-guide-desktop.png"),
        fullPage: false,
        animations: "disabled",
      });
      const axe = await new AxeBuilder({ page })
        .withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"])
        .analyze();
      expect(axe.violations).toEqual([]);
    }
    await guide.getByRole("button", { name: "Got it", exact: true }).click();
    await page.reload();
    await expect(
      page.getByRole("button", { name: "Page guide", exact: true }),
    ).toBeVisible();
    await expect(guide).not.toBeVisible();
    await page.getByRole("button", { name: "Page guide", exact: true }).click();
    await expect(guide).toBeVisible();
    await expect(guide).toContainText("1 / 3");
    await guide
      .getByRole("button", { name: "Close page guide", exact: true })
      .click();
  }
  await page.setViewportSize({ width: 360, height: 900 });
  await page.goto("/ai");
  await page.getByRole("button", { name: "Page guide", exact: true }).click();
  const mobile = page.getByRole("region", {
    name: "AI operations & evidence page guide",
    exact: true,
  });
  await expect(mobile).toBeVisible();
  const box = await mobile.boundingBox();
  expect(box!.x).toBeGreaterThanOrEqual(0);
  expect(box!.x + box!.width).toBeLessThanOrEqual(360);
  expect(box!.y + box!.height).toBeLessThanOrEqual(900);
  expect(
    await page.evaluate(() => document.documentElement.scrollWidth),
  ).toBeLessThanOrEqual(360);
  await page.screenshot({
    path: resolve(evidence, "ai-page-guide-mobile.png"),
    fullPage: false,
    animations: "disabled",
  });
  await mobile.focus();
  await page.keyboard.press("Escape");
  await expect(mobile).not.toBeVisible();
  expect(errors).toEqual([]);
});
