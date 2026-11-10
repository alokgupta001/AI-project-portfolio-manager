import { test, expect } from "./test";
import AxeBuilder from "@axe-core/playwright";
import { readFileSync } from "node:fs";

test("a second person freezes fixture labels; unavailable API never becomes a quality pass", async ({
  page,
}) => {
  test.setTimeout(150000);
  test.skip(
    !process.env.PPM_IDENTITY_FIXTURE || process.env.PPM_TEST_AI_V2 !== "1",
    "Use isolated guided runner",
  );
  const f = JSON.parse(readFileSync(process.env.PPM_IDENTITY_FIXTURE!, "utf8"));
  async function signIn(email: string) {
    await page.goto("/login");
    await page.getByLabel("Email address", { exact: true }).fill(email);
    await page.getByLabel("Password", { exact: true }).fill(f.password);
    await page.getByRole("button", { name: "Sign in", exact: true }).click();
    await expect(
      page.getByRole("button", { name: "Sign out", exact: true }),
    ).toBeVisible();
    await page.goto("/agents");
    await page
      .getByRole("combobox", { name: "Analysis project", exact: true })
      .selectOption(f.agent_project);
    await page
      .getByText("Evaluate financial API selection", { exact: true })
      .click();
  }
  await signIn(f.agent_email);
  await expect(
    page.getByText(/Ordinary cloud guided reviews can wait up to 60 seconds/),
  ).toBeVisible();
  const pilot = page.getByRole("region", {
    name: "Financial selection pilot",
    exact: true,
  });
  const response = page.waitForResponse(
    (r) =>
      r.url().endsWith("/agents/selection-pilots") &&
      r.request().method() === "POST",
  );
  await pilot
    .getByRole("button", { name: "Prepare selection pilot", exact: true })
    .click();
  const id = (await (await response).json()).id;
  await expect(
    pilot.getByText("awaiting_label_review", { exact: true }),
  ).toBeVisible();
  await expect(
    pilot.getByRole("button", { name: "Measure case f01", exact: true }),
  ).toBeDisabled();
  await expect(
    pilot.getByRole("button", { name: "Freeze reviewed labels", exact: true }),
  ).toHaveCount(0);
  await page.goto("/account");
  await page.getByRole("button", { name: "Sign out", exact: true }).click();
  await page.waitForURL("**/login");
  await signIn(f.pilot_reviewer_email);
  await pilot
    .getByRole("combobox", { name: "Saved selection pilot", exact: true })
    .selectOption(id);
  for (let n = 1; n <= 12; n++) {
    await pilot
      .getByRole("checkbox", {
        name: `Reviewed label f${String(n).padStart(2, "0")}`,
        exact: true,
      })
      .check();
  }
  await pilot
    .getByLabel("Label review reason", { exact: true })
    .fill("Simulated human review for this isolated browser fixture only.");
  await pilot.getByRole("checkbox", { name: /I personally reviewed/ }).check();
  await pilot
    .getByRole("button", { name: "Freeze reviewed labels", exact: true })
    .click();
  await expect(
    pilot.getByText("insufficient_data", { exact: true }),
  ).toBeVisible();
  await pilot
    .getByRole("button", { name: "Measure case f01", exact: true })
    .click();
  await expect(
    pilot.getByText(/This pilot stopped after an unavailable attempt/),
  ).toBeVisible({ timeout: 45000 });
  await expect(
    pilot.getByRole("button", { name: "Measure case f02", exact: true }),
  ).toBeDisabled();
  const downloadEvent = page.waitForEvent("download");
  await pilot
    .getByRole("button", { name: "Download pilot report", exact: true })
    .click();
  const download = await downloadEvent;
  const report = JSON.parse(readFileSync((await download.path())!, "utf8"));
  expect(report.summary.measured_cases).toBe(0);
  expect(report.summary.unavailable_cases).toBe(1);
  expect(report.summary.at17).toBe("BLOCKED");
  expect(report.binding.lineage).toBe("synthetic");
  await page.reload();
  await page
    .getByRole("combobox", { name: "Analysis project", exact: true })
    .selectOption(f.agent_project);
  await page
    .getByText("Evaluate financial API selection", { exact: true })
    .click();
  await expect(
    pilot.getByText(/This pilot stopped after an unavailable attempt/),
  ).toBeVisible();
  for (const width of [1440, 768, 360]) {
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
    await pilot
      .getByRole("heading", { name: "Financial selection pilot", exact: true })
      .scrollIntoViewIfNeeded();
    await page.screenshot({
      path: `test-results/selection-pilot-${width}.png`,
      fullPage: false,
    });
  }
});

