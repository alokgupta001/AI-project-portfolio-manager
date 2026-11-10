import { test, expect, type Locator, type Page } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { mkdirSync, readFileSync } from "node:fs";
import { resolve } from "node:path";

const evidence = resolve("..", "output", "frontend-redesign");
test.beforeEach(async ({ context }) => {
  await context.addInitScript(() => {
    const read = Storage.prototype.getItem;
    Storage.prototype.getItem = function (key) {
      return key.startsWith("ppm-page-guide-v1:")
        ? "seen"
        : read.call(this, key);
    };
  });
});
const titles = [
  "Your navigation hub",
  "Your portfolio, in perspective",
  "Create your first project",
  "Find and manage your work",
  "Explore a project in depth",
  "Track progress with evidence",
  "Keep evidence connected",
  "Make the workspace yours",
];

async function login(page: Page) {
  test.skip(!process.env.PPM_IDENTITY_FIXTURE, "Use isolated browser runner");
  const fixture = JSON.parse(
    readFileSync(process.env.PPM_IDENTITY_FIXTURE!, "utf8"),
  );
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
  const response = await page.request.get("/api/v1/auth/me");
  expect(response.ok()).toBeTruthy();
  const account: { id: string } = await response.json();
  return `ppm-tutorial-v1:${account.id}`;
}

async function accessible(page: Page) {
  const card = page.locator(".tutorial-card");
  if (await card.isVisible()) await expect(card).toHaveCSS("opacity", "1");
  const result = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"])
    .analyze();
  expect(
    result.violations.map((violation) => ({
      id: violation.id,
      targets: violation.nodes.map((node) => node.target),
    })),
  ).toEqual([]);
}

async function capture(page: Page, name: string) {
  mkdirSync(evidence, { recursive: true });
  await page.screenshot({ path: resolve(evidence, name), fullPage: false });
}

async function expectStep(page: Page, tour: Locator, index: number) {
  await expect(
    tour.getByRole("heading", { name: titles[index], exact: true }),
  ).toBeVisible();
  await expect(
    page.getByRole("progressbar", { name: "Tutorial progress" }),
  ).toHaveAttribute("aria-valuenow", String(index + 1));
  await expect(
    tour.getByRole("button", {
      name: `Go to step ${index + 1}: ${titles[index]}`,
      exact: true,
    }),
  ).toHaveAttribute("aria-current", "step");
}

test("tutorial: eight real feature steps, keyboard navigation, route resume and completed preference", async ({
  page,
}) => {
  test.setTimeout(180000);
  await page.setViewportSize({ width: 1440, height: 1000 });
  const key = await login(page);
  const errors: string[] = [];
  page.on("pageerror", (error) => errors.push(error.message));
  await page.evaluate((storageKey) => localStorage.removeItem(storageKey), key);
  await page.goto("/");
  const welcome = page.getByRole("dialog", {
    name: "Welcome to Enterprise PPM",
    exact: true,
  });
  await expect(welcome).toBeVisible();
  await expect(
    welcome.getByRole("button", { name: "Start guided tour" }),
  ).toBeFocused();
  await accessible(page);
  await capture(page, "tutorial-welcome-desktop.png");
  await welcome.getByRole("button", { name: "Start guided tour" }).click();
  const tour = page.getByRole("region", {
    name: "Guided tutorial",
    exact: true,
  });
  await expectStep(page, tour, 0);
  await expect(tour).toBeFocused();
  await expect(
    tour.getByRole("button", { name: "Back", exact: true }),
  ).toBeDisabled();
  await page.keyboard.press("ArrowRight");
  await expectStep(page, tour, 1);
  await page.keyboard.press("ArrowLeft");
  await expectStep(page, tour, 0);
  await page.keyboard.press("Enter");
  await expectStep(page, tour, 1);
  await expect(page.locator(".tutorial-spotlight")).toBeVisible();
  await accessible(page);
  await capture(page, "tutorial-spotlight-desktop.png");
  await tour.getByRole("button", { name: "Next", exact: true }).click();
  await expectStep(page, tour, 2);
  await expect(page).toHaveURL(/\/projects$/);
  await expectStep(page, tour, 2);
  await expect(page.locator(".tutorial-spotlight")).toBeVisible();
  await page.reload();
  await expectStep(page, tour, 2);
  await tour.getByRole("button", { name: "Next", exact: true }).click();
  await expectStep(page, tour, 3);
  await tour.getByRole("button", { name: "Skip step", exact: true }).click();
  await expectStep(page, tour, 4);
  await tour
    .getByRole("link", {
      name: /^(Open a project|Find a project to explore)$/,
    })
    .click();
  await expectStep(page, tour, 4);
  await tour.getByRole("button", { name: "Next", exact: true }).click();
  await expectStep(page, tour, 5);
  await expect(page).toHaveURL(/\/command-center$/);
  await tour.getByRole("button", { name: "Back", exact: true }).click();
  await expectStep(page, tour, 4);
  await expect(page).toHaveURL(/\/projects(?:\/[^/]+)?$/);
  await tour.getByRole("button", { name: "Next", exact: true }).click();
  await expect(page).toHaveURL(/\/command-center$/);
  await expectStep(page, tour, 5);
  await tour.getByRole("button", { name: "Next", exact: true }).click();
  await expectStep(page, tour, 6);
  await expect(page).toHaveURL(/\/documents$/);
  await expectStep(page, tour, 6);
  await tour.getByRole("button", { name: "Next", exact: true }).click();
  await expectStep(page, tour, 7);
  await expect(page).toHaveURL(/\/account$/);
  const theme = page.locator("html");
  const previousTheme = await theme.getAttribute("data-theme");
  await page
    .getByRole("button", { name: /^Switch to (light|dark) theme$/ })
    .click();
  await expect(theme).not.toHaveAttribute(
    "data-theme",
    previousTheme || "light",
  );
  await tour.getByRole("button", { name: "Finish tour", exact: true }).click();
  const completion = page.getByRole("dialog", {
    name: "You're all set!",
    exact: true,
  });
  await expect(completion).toBeVisible();
  await accessible(page);
  await capture(page, "tutorial-complete-desktop.png");
  expect(
    await page.evaluate(
      (storageKey) => JSON.parse(localStorage.getItem(storageKey) || "null"),
      key,
    ),
  ).toEqual({ version: 1, status: "completed", step: 7 });
  await completion
    .getByRole("button", { name: "Explore the workspace" })
    .click();
  await page.goto("/");
  await expect(page.getByRole("heading", { name: /Welcome,/ })).toBeVisible();
  await expect(welcome).not.toBeVisible();
  await expect(tour).not.toBeVisible();
  expect(errors).toEqual([]);
});

