import { defineConfig, devices } from "@playwright/test";
export default defineConfig({
  testDir: "./tests/browser", fullyParallel: false, retries: 0,
  reporter: [["list"], ["html", { open: "never" }]],
  use: { baseURL: process.env.PPM_WEB_URL || "http://localhost:3000", trace: "retain-on-failure" },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
});
