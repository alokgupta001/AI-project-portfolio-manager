import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { readFileSync } from "node:fs";

test("project manager can run a granted guided review without admin controls", async ({
  page,
}) => {
  test.setTimeout(120000);
  test.skip(
    !process.env.PPM_IDENTITY_FIXTURE || process.env.PPM_TEST_AI_V2 !== "1",
    "Use isolated v2 browser runner",
  );
  const f = JSON.parse(readFileSync(process.env.PPM_IDENTITY_FIXTURE!, "utf8"));
  await page.goto("/login");
  await page
    .getByLabel("Email address", { exact: true })
    .fill(f.agent_reviewer_email);
  await page.getByLabel("Password", { exact: true }).fill(f.password);
  await page.getByRole("button", { name: "Sign in", exact: true }).click();
  await expect(
    page.getByRole("button", { name: "Sign out", exact: true }),
  ).toBeVisible();
  await page.goto("/agents");
  await expect(
    page.getByText(
      "You can run guided reviews for explicitly permitted projects. Your existing project role is unchanged.",
      { exact: true },
    ),
  ).toBeVisible();
  const goal = page.getByRole("combobox", {
    name: "Analysis goal",
    exact: true,
  });
  await expect(goal).toHaveValue("guided");
  await expect(goal.locator("option")).toHaveCount(1);
  await expect(
    page.getByRole("combobox", { name: "Assessment (optional)", exact: true }),
  ).toBeDisabled();
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
  for (const width of [1440, 360]) {
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
      path: `test-results/guided-access-${width}.png`,
      fullPage: true,
    });
  }
});