test("tutorial: skip step three requires confirmation and replay remains available in account settings", async ({
  page,
}) => {
  test.setTimeout(120000);
  const key = await login(page);
  await page.evaluate((storageKey) => localStorage.removeItem(storageKey), key);
  await page.goto("/");
  await page.getByRole("button", { name: "Start guided tour" }).click();
  const tour = page.getByRole("region", {
    name: "Guided tutorial",
    exact: true,
  });
  await tour
    .getByRole("button", {
      name: "Go to step 3: Create your first project",
      exact: true,
    })
    .click();
  await expectStep(page, tour, 2);
  await page.keyboard.press("Escape");
  const confirmation = page.getByRole("dialog", {
    name: "Skip the tutorial?",
    exact: true,
  });
  await expect(confirmation).toBeVisible();
  await expect(
    confirmation.getByRole("button", { name: "Keep exploring" }),
  ).toBeFocused();
  await confirmation.getByRole("button", { name: "Keep exploring" }).click();
  await expectStep(page, tour, 2);
  await page.keyboard.press("Escape");
  await confirmation.getByRole("button", { name: "Confirm skip" }).click();
  await expect(tour).not.toBeVisible();
  expect(
    await page.evaluate(
      (storageKey) => JSON.parse(localStorage.getItem(storageKey) || "null"),
      key,
    ),
  ).toEqual({ version: 1, status: "skipped", step: 2 });
  await page.goto("/");
  await expect(page.getByRole("heading", { name: /Welcome,/ })).toBeVisible();
  await expect(
    page.getByRole("dialog", {
      name: "Welcome to Enterprise PPM",
      exact: true,
    }),
  ).not.toBeVisible();
  await page.goto("/account");
  await expect(
    page.getByRole("heading", { name: "Profile & security" }),
  ).toBeVisible();
  await page
    .getByRole("button", { name: "Replay tutorial", exact: true })
    .last()
    .click();
  const welcome = page.getByRole("dialog", {
    name: "Welcome to Enterprise PPM",
    exact: true,
  });
  await expect(welcome).toBeVisible();
  await welcome.getByRole("button", { name: "Start guided tour" }).click();
  await expectStep(page, tour, 0);
  await tour
    .getByRole("button", {
      name: "Go to step 8: Make the workspace yours",
      exact: true,
    })
    .click();
  await expectStep(page, tour, 7);
  await tour.getByRole("button", { name: "Finish tour", exact: true }).click();
  const completion = page.getByRole("dialog", {
    name: "You're all set!",
    exact: true,
  });
  await completion
    .getByRole("button", { name: "Replay tour", exact: true })
    .click();
  await expectStep(page, tour, 0);
  await tour.getByRole("button", { name: "Skip tour", exact: true }).click();
  await confirmation.getByRole("button", { name: "Confirm skip" }).click();
  await expect(tour).not.toBeVisible();
});

