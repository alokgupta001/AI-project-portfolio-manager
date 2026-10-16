import { test, expect } from "@playwright/test";
import { readFileSync, mkdirSync } from "node:fs";

test("Gemini free-tier disclosure and paused recovery without real provider calls", async ({
  page,
}) => {
  test.skip(
    !process.env.PPM_IDENTITY_FIXTURE,
    "Use the isolated browser runner",
  );
  const fixture = JSON.parse(
    readFileSync(process.env.PPM_IDENTITY_FIXTURE!, "utf8"),
  );
  await page.goto("/login");
  await page
    .getByLabel("Email address", { exact: true })
    .fill(fixture.ai_email);
  await page.getByLabel("Password", { exact: true }).fill(fixture.password);
  await page.getByRole("button", { name: "Sign in", exact: true }).click();
  const switched = page.waitForResponse(
    (r) =>
      r.url().endsWith("/api/v1/auth/switch") &&
      r.request().method() === "POST",
  );
  await page
    .getByRole("combobox", { name: "Organization", exact: true })
    .selectOption(fixture.ai_org);
  expect((await switched).status()).toBe(200);
  let enabled = true;
  await page.route("**/api/v1/ai/status", (route) =>
    route.fulfill({
      json: {
        provider: "gemini",
        enabled,
        reason: enabled
          ? "FREE_TIER_OPERATOR_CONFIRMED"
          : "GEMINI_FREE_TIER_UNCONFIRMED",
        completion_model: "gemini-3.5-flash-lite",
        embedding_model: null,
        real_provider_acceptance: "not_verified",
      },
    }),
  );
  await page.goto("/ai");
  await expect(
    page.getByText("Gemini free tier — $0 spending limit", { exact: true }),
  ).toBeVisible();
  await expect(page.getByText(/Free-tier use is authorized/)).toBeVisible();
  await expect(
    page.getByText(/Free-tier content may be used to improve Google products/),
  ).toBeVisible();
  await expect(
    page.getByRole("button", { name: "Index source embeddings", exact: true }),
  ).toBeDisabled();
  mkdirSync("docs/verification", { recursive: true });
  await page.screenshot({
    path: "docs/verification/gemini-free-tier-ui.png",
    fullPage: true,
  });
  enabled = false;
  await page
    .getByRole("button", { name: "Refresh AI view", exact: true })
    .click();
  await expect(page.getByText(/Gemini is paused/)).toBeVisible();
  await expect(
    page.getByText("AI provider disabled — no model calls", { exact: true }),
  ).toBeVisible();
});
