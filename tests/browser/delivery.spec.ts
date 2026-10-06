import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { readFileSync } from "node:fs";
test("delivery workflow persists hierarchy, work, budgets, baselines and archive", async ({
  page,
}) => {
  test.setTimeout(120000);
  test.skip(!process.env.PPM_IDENTITY_FIXTURE, "Use isolated browser runner");
  const f = JSON.parse(readFileSync(process.env.PPM_IDENTITY_FIXTURE!, "utf8"));
  await page.goto("/login");
  await page.getByLabel("Email address", { exact: true }).fill(f.email);
  await page.getByLabel("Password", { exact: true }).fill(f.password);
  await page.getByRole("button", { name: "Sign in", exact: true }).click();
  await page
    .getByRole("combobox", { name: "Organization", exact: true })
    .selectOption(f.admin_org);
  await expect(
    page.getByRole("heading", { name: "Organization members" }),
  ).toBeVisible();
  await page.goto("/organization");
  await page
    .getByRole("button", { name: "Configure organization", exact: true })
    .click();
  let dialog = page.getByRole("dialog", {
    name: "Create Organization configuration",
  });
  await dialog
    .getByLabel("Name", { exact: true })
    .fill("Browser delivery settings");
  await dialog
    .getByRole("button", { name: "Save record", exact: true })
    .click();
  await expect(dialog).not.toBeVisible();
  await page.goto("/portfolios");
  await page
    .getByRole("button", { name: "Create portfolios", exact: true })
    .click();
  dialog = page.getByRole("dialog", { name: "Create Portfolios" });
  await dialog.getByLabel("Name", { exact: true }).fill("Browser portfolio");
  await dialog
    .getByRole("button", { name: "Save record", exact: true })
    .click();
  await expect(dialog).not.toBeVisible();
  await page.goto("/projects");
  await page
    .getByRole("button", { name: "Create projects", exact: true })
    .click();
  dialog = page.getByRole("dialog", { name: "Create Projects" });
  await dialog.getByLabel("Name", { exact: true }).fill("Browser project");
  await expect(
    dialog
      .getByRole("combobox", { name: "Portfolio", exact: true })
      .getByRole("option")
      .filter({ hasText: "Browser portfolio" }),
  ).toHaveCount(1);
  await dialog
    .getByRole("combobox", { name: "Portfolio", exact: true })
    .selectOption({
      label: (await dialog
        .getByRole("combobox", { name: "Portfolio", exact: true })
        .getByRole("option")
        .filter({ hasText: "Browser portfolio" })
        .textContent())!,
    });
  await dialog.getByLabel("Start date", { exact: true }).fill("2026-10-01");
  await dialog.getByLabel("Planned finish", { exact: true }).fill("2026-11-01");
  await dialog
    .getByRole("button", { name: "Save record", exact: true })
    .click();
  await expect(dialog).not.toBeVisible();
  await page
    .getByRole("link", { name: "Browser project", exact: true })
    .click();
  await expect(
    page.getByRole("heading", { name: "Browser project", exact: true }),
  ).toBeVisible();
  await page
    .getByRole("button", { name: "Create work items", exact: true })
    .click();
  dialog = page.getByRole("dialog", { name: "Create Work items" });
  await dialog.getByLabel("Name", { exact: true }).fill("Browser work");
  await dialog.getByLabel("Due date", { exact: true }).fill("2026-10-20");
  await dialog
    .getByRole("button", { name: "Save record", exact: true })
    .click();
  await expect(dialog).not.toBeVisible();
  await page
    .getByRole("button", { name: "Edit Browser work", exact: true })
    .click();
  dialog = page.getByRole("dialog", { name: "Edit Work items" });
  await dialog
    .getByRole("combobox", { name: "Status", exact: true })
    .selectOption("ready");
  await dialog
    .getByRole("button", { name: "Save record", exact: true })
    .click();
  await expect(dialog).not.toBeVisible();
  await page.getByRole("button", { name: "Budget lines", exact: true }).click();
  await page
    .getByRole("button", { name: "Create budget lines", exact: true })
    .click();
  dialog = page.getByRole("dialog", { name: "Create Budget lines" });
  await dialog.getByLabel("Name", { exact: true }).fill("Approved budget");
  await dialog.getByLabel("Amount", { exact: true }).fill("1000.10");
  await dialog
    .getByRole("button", { name: "Save record", exact: true })
    .click();
  await expect(dialog).not.toBeVisible();
  await expect(page.getByText("INR 1000.10", { exact: true })).toBeVisible();
  await page.getByRole("button", { name: "Expenditure", exact: true }).click();
  await page
    .getByRole("button", { name: "Create expenditure", exact: true })
    .click();
  dialog = page.getByRole("dialog", { name: "Create Expenditure" });
  await dialog.getByLabel("Name", { exact: true }).fill("Delivery spend");
  await dialog
    .getByLabel("Amount (negative only for reversal)", { exact: true })
    .fill("250.01");
  await dialog
    .getByLabel("Expenditure date", { exact: true })
    .fill("2026-10-06");
  await dialog
    .getByRole("button", { name: "Save record", exact: true })
    .click();
  await expect(dialog).not.toBeVisible();
  await expect(page.getByText("INR 250.01", { exact: true })).toBeVisible();
  await page
    .getByRole("button", { name: "Plan baselines", exact: true })
    .click();
  await page
    .getByRole("button", { name: "Create plan baselines", exact: true })
    .click();
  dialog = page.getByRole("dialog", { name: "Create Plan baselines" });
  await dialog.getByLabel("Name", { exact: true }).fill("Initial plan");
  await dialog
    .getByLabel("Baseline reason", { exact: true })
    .fill("Approved delivery plan");
  await dialog
    .getByRole("button", { name: "Save record", exact: true })
    .click();
  await expect(dialog).not.toBeVisible();
  await expect(
    page.getByText("Version 1 · Approved delivery plan"),
  ).toBeVisible();
  await page.getByRole("button", { name: "Edit project", exact: true }).click();
  dialog = page.getByRole("dialog", { name: "Edit Projects" });
  await dialog
    .getByLabel("Forecast finish", { exact: true })
    .fill("2026-11-15");
  await dialog
    .getByRole("button", { name: "Save record", exact: true })
    .click();
  await expect(dialog).not.toBeVisible();
  await page
    .getByRole("button", { name: "Create plan baselines", exact: true })
    .click();
  dialog = page.getByRole("dialog", { name: "Create Plan baselines" });
  await dialog.getByLabel("Name", { exact: true }).fill("Revised plan");
  await dialog
    .getByLabel("Baseline reason", { exact: true })
    .fill("Reforecast reviewed");
  await dialog
    .getByRole("button", { name: "Save record", exact: true })
    .click();
  await expect(dialog).not.toBeVisible();
  await expect(page.getByText("Version 2 · Reforecast reviewed")).toBeVisible();
  const violations = (
    await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"])
      .analyze()
  ).violations;
  expect(violations.map((v) => v.id)).toEqual([]);
  await page.locator("#main-content").focus();
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.screenshot({
    path: "artifacts/local/sprint04-project-desktop.png",
    fullPage: true,
  });
  await page.setViewportSize({ width: 360, height: 800 });
  expect(
    await page.evaluate(() => document.documentElement.scrollWidth),
  ).toBeLessThanOrEqual(360);
  await page.screenshot({
    path: "artifacts/local/sprint04-project-mobile.png",
    fullPage: true,
  });
  await page.getByRole("button", { name: "Edit project", exact: true }).click();
  dialog = page.getByRole("dialog", { name: "Edit Projects" });
  await dialog.getByLabel("Archived", { exact: true }).check();
  await dialog
    .getByRole("button", { name: "Save record", exact: true })
    .click();
  await page
    .getByRole("button", { name: "Confirm change", exact: true })
    .click();
  await expect(dialog).not.toBeVisible();
  await page.reload();
  await expect(page.getByText(/Archived · restore to edit/)).toBeVisible();
  await page
    .getByRole("combobox", { name: "Organization", exact: true })
    .selectOption(f.viewer_org);
  await expect(
    page.getByRole("alert").filter({ hasText: /not available|completed/ }),
  ).toBeVisible();
  await expect(
    page.getByRole("heading", { name: "Browser project", exact: true }),
  ).toHaveCount(0);
});
