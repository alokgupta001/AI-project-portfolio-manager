"use client";

import { useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { usePathname } from "next/navigation";
import { Button } from "./ui";
import { Icon } from "./icon";

type Tip = { title: string; text: string; heading?: string; selector?: string };
type Guide = { title: string; tips: Tip[] };
const guides: Record<string, Guide> = {
  "/": {
    title: "Workspace overview",
    tips: [
      {
        title: "Read your portfolio at a glance",
        text: "These figures come from projects you can access. Choose a portfolio and activity period; unknown health stays separate from healthy projects.",
        selector: ".portfolio-overview h2",
      },
      {
        title: "Explore the health behind the numbers",
        text: "Select a health category to filter the project list. Open the chart data table for exact counts, then follow a project link to its details.",
        heading: "Portfolio health",
      },
      {
        title: "Pick up your next task",
        text: "My work shows permitted assignments and updates. Getting started links to the remaining organization setup tasks.",
        heading: "My work",
      },
    ],
  },
  "/projects": {
    title: "Projects",
    tips: [
      {
        title: "Find the right project",
        text: "Search records and combine status, industry and portfolio filters. The service returns matching projects within your current permissions.",
        selector: ".server-filters",
      },
      {
        title: "Create or update work",
        text: "Use Create projects when your role and organization setup allow it. Required fields are validated; saving creates a real record. Cancel keeps existing records unchanged.",
        selector: '[data-tutorial="create-project"]',
      },
      {
        title: "Open the full picture",
        text: "Open a project to explore work, milestones, risks, spending and history. Previous and Next move through the server's matching records.",
        selector: ".data-table",
      },
    ],
  },
  "/projects/detail": {
    title: "Project details",
    tips: [
      {
        title: "Check project health and finances",
        text: "The overview summarizes this project's recorded facts. Unavailable values mean missing evidence, not zero. Different currencies stay separate.",
        heading: "Project overview",
      },
      {
        title: "Move between project sections",
        text: "Use the section buttons to explore work, milestones, risks, budgets and dependencies. Edit actions follow your project grants.",
        selector: ".delivery-tabs",
      },
      {
        title: "Review the underlying records",
        text: "Search or sort the current records, open their details, and inspect history or preserved baselines before making changes.",
        selector: ".data-table",
      },
    ],
  },
  "/portfolios": {
    title: "Portfolios",
    tips: [
      {
        title: "Organize delivery",
        text: "Portfolios group projects into a shared planning structure. Select a portfolio to explore its permitted projects and summary.",
        selector: ".page-heading",
      },
      {
        title: "Find and maintain records",
        text: "Use filters and the record table to find portfolios. Authorized roles can create or edit them; archived records retain their history.",
        selector: ".server-filters",
      },
      {
        title: "Drill into delivery",
        text: "Follow project links for milestones, work, risk and budget details. Totals follow the selected scope and keep currencies separate.",
        selector: ".data-table",
      },
    ],
  },
  "/resources": {
    title: "Resource planning",
    tips: [
      {
        title: "Choose your staffing scope",
        text: "Choose a resource or team to review available capacity and allocations. Resource profiles describe staffing; they do not create login accounts.",
        heading: "Staffing scope",
      },
      {
        title: "Check workload before allocating",
        text: "Capacity views reconcile working time, time off and allocations. Heatmaps have equivalent tables; missing data remains explicit.",
        selector: ".chart-frame, .data-table",
      },
      {
        title: "Keep an auditable plan",
        text: "Authorized writers can maintain allocations and related records. Snapshots preserve planning evidence and history explains changes.",
        heading: "Staffing matrix",
      },
    ],
  },
  "/assessments": {
    title: "Maturity assessments",
    tips: [
      {
        title: "Start with a published framework",
        text: "Frameworks define dimensions, questions, weights and scoring rubrics. Publishing freezes a version so later results remain comparable.",
        heading: "Framework library",
      },
      {
        title: "Collect and review answers",
        text: "Open an assessment to see assignments and permitted answers. Answers autosave; failed saves remain visible and must be resolved before submission.",
        heading: "Assessments",
      },
      {
        title: "Read scores with their evidence",
        text: "Review results, comparisons and released evidence within your access. Independent review and private-evidence boundaries still apply.",
        selector: ".assessment-workspace h1",
      },
    ],
  },
  "/command-center": {
    title: "Command center",
    tips: [
      {
        title: "Set the scope first",
        text: "Choose dates and a portfolio before interpreting the figures. Every snapshot uses the organization's calendar and your current permissions.",
        selector: ".command-filters",
      },
      {
        title: "Switch the decision view",
        text: "Executive, Delivery, Risk and Resource views organize the same authorized snapshot. Charts expose equivalent tables and metric evidence.",
        selector: '.tabs[aria-label="Dashboard"]',
      },
      {
        title: "Inspect and share evidence",
        text: "Open a metric's evidence to inspect its inputs. Save a personal view or export the metric DTO when available; exports recheck access.",
        selector: ".chart-frame, .metric-card",
      },
    ],
  },
  "/documents": {
    title: "Document library",
    tips: [
      {
        title: "Find trusted sources",
        text: "Filter the library to find documents you may access. Processing state and versions explain which source is ready to use.",
        heading: "Find sources",
      },
      {
        title: "Search the evidence",
        text: "Search source text and open permitted results to read escaped previews and citations. A citation always rechecks access to its source.",
        heading: "Search source text",
      },
      {
        title: "Manage the source lifecycle",
        text: "Authorized managers can upload versions and use retention or governance controls. Pending processing, unavailable content and restricted actions are explained on screen.",
        heading: "Upload evidence",
      },
    ],
  },
  "/integrations": {
    title: "Integrations & jobs",
    tips: [
      {
        title: "Connect a source carefully",
        text: "Authorized operators can create connections and preview source data before syncing. Connector permissions and approvals remain enforced.",
        heading: "Create connection",
      },
      {
        title: "Follow sync history",
        text: "Select a connection to review previous syncs, source changes and available actions. Revoked access is shown explicitly.",
        heading: "Connections & sync history",
      },
      {
        title: "Track processing",
        text: "Job activity shows real progress and data-quality results. Retry or cancel only when the job offers that action.",
        heading: "Job progress & data quality",
      },
    ],
  },
  "/ai": {
    title: "AI operations & evidence",
    tips: [
      {
        title: "Check availability first",
        text: "Provider status explains whether AI is enabled, paused or unavailable. Evidence fallback remains useful when no model response is available.",
        heading: "Provider status",
      },
      {
        title: "Inspect the evidence scope",
        text: "Preview permitted source evidence before interpreting a run. AI output does not automatically change project plans or expand access.",
        heading: "Evidence preview",
      },
      {
        title: "Review runs and limits",
        text: "Open a permitted run for its outcome and citations. Budget, circuit and diagnostic controls appear only for authorized roles.",
        heading: "Recent permitted runs",
      },
    ],
  },
  "/agents": {
    title: "Agents & recommendations",
    tips: [
      {
        title: "Choose a permitted analysis",
        text: "Select a project and analysis goal. Availability, model-call limits and fallback behavior are shown before starting a real run.",
        heading: "Start a scoped analysis",
      },
      {
        title: "Review the outcome honestly",
        text: "Open an analysis run to read its evidence, checklist and discrepancies. Unavailable or unverified results are not successful recommendations.",
        heading: "Analysis runs",
      },
      {
        title: "Keep decisions under human control",
        text: "Independent authorized reviewers can accept or reject supported suggestions. Review records history; any later plan change uses normal project forms.",
        heading: "Evidence and human review",
      },
    ],
  },
  "/ml": {
    title: "History & baselines",
    tips: [
      {
        title: "Bring in dated history",
        text: "Import supported history with clear provenance. Synthetic fixtures remain labeled and separate from real performance claims.",
        heading: "1. Import history",
      },
      {
        title: "Freeze the evidence",
        text: "Create an as-of dataset so a baseline can be reproduced. Its included and excluded records determine what the result can support.",
        heading: "2. Freeze an as-of dataset",
      },
      {
        title: "Review a baseline",
        text: "Run an available baseline and inspect its model card and artifacts. Insufficient-data and withdrawn states remain explicit; this page does not promote a production model.",
        heading: "3. Run & review a baseline",
      },
    ],
  },
  "/organization": {
    title: "Organization setup",
    tips: [
      {
        title: "Set up your organization",
        text: "Review the saved organization configuration. Use Edit settings to maintain the fields available to your role; changes are recorded in history.",
        heading: "Organization configuration",
      },
      {
        title: "Build your planning structure",
        text: "Use the section buttons to maintain metric policy, departments, teams, strategic goals and programs. Each section has its own records and permitted actions.",
        selector: ".delivery-tabs",
      },
      {
        title: "Manage delivery access",
        text: "Open Project & portfolio access to review delivery grants. Organization invitations and membership are managed from Account & access.",
        selector: ".delivery-tabs",
      },
    ],
  },
  "/account": {
    title: "Account & access",
    tips: [
      {
        title: "Choose the right organization",
        text: "Switch organizations to change the workspace scope. Your role and project grants apply independently in each organization.",
        heading: "Active organization",
      },
      {
        title: "Manage your profile and preferences",
        text: "Update your display name, switch the theme from the top bar, or replay the main tutorial from Profile & security.",
        heading: "Profile & security",
      },
      {
        title: "Review account access",
        text: "Inspect active sessions and revoke access when needed. Admins can also manage organization membership; sensitive changes require confirmation.",
        heading: "Active sessions",
      },
    ],
  },
  "/design-system": {
    title: "Component gallery",
    tips: [
      {
        title: "Explore the shared controls",
        text: "This gallery demonstrates the components used throughout the application. Examples are local demonstrations, separate from tenant records.",
        selector: "main h1",
      },
      {
        title: "Compare states and themes",
        text: "Try controls and dialogs to see loading, empty, error and success states. Use the theme switch to compare contrast and surfaces.",
        selector: "main .panel, main section",
      },
      {
        title: "Try keyboard interactions",
        text: "Tab moves between controls, Enter activates them and Escape closes dialogs. Visible focus and chart tables help make each example usable.",
        selector: "main .data-table, main .button",
      },
    ],
  },
};
const visited = new Set<string>();

export function PageGuide({
  userId,
  role,
  enabled,
}: {
  userId: string;
  role: string;
  enabled: boolean;
}) {
  const pathname = usePathname();
  const route = /^\/projects\/[^/]+$/.test(pathname)
    ? "/projects/detail"
    : pathname;
  const guide = guides[route];
  const key = `ppm-page-guide-v1:${userId}:${route}`;
  const [open, setOpen] = useState(false);
  const [index, setIndex] = useState(0);
  const [targetNotice, setTargetNotice] = useState("");
  const [highlight, setHighlight] = useState<{
    top: number;
    left: number;
    width: number;
    height: number;
  } | null>(null);
  const trigger = useRef<HTMLButtonElement | null>(null);
  const card = useRef<HTMLElement>(null);
  const targetRef = useRef<HTMLElement | null>(null);
  const tip = guide?.tips[index];

  useEffect(() => {
    setOpen(false);
    setIndex(0);
    setHighlight(null);
    if (!enabled || !guide) return;
    let seen = visited.has(key);
    try {
      seen = seen || localStorage.getItem(key) === "seen";
    } catch {
      /* Page-session fallback. */
    }
    if (!seen) {
      visited.add(key);
      try {
        localStorage.setItem(key, "seen");
      } catch {
        /* Page-session fallback. */
      }
      setOpen(true);
    }
  }, [key, enabled, guide]);

  useEffect(() => {
    if (!open || !enabled) setHighlight(null);
  }, [open, enabled]);
  useEffect(() => {
    targetRef.current = null;
    setTargetNotice("");
    const update = () => {
      const target = targetRef.current;
      if (!target) return;
      const rect = target.getBoundingClientRect();
      setHighlight(
        rect.bottom < 0 || rect.top > window.innerHeight
          ? null
          : {
              top: Math.max(4, rect.top - 4),
              left: Math.max(4, rect.left - 4),
              width: Math.min(rect.width + 8, window.innerWidth - 8),
              height: Math.min(rect.height + 8, 100),
            },
      );
    };
    window.addEventListener("scroll", update, true);
    window.addEventListener("resize", update);
    return () => {
      window.removeEventListener("scroll", update, true);
      window.removeEventListener("resize", update);
    };
  }, [index, open, key]);

  function finish() {
    visited.add(key);
    try {
      localStorage.setItem(key, "seen");
    } catch {
      /* Page-session fallback. */
    }
    setOpen(false);
    setHighlight(null);
    trigger.current?.focus();
  }
  function showSection() {
    if (!tip) return;
    const target = tip.heading
      ? Array.from(
          document.querySelectorAll<HTMLElement>("main h1, main h2, main h3"),
        ).find((heading) => heading.textContent?.trim() === tip.heading)
      : Array.from(
          document.querySelectorAll<HTMLElement>(tip.selector || "main h1"),
        ).find((item) => item.getBoundingClientRect().width > 0);
    if (!target || target.getBoundingClientRect().width === 0) {
      setTargetNotice(
        "This section is not available in your current scope, or is still loading. You can continue to the next tip.",
      );
      setHighlight(null);
      return;
    }
    setTargetNotice("");
    targetRef.current = target;
    target.scrollIntoView({ block: "start", behavior: "instant" });
    const headerHeight =
      document.querySelector(".topbar")?.getBoundingClientRect().height || 0;
    window.scrollBy({ top: -(headerHeight + 16), behavior: "instant" });
    const rect = target.getBoundingClientRect();
    setHighlight({
      top: Math.max(4, rect.top - 4),
      left: Math.max(4, rect.left - 4),
      width: Math.min(rect.width + 8, window.innerWidth - 8),
      height: Math.min(rect.height + 8, 100),
    });
  }
  if (!guide) return null;
  return (
    <>
      <button
        className="button secondary page-guide-trigger"
        aria-label="Page guide"
        disabled={!enabled}
        title={`About ${guide.title}`}
        ref={trigger}
        onClick={() => {
          setIndex(0);
          setOpen(true);
          requestAnimationFrame(() => card.current?.focus());
        }}
      >
        <Icon name="help" size={17} />
        <span>Page guide</span>
      </button>
      {enabled &&
        open &&
        typeof document !== "undefined" &&
        createPortal(
          <div className="page-guide-layer">
            {highlight && (
              <div
                className="page-guide-highlight"
                aria-hidden="true"
                style={highlight}
              />
            )}
            <section
              ref={card}
              className="page-guide-card"
              role="region"
              aria-label={`${guide.title} page guide`}
              tabIndex={-1}
              onKeyDown={(event) => {
                if (event.key === "Escape") {
                  event.preventDefault();
                  finish();
                }
                if (
                  event.target === card.current &&
                  event.key === "ArrowRight"
                ) {
                  event.preventDefault();
                  setIndex((value) =>
                    Math.min(value + 1, guide.tips.length - 1),
                  );
                  setHighlight(null);
                }
                if (
                  event.target === card.current &&
                  event.key === "ArrowLeft"
                ) {
                  event.preventDefault();
                  setIndex((value) => Math.max(0, value - 1));
                  setHighlight(null);
                }
              }}
            >
              <div className="page-guide-heading">
                <span>
                  ABOUT THIS PAGE · {index + 1} / {guide.tips.length}
                </span>
                <Button
                  variant="secondary"
                  aria-label="Close page guide"
                  onClick={finish}
                >
                  ×
                </Button>
              </div>
              <p className="page-guide-name">{guide.title}</p>
              <span className="guide-announcement" role="status">
                {guide.title} page guide. Three short tips; close or replay at
                any time.
              </span>
              <h2 aria-live="polite">{tip.title}</h2>
              <p>{tip.text}</p>
              {role === "Viewer" && (
                <p className="muted">
                  Viewer access: editing controls may be unavailable.
                </p>
              )}
              <Button variant="secondary" onClick={showSection}>
                Show section <Icon name="arrow" size={15} />
              </Button>
              {targetNotice && <p role="status">{targetNotice}</p>}
              <div className="page-guide-controls">
                <Button
                  variant="secondary"
                  disabled={index === 0}
                  onClick={() => {
                    setIndex(index - 1);
                    setHighlight(null);
                  }}
                >
                  Back
                </Button>
                <Button
                  onClick={() => {
                    if (index === guide.tips.length - 1) finish();
                    else {
                      setIndex(index + 1);
                      setHighlight(null);
                    }
                  }}
                >
                  {index === guide.tips.length - 1 ? "Got it" : "Next tip"}
                </Button>
              </div>
              <p className="page-guide-footnote">
                First visit only. Replay anytime with Page guide.
              </p>
            </section>
          </div>,
          document.body,
        )}
    </>
  );
}