test("mocked automated review provenance is explicit in the UI and downloaded report", async ({
  page,
}) => {
  test.skip(
    !process.env.PPM_IDENTITY_FIXTURE || process.env.PPM_TEST_AI_V2 !== "1",
    "Use isolated guided runner",
  );
  const initialTime = new Date();
  await page.clock.install({ time: initialTime });
  const f = JSON.parse(readFileSync(process.env.PPM_IDENTITY_FIXTURE!, "utf8"));
  await page.goto("/login");
  await page.getByLabel("Email address", { exact: true }).fill(f.agent_email);
  await page.getByLabel("Password", { exact: true }).fill(f.password);
  await page.getByRole("button", { name: "Sign in", exact: true }).click();
  await expect(
    page.getByRole("button", { name: "Sign out", exact: true }),
  ).toBeVisible();
  await page.goto("/agents");
  await page
    .getByRole("combobox", { name: "Analysis project", exact: true })
    .selectOption(f.agent_project);
  await page
    .getByText("Evaluate financial API selection", { exact: true })
    .click();
  const pilot = page.getByRole("region", {
    name: "Financial selection pilot",
    exact: true,
  });
  const created = page.waitForResponse(
    (r) =>
      r.url().endsWith("/agents/selection-pilots") &&
      r.request().method() === "POST",
  );
  await pilot
    .getByRole("button", { name: "Prepare selection pilot", exact: true })
    .click();
  let report = await (await created).json();
  report.can_automated_review = true;
  // Only this browser presentation test simulates the operator allowlist/audit.
  // API authorization and durable audit writes are tested by test_selection_pilot.py.
  await page.route("**/agents/selection-pilots**", async (route) => {
    const url = new URL(route.request().url());
    if (url.pathname.endsWith(`/${report.id}/automated-review`)) {
      expect(route.request().postDataJSON()).toEqual({
        corpus_sha256: report.protocol.corpus_sha256,
        strategy_sha256: report.protocol.strategy_sha256,
        synthetic_only: true,
      });
      report = {
        ...report,
        revision: report.revision + 1,
        can_automated_review: false,
        can_review: false,
        binding_current: true,
        review_kind: "automated_rule_audit",
        human_reviewed: false,
        review: { kind: "automated_rule_audit", human_reviewed: false },
        summary: {
          ...report.summary,
          state: "insufficient_data",
          label_review_kind: "automated_rule_audit",
          independent_human_review: false,
        },
      };
      await route.fulfill({ json: report });
    } else if (route.request().method() === "GET") {
      await route.fulfill({
        json: url.pathname.endsWith(`/${report.id}`) ? report : [report],
      });
    } else await route.continue();
  });
  await pilot
    .getByRole("button", { name: "Refresh pilot", exact: true })
    .click();
  await pilot
    .getByRole("button", { name: "Run approved automated check", exact: true })
    .click();
  await expect(
    pilot.getByText(
      /Automated arithmetic check recorded. Human review: false./,
    ),
  ).toBeVisible();
  await expect(
    pilot.getByRole("checkbox", { name: /I personally reviewed/ }),
  ).toHaveCount(0);
  await expect(
    pilot.getByRole("button", { name: "Measure case f01", exact: true }),
  ).toBeEnabled();
  const downloaded = page.waitForEvent("download");
  await pilot
    .getByRole("button", { name: "Download pilot report", exact: true })
    .click();
  const file = await downloaded;
  const saved = JSON.parse(readFileSync((await file.path())!, "utf8"));
  expect(saved.review_kind).toBe("automated_rule_audit");
  expect(saved.human_reviewed).toBe(false);
  expect(saved.summary.independent_human_review).toBe(false);
  expect(saved.summary.measured_cases).toBe(0);
  expect(saved.summary.at17).toBe("BLOCKED");
  const pausedAt = new Date(initialTime.getTime() + 60000);
  report.next_case_at = new Date(pausedAt.getTime() - 1000).toISOString();
  await page.clock.pauseAt(pausedAt);
  await page.reload();
  const projectSelector = page.getByRole("combobox", {
    name: "Analysis project",
    exact: true,
  });
  // Advance setup timers until choices arrive. The pilot is not mounted until
  // selecting a project, so its first interval cannot repair the initial state.
  await expect
    .poll(async () => {
      await page.clock.runFor(200);
      return projectSelector
        .locator(`option[value="${f.agent_project}"]`)
        .count();
    })
    .toBe(1);
  await projectSelector.selectOption(f.agent_project);
  await page
    .getByText("Evaluate financial API selection", { exact: true })
    .click();
  // No interval tick can repair an incorrect initial clock while time is paused.
  await expect(
    pilot.getByRole("button", { name: "Measure case f01", exact: true }),
  ).toBeEnabled();
  const mountedAt = await page.evaluate(() => Date.now());
  report.next_case_at = new Date(mountedAt + 30000).toISOString();
  await pilot
    .getByRole("button", { name: "Refresh pilot", exact: true })
    .click();
  await expect(
    pilot.getByRole("button", { name: "Measure case f01", exact: true }),
  ).toBeDisabled();
  await page.clock.runFor(30000);
  await expect(
    pilot.getByRole("button", { name: "Measure case f01", exact: true }),
  ).toBeEnabled();
  await page.clock.resume();
  report.cases[0] = {
    ...report.cases[0],
    status: "unavailable",
    diagnostic: "TIMEOUT",
    latency_ms: 22000,
    elapsed_ms: 22000,
    timing_kind: "unavailable_attempt",
  };
  await pilot
    .getByRole("button", { name: "Refresh pilot", exact: true })
    .click();
  await expect(
    pilot.getByText(
      /Unavailable attempt elapsed: 22000 ms \(excluded from p95\)/,
    ),
  ).toBeVisible();
  await expect(
    pilot.getByRole("button", { name: "Measure case f02", exact: true }),
  ).toBeDisabled();
  const timingDownload = page.waitForEvent("download");
  await pilot
    .getByRole("button", { name: "Download pilot report", exact: true })
    .click();
  const timingFile = await timingDownload;
  const timingReport = JSON.parse(
    readFileSync((await timingFile.path())!, "utf8"),
  );
  expect(timingReport.cases[0].elapsed_ms).toBe(22000);
  expect(timingReport.cases[0].timing_kind).toBe("unavailable_attempt");
  expect(timingReport.summary.p95_ms).toBeNull();
  for (const width of [1440, 768, 360]) {
    await page.setViewportSize({ width, height: 1000 });
    await pilot
      .getByText(/Unavailable attempt elapsed: 22000 ms/)
      .scrollIntoViewIfNeeded();
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
    await page.screenshot({ path: `test-results/pilot-timing-${width}.png` });
  }
  report.cases[0] = {
    ...report.cases[0],
    latency_ms: 0,
    elapsed_ms: null,
    timing_kind: "not_recorded",
  };
  await pilot
    .getByRole("button", { name: "Refresh pilot", exact: true })
    .click();
  await expect(pilot.getByText(/Elapsed time not recorded/)).toBeVisible();
});
