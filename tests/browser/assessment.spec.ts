import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { readFileSync } from "node:fs";

test("assessment builder, autosave, private evidence and independent review", async ({
  page,
}) => {
  test.setTimeout(120000);
  test.skip(!process.env.PPM_IDENTITY_FIXTURE, "Use isolated browser runner");
  const f = JSON.parse(readFileSync(process.env.PPM_IDENTITY_FIXTURE!, "utf8"));
  async function login(email: string) {
    await page.goto("/login");
    await page.getByLabel("Email address", { exact: true }).fill(email);
    await page.getByLabel("Password", { exact: true }).fill(f.password);
    await page.getByRole("button", { name: "Sign in", exact: true }).click();
    await expect(
      page.getByRole("button", { name: "Sign out", exact: true }),
    ).toBeVisible();
  }
  await login(f.assessment_email);
  await page.goto("/assessments");
  await expect(
    page.getByRole("heading", { name: "Maturity assessments", exact: true }),
  ).toBeVisible();
  await page
    .getByRole("button", { name: "Create framework", exact: true })
    .click();
  let dialog = page.getByRole("dialog");
  await dialog
    .getByLabel("Framework name", { exact: true })
    .fill("Browser governance");
  await dialog.getByRole("button", { name: "Save framework draft" }).click();
  await expect(
    page.getByRole("heading", { name: "Browser governance" }),
  ).toBeVisible();
  await page
    .getByRole("button", { name: "Publish version", exact: true })
    .click();
  await expect(
    page.getByText("Published version 1", { exact: true }),
  ).toBeVisible();
  await page
    .getByRole("button", { name: "Assign assessment", exact: true })
    .click();
  dialog = page.getByRole("dialog");
  await dialog
    .getByLabel("Assessment name", { exact: true })
    .fill("Browser assessment");
  await dialog
    .getByRole("combobox", { name: /^Respondent/ })
    .selectOption(f.assessment_user);
  await dialog
    .getByRole("combobox", { name: /^Independent reviewer/ })
    .selectOption(f.assessment_reviewer);
  await dialog.getByRole("button", { name: "Create assignment" }).click();
  await page.getByRole("button", { name: "Open Browser assessment" }).click();
  await page
    .getByRole("combobox", { name: /^New question \(required\)/ })
    .selectOption("true");
  await expect(page.getByText("Draft saved.", { exact: true })).toBeVisible();
  await page
    .getByLabel("Evidence notes for New question", { exact: true })
    .fill("The operating procedure is approved.");
  await expect(page.getByText("Draft saved.", { exact: true })).toBeVisible();
  await page.getByLabel("Attach evidence for New question").setInputFiles({
    name: "procedure.txt",
    mimeType: "text/plain",
    buffer: Buffer.from("Approved procedure v1"),
  });
  await expect(
    page.getByText("procedure.txt — quarantined", { exact: true }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Submit for review" }).click();
  await expect(
    page.getByText("Assessment submitted.", { exact: true }),
  ).toBeVisible();
  // Switch actor using isolated browser session; no test alters live accounts.
  await page.context().clearCookies();
  await login(f.reviewer_email);
  await page.goto("/assessments");
  await page.getByRole("button", { name: "Open Browser assessment" }).click();
  await page
    .getByLabel("Review or submission note", { exact: true })
    .fill("Confirmed against the approved procedure.");
  await page.getByRole("button", { name: "Start review", exact: true }).click();
  await expect(
    page.getByText("Assessment in review.", { exact: true }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Preview procedure.txt" }).click();
  await expect(
    page.getByText("Approved procedure v1", { exact: true }),
  ).toBeVisible();
  await page
    .getByLabel("Review or submission note", { exact: true })
    .fill("Reviewed plain text; safe to release.");
  await page.getByRole("button", { name: "Release procedure.txt" }).click();
  await expect(
    page.getByRole("link", { name: "procedure.txt", exact: true }),
  ).toBeVisible();
  await page
    .getByLabel("Review or submission note", { exact: true })
    .fill("Independent review complete.");
  await page
    .getByRole("button", { name: "Complete review", exact: true })
    .click();
  await expect(
    page.getByText("Assessment completed.", { exact: true }),
  ).toBeVisible();
  await page.getByText("View chart data table", { exact: true }).click();
  await expect(
    page.getByRole("table", { name: "Assessment scores and coverage" }),
  ).toContainText("100.00");
  await expect(
    page.getByRole("button", { name: "Submit for review" }),
  ).toHaveCount(0);
  for (const width of [1440, 768, 360]) {
    await page.setViewportSize({ width, height: 1000 });
    await expect(
      page.getByRole("heading", { name: "Maturity assessments", exact: true }),
    ).toBeVisible();
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= window.innerWidth,
      ),
    ).toBe(true);
    await page.evaluate(() => {
      (document.activeElement as HTMLElement)?.blur();
      window.scrollTo(0, 0);
    });
    await page.screenshot({
      path: `docs/verification/sprint-06-${width}.png`,
      fullPage: true,
    });
  }
  const axe = await new AxeBuilder({ page }).analyze();
  expect(
    axe.violations.filter((v) =>
      ["critical", "serious"].includes(v.impact || ""),
    ),
  ).toEqual([]);
});