test("tutorial: skipping the welcome restores page scrolling and can be cancelled", async ({
  page,
}) => {
  const key = await login(page);
  await page.evaluate((storageKey) => localStorage.removeItem(storageKey), key);
  await page.goto("/");
  const welcome = page.getByRole("dialog", {
    name: "Welcome to Enterprise PPM",
    exact: true,
  });
  await welcome.getByRole("button", { name: "Skip tour", exact: true }).click();
  const confirmation = page.getByRole("dialog", {
    name: "Skip the tutorial?",
    exact: true,
  });
  await expect(welcome).not.toBeVisible();
  await confirmation.getByRole("button", { name: "Keep exploring" }).click();
  await expect(welcome).toBeVisible();
  await welcome.getByRole("button", { name: "Skip tour", exact: true }).click();
  await confirmation.getByRole("button", { name: "Confirm skip" }).click();
  await expect(welcome).not.toBeVisible();
  await expect(page.locator("body")).not.toHaveCSS("overflow", "hidden");
  await page.reload();
  await expect(page.getByRole("heading", { name: /Welcome,/ })).toBeVisible();
  await expect(welcome).not.toBeVisible();
});

test("tutorial: mobile spotlight remains contained and keyboard usable with reduced motion and unavailable storage", async ({
  page,
}) => {
  test.setTimeout(120000);
  await page.setViewportSize({ width: 360, height: 900 });
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.addInitScript(() => {
    const write = Storage.prototype.setItem;
    Storage.prototype.setItem = function (key, value) {
      if (key.startsWith("ppm-tutorial-v1:"))
        throw new DOMException(
          "Synthetic browser storage denial",
          "SecurityError",
        );
      return write.call(this, key, value);
    };
  });
  await login(page);
  await page.goto("/");
  const welcome = page.getByRole("dialog", {
    name: "Welcome to Enterprise PPM",
    exact: true,
  });
  await expect(welcome).toBeVisible();
  await accessible(page);
  await capture(page, "tutorial-welcome-mobile.png");
  await welcome.getByRole("button", { name: "Start guided tour" }).click();
  const tour = page.getByRole("region", {
    name: "Guided tutorial",
    exact: true,
  });
  await expectStep(page, tour, 0);
  await expect(tour.getByRole("status")).toContainText(
    "Browser storage is unavailable",
  );
  await expect(tour).toHaveCSS("animation-name", "none");
  await expect(page.locator(".tutorial-spotlight")).toHaveCSS(
    "animation-name",
    "none",
  );
  await accessible(page);
  await capture(page, "tutorial-spotlight-mobile.png");
  const bounds = await tour.boundingBox();
  expect(bounds).not.toBeNull();
  expect(bounds!.x).toBeGreaterThanOrEqual(0);
  expect(bounds!.y).toBeGreaterThanOrEqual(0);
  expect(bounds!.x + bounds!.width).toBeLessThanOrEqual(360);
  expect(bounds!.y + bounds!.height).toBeLessThanOrEqual(900);
  for (const button of await tour.getByRole("button").all()) {
    const target = await button.boundingBox();
    expect(target!.width).toBeGreaterThanOrEqual(44);
    expect(target!.height).toBeGreaterThanOrEqual(44);
  }
  expect(
    await page.evaluate(() => document.documentElement.scrollWidth),
  ).toBeLessThanOrEqual(360);
  await page.keyboard.press("ArrowRight");
  await expectStep(page, tour, 1);
  await tour
    .getByRole("button", {
      name: "Go to step 8: Make the workspace yours",
      exact: true,
    })
    .click();
  await expectStep(page, tour, 7);
  await tour.getByRole("button", { name: "Finish tour", exact: true }).click();
  const completion = page.getByRole("dialog", {
    name: "You're all set!",
    exact: true,
  });
  await expect(completion).toBeVisible();
  await expect(
    completion.locator(".tutorial-celebration > i").first(),
  ).toBeHidden();
  await accessible(page);
  await capture(page, "tutorial-complete-mobile.png");
  await completion
    .getByRole("button", { name: "Explore the workspace" })
    .click();
  await expect(tour).not.toBeVisible();
});
