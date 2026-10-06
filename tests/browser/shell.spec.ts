import { test, expect, type Page } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { readFileSync } from "node:fs";

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
test("enterprise shell: themes, keyboard, responsive, gallery and permissions", async ({
  page,
}) => {
  test.setTimeout(120000);
  const fixturePath = process.env.PPM_IDENTITY_FIXTURE;
  test.skip(!fixturePath, "Use the isolated identity browser runner");
  const fixture = JSON.parse(readFileSync(fixturePath!, "utf8"));
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto("/login");
  await accessible(page);
  await page.getByLabel("Email address", { exact: true }).fill(fixture.email);
  await page.getByLabel("Password", { exact: true }).fill(fixture.password);
  await page.getByRole("button", { name: "Sign in", exact: true }).click();
  await expect(
    page.getByRole("heading", { name: "Active organization" }),
  ).toBeVisible();
  await page
    .getByRole("combobox", { name: "Organization", exact: true })
    .selectOption(fixture.admin_org);
  await expect(
    page.getByRole("heading", { name: "Organization members" }),
  ).toBeVisible();
  await accessible(page);
  // Confirm destructive actions without revoking this acceptance session.
  await page
    .getByRole("button", { name: "Revoke current", exact: true })
    .click();
  await expect(
    page.getByRole("dialog", { name: "Revoke session?" }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Cancel", exact: true }).click();
  await expect(
    page.getByRole("button", { name: "Revoke current", exact: true }),
  ).toBeFocused();
  await page.goto("/");
  await expect(page.getByRole("heading", { name: /Welcome,/ })).toBeVisible();
  await page.keyboard.press("Tab");
  await expect(
    page.getByRole("link", { name: "Skip to main content" }),
  ).toBeFocused();
  await page.keyboard.press("Enter");
  await expect(page.locator("#main-content")).toBeFocused();
  await page.keyboard.press("Control+k");
  await expect(
    page.getByRole("dialog", { name: "Workspace commands" }),
  ).toBeVisible();
  await page.getByLabel("Find a page").fill("account");
  await page.keyboard.press("ArrowDown");
  await expect(
    page
      .getByRole("navigation", { name: "Available commands" })
      .getByRole("link", { name: "Account & access" }),
  ).toBeFocused();
  await page.keyboard.press("Escape");
  await page.getByRole("button", { name: "Open notifications" }).click();
  await accessible(page);
  await page.keyboard.press("Escape");
  await expect(
    page.getByRole("button", { name: "Open notifications" }),
  ).toBeFocused();
  for (const theme of ["light", "dark"]) {
    if ((await page.locator("html").getAttribute("data-theme")) !== theme)
      await page
        .getByRole("button", { name: `Switch to ${theme} theme` })
        .click();
    for (const width of [360, 768, 1440]) {
      await page.setViewportSize({ width, height: 1000 });
      expect(
        await page.evaluate(() => document.documentElement.scrollWidth),
      ).toBeLessThanOrEqual(width);
      await accessible(page);
      await page.screenshot({
        path: `artifacts/local/sprint03-home-${theme}-${width}.png`,
        fullPage: true,
      });
    }
  }
  await page.reload();
  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("/design-system");
  await expect(
    page.getByRole("heading", { name: "Component gallery" }),
  ).toBeVisible();
  await expect(page.locator(".skeleton div").first()).toHaveCSS(
    "animation-name",
    "none",
  );
  await page.getByRole("button", { name: "Next", exact: true }).click();
  await expect(page.getByText("Page 2 of 2")).toBeVisible();
  await page.getByLabel("Filter Example activities").fill("governance");
  await expect(
    page.getByRole("cell", { name: "Governance review", exact: true }),
  ).toBeVisible();
  await expect(page.getByText("Page 1 of 1")).toBeVisible();
  await page.getByLabel("Filter Example activities").fill("no such item");
  await expect(
    page.getByText("No matching records. Try a different filter."),
  ).toBeVisible();
  await page.getByLabel("Filter Example activities").fill("");
  await page.getByRole("button", { name: /Activity/ }).click();
  await expect(
    page.getByRole("columnheader", { name: /Activity/ }),
  ).toHaveAttribute("aria-sort", "ascending");
  await page.getByText("View chart data table").click();
  await accessible(page);
  await page.getByRole("button", { name: "Open example drawer" }).click();
  await accessible(page);
  await page.keyboard.press("Escape");
  await expect(
    page.getByRole("button", { name: "Open example drawer" }),
  ).toBeFocused();
  await page.setViewportSize({ width: 360, height: 800 });
  await page.getByRole("button", { name: "Open navigation" }).click();
  await accessible(page);
  await page.keyboard.press("Escape");
  expect(
    await page.evaluate(() => document.documentElement.scrollWidth),
  ).toBeLessThanOrEqual(360);
  await page.goto("/account");
  await page
    .getByRole("combobox", { name: "Organization", exact: true })
    .selectOption(fixture.viewer_org);
  await expect(
    page.getByRole("heading", { name: "Membership access" }),
  ).toBeVisible();
  await page.keyboard.press("Control+k");
  await expect(
    page
      .getByRole("navigation", { name: "Available commands" })
      .getByRole("link", { name: "Organization members" }),
  ).toHaveCount(0);
  await page.keyboard.press("Escape");
  await accessible(page);
  expect(errors).toEqual([]);
});
