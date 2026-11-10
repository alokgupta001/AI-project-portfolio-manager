import { test as base, type BrowserContext } from "@playwright/test";
export * from "@playwright/test";

/** Domain journeys run after onboarding; dedicated suites verify first visits. */
export async function completeGuides(context: BrowserContext) {
  await context.addInitScript(() => {
    const read = Storage.prototype.getItem;
    Storage.prototype.getItem = function (key) {
      if (key.startsWith("ppm-page-guide-v1:")) return "seen";
      if (key.startsWith("ppm-tutorial-v1:"))
        return JSON.stringify({ version: 1, status: "completed", step: 7 });
      return read.call(this, key);
    };
  });
}
export const test = base.extend({
  context: async ({ context }, use) => {
    await completeGuides(context);
    await use(context);
  },
});
