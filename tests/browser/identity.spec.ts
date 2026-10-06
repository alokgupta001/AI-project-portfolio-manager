import { expect, test } from "@playwright/test";
import { readFileSync } from "node:fs";
import { execFileSync } from "node:child_process";

test("identity lifecycle uses real cookies, memberships, invitations and recovery", async ({
  page,
  context,
}) => {
  test.setTimeout(90000);
  const fixturePath = process.env.PPM_IDENTITY_FIXTURE;
  test.skip(
    !fixturePath,
    "Run scripts/check-identity-browser.mjs for the isolated identity stack",
  );
  const fixture = JSON.parse(readFileSync(fixturePath!, "utf8"));
  const errors: string[] = [];
  page.on("pageerror", (error) => errors.push(error.message));
  await page.goto("/login");
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
  const cookies = await context.cookies();
  for (const name of ["ppm_access", "ppm_refresh"]) {
    const cookie = cookies.find((item) => item.name === name)!;
    expect(cookie.secure).toBe(true);
    expect(cookie.httpOnly).toBe(true);
    expect(cookie.sameSite).toBe("Strict");
  }
  expect(
    await page.evaluate(() =>
      Object.keys(localStorage).filter((key) => key !== "ppm-theme"),
    ),
  ).toEqual([]);
  await page
    .getByLabel("Display name", { exact: true })
    .fill("Updated acceptance admin");
  await page.getByRole("button", { name: "Save profile" }).click();
  await expect(page.getByRole("status")).toHaveText("Profile saved.");
  await page.reload();
  await expect(page.getByLabel("Display name", { exact: true })).toHaveValue(
    "Updated acceptance admin",
  );
  await page.screenshot({
    path: "artifacts/local/identity-account-desktop.png",
    fullPage: true,
  });
  await page
    .getByRole("combobox", { name: "Organization", exact: true })
    .selectOption(fixture.viewer_org);
  await expect(
    page.getByRole("heading", { name: "Membership access" }),
  ).toBeVisible();
  await expect(
    page.getByRole("heading", { name: "Organization members" }),
  ).toHaveCount(0);
  const forbidden = await page.request.get("/api/v1/organization/members");
  expect(forbidden.status()).toBe(403);
  await page.setViewportSize({ width: 360, height: 800 });
  expect(
    await page.evaluate(() => document.documentElement.scrollWidth),
  ).toBeLessThanOrEqual(360);
  await page.screenshot({
    path: "artifacts/local/identity-account-mobile.png",
    fullPage: true,
  });
  await page
    .getByRole("combobox", { name: "Organization", exact: true })
    .selectOption(fixture.admin_org);
  const invited = `invited-${Date.now()}@example.com`;
  await page.getByLabel("Email address", { exact: true }).fill(invited);
  await page.getByRole("button", { name: "Create invitation" }).click();
  await expect(page.getByRole("status")).toHaveText(
    "Invitation created in the local mailbox.",
  );
  const mailbox = (email: string) => {
    const output = execFileSync(
      process.env.PPM_DOCKER || "docker",
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
        "scripts/local_mailbox.py",
        "--email",
        email,
      ],
      { encoding: "utf8" },
    );
    // The fixture email is unique, so exactly one message is expected for each operation.
    return JSON.parse(output).link as string;
  };
  const inviteLink = mailbox(invited);
  await page.getByRole("button", { name: "Sign out", exact: true }).click();
  await expect(page).toHaveURL(/\/login$/);
  await page.goto(inviteLink);
  await page.getByLabel("Display name", { exact: true }).fill("Invited viewer");
  await page.getByLabel("Password (12–72 bytes)").fill(fixture.password);
  await page.getByRole("button", { name: "Verify and continue" }).click();
  await expect(page.getByRole("status")).toContainText("Account verified");
  await page.goto("/login");
  await page.getByLabel("Email address", { exact: true }).fill(invited);
  await page.getByLabel("Password", { exact: true }).fill(fixture.password);
  await page.getByRole("button", { name: "Sign in", exact: true }).click();
  await expect(
    page.getByRole("heading", { name: "Membership access" }),
  ).toBeVisible();
  await page.goto("/account/reset");
  await page.getByLabel("Email address", { exact: true }).fill(invited);
  await page
    .getByRole("button", { name: "Send recovery instructions" })
    .click();
  await expect(page.getByRole("status")).toContainText(
    "If the account is eligible",
  );
  // Mailbox has invitation + reset; select the last JSON object using the operator helper filter.
  const output = execFileSync(
    process.env.PPM_DOCKER || "docker",
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
      "scripts/local_mailbox.py",
      "--email",
      invited,
      "--kind",
      "reset",
    ],
    { encoding: "utf8" },
  );
  await page.goto(JSON.parse(output).link);
  await page
    .getByLabel("Display name", { exact: true })
    .fill("Recovered viewer");
  await page
    .getByLabel("Password (12–72 bytes)")
    .fill(fixture.password + "new");
  await page.getByRole("button", { name: "Verify and continue" }).click();
  await expect(page.getByRole("status")).toContainText("Account verified");
  expect((await page.request.get("/api/v1/auth/me")).status()).toBe(401);
  await page.goto("/login");
  await page.getByLabel("Email address", { exact: true }).fill(invited);
  await page
    .getByLabel("Password", { exact: true })
    .fill(fixture.password + "new");
  await page.getByRole("button", { name: "Sign in", exact: true }).click();
  await expect(
    page.getByRole("heading", { name: "Membership access" }),
  ).toBeVisible();
  expect(errors).toEqual([]);
});
