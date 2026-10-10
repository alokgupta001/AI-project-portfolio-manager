import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { readFileSync } from "node:fs";

test("password visibility, retained input, profile editing and account without membership", async ({
  page,
}) => {
  test.setTimeout(90000);
  test.skip(!process.env.PPM_IDENTITY_FIXTURE, "Use isolated browser runner");
  const f = JSON.parse(readFileSync(process.env.PPM_IDENTITY_FIXTURE!, "utf8"));
  await page.goto("/login");
  const password = page.getByLabel("Password", { exact: true });
  await password.fill(f.password);
  await expect(password).toHaveAttribute("type", "password");
  await page
    .getByRole("button", { name: "Show password", exact: true })
    .focus();
  await page.keyboard.press("Enter");
  await expect(password).toHaveAttribute("type", "text");
  await expect(password).toHaveValue(f.password);
  await page.keyboard.press("Space");
  await expect(password).toHaveAttribute("type", "password");
  await expect(password).toHaveValue(f.password);
  await page.getByLabel("Email address", { exact: true }).fill(f.no_org_email);
  await page.getByRole("button", { name: "Sign in", exact: true }).click();
  await expect(
    page.getByRole("heading", { name: "Your account is active" }),
  ).toBeVisible();
  await expect(
    page.getByText("You have no active organization memberships.", {
      exact: false,
    }),
  ).toBeVisible();
  await page
    .getByLabel("Display name", { exact: true })
    .fill("Account without an organization");
  await page.getByRole("button", { name: "Save profile", exact: true }).click();
  await expect(
    page.getByRole("status").filter({ hasText: "Profile saved." }),
  ).toBeVisible();
  await page.reload();
  await expect(page.getByLabel("Display name", { exact: true })).toHaveValue(
    "Account without an organization",
  );
  await page.goto("/projects");
  await expect(
    page.getByRole("heading", { name: "Your account is active" }),
  ).toBeVisible();
  await expect(
    page.getByRole("button", { name: "Create projects", exact: true }),
  ).toHaveCount(0);
  await page.context().clearCookies();
  await page.goto("/login");
  await page.getByLabel("Email address", { exact: true }).fill(f.email);
  await password.fill("incorrect-password");
  await page.getByRole("button", { name: "Sign in", exact: true }).click();
  await expect(
    page.getByRole("alert").filter({ hasText: "Sign-in failed" }),
  ).toBeVisible();
  await expect(password).toHaveValue("incorrect-password");
  await password.fill(f.password);
  await page.getByRole("button", { name: "Sign in", exact: true }).click();
  await page
    .getByRole("combobox", { name: "Organization", exact: true })
    .selectOption(f.admin_org);
  const profile = page.locator("#organization-profile");
  await expect(
    profile.getByLabel("Organization name", { exact: true }),
  ).toHaveCount(0);
  await profile.getByRole("button", { name: "Edit name", exact: true }).click();
  await expect(
    profile.getByRole("button", { name: "Save organization name" }),
  ).toBeDisabled();
  await profile
    .getByLabel("Organization name", { exact: true })
    .fill("Discard this name");
  await profile.getByRole("button", { name: "Cancel name change" }).click();
  await expect(
    profile.getByRole("heading", { name: "Discard this name" }),
  ).toHaveCount(0);
  await profile.getByRole("button", { name: "Edit name", exact: true }).click();
  await profile
    .getByLabel("Organization name", { exact: true })
    .fill("Repair browser organization");
  await profile.getByRole("button", { name: "Save organization name" }).click();
  await expect(profile.getByRole("status")).toContainText(
    "Organization name saved",
  );
  await profile
    .getByRole("button", { name: "Edit organization details" })
    .click();
  await profile
    .getByLabel("Short description", { exact: true })
    .fill("Fictional browser verification");
  await profile.getByLabel("Industry", { exact: true }).fill("Technology");
  await profile
    .getByLabel("Website", { exact: true })
    .fill("https://example.com/");
  await page.route("**/api/v1/organization/profile", async (route) => {
    if (route.request().method() === "PATCH") await route.abort("failed");
    else await route.continue();
  });
  await profile
    .getByRole("button", { name: "Save organization details" })
    .click();
  await expect(profile.getByRole("alert")).toBeVisible();
  await expect(
    profile.getByRole("textbox", { name: "Short description", exact: true }),
  ).toHaveValue("Fictional browser verification");
  await page.unroute("**/api/v1/organization/profile");
  await profile
    .getByRole("button", { name: "Save organization details" })
    .click();
  await expect(profile.getByRole("status")).toContainText(
    "Organization details saved",
  );
  await page.reload();
  await expect(profile).toContainText("Fictional browser verification");
  await expect(profile).toContainText("Administrators:");
  for (const width of [1440, 768, 360]) {
    await page.setViewportSize({ width, height: 900 });
    await expect(
      profile.getByRole("heading", { name: "Repair browser organization" }),
    ).toBeVisible();
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= window.innerWidth,
      ),
    ).toBe(true);
    await page.screenshot({
      path: `artifacts/local/repair-20261010/account-${width}.png`,
      fullPage: true,
    });
  }
  const axe = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"])
    .analyze();
  expect(axe.violations.map((v) => v.id)).toEqual([]);
});
