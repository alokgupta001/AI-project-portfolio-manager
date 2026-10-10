import { test, expect, type Page, type Locator } from "@playwright/test";
import { readFileSync, writeFileSync } from "node:fs";
import { spawnSync } from "node:child_process";
import {
  fields,
  labels,
  type Kind,
} from "../../apps/web/components/delivery-fields";

test("complete Northstar website walkthrough through delivery, independent review and Viewer revocation", async ({
  browser,
}) => {
  test.setTimeout(900000);
  test.skip(!process.env.PPM_IDENTITY_FIXTURE, "Use isolated browser runner");
  const fixture = JSON.parse(
    readFileSync(process.env.PPM_IDENTITY_FIXTURE!, "utf8"),
  );
  const evidence: {
    section: string;
    action: string;
    status: string;
    record?: string;
  }[] = [];
  let current = "4";
  const pass = (section: string, action: string, record?: string) => {
    evidence.push({ section, action, status: "PASS", record });
    writeFileSync(
      "artifacts/local/repair-20261010/walkthrough-browser.json",
      JSON.stringify(evidence, null, 2),
    );
  };
  const contexts = await Promise.all(
    [0, 1, 2, 3].map(() =>
      browser.newContext({ baseURL: process.env.PPM_WEB_URL }),
    ),
  );
  const [asha, priya, ravi, vera] = await Promise.all(
    contexts.map((c) => c.newPage()),
  );
  for (const p of [asha, priya, ravi, vera]) p.setDefaultTimeout(20000);
  const names = ["Asha Admin", "Priya Manager", "Ravi Reviewer", "Vera Viewer"];
  const roles = ["Admin", "Project Manager", "Project Manager", "Viewer"];
  const emails = names.map(
    (_, i) => `walkthrough-${i}-${crypto.randomUUID()}@example.com`,
  );
  const people: string[] = [];
  let project = "";
  let organization = "";
  const resourceKinds: Kind[] = [
    "resources",
    "calendars",
    "resource_access",
    "availability",
    "resource_teams",
    "resource_skills",
    "allocations",
    "time_off",
    "effort",
    "effort_coverage",
  ];
  const orgKinds: Kind[] = [
    "settings",
    "departments",
    "teams",
    "team_members",
    "goals",
    "grants",
    "metric_policies",
  ];
  function mail(email: string) {
    const result = spawnSync(
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
        "scripts/pilot_browser_mail.py",
        email,
      ],
      { encoding: "utf8", env: process.env },
    );
    expect(result.status).toBe(0);
    return JSON.parse(result.stdout)[0].link as string;
  }
  async function login(p: Page, i: number) {
    await p.goto("/login");
    await p.getByLabel("Email address", { exact: true }).fill(emails[i]);
    await p.getByLabel("Password", { exact: true }).fill(fixture.password);
    await p.getByRole("button", { name: "Sign in", exact: true }).click();
    await expect(
      p.getByRole("button", { name: "Sign out", exact: true }),
    ).toBeVisible();
    const me = await (await p.request.get("/api/v1/auth/me")).json();
    expect(me.name).toBe(names[i]);
    expect(me.role).toBe(roles[i]);
    organization = me.organization_id;
    people[i] = me.id;
  }
  async function complete(p: Page, email: string, i: number) {
    await p.goto(mail(email));
    await p.getByLabel("Display name", { exact: true }).fill(names[i]);
    await p
      .getByLabel("Password (12–72 bytes)", { exact: true })
      .fill(fixture.password);
    await p
      .getByRole("button", { name: "Verify and continue", exact: true })
      .click();
    await expect(p.getByRole("status")).toContainText("Account verified");
    await login(p, i);
  }
  async function navigate(p: Page, kind: Kind) {
    if (resourceKinds.includes(kind)) {
      await p.goto("/resources");
      if (p === priya)
        await p
          .getByRole("combobox", { name: "Resource profile", exact: true })
          .selectOption({ label: "Priya delivery capacity" });
      await p
        .getByRole("combobox", { name: "Planning records", exact: true })
        .selectOption(kind);
    } else if (orgKinds.includes(kind)) {
      await p.goto("/organization");
      if (kind !== "settings")
        await p
          .getByRole("button", { name: labels[kind], exact: true })
          .click();
    } else if (["portfolios", "programs"].includes(kind)) {
      await p.goto("/portfolios");
      await p.getByRole("button", { name: labels[kind], exact: true }).click();
    } else if (kind === "projects") await p.goto("/projects");
    else {
      await p.goto("/projects/" + project);
      await p.getByRole("button", { name: labels[kind], exact: true }).click();
    }
  }
  async function fill(
    dialog: Locator,
    kind: Kind,
    values: Record<string, string | boolean>,
  ) {
    for (const [key, value] of Object.entries(values)) {
      const spec = fields[kind].find((f) => f.key === key);
      const control = dialog.getByLabel(
        spec?.label ||
          (key === "name"
            ? "Name"
            : key === "description"
              ? kind === "baselines"
                ? "Baseline reason"
                : "Description"
              : "Archived"),
        { exact: true },
      );
      if (
        key === "project_id" &&
        (await dialog
          .getByRole("combobox", { name: "Project", exact: true })
          .count()) === 0
      )
        continue;
      if (spec?.reference || spec?.options)
        await dialog
          .getByRole("combobox", { name: spec.label, exact: true })
          .selectOption(String(value));
      else if (spec?.type === "checkbox" || key === "archived")
        await control.setChecked(Boolean(value));
      else await control.fill(String(value));
    }
  }
  async function create(
    p: Page,
    section: string,
    kind: Kind,
    name: string,
    values: Record<string, string | boolean> = {},
    expectedStatus = 201,
  ) {
    current = section;
    const descriptions: Record<string, string> = {
      "Digital Delivery":
        "Owns the customer portal and its delivery practices.",
      "Portal Delivery Team":
        "Plans, builds, tests and releases the onboarding portal.",
      "Reduce customer onboarding effort":
        "Enable self-service onboarding and target 100 staff hours saved per reporting period.",
      "Customer Experience Portfolio":
        "Customer-facing improvements with measurable service benefits.",
      "Customer Self-Service Program":
        "Coordinates the portal and related customer self-service work.",
      "Northstar training metric policy":
        "Training thresholds for deterministic risk indicators.",
      "India weekday calendar — v1":
        "Training calendar: eight hours per weekday.",
      "Priya delivery capacity":
        "Training resource linked to the project manager.",
      "Customer Onboarding Portal":
        "Deliver a self-service onboarding portal; success means an agreed release and evidence of lower manual follow-up.",
      "Portal Sprint 1":
        "Confirm requirements and prepare the first portal slice.",
      "Confirm onboarding requirements":
        "Capture required fields, validation and acceptance criteria.",
      "Build onboarding form":
        "Implement the agreed portal form for the training release.",
      "Run acceptance checks":
        "Validate form completion and agreed error handling.",
      "Requirements agreed":
        "Training scope and acceptance criteria confirmed.",
      "Portal release": "Agreed portal release ready for customers.",
      "Portal delivery budget": "Training budget allocation.",
      "Portal design workshop": "Fictional training expenditure.",
      "Customer validation rules may arrive late":
        "Late agreement on validation rules could delay the portal form.",
      "Awaiting validation examples":
        "Training blocker: missing valid and invalid customer examples.",
      "Onboarding administration hours saved":
        "Fictional measured benefit for the training period.",
      "Portal approved plan — v1":
        "Initial training schedule and budget before changes.",
      "Portal measurement plan — v1":
        "Manual training estimate of final delivery cost.",
      "Portal weekly update — 12 October":
        "Requirements are being confirmed. Validation examples are outstanding. Mitigation owner: Priya; next review: 16 October.",
    };
    if (descriptions[name])
      values = { ...values, description: descriptions[name] };
    await navigate(p, kind);
    await p
      .getByRole("button", {
        name:
          kind === "settings"
            ? "Configure organization"
            : `Create ${labels[kind].toLowerCase()}`,
        exact: true,
      })
      .click();
    const dialog = p.getByRole("dialog", {
      name: `Create ${labels[kind]}`,
      exact: true,
    });
    await fill(dialog, kind, { name, ...values });
    const response = p.waitForResponse(
      (r) =>
        r.request().method() === "POST" &&
        r.url().endsWith("/delivery/" + kind),
    );
    await dialog
      .getByRole("button", { name: "Save record", exact: true })
      .click();
    const saved = await response;
    expect(saved.status(), await saved.text()).toBe(expectedStatus);
    if (expectedStatus !== 201) {
      await expect(dialog.getByRole("alert")).toContainText(
        "already has a grant",
      );
      await expect(dialog.getByLabel("Name", { exact: true })).toHaveValue(
        name,
      );
      await dialog.getByRole("button", { name: "Cancel", exact: true }).click();
      pass(
        section,
        "Duplicate grant returns actionable conflict and retains unsaved values",
      );
      return "";
    }
    const record = await saved.json();
    await expect(dialog).not.toBeVisible();
    const reload = await p.request.get(`/api/v1/delivery/${kind}/${record.id}`);
    expect(reload.status()).toBe(200);
    const data = (await reload.json()).data;
    expect(data.name).toBe(name);
    for (const [key, value] of Object.entries(values)) {
      const spec = fields[kind].find((f) => f.key === key);
      if (spec?.type === "number")
        expect(Number(data[key])).toBe(Number(value));
      else expect(data[key]).toBe(value);
    }
    pass(section, `Create, save and reload ${name}`, record.id);
    return record.id as string;
  }
  async function edit(
    p: Page,
    section: string,
    kind: Kind,
    name: string,
    values: Record<string, string | boolean>,
  ) {
    current = section;
    await navigate(p, kind);
    await p.getByRole("button", { name: `Edit ${name}`, exact: true }).click();
    const dialog = p.getByRole("dialog", {
      name: `Edit ${labels[kind]}`,
      exact: true,
    });
    await fill(dialog, kind, values);
    const response = p.waitForResponse(
      (r) =>
        r.request().method() === "PATCH" &&
        r.url().includes("/delivery/" + kind + "/"),
    );
    await dialog
      .getByRole("button", { name: "Save record", exact: true })
      .click();
    if (kind === "grants" || kind === "resource_access" || "archived" in values)
      await p
        .getByRole("button", { name: "Confirm change", exact: true })
        .click();
    const saved = await response;
    expect(saved.status(), await saved.text()).toBe(200);
    await expect(dialog).not.toBeVisible();
    pass(
      section,
      `Edit and persist ${name}: ${Object.keys(values).join(", ")}`,
    );
  }
  async function openAssessment(p: Page, name: string) {
    await p.goto("/assessments");
    await p.getByRole("button", { name: `Open ${name}`, exact: true }).click();
  }
  try {
    await asha.goto("/signup");
    await asha.getByLabel("Email address", { exact: true }).fill(emails[0]);
    await asha
      .getByLabel("Organization name", { exact: true })
      .fill("Northstar Website Training");
    await asha
      .getByRole("button", { name: "Send verification instructions" })
      .click();
    await expect(asha.getByRole("status")).toContainText("If eligible");
    await complete(asha, emails[0], 0);
    await expect(asha.locator("#organization-profile")).toContainText(
      "Asha Admin",
    );
    await expect(
      asha.locator("#organization-profile").getByRole("heading", {
        name: "Northstar Website Training",
        exact: true,
      }),
    ).toBeVisible();
    await asha.goto("/");
    await expect(
      asha.getByRole("heading", { name: "Getting started", exact: true }),
    ).toBeVisible();
    await asha.goto("/account");
    pass(
      "4",
      "Request verification, activate, authenticate and confirm first Admin",
    );
    current = "5";
    for (const [i, p] of [
      [1, priya],
      [2, ravi],
      [3, vera],
    ] as const) {
      await asha.getByLabel("Email address", { exact: true }).fill(emails[i]);
      await asha
        .getByRole("combobox", { name: "Role", exact: true })
        .selectOption(roles[i]);
      const invitation = asha.waitForResponse(
        (r) =>
          r.request().method() === "POST" &&
          r.url().endsWith("/organization/invitations"),
      );
      await asha
        .getByRole("button", { name: "Create invitation", exact: true })
        .click();
      expect((await invitation).status()).toBe(201);
      await complete(p, emails[i], i);
      pass(
        "5.1–5.2",
        `Invite and accept ${names[i]} with ${roles[i]} membership`,
      );
    }
    const dates = { start_date: "2026-10-12", end_date: "2026-11-07" };
    await create(asha, "6.1", "settings", "Northstar operating settings", {
      description: "Training organization using India time and INR reporting.",
      timezone: "Asia/Kolkata",
      currency: "INR",
    });
    const department = await create(
      asha,
      "6.2",
      "departments",
      "Digital Delivery",
      { owner_id: people[0] },
    );
    const team = await create(asha, "6.3", "teams", "Portal Delivery Team", {
      department_id: department,
      owner_id: people[1],
    });
    for (const i of [1, 2])
      await create(
        asha,
        "6.4",
        "team_members",
        `${names[i].split(" ")[0]} — Portal Delivery Team`,
        { team_id: team, user_id: people[i], start_date: "2026-10-12" },
      );
    const goal = await create(
      asha,
      "6.5",
      "goals",
      "Reduce customer onboarding effort",
      { owner_id: people[0] },
    );
    const portfolio = await create(
      asha,
      "6.6",
      "portfolios",
      "Customer Experience Portfolio",
      { owner_id: people[0] },
    );
    const program = await create(
      asha,
      "6.6",
      "programs",
      "Customer Self-Service Program",
      { portfolio_id: portfolio, owner_id: people[1] },
    );
    await create(asha, "6.7", "grants", "Priya — customer portfolio manage", {
      user_id: people[1],
      portfolio_id: portfolio,
      access: "manage",
    });
    await create(asha, "6.7", "grants", "Vera — customer portfolio read", {
      user_id: people[3],
      portfolio_id: portfolio,
      access: "read",
    });
    await create(
      asha,
      "6.8",
      "metric_policies",
      "Northstar training metric policy",
      { amber: "30", red: "60", stale_days: "7" },
    );
    const calendar = await create(
      asha,
      "7",
      "calendars",
      "India weekday calendar — v1",
      {
        timezone: "Asia/Kolkata",
        monday: "8",
        tuesday: "8",
        wednesday: "8",
        thursday: "8",
        friday: "8",
        saturday: "0",
        sunday: "0",
      },
    );
    const resource = await create(
      asha,
      "7",
      "resources",
      "Priya delivery capacity",
      { user_id: people[1] },
    );
    await create(
      asha,
      "7",
      "resource_access",
      "Priya — own training resource management",
      {
        resource_id: resource,
        user_id: people[1],
        manage: true,
        effort: false,
      },
    );
    await create(asha, "7", "availability", "Priya — October availability", {
      resource_id: resource,
      calendar_id: calendar,
      ...dates,
    });
    await create(asha, "7", "resource_teams", "Priya — portal staffing", {
      resource_id: resource,
      team_id: team,
      ...dates,
    });
    await create(asha, "7", "resource_skills", "Priya — delivery planning", {
      resource_id: resource,
      skill: "Project delivery planning",
    });
    project = await create(
      priya,
      "8.1",
      "projects",
      "Customer Onboarding Portal",
      {
        description:
          "Deliver a self-service onboarding portal and lower manual follow-up.",
        portfolio_id: portfolio,
        program_id: program,
        department_id: department,
        team_id: team,
        owner_id: people[1],
        priority: "high",
        industry: "technology",
        category: "delivery",
        methodology: "agile",
        size_band: "small",
        status: "active",
        reported_health: "Green",
        currency: "INR",
        start_date: "2026-10-12",
        target_end_date: "2026-11-06",
        forecast_end_date: "2026-11-06",
      },
    );
    await create(asha, "8.2", "grants", "Ravi — portal project read", {
      user_id: people[2],
      project_id: project,
      access: "read",
    });
    await create(
      asha,
      "H",
      "grants",
      "Duplicate Ravi grant",
      {
        user_id: people[2],
        project_id: project,
        access: "read",
      },
      409,
    );
    await create(priya, "8.3", "sprints", "Portal Sprint 1", {
      project_id: project,
      team_id: team,
      start_date: "2026-10-12",
      end_date: "2026-10-23",
      status: "planned",
    });
    await edit(priya, "8.3", "sprints", "Portal Sprint 1", {
      status: "active",
    });
    const sprintList = await (
      await priya.request.get("/api/v1/delivery/sprints")
    ).json();
    const sprint = sprintList.items.find(
      (r: { data: { name: string } }) => r.data.name === "Portal Sprint 1",
    ).id;
    const work: string[] = [];
    const workNames = [
      "Confirm onboarding requirements",
      "Build onboarding form",
      "Run acceptance checks",
    ];
    for (const [i, points, type, start, due] of [
      [0, "3", "story", "2026-10-12", "2026-10-14"],
      [1, "5", "feature", "2026-10-15", "2026-10-21"],
      [2, "2", "task", "2026-10-21", "2026-10-23"],
    ] as const)
      work.push(
        await create(priya, "8.4", "work_items", workNames[i], {
          project_id: project,
          sprint_id: sprint,
          owner_id: people[1],
          work_type: type,
          priority: i === 2 ? "normal" : "high",
          points,
          status: i === 0 ? "ready" : "backlog",
          start_date: start,
          due_date: due,
        }),
      );
    const milestone = await create(
      priya,
      "8.5",
      "milestones",
      "Requirements agreed",
      { project_id: project, due_date: "2026-10-14", critical: true },
    );
    await create(priya, "8.5", "milestones", "Portal release", {
      project_id: project,
      due_date: "2026-11-06",
      critical: true,
    });
    await create(priya, "8.6", "budget_lines", "Portal delivery budget", {
      project_id: project,
      amount: "200000",
      currency: "INR",
      approved: true,
    });
    await create(priya, "8.6", "expenditures", "Portal design workshop", {
      project_id: project,
      amount: "20000",
      currency: "INR",
      spent_on: "2026-10-12",
    });
    const financial = await (
      await priya.request.get("/api/v1/delivery/project-summary/" + project)
    ).json();
    expect(Number(financial.money[0].approved_budget)).toBe(200000);
    expect(Number(financial.money[0].recorded_spend)).toBe(20000);
    pass(
      "8.6",
      "Project summary reconciles INR 200000 budget and INR 20000 partial ledger",
    );
    await create(
      priya,
      "8.7",
      "risks",
      "Customer validation rules may arrive late",
      {
        project_id: project,
        owner_id: people[1],
        severity: "3",
        likelihood: "3",
        mitigation:
          "Review validation rules with stakeholders before form development.",
        review_on: "2026-10-16",
      },
    );
    await create(priya, "8.7", "blockers", "Awaiting validation examples", {
      project_id: project,
      work_item_id: work[1],
      owner_id: people[1],
      status: "open",
    });
    await edit(priya, "8.7", "work_items", workNames[1], { blocked: true });
    await create(
      priya,
      "8.8",
      "alignments",
      "Portal contribution to onboarding goal",
      { project_id: project, goal_id: goal, weight: "1", contribution: "0.8" },
    );
    await create(
      priya,
      "8.8",
      "benefits",
      "Onboarding administration hours saved",
      {
        project_id: project,
        unit: "hours saved",
        target: "100",
        realized: "20",
        period_start: "2026-10-12",
        period_end: "2026-11-07",
      },
    );
    const baseline = await create(
      priya,
      "8.9",
      "baselines",
      "Portal approved plan — v1",
      {
        project_id: project,
        description: "Initial training schedule and budget before changes.",
      },
    );
    await create(priya, "8.9", "metric_plans", "Portal measurement plan — v1", {
      project_id: project,
      baseline_id: baseline,
      calendar_id: calendar,
      forecast_cost: "210000",
    });
    await create(
      priya,
      "8.10",
      "status_updates",
      "Portal weekly update — 12 October",
      {
        project_id: project,
        reported_health: "Amber",
        description:
          "Requirements being confirmed; validation examples outstanding. Owner Priya.",
      },
    );
    await create(priya, "9.1", "allocations", "Priya — portal allocation", {
      resource_id: resource,
      project_id: project,
      hours_per_day: "4",
      ...dates,
    });
    const capacity = await (
      await priya.request.get(
        `/api/v1/capacity/resources/${resource}?start=2026-10-12&end=2026-11-07`,
        { headers: { "x-organization-id": organization } },
      )
    ).json();
    const firstDay = capacity.days.find(
      (day: { day: string }) => day.day === "2026-10-12",
    );
    expect(Number(firstDay.available_hours)).toBe(8);
    expect(Number(firstDay.allocated_hours)).toBe(4);
    expect(firstDay.timezone).toBe("Asia/Kolkata");
    pass(
      "9.1",
      "Persisted calendar drives eight available hours and four allocated hours on a weekday",
    );
    await create(priya, "9.2", "time_off", "Priya — training half day", {
      resource_id: resource,
      start_date: "2026-10-16",
      end_date: "2026-10-17",
      hours_per_day: "4",
    });
    const me = await (await priya.request.get("/api/v1/auth/me")).json();
    const cookies = await priya.context().cookies();
    const csrf = cookies.find((c) => c.name === "ppm_csrf")!.value;
    const effortDenied = await priya.request.post("/api/v1/delivery/effort", {
      headers: {
        origin: process.env.PPM_WEB_URL!,
        "x-csrf-token": csrf,
        "x-organization-id": me.organization_id,
        "idempotency-key": crypto.randomUUID(),
      },
      data: {
        kind: "effort",
        name: "Denied private effort",
        resource_id: resource,
        project_id: project,
        worked_on: "2026-10-12",
        hours: "4",
      },
    });
    expect(effortDenied.status()).toBe(403);
    pass("7/9.2", "Private effort denied before explicit sensitive grant");
    await asha.goto("/resources");
    await asha
      .getByRole("combobox", { name: "Planning records", exact: true })
      .selectOption("resource_access");
    await asha
      .getByRole("row")
      .filter({ hasText: "Priya — own training resource management" })
      .getByRole("button", { name: "Edit", exact: true })
      .click();
    let dialog = asha.getByRole("dialog");
    await fill(dialog, "resource_access", { effort: true });
    await dialog
      .getByRole("button", { name: "Save record", exact: true })
      .click();
    await asha
      .getByRole("button", { name: "Confirm change", exact: true })
      .click();
    await expect(dialog).not.toBeVisible();
    await create(priya, "9.2", "effort", "Priya — portal work — 12 October", {
      resource_id: resource,
      project_id: project,
      worked_on: "2026-10-12",
      hours: "4",
      overtime_hours: "0",
    });
    await edit(priya, "9.4", "blockers", "Awaiting validation examples", {
      status: "resolved",
    });
    await edit(priya, "9.4", "work_items", workNames[1], { blocked: false });
    for (const [i, name] of workNames.entries()) {
      if (i > 0)
        await edit(priya, "9.4", "work_items", name, { status: "ready" });
      await edit(priya, "9.4", "work_items", name, { status: "in_progress" });
      await edit(priya, "9.4", "work_items", name, { status: "done" });
    }
    await edit(priya, "9.4", "milestones", "Requirements agreed", {
      actual_date: "2026-10-14",
    });
    await edit(priya, "9.4", "sprints", "Portal Sprint 1", {
      status: "closed",
    });
    current = "10";
    await asha.goto("/assessments");
    await asha
      .getByRole("button", { name: "Create framework", exact: true })
      .click();
    dialog = asha.getByRole("dialog");
    await dialog
      .getByLabel("Framework name", { exact: true })
      .fill("Northstar Delivery Readiness");
    await dialog
      .getByRole("combobox", { name: "Category", exact: true })
      .selectOption("delivery");
    for (let i = 0; i < 2; i++)
      await dialog
        .getByRole("button", { name: "Add dimension", exact: true })
        .click();
    const dimensions = [
        "Governance",
        "Delivery planning",
        "Evidence discipline",
      ],
      weights = ["0.30", "0.40", "0.30"];
    const questions = [
      "Named accountable owner",
      "Governance practice",
      "Baseline and milestones",
      "Risk management practice",
      "Traceable supporting evidence",
      "Evidence summary",
    ];
    const prompts = [
      "Does the portal have a named owner and agreed responsibility for scope decisions?",
      "Select the level that best describes documented decisions and review practice.",
      "Are an initial plan baseline and dated critical milestones recorded for the portal?",
      "Select the level that best describes how delivery risks are recorded, owned and reviewed.",
      "Do the answers reference dated evidence and identify who owns it?",
      "Summarize the documents reviewed, the main gaps, and the next improvement action.",
    ];
    for (let i = 0; i < 3; i++) {
      await dialog
        .getByLabel(`Dimension ${i + 1} name`, { exact: true })
        .fill(dimensions[i]);
      await dialog
        .getByLabel(`Dimension ${i + 1} weight`, { exact: true })
        .fill(weights[i]);
      const dimension = dialog.getByRole("group", {
        name: `Dimension ${i + 1}`,
        exact: true,
      });
      await dimension
        .getByRole("button", { name: "Add question", exact: true })
        .click();
      for (let j = 0; j < 2; j++) {
        const question = dimension.getByRole("group", {
          name: `Question ${j + 1}`,
          exact: true,
        });
        await question
          .getByLabel(`Question ${i + 1}.${j + 1} name`, { exact: true })
          .fill(questions[i * 2 + j]);
        await question.getByLabel("Question prompt").fill(prompts[i * 2 + j]);
        if (j === 1)
          await question
            .getByRole("combobox", { name: "Answer type", exact: true })
            .selectOption(i === 2 ? "text" : "rubric");
        if (j === 1 && i < 2) {
          await question
            .getByLabel("Level 1 label", { exact: true })
            .fill("Not demonstrated");
          await question
            .getByLabel("Level 2 label", { exact: true })
            .fill("Partially established");
          await question
            .getByRole("button", { name: "Add rubric level", exact: true })
            .click();
          await question
            .getByLabel("Level 3 label", { exact: true })
            .fill("Established and repeatable");
        }
      }
    }
    await dialog
      .getByRole("button", { name: "Save framework draft", exact: true })
      .click();
    await expect(dialog).not.toBeVisible();
    await asha
      .getByRole("button", { name: "Publish version", exact: true })
      .click();
    await expect(
      asha.getByText("Published version 1", { exact: true }),
    ).toBeVisible();
    pass(
      "10.1–10.3",
      "Build all three weighted dimensions and six questions; publish immutable Version 1",
    );
    const frameworkAccess = asha.getByRole("region", {
      name: "Assessment access",
    });
    await frameworkAccess
      .getByRole("combobox", { name: /^Member/ })
      .selectOption(people[1]);
    await frameworkAccess
      .getByRole("button", { name: "Grant framework editing" })
      .click();
    await expect(
      frameworkAccess.getByRole("button", { name: "Revoke access" }),
    ).toBeVisible();
    await priya.goto("/assessments");
    await priya
      .getByRole("button", { name: "Edit draft", exact: true })
      .click();
    await priya
      .getByRole("dialog")
      .getByLabel("Description")
      .fill("Delegated draft edit; published Version 1 is retained.");
    await priya
      .getByRole("button", { name: "Save framework draft", exact: true })
      .click();
    await expect(priya.getByRole("dialog")).not.toBeVisible();
    await expect(
      priya.getByRole("button", { name: "Publish version", exact: true }),
    ).toHaveCount(0);
    await expect(
      priya.getByText("Published version 1", { exact: true }),
    ).toBeVisible();
    pass(
      "10.4",
      "Explicit PM framework draft editing without publication or changing Version 1",
    );
    const assessmentName = "Digital Delivery — Portal Readiness — October 2026";
    await asha
      .getByRole("button", { name: "Assign assessment", exact: true })
      .click();
    dialog = asha.getByRole("dialog");
    await dialog
      .getByLabel("Assessment name", { exact: true })
      .fill(assessmentName);
    await dialog
      .getByRole("combobox", { name: /^Department/ })
      .selectOption(department);
    await dialog.getByRole("combobox", { name: /^Team/ }).selectOption(team);
    await dialog
      .getByRole("combobox", { name: /^Respondent/ })
      .selectOption(people[1]);
    await dialog
      .getByRole("combobox", { name: /^Independent reviewer/ })
      .selectOption(people[2]);
    await dialog
      .getByRole("button", { name: "Create assignment", exact: true })
      .click();
    await expect(dialog).not.toBeVisible();
    pass(
      "11",
      "Assign different active Project Managers as respondent and independent reviewer",
    );
    current = "12";
    await openAssessment(priya, assessmentName);
    const manual = readFileSync(
      "docs/06-user-guides/WEBSITE_WALKTHROUGH.md",
      "utf8",
    );
    const documents = ["A", "B", "C", "D", "E", "F"].map((letter) => {
      const start = manual.indexOf(`### Document ${letter}`);
      const next = manual.indexOf("### ", start + 5);
      return manual
        .slice(start, next < 0 ? undefined : next)
        .split("\n")
        .filter((l) => l.startsWith("> "))
        .map((l) => l.slice(2))
        .join("\n");
    });
    for (let i = 0; i < 6; i++) {
      const answer =
        i === 5
          ? priya.getByRole("textbox", {
              name: `${questions[i]} (required)`,
              exact: false,
            })
          : priya.getByRole("combobox", {
              name: `${questions[i]} (required)`,
              exact: false,
            });
      if (i === 5) await answer.fill(documents[i].split("\n")[0]);
      else await answer.selectOption(i === 1 ? "1" : i === 3 ? "2" : "true");
      await priya
        .getByRole("textbox", {
          name: `Evidence notes for ${questions[i]}`,
          exact: true,
        })
        .fill(
          i === 5 ? documents[i].split("\n").slice(1).join("\n") : documents[i],
        );
      await expect(
        priya.getByText("Draft saved.", { exact: true }),
      ).toBeVisible();
    }
    await priya
      .getByLabel(`Attach evidence for ${questions[0]}`)
      .setInputFiles({
        name: "portal-project-charter.txt",
        mimeType: "text/plain",
        buffer: Buffer.from(documents[0]),
      });
    await expect(
      priya.getByText("portal-project-charter.txt — quarantined", {
        exact: true,
      }),
    ).toBeVisible();
    await priya
      .getByLabel("Review or submission note", { exact: true })
      .fill("Training answers and Documents A–F ready for independent review.");
    await priya
      .getByRole("button", { name: "Submit for review", exact: true })
      .click();
    await expect(
      priya.getByText("Assessment submitted.", { exact: true }),
    ).toBeVisible();
    pass(
      "12.1–12.3",
      "Answer all six questions with supplied evidence, autosave, quarantine text attachment and submit",
    );
    current = "13";
    await openAssessment(ravi, assessmentName);
    await ravi
      .getByLabel("Review or submission note", { exact: true })
      .fill("Starting independent review of fictional evidence.");
    await ravi
      .getByRole("button", { name: "Start review", exact: true })
      .click();
    await expect(
      ravi.getByText("Assessment in review.", { exact: true }),
    ).toBeVisible();
    await ravi
      .getByRole("button", { name: "Preview portal-project-charter.txt" })
      .click();
    await expect(
      ravi.getByText(/TRAINING DOCUMENT — Portal project charter/).last(),
    ).toBeVisible();
    await ravi
      .getByLabel("Review or submission note", { exact: true })
      .fill("Reviewed fictional plain text; safe to release.");
    await ravi
      .getByRole("button", { name: "Release portal-project-charter.txt" })
      .click();
    await expect(
      ravi.getByRole("link", {
        name: "portal-project-charter.txt",
        exact: true,
      }),
    ).toBeVisible();
    await ravi
      .getByLabel("Review or submission note", { exact: true })
      .fill("Please clarify fictional evidence limitations in the summary.");
    await ravi
      .getByRole("button", { name: "Return for changes", exact: true })
      .click();
    await expect(
      ravi.getByText("Assessment returned.", { exact: true }),
    ).toBeVisible();
    await openAssessment(priya, assessmentName);
    await priya
      .getByRole("textbox", {
        name: "Evidence summary (required)",
        exact: false,
      })
      .fill(
        documents[5].split("\n")[0] +
          " These are fictional training claims; no real certification.",
      );
    await expect(
      priya.getByText("Draft saved.", { exact: true }),
    ).toBeVisible();
    await priya
      .getByRole("button", { name: "Submit for review", exact: true })
      .click();
    await expect(
      priya.getByText("Assessment submitted.", { exact: true }),
    ).toBeVisible();
    await openAssessment(ravi, assessmentName);
    await ravi
      .getByLabel("Review or submission note", { exact: true })
      .fill(
        "Fictional training answers reviewed; governance remains partial. Priya owns follow-up.",
      );
    await ravi
      .getByRole("button", { name: "Start review", exact: true })
      .click();
    await expect(
      ravi.getByText("Assessment in review.", { exact: true }),
    ).toBeVisible();
    await ravi
      .getByLabel("Review or submission note", { exact: true })
      .fill(
        "Reviewed fictional training answers and evidence. Governance remains partial. Priya owns follow-up.",
      );
    await ravi
      .getByRole("button", { name: "Complete review", exact: true })
      .click();
    await expect(
      ravi.getByText("Assessment completed.", { exact: true }),
    ).toBeVisible();
    await expect(
      ravi.getByText("92.50", { exact: false }).first(),
    ).toBeVisible();
    pass(
      "13",
      "Independent preview/release, return, respondent correction, resubmission and completed score 92.50",
    );
    current = "14";
    await openAssessment(asha, assessmentName);
    const access = asha
      .getByRole("region", { name: "Assessment access" })
      .filter({
        has: asha.getByRole("button", {
          name: "Grant result access",
          exact: true,
        }),
      });
    await access
      .getByRole("combobox", { name: /^Member/ })
      .selectOption(people[3]);
    await access.getByRole("button", { name: "Grant result access" }).click();
    await expect(
      access.getByRole("button", { name: "Revoke access", exact: true }),
    ).toBeVisible();
    await openAssessment(vera, assessmentName);
    await expect(
      vera.getByText("92.50", { exact: false }).first(),
    ).toBeVisible();
    await expect(
      vera.getByLabel(`Evidence notes for ${questions[0]}`),
    ).toHaveCount(0);
    await expect(
      vera.getByRole("button", { name: "Submit for review" }),
    ).toHaveCount(0);
    pass(
      "14.1/15.3",
      "Share and read completed scores without private evidence or respondent actions",
    );
    await vera.getByLabel("Comparison from").fill("2026-10-01");
    await vera.getByLabel("Comparison through").fill("2026-11-07");
    await expect(
      vera.getByRole("region", { name: "Department comparison scores" }),
    ).toContainText("Digital Delivery");
    pass(
      "15.3",
      "Read permitted completed department comparison for Version 1",
    );
    await access
      .getByRole("button", { name: "Revoke access", exact: true })
      .click();
    await expect(
      access.getByRole("button", { name: "Revoke access", exact: true }),
    ).toHaveCount(0);
    await vera.goto("/assessments");
    await expect(
      vera.getByRole("button", { name: `Open ${assessmentName}`, exact: true }),
    ).toHaveCount(0);
    await access
      .getByRole("combobox", { name: /^Member/ })
      .selectOption(people[3]);
    await access
      .getByRole("button", { name: "Grant result access", exact: true })
      .click();
    await expect(
      access.getByRole("button", { name: "Revoke access", exact: true }),
    ).toBeVisible();
    pass(
      "14.2/16.33",
      "Revoke completed result independently of delivery access, then restore",
    );
    await edit(asha, "14.2", "grants", "Vera — customer portfolio read", {
      archived: true,
    });
    await create(asha, "14.2", "grants", "Vera — portal project read", {
      user_id: people[3],
      project_id: project,
      access: "read",
    });
    await vera.goto("/projects/" + project);
    await expect(
      vera.getByRole("heading", {
        name: "Customer Onboarding Portal",
        exact: true,
      }),
    ).toBeVisible();
    await expect(
      vera.getByRole("button", { name: "Edit project", exact: true }),
    ).toHaveCount(0);
    pass("15.1", "Viewer reads granted project and cannot edit delivery");
    for (const [kind, recordName] of [
      ["work_items", "Confirm onboarding requirements"],
      ["milestones", "Requirements agreed"],
      ["risks", "Customer validation rules may arrive late"],
      ["blockers", "Awaiting validation examples"],
      ["status_updates", "Portal weekly update — 12 October"],
    ] as const) {
      await vera
        .getByRole("button", { name: labels[kind], exact: true })
        .click();
      await expect(
        vera.getByRole("row").filter({ hasText: recordName }).last(),
      ).toBeVisible();
      await expect(
        vera.getByRole("button", {
          name: `Create ${labels[kind].toLowerCase()}`,
          exact: true,
        }),
      ).toHaveCount(0);
    }
    await vera.goto("/account");
    await expect(
      vera.getByRole("button", { name: "Save profile", exact: true }),
    ).toBeVisible();
    await expect(
      vera.getByRole("button", { name: "Create invitation", exact: true }),
    ).toHaveCount(0);
    await vera.goto("/projects/" + project);
    pass(
      "15.1",
      "Viewer reads all five delivery tabs and own account without organization admin actions",
    );
    await edit(asha, "14.2", "grants", "Vera — portal project read", {
      archived: true,
    });
    await vera.reload();
    await expect(
      vera.getByRole("alert").filter({ hasText: "not available" }),
    ).toBeVisible();
    await vera
      .getByRole("button", { name: "Search workspace commands" })
      .click();
    await vera
      .getByLabel("Find a record", { exact: true })
      .fill("Customer Onboarding Portal");
    await expect(
      vera.getByText("No permitted records match your search.", {
        exact: true,
      }),
    ).toBeVisible();
    await vera.keyboard.press("Escape");
    await vera.goto("/command-center");
    await expect(
      vera.getByRole("heading", { name: "No visible projects", exact: true }),
    ).toBeVisible();
    pass(
      "14.2/16.29",
      "Revoked project disappears from existing tab, fresh search and Command center",
    );
    await asha.getByLabel("Show archived", { exact: true }).check();
    await asha
      .getByRole("button", {
        name: "Edit Vera — portal project read",
        exact: true,
      })
      .click();
    dialog = asha.getByRole("dialog");
    await fill(dialog, "grants", { archived: false });
    await dialog
      .getByRole("button", { name: "Save record", exact: true })
      .click();
    await asha
      .getByRole("button", { name: "Confirm change", exact: true })
      .click();
    await expect(dialog).not.toBeVisible();
    pass(
      "14.2",
      "Revoke sole project path, deny open project and restore archived grant",
    );
    current = "15.2";
    await vera.goto("/command-center");
    await vera.getByLabel("From date", { exact: true }).fill("2026-10-12");
    await vera
      .getByLabel("To date (excluded)", { exact: true })
      .fill("2026-11-07");
    await vera.getByRole("button", { name: "Refresh", exact: true }).click();
    for (const name of ["Executive", "Delivery", "Risk", "Resource"]) {
      await vera.getByRole("button", { name, exact: true }).click();
      await expect(
        vera.getByRole("heading", { name: "Command center", exact: true }),
      ).toBeVisible();
    }
    await vera.getByRole("button", { name: "Executive", exact: true }).click();
    await vera
      .getByRole("button", { name: /^Inspect / })
      .first()
      .click();
    await expect(vera.getByRole("dialog")).toContainText("Coverage");
    await expect(vera.getByRole("dialog")).toContainText("source");
    await vera.keyboard.press("Escape");
    pass(
      "15.2",
      "Viewer opens metric evidence drawer with coverage and source explanation",
    );
    await vera
      .getByLabel("New view name", { exact: true })
      .fill("Vera — portal oversight");
    await vera.getByRole("button", { name: "Save view", exact: true }).click();
    await vera.reload();
    await vera
      .getByRole("combobox", { name: "Personal saved view", exact: true })
      .selectOption({ label: "Vera — portal oversight" });
    pass(
      "15.2",
      "Inspect four dashboards and save/reload personal view without expanding permissions",
    );
    const snapshot = await (
      await vera.request.get(
        "/api/v1/command/snapshot?start=2026-10-12&end=2026-11-07",
        { headers: { "x-organization-id": organization } },
      )
    ).json();
    expect(
      Number(
        snapshot.velocity.find(
          (v: { sprint_id: string }) => v.sprint_id === sprint,
        ).points,
      ),
    ).toBe(10);
    pass("9.4/15.2", "Verify persisted closed-sprint velocity of ten points");
    await priya.goto("/");
    await expect(
      priya
        .getByText("Customer validation rules may arrive late", {
          exact: false,
        })
        .first(),
    ).toBeVisible();
    await priya
      .getByRole("button", { name: "Open notifications", exact: true })
      .click();
    await priya.getByLabel("Show in-app notifications").check();
    const unread = priya.getByRole("button", {
      name: "Mark read",
      exact: true,
    });
    await expect(unread.first()).toBeVisible();
    await unread.first().click();
    await expect(
      priya.getByRole("button", { name: "Read", exact: true }).first(),
    ).toBeVisible();
    await priya.keyboard.press("Escape");
    await priya.reload();
    await priya
      .getByRole("button", { name: "Open notifications", exact: true })
      .click();
    await expect(
      priya.getByRole("button", { name: "Read", exact: true }).first(),
    ).toBeVisible();
    pass("9.3", "My work and persistent notification read state");
    await vera.goto("/command-center");
    await expect(
      vera.getByText("Listening for saved changes", { exact: true }),
    ).toBeVisible();
    const fresh = vera.getByText(/Saved change received/);
    await edit(priya, "16.34", "milestones", "Requirements agreed", {
      due_date: "2026-10-15",
    });
    await expect(fresh.first()).toBeVisible();
    const persisted = await (
      await priya.request.get("/api/v1/delivery/milestones/" + milestone)
    ).json();
    expect(persisted.data.due_date).toBe("2026-10-15");
    pass(
      "16.34",
      "Viewer receives authorized saved-change notice and updated milestone persists",
    );
    pass(
      "18",
      "All four fictional responsibilities completed through the final applicable workflow",
    );
  } catch (error) {
    for (const [index, p] of [asha, priya, ravi, vera].entries()) {
      await p.screenshot({
        path: `artifacts/local/repair-20261010/walkthrough-failure-${index}.png`,
        fullPage: true,
      });
      writeFileSync(
        `artifacts/local/repair-20261010/walkthrough-failure-${index}.txt`,
        await p.locator("body").innerText(),
      );
    }
    evidence.push({
      section: current,
      action:
        error instanceof Error
          ? error.message.split("\n")[0]
          : "Unexpected failure",
      status: "FAIL",
    });
    throw error;
  } finally {
    writeFileSync(
      "artifacts/local/repair-20261010/walkthrough-browser.json",
      JSON.stringify(evidence, null, 2),
    );
    for (const context of contexts) await context.close();
  }
});
