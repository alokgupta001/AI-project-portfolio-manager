import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { readFileSync } from "node:fs";

test("guided review remains usable without cloud and persists its nine checklists", async ({
  page,
}) => {
  test.setTimeout(120000);
  test.skip(
    !process.env.PPM_IDENTITY_FIXTURE || process.env.PPM_TEST_AI_V2 !== "1",
    "Use the isolated v2 browser runner",
  );
  const f = JSON.parse(readFileSync(process.env.PPM_IDENTITY_FIXTURE!, "utf8"));
  await page.goto("/login");
  await page.getByLabel("Email address", { exact: true }).fill(f.agent_email);
  await page.getByLabel("Password", { exact: true }).fill(f.password);
  await page.getByRole("button", { name: "Sign in", exact: true }).click();
  await expect(
    page.getByRole("button", { name: "Sign out", exact: true }),
  ).toBeVisible();
  await page.goto("/agents");
  await expect(
    page.getByRole("combobox", { name: "Analysis goal", exact: true }),
  ).toHaveValue("guided");
  await page
    .getByRole("combobox", { name: "Analysis project", exact: true })
    .selectOption(f.agent_project);
  await page
    .getByRole("combobox", { name: "Guided review role", exact: true })
    .selectOption("executive");
  await page
    .getByRole("button", { name: "Run scoped analysis", exact: true })
    .click();
  const result = page.getByRole("region", { name: "Guided review results" });
  await expect(
    result.getByText("Rules-only checklist", { exact: true }),
  ).toBeVisible({ timeout: 45000 });
  await result
    .getByText("Review actions for all nine roles", { exact: true })
    .click();
  await expect(result.getByRole("listitem")).toHaveCount(9);
  const firstRun = page.getByRole("button", { name: /^Open run / }).first();
  const label =
    (await firstRun.getAttribute("aria-label")) ?? (await firstRun.innerText());
  await page.reload();
  await page.getByRole("button", { name: label!, exact: true }).click();
  await expect(
    result.getByText("Rules-only checklist", { exact: true }),
  ).toBeVisible();
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
      path: `test-results/guided-review-${width}.png`,
      fullPage: true,
    });
  }
});
