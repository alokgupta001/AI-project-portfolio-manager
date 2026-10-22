import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { readFileSync, mkdirSync } from "node:fs";

test("hybrid goals, zero-call metrics, honest deferred AI and accessible coverage", async ({
  page,
}) => {
  test.setTimeout(180000);
  test.skip(
    !process.env.PPM_IDENTITY_FIXTURE || process.env.PPM_TEST_AI_V2 !== "1",
    "Use isolated v2 browser runner",
  );
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
  await page.goto("/agents");
  await page
    .getByRole("combobox", { name: "Analysis project", exact: true })
    .selectOption(f.agent_project);
  await page
    .getByRole("combobox", { name: "Analysis goal", exact: true })
    .selectOption("metrics");
  await page
    .getByRole("button", { name: "Run scoped analysis", exact: true })
    .click();
  await expect(
    page.getByText("Execution: succeeded · Semantic result: hybrid_complete", {
      exact: true,
    }),
  ).toBeVisible({ timeout: 30000 });
  const coverage = page.getByRole("region", {
    name: "Capability coverage table",
    exact: true,
  });
  await expect(
    coverage.getByText("not_requested", { exact: true }),
  ).toHaveCount(9);
  await page.getByText("Model attempts and usage", { exact: true }).click();
  await expect(
    page.getByText("No model calls were admitted.", { exact: true }),
  ).toBeVisible();
  await page
    .getByRole("combobox", { name: "Analysis goal", exact: true })
    .selectOption("domain");
  await page.getByRole("checkbox", { name: "financial", exact: true }).check();
  await page
    .getByRole("button", { name: "Run scoped analysis", exact: true })
    .click();
  await expect(
    page.getByText(
      "Execution: partially_succeeded · Semantic result: hybrid_partial",
      { exact: true },
    ),
  ).toBeVisible({ timeout: 30000 });
  await expect(
    coverage.getByText("unavailable · UNAVAILABLE", { exact: true }),
  ).toBeVisible();
  await expect(
    page.getByText("Requested AI interpretation is incomplete: financial", {
      exact: true,
    }),
  ).toBeVisible();
  await page
    .getByRole("combobox", { name: "Analysis goal", exact: true })
    .selectOption("all_specialists");
  for (const role of [
    "financial",
    "schedule",
    "resource",
    "risk",
    "governance",
    "agile_coach",
    "sentiment",
    "pmo",
    "executive",
  ]) {
    const input = page.getByRole("checkbox", { name: role, exact: true });
    await expect(input).toBeChecked();
    await expect(input).toBeDisabled();
  }
  const pending = page.waitForResponse(
    (r) =>
      r.url().endsWith("/api/v1/agents/runs") &&
      r.request().method() === "POST",
  );
  await page
    .getByRole("button", { name: "Run scoped analysis", exact: true })
    .click();
  const all = await pending;
  expect(all.status()).toBe(202);
  await expect(coverage.getByText(/Goal: all_specialists/)).toBeVisible({
    timeout: 30000,
  });
  await expect(
    page.getByText(
      "Execution: partially_succeeded · Semantic result: hybrid_partial",
      { exact: true },
    ),
  ).toBeVisible({ timeout: 30000 });
  mkdirSync("test-results/sprint111", { recursive: true });
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
        () => document.documentElement.scrollWidth <= window.innerWidth,
      ),
    ).toBe(true);
    await page.screenshot({
      path: `test-results/sprint111/coverage-${width}.png`,
      fullPage: true,
    });
  }
  await coverage.focus();
  await page.keyboard.press("ArrowRight");
  await expect
    .poll(() => coverage.evaluate((el) => el.scrollLeft))
    .toBeGreaterThan(0);
  expect(errors).toEqual([]);
});
