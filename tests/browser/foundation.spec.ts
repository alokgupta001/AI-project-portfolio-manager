import { expect, test } from "@playwright/test";

test("web renders the real API database checkpoint and reloads it", async ({
  page,
  request,
}) => {
  const errors: string[] = [];
  page.on("pageerror", (error) => errors.push(error.message));
  const api = process.env.PPM_API_URL || "http://127.0.0.1:8000";
  const response = await request.get(`${api}/api/v1/foundation`);
  expect(response.ok()).toBeTruthy();
  const data = await response.json();
  await page.goto("/system");
  await expect(
    page.getByRole("heading", { name: "Foundation status" }),
  ).toBeVisible();
  await expect(page.getByText("Services ready", { exact: true })).toBeVisible();
  await expect(page.getByTestId("instance-id")).toHaveText(data.instance_id);
  await page.keyboard.press("Tab");
  await expect(
    page.getByRole("link", { name: "P Enterprise PPM" }),
  ).toBeFocused();
  await page.keyboard.press("Tab");
  await expect(
    page.getByRole("link", { name: /Refresh status/ }),
  ).toBeFocused();
  await page.keyboard.press("Enter");
  await expect(page.getByTestId("instance-id")).toHaveText(data.instance_id);
  await page.getByRole("link", { name: /Refresh status/ }).click();
  await expect(page.getByTestId("instance-id")).toHaveText(data.instance_id);
  expect(errors).toEqual([]);
  await page.screenshot({
    path: "artifacts/local/foundation-desktop.png",
    fullPage: true,
  });
});

test("mobile foundation remains readable without horizontal overflow", async ({
  page,
}) => {
  await page.setViewportSize({ width: 360, height: 800 });
  await page.goto("/system");
  await expect(
    page.getByRole("heading", { name: "Foundation status" }),
  ).toBeVisible();
  expect(
    await page.evaluate(() => document.documentElement.scrollWidth),
  ).toBeLessThanOrEqual(360);
  await page.screenshot({
    path: "artifacts/local/foundation-mobile.png",
    fullPage: true,
  });
});
