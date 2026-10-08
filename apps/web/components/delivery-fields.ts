import type { components } from "@ppm/contracts/schema";
export type DeliveryRecord = components["schemas"]["RecordView"];
export type DeliveryInput = DeliveryRecord["data"];
export type Kind = DeliveryInput["kind"];
export type FieldSpec = {
  key: string;
  label: string;
  type?: "date" | "number" | "checkbox" | "textarea";
  required?: boolean;
  options?: string[];
  reference?: Kind | "people";
  default?: string | boolean;
  step?: string;
  emptyString?: boolean;
};
const owner: FieldSpec = {
  key: "owner_id",
  label: "Owner",
  reference: "people",
};
const project: FieldSpec = {
  key: "project_id",
  label: "Project",
  reference: "projects",
  required: true,
};
const portfolio: FieldSpec = {
  key: "portfolio_id",
  label: "Portfolio",
  reference: "portfolios",
  required: true,
};
const currency: FieldSpec = {
  key: "currency",
  label: "Currency (3-letter code)",
  required: true,
  default: "INR",
};
const start: FieldSpec = {
  key: "start_date",
  label: "Start date",
  type: "date",
};
const end: FieldSpec = { key: "end_date", label: "End date", type: "date" };
const person: FieldSpec = {
  key: "user_id",
  label: "Member",
  reference: "people",
  required: true,
};
const health: FieldSpec = {
  key: "reported_health",
  label: "Reported health",
  options: ["Unknown", "Green", "Amber", "Red"],
  default: "Unknown",
};
export const labels: Record<Kind, string> = {
  risks: "Risk register",
  benefits: "Business benefits",
  metric_plans: "Metric plans",
  metric_policies: "Metric policy",
  saved_views: "Saved dashboard views",
  resources: "Resource profiles",
  calendars: "Working calendars",
  availability: "Availability",
  resource_teams: "Resource teams",
  resource_skills: "Skills",
  time_off: "Approved time off",
  allocations: "Allocations",
  resource_access: "Resource access",
  effort: "Actual effort",
  effort_coverage: "Timesheet coverage",
  capacity_snapshots: "Allocation snapshots",
  settings: "Organization configuration",
  departments: "Departments",
  teams: "Teams",
  team_members: "Team membership",
  goals: "Strategic goals",
  portfolios: "Portfolios",
  programs: "Programs",
  projects: "Projects",
  grants: "Project & portfolio access",
  sprints: "Sprints",
  work_items: "Work items",
  milestones: "Milestones",
  blockers: "Blockers",
  dependencies: "Dependencies",
  budget_lines: "Budget lines",
  expenditures: "Expenditure",
  status_updates: "Status updates",
  baselines: "Plan baselines",
  alignments: "Goal alignment",
};
export const fields: Record<Kind, FieldSpec[]> = {
  risks: [
    project,
    owner,
    {
      key: "severity",
      label: "Severity (1–5)",
      type: "number",
      required: true,
      default: "3",
    },
    {
      key: "likelihood",
      label: "Likelihood (1–5)",
      type: "number",
      required: true,
      default: "3",
    },
    {
      key: "mitigation",
      label: "Mitigation",
      type: "textarea",
      emptyString: true,
    },
    {
      key: "status",
      label: "Status",
      options: ["open", "mitigating", "accepted", "closed"],
      default: "open",
    },
    { key: "review_on", label: "Review date", type: "date", required: true },
    {
      key: "resolution",
      label: "Resolution / acceptance reason",
      type: "textarea",
      emptyString: true,
    },
  ],
  benefits: [
    project,
    { key: "unit", label: "Unit (e.g. INR or hours saved)", required: true },
    {
      key: "target",
      label: "Target",
      type: "number",
      step: "0.01",
      required: true,
    },
    {
      key: "realized",
      label: "Realized (blank = unknown)",
      type: "number",
      step: "0.01",
    },
    {
      key: "period_start",
      label: "Period start",
      type: "date",
      required: true,
    },
    {
      key: "period_end",
      label: "Period end (excluded)",
      type: "date",
      required: true,
    },
  ],
  metric_plans: [
    project,
    {
      key: "baseline_id",
      label: "Frozen baseline",
      reference: "baselines",
      required: true,
    },
    {
      key: "calendar_id",
      label: "Working calendar",
      reference: "calendars",
      required: true,
    },
    {
      key: "forecast_cost",
      label: "Forecast final cost (project currency)",
      type: "number",
      step: "0.01",
    },
  ],
  metric_policies: [
    {
      key: "amber",
      label: "Amber risk threshold",
      type: "number",
      default: "30",
      required: true,
    },
    {
      key: "red",
      label: "Red risk threshold",
      type: "number",
      default: "60",
      required: true,
    },
    {
      key: "stale_days",
      label: "Source stale after days",
      type: "number",
      default: "7",
      required: true,
    },
  ],
  saved_views: [
    person,
    { ...portfolio, required: false },
    { ...start, required: true },
    { ...end, required: true },
    {
      key: "dashboard",
      label: "Dashboard",
      options: ["Executive", "Delivery", "Risk", "Resource"],
      default: "Executive",
    },
  ],
  resources: [{ ...person, label: "Login member (optional)", required: false }],
  calendars: [
    {
      key: "timezone",
      label: "IANA timezone",
      required: true,
      default: "Asia/Kolkata",
    },
    {
      key: "monday",
      label: "Monday hours",
      type: "number",
      step: "0.01",
      required: true,
      default: "8",
    },
    {
      key: "tuesday",
      label: "Tuesday hours",
      type: "number",
      step: "0.01",
      required: true,
      default: "8",
    },
    {
      key: "wednesday",
      label: "Wednesday hours",
      type: "number",
      step: "0.01",
      required: true,
      default: "8",
    },
    {
      key: "thursday",
      label: "Thursday hours",
      type: "number",
      step: "0.01",
      required: true,
      default: "8",
    },
    {
      key: "friday",
      label: "Friday hours",
      type: "number",
      step: "0.01",
      required: true,
      default: "8",
    },
    {
      key: "saturday",
      label: "Saturday hours",
      type: "number",
      step: "0.01",
      required: true,
      default: "0",
    },
    {
      key: "sunday",
      label: "Sunday hours",
      type: "number",
      step: "0.01",
      required: true,
      default: "0",
    },
    {
      key: "holidays",
      label: "Holiday dates (comma-separated ISO dates)",
      default: "",
    },
  ],
  availability: [
    {
      key: "resource_id",
      label: "Resource",
      reference: "resources",
      required: true,
    },
    { ...start, required: true },
    { ...end, label: "End date (excluded)", required: true },
    {
      key: "calendar_id",
      label: "Calendar version",
      reference: "calendars",
      required: true,
    },
  ],
  resource_teams: [
    {
      key: "resource_id",
      label: "Resource",
      reference: "resources",
      required: true,
    },
    { ...start, required: true },
    { ...end, label: "End date (excluded)", required: true },
    { key: "team_id", label: "Team", reference: "teams", required: true },
  ],
  resource_skills: [
    {
      key: "resource_id",
      label: "Resource",
      reference: "resources",
      required: true,
    },
    { key: "skill", label: "Skill", required: true },
  ],
  time_off: [
    {
      key: "resource_id",
      label: "Resource",
      reference: "resources",
      required: true,
    },
    { ...start, required: true },
    { ...end, label: "End date (excluded)", required: true },
    {
      key: "hours_per_day",
      label: "Hours per scheduled day",
      type: "number",
      step: "0.01",
      required: true,
    },
  ],
  allocations: [
    {
      key: "resource_id",
      label: "Resource",
      reference: "resources",
      required: true,
    },
    project,
    { ...start, required: true },
    { ...end, label: "End date (excluded)", required: true },
    {
      key: "hours_per_day",
      label: "Hours per scheduled day",
      type: "number",
      step: "0.01",
      required: true,
    },
  ],
  resource_access: [
    {
      key: "resource_id",
      label: "Resource",
      reference: "resources",
      required: true,
    },
    person,
    { key: "manage", label: "May manage resource", type: "checkbox" },
    { key: "effort", label: "May access sensitive effort", type: "checkbox" },
  ],
  effort: [
    {
      key: "resource_id",
      label: "Resource",
      reference: "resources",
      required: true,
    },
    project,
    { key: "worked_on", label: "Worked on", type: "date", required: true },
    {
      key: "hours",
      label: "Total hours",
      type: "number",
      step: "0.01",
      required: true,
    },
    {
      key: "overtime_hours",
      label: "Included overtime hours",
      type: "number",
      step: "0.01",
      default: "0",
      required: true,
    },
  ],
  effort_coverage: [
    {
      key: "resource_id",
      label: "Resource",
      reference: "resources",
      required: true,
    },
    { key: "worked_on", label: "Worked on", type: "date", required: true },
    {
      key: "complete",
      label: "Full resource timesheet is complete",
      type: "checkbox",
    },
  ],
  capacity_snapshots: [
    {
      key: "resource_id",
      label: "Resource",
      reference: "resources",
      required: true,
    },
    { ...start, required: true },
    { ...end, label: "End date (excluded)", required: true },
  ],

  settings: [
    {
      key: "timezone",
      label: "IANA timezone",
      required: true,
      default: "Asia/Kolkata",
    },
    currency,
  ],
  departments: [owner],
  goals: [owner],
  portfolios: [owner],
  teams: [
    { key: "department_id", label: "Department", reference: "departments" },
    owner,
  ],
  programs: [portfolio, owner],
  projects: [
    portfolio,
    { key: "program_id", label: "Program (optional)", reference: "programs" },
    { key: "department_id", label: "Department", reference: "departments" },
    { key: "team_id", label: "Delivery team", reference: "teams" },
    owner,
    {
      key: "status",
      label: "Status",
      options: ["draft", "active", "on_hold", "completed", "cancelled"],
      default: "draft",
    },
    health,
    currency,
    {
      key: "ledger_complete",
      label: "Expenditure ledger is complete",
      type: "checkbox",
      default: false,
    },
    start,
    { key: "target_end_date", label: "Planned finish", type: "date" },
    { key: "forecast_end_date", label: "Forecast finish", type: "date" },
    { key: "actual_start_date", label: "Actual start", type: "date" },
    { key: "actual_end_date", label: "Actual finish", type: "date" },
  ],
  grants: [
    person,
    { ...project, required: false },
    { ...portfolio, required: false },
    {
      key: "access",
      label: "Access",
      options: ["read", "edit", "manage"],
      default: "read",
    },
  ],
  team_members: [
    { key: "team_id", label: "Team", reference: "teams", required: true },
    person,
    { ...start, required: true },
    end,
  ],
  sprints: [
    project,
    { key: "team_id", label: "Team", reference: "teams", required: true },
    { ...start, required: true },
    { ...end, required: true },
    {
      key: "status",
      label: "Status",
      options: ["planned", "active", "closed"],
      default: "planned",
    },
  ],
  work_items: [
    project,
    owner,
    { key: "sprint_id", label: "Sprint", reference: "sprints" },
    {
      key: "status",
      label: "Status",
      options: ["backlog", "ready", "in_progress", "done"],
      default: "backlog",
    },
    { key: "blocked", label: "Blocked", type: "checkbox", default: false },
    {
      key: "points",
      label: "Story points (team-specific)",
      type: "number",
      step: "0.01",
    },
    start,
    { key: "due_date", label: "Due date", type: "date" },
  ],
  milestones: [
    project,
    { key: "due_date", label: "Due date", type: "date", required: true },
    { key: "actual_date", label: "Actual finish", type: "date" },
    {
      key: "critical",
      label: "Critical milestone",
      type: "checkbox",
      default: false,
    },
  ],
  blockers: [
    project,
    {
      key: "work_item_id",
      label: "Related work item",
      reference: "work_items",
    },
    owner,
    {
      key: "status",
      label: "Status",
      options: ["open", "resolved"],
      default: "open",
    },
  ],
  dependencies: [
    project,
    {
      key: "target_project_id",
      label: "Successor project",
      reference: "projects",
      required: true,
    },
    {
      key: "source_milestone_id",
      label: "Predecessor milestone",
      reference: "milestones",
    },
    {
      key: "source_work_item_id",
      label: "Predecessor work item",
      reference: "work_items",
    },
    {
      key: "target_milestone_id",
      label: "Successor milestone",
      reference: "milestones",
    },
    {
      key: "target_work_item_id",
      label: "Successor work item",
      reference: "work_items",
    },
  ],
  budget_lines: [
    project,
    {
      key: "amount",
      label: "Amount",
      type: "number",
      required: true,
      step: "0.01",
    },
    currency,
    {
      key: "approved",
      label: "Approved budget",
      type: "checkbox",
      default: true,
    },
  ],
  expenditures: [
    project,
    {
      key: "amount",
      label: "Amount (negative only for reversal)",
      type: "number",
      required: true,
      step: "0.01",
    },
    currency,
    {
      key: "spent_on",
      label: "Expenditure date",
      type: "date",
      required: true,
    },
    {
      key: "reversal_of",
      label: "Reverse original expenditure",
      reference: "expenditures",
    },
  ],
  status_updates: [project, health],
  baselines: [project],
  alignments: [
    { ...project, required: false },
    { ...portfolio, required: false },
    {
      key: "goal_id",
      label: "Strategic goal",
      reference: "goals",
      required: true,
    },
    {
      key: "weight",
      label: "Weight (0–1; total must equal 1)",
      type: "number",
      required: true,
      step: "0.00001",
      default: "1",
    },
    {
      key: "contribution",
      label: "Contribution (0–1)",
      type: "number",
      required: true,
      step: "0.00001",
      default: "1",
    },
  ],
};
export const immutable: Kind[] = [
  "calendars",
  "capacity_snapshots",
  "expenditures",
  "baselines",
  "status_updates",
];
