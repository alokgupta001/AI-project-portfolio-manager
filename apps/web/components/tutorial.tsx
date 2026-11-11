"use client";

import {
  useCallback,
  useEffect,
  useRef,
  useState,
  type CSSProperties,
} from "react";
import { createPortal } from "react-dom";
import { usePathname, useRouter } from "next/navigation";
import { Button, Modal } from "./ui";
import { Icon, type IconName } from "./icon";
import { PageGuide } from "./page-guide";

type Progress = {
  version: 1;
  status: "active" | "completed" | "skipped";
  step: number;
};
type Stage = "initializing" | "closed" | "welcome" | "tour" | "complete";
type Rect = { top: number; left: number; width: number; height: number };
type Step = {
  title: string;
  description: string;
  icon: IconName;
  route: string;
  action: string;
  selectors: string[];
  compactSelectors?: string[];
  detail?: boolean;
};
const memory = new Map<string, Progress>();
const projectRoutes = new Map<string, string>();
const replayEvent = "ppm:replay-tutorial";

function readProgress(key: string): Progress | null {
  try {
    const raw = localStorage.getItem(key);
    if (raw) {
      const saved = JSON.parse(raw) as Partial<Progress>;
      if (
        saved.version === 1 &&
        ["active", "completed", "skipped"].includes(saved.status || "") &&
        Number.isInteger(saved.step) &&
        Number(saved.step) >= 0 &&
        Number(saved.step) < 8
      )
        return saved as Progress;
    }
  } catch {
    // The tour remains usable when browser storage is blocked or invalid.
  }
  return memory.get(key) || null;
}

export function ReplayTutorialButton({
  className = "",
}: {
  className?: string;
}) {
  return (
    <Button
      variant="secondary"
      className={`tutorial-replay ${className}`}
      aria-label="Replay tutorial"
      title="Replay tutorial"
      type="button"
      onClick={() => window.dispatchEvent(new Event(replayEvent))}
    >
      <Icon name="history" size={17} />
      <span>Replay tutorial</span>
    </Button>
  );
}

/** Only tutorial preference/progress is stored; no records, grants or tokens. */
export function Tutorial({
  userId,
  organizationId,
  role,
}: {
  userId: string;
  organizationId: string;
  role: string;
}) {
  const pathname = usePathname();
  const router = useRouter();
  const key = `ppm-tutorial-v1:${userId}`;
  const [stage, setStage] = useState<Stage>("initializing");
  const [stepIndex, setStepIndex] = useState(0);
  const [skipConfirm, setSkipConfirm] = useState(false);
  const [persistent, setPersistent] = useState(true);
  const [rect, setRect] = useState<Rect | null>(null);
  const [placement, setPlacement] = useState({ top: 88, left: 16 });
  const projectScope = `${userId}:${organizationId}`;
  const [projectHref, setProjectHref] = useState<string | null>(() =>
    /^\/projects\/[^/]+$/.test(pathname)
      ? pathname
      : projectRoutes.get(projectScope) || null,
  );
  const [direction, setDirection] = useState("next");
  const cardRef = useRef<HTMLElement>(null);
  const targetRef = useRef<HTMLElement | null>(null);
  const previousFocus = useRef<HTMLElement | null>(null);
  const initializedKey = useRef("");
  const steps: Step[] = [
    {
      title: "Your navigation hub",
      description:
        "Plan & deliver brings your daily work together. Evidence & intelligence connects the records behind decisions. Use Ctrl or Cmd + K to find a page or a permitted record.",
      icon: "overview",
      route: pathname,
      action: "Explore the navigation",
      selectors: [
        '.sidebar nav[aria-label="Primary navigation"]',
        '[aria-label="Open navigation"]',
      ],
    },
    {
      title: "Your portfolio, in perspective",
      description:
        "The overview uses your authorized command snapshot. Change its date range or portfolio, then select a health category to inspect the matching projects. Unknown values stay distinct from zero.",
      icon: "command",
      route: "/",
      action: "Open workspace overview",
      selectors: [".portfolio-overview", ".home-heading"],
      compactSelectors: [
        ".overview-filters .field:first-child",
        ".home-heading h1",
      ],
    },
    {
      title:
        role === "Viewer"
          ? "How projects get started"
          : "Create your first project",
      description:
        role === "Viewer"
          ? "Your Viewer membership can read projects within its grants. Ask an Admin or an authorized Project Manager to create or change a project; the tour never creates sample records or expands your access."
          : "In Projects, use Create projects, choose an accessible portfolio and enter the required name. Organization configuration must be saved first. Save creates a real record; this tour never submits a form for you.",
      icon: "projects",
      route: "/projects",
      action: "Open projects",
      selectors:
        role === "Viewer"
          ? [".page-heading"]
          : ['[data-tutorial="create-project"]'],
      compactSelectors: role === "Viewer" ? [".page-heading h1"] : undefined,
    },
    {
      title: "Find and manage your work",
      description:
        "Search records, choose a status or industry and change the sort order. These filters query the service; pagination moves through matching records. Clear a filter to widen the results again.",
      icon: "search",
      route: "/projects",
      action: "Open project filters",
      selectors: [".server-filters"],
      compactSelectors: [".server-filters .field:first-child"],
    },
    {
      title: "Explore a project in depth",
      description:
        "Open a permitted project to see its work, milestones, risks, budget and preserved baselines. Section buttons reveal the related records. Edit controls follow your current grants; history explains changes.",
      icon: "portfolios",
      route: projectHref || "/projects",
      action: projectHref ? "Open a project" : "Find a project to explore",
      selectors: [".project-overview", ".delivery-tabs"],
      compactSelectors: [".project-overview h2", ".delivery-tabs"],
      detail: true,
    },
    {
      title: "Track progress with evidence",
      description:
        "Command center connects Executive, Delivery, Risk and Resource views to one date and portfolio scope. Charts include data tables; evidence opens the underlying facts. Export metric DTO downloads the authorized snapshot.",
      icon: "command",
      route: "/command-center",
      action: "Open command center",
      selectors: [".command-filters", '.tabs[aria-label="Dashboard"]'],
      compactSelectors: [".command-filters .field:first-child"],
    },
    {
      title: "Keep evidence connected",
      description:
        "The document library lets you find permitted source text, review versions and follow citations. Upload, retention and governance actions appear only for the right role and project access. Processing and unavailable states stay visible.",
      icon: "documents",
      route: "/documents",
      action: "Open document library",
      selectors: [".document-workspace .page-heading", ".document-workspace"],
      compactSelectors: [".document-workspace .page-heading h1"],
    },
    {
      title: "Make the workspace yours",
      description:
        "Try the theme switch above, review your profile and signed-in sessions in Account & access, or manage in-app notifications from the bell. Replay tutorial is always available in the workspace and account settings.",
      icon: "settings",
      route: "/account",
      action: "Open account & access",
      selectors: ['.top-actions button[aria-label^="Switch to"]'],
    },
  ];
  const step = steps[stepIndex];
  const routeForStep = useCallback(
    (index: number) => {
      if (index === 0 || index === 1) return "/";
      if (index === 2 || index === 3) return "/projects";
      if (index === 4) return projectHref || "/projects";
      if (index === 5) return "/command-center";
      if (index === 6) return "/documents";
      return "/account";
    },
    [projectHref],
  );
  const onStepRoute =
    stepIndex === 0 ||
    stepIndex === 7 ||
    (step.detail
      ? /^\/projects\/[^/]+$/.test(pathname)
      : pathname === step.route);

  const save = useCallback(
    (status: Progress["status"], index: number) => {
      const value: Progress = { version: 1, status, step: index };
      memory.set(key, value);
      try {
        localStorage.setItem(key, JSON.stringify(value));
        setPersistent(true);
      } catch {
        setPersistent(false);
      }
    },
    [key],
  );

  useEffect(() => {
    if (initializedKey.current === key) return;
    const saved = readProgress(key);
    if (!saved && pathname !== "/") {
      setStage("closed");
      return;
    }
    initializedKey.current = key;
    if (saved?.status === "active") {
      setStepIndex(saved.step);
      setStage("tour");
    } else if (!saved) {
      setStage("welcome");
    } else {
      setStage("closed");
    }
  }, [key, pathname]);

  useEffect(() => {
    const replay = () => {
      previousFocus.current = document.activeElement as HTMLElement;
      setStepIndex(0);
      setSkipConfirm(false);
      setStage("welcome");
    };
    window.addEventListener(replayEvent, replay);
    return () => window.removeEventListener(replayEvent, replay);
  }, []);

  function start() {
    save("active", 0);
    setStepIndex(0);
    setStage("tour");
  }
  const move = useCallback(
    (next: number) => {
      if (next < 0) return;
      setDirection(next < stepIndex ? "back" : "next");
      if (next >= 8) {
        save("completed", 7);
        setStage("complete");
      } else {
        save("active", next);
        setStepIndex(next);
        const destination = routeForStep(next);
        if (pathname !== destination) router.push(destination);
      }
    },
    [save, stepIndex, routeForStep, pathname, router],
  );
  function close() {
    setStage("closed");
    setSkipConfirm(false);
    previousFocus.current?.focus();
  }

  useEffect(() => {
    if (stage !== "tour") return;
    let frame = 0;
    let scrolled = false;
    const update = () => {
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(() => {
        const links = Array.from(
          document.querySelectorAll<HTMLAnchorElement>(
            'main a[href^="/projects/"]',
          ),
        );
        const project = links.find((link) =>
          /^\/projects\/[a-zA-Z0-9-]+$/.test(link.getAttribute("href") || ""),
        );
        if (project) {
          const href = project.getAttribute("href")!;
          projectRoutes.set(projectScope, href);
          setProjectHref(href);
        } else if (/^\/projects\/[^/]+$/.test(pathname)) {
          projectRoutes.set(projectScope, pathname);
          setProjectHref(pathname);
        }
        let target: HTMLElement | null = null;
        if (onStepRoute) {
          const selectors =
            window.innerWidth < 1024 && step.compactSelectors
              ? step.compactSelectors
              : step.selectors;
          for (const selector of selectors) {
            const candidates = Array.from(
              document.querySelectorAll<HTMLElement>(selector),
            );
            target =
              candidates.find(
                (candidate) => candidate.getBoundingClientRect().width > 0,
              ) || null;
            if (target) break;
          }
          if (!target && stepIndex === 2 && role !== "Viewer")
            target =
              Array.from(
                document.querySelectorAll<HTMLButtonElement>("main button"),
              ).find(
                (button) => button.textContent?.trim() === "Create projects",
              ) || null;
        }
        targetRef.current = target;
        if (target && !scrolled) {
          const bounds = target.getBoundingClientRect();
          if (window.innerWidth < 1024 && target.closest("main")) {
            const headerBottom =
              document.querySelector(".topbar")?.getBoundingClientRect()
                .bottom || 72;
            window.scrollBy({
              top: bounds.top - Math.max(88, headerBottom + 16),
              behavior: "instant",
            });
          } else if (bounds.top < 8 || bounds.bottom > window.innerHeight - 8)
            target.scrollIntoView({ block: "center", behavior: "instant" });
          scrolled = true;
        }
        const bounds = target?.getBoundingClientRect();
        const width = window.innerWidth;
        const height = window.innerHeight;
        const padding = 7;
        const inViewport =
          bounds &&
          bounds.bottom > 8 &&
          bounds.top < height - 8 &&
          bounds.right > 8 &&
          bounds.left < width - 8;
        const nextRect =
          bounds && inViewport
            ? {
                left: Math.max(8, bounds.left - padding),
                top: Math.max(8, bounds.top - padding),
                width: Math.max(
                  0,
                  Math.min(width - 8, bounds.right + padding) -
                    Math.max(8, bounds.left - padding),
                ),
                height: Math.max(
                  0,
                  Math.min(height - 8, bounds.bottom + padding) -
                    Math.max(8, bounds.top - padding),
                ),
              }
            : null;
        setRect((previous) =>
          JSON.stringify(previous) === JSON.stringify(nextRect)
            ? previous
            : nextRect,
        );
        const cardWidth = Math.min(376, width - 32);
        const cardHeight = cardRef.current?.offsetHeight || 345;
        let left = width - cardWidth - 24;
        let top = Math.max(24, height - cardHeight - 24);
        if (nextRect) {
          const right = nextRect.left + nextRect.width;
          const bottom = nextRect.top + nextRect.height;
          if (width - right > cardWidth + 36) {
            left = right + 20;
            top = nextRect.top;
          } else if (height - bottom > cardHeight + 36) {
            left = nextRect.left;
            top = bottom + 20;
          } else if (nextRect.top > cardHeight + 36) {
            left = nextRect.left;
            top = nextRect.top - cardHeight - 20;
          } else if (nextRect.left > cardWidth + 36) {
            left = nextRect.left - cardWidth - 20;
            top = nextRect.top;
          }
        }
        left = Math.max(16, Math.min(left, width - cardWidth - 16));
        top = Math.max(20, Math.min(top, height - cardHeight - 16));
        setPlacement((previous) =>
          previous.left === left && previous.top === top
            ? previous
            : { left, top },
        );
      });
    };
    update();
    const observer = new MutationObserver(update);
    observer.observe(document.querySelector(".app-shell") || document.body, {
      childList: true,
      subtree: true,
    });
    const resize = new ResizeObserver(update);
    if (cardRef.current) resize.observe(cardRef.current);
    window.addEventListener("resize", update);
    window.addEventListener("scroll", update, true);
    return () => {
      cancelAnimationFrame(frame);
      observer.disconnect();
      resize.disconnect();
      window.removeEventListener("resize", update);
      window.removeEventListener("scroll", update, true);
    };
    // Selectors are stable for a step; target geometry is observed separately.
  }, [stage, stepIndex, pathname, onStepRoute, role, projectScope]);

  useEffect(() => {
    if (stage !== "tour" || skipConfirm) return;
    cardRef.current?.focus({ preventScroll: true });
    const handleKey = (event: KeyboardEvent) => {
      if (document.querySelector("dialog[open]")) return;
      const element = event.target as HTMLElement;
      if (event.key === "Escape") {
        event.preventDefault();
        setSkipConfirm(true);
      } else if (
        !element.closest("input, textarea, select, [contenteditable='true']") &&
        !event.ctrlKey &&
        !event.metaKey &&
        !event.altKey
      ) {
        if (
          event.key === "ArrowRight" ||
          (event.key === "Enter" && element === cardRef.current)
        ) {
          event.preventDefault();
          move(stepIndex + 1);
        } else if (event.key === "ArrowLeft") {
          event.preventDefault();
          move(stepIndex - 1);
        }
      }
    };
    const keepFocusVisible = (event: FocusEvent) => {
      if (document.querySelector("dialog[open]")) return;
      const element = event.target as HTMLElement;
      if (
        !cardRef.current?.contains(element) &&
        !targetRef.current?.contains(element) &&
        !element.closest(".tutorial-progress")
      )
        cardRef.current?.focus({ preventScroll: true });
    };
    document.addEventListener("keydown", handleKey);
    document.addEventListener("focusin", keepFocusVisible);
    return () => {
      document.removeEventListener("keydown", handleKey);
      document.removeEventListener("focusin", keepFocusVisible);
    };
  }, [stage, stepIndex, skipConfirm, move]);

  return (
    <>
      <ReplayTutorialButton />
      <PageGuide userId={userId} role={role} enabled={stage === "closed"} />
      <Modal
        open={stage === "welcome" && !skipConfirm}
        onClose={() => setSkipConfirm(true)}
        title="Welcome to Enterprise PPM"
      >
        <div className="tutorial-welcome">
          <div className="tutorial-illustration" aria-hidden="true">
            <span>
              <Icon name="projects" size={26} />
            </span>
            <span>
              <Icon name="command" size={40} />
            </span>
            <span>
              <Icon name="documents" size={26} />
            </span>
          </div>
          <h3>A clearer path from plans to decisions.</h3>
          <p>
            Get to know your workspace in eight short steps: projects, evidence,
            portfolio insights and the tools that make them work together.
          </p>
          <p className="muted">
            About 3 minutes. Explore real controls at your own pace; nothing is
            created or submitted automatically.
          </p>
          <div className="tutorial-welcome-actions">
            <Button onClick={start} autoFocus>
              Start guided tour <Icon name="arrow" size={17} />
            </Button>
            <Button variant="secondary" onClick={() => setSkipConfirm(true)}>
              Skip tour
            </Button>
          </div>
        </div>
      </Modal>
      {stage === "tour" &&
        typeof document !== "undefined" &&
        createPortal(
          <div className="tutorial-layer" data-direction={direction}>
            <div
              className="tutorial-progress"
              role="progressbar"
              aria-label="Tutorial progress"
              aria-valuenow={stepIndex + 1}
              aria-valuemin={0}
              aria-valuemax={8}
            >
              <span style={{ width: `${((stepIndex + 1) / 8) * 100}%` }} />
            </div>
            <div className="tutorial-mask" aria-hidden="true">
              {rect ? (
                <>
                  <div
                    style={{ left: 0, top: 0, width: "100%", height: rect.top }}
                  />
                  <div
                    style={{
                      left: 0,
                      top: rect.top,
                      width: rect.left,
                      height: rect.height,
                    }}
                  />
                  <div
                    style={{
                      left: rect.left + rect.width,
                      top: rect.top,
                      right: 0,
                      height: rect.height,
                    }}
                  />
                  <div
                    style={{
                      left: 0,
                      top: rect.top + rect.height,
                      width: "100%",
                      bottom: 0,
                    }}
                  />
                  <span className="tutorial-spotlight" style={rect} />
                </>
              ) : (
                <div style={{ inset: 0 }} />
              )}
            </div>
            <section
              ref={cardRef}
              className="tutorial-card"
              style={placement}
              tabIndex={-1}
              aria-label="Guided tutorial"
              aria-describedby="tutorial-title tutorial-description"
              key={stepIndex}
            >
              <div className="tutorial-card-top">
                <span>
                  <Icon name={step.icon} size={19} />
                  Step {stepIndex + 1} of 8
                </span>
                <button
                  className="tutorial-text-button"
                  onClick={() => setSkipConfirm(true)}
                >
                  Skip tour
                </button>
              </div>
              <h2 id="tutorial-title" aria-live="polite">
                {step.title}
              </h2>
              <p id="tutorial-description">{step.description}</p>
              {(!onStepRoute || !rect) && (
                <p className="tutorial-target-note">
                  {!onStepRoute
                    ? "Open this screen to try the highlighted controls, or continue the tour."
                    : stepIndex === 2 && role !== "Viewer"
                      ? "Creation appears after organization setup and with the required role or grant. You can continue without creating a record."
                      : stepIndex === 4
                        ? "Choose a project you can access to see its details. An empty workspace can still complete the tour."
                        : "This section may still be loading or unavailable in your current scope. You can continue the tour."}
                </p>
              )}
              {stepIndex > 0 && (
                <a
                  className="tutorial-route"
                  href={step.route}
                  onClick={() => save("active", stepIndex)}
                >
                  {step.action}
                  <Icon name="arrow" size={15} />
                </a>
              )}
              <div className="tutorial-dots" aria-label="Tutorial steps">
                {steps.map((item, index) => (
                  <button
                    key={item.title}
                    aria-label={`Go to step ${index + 1}: ${item.title}`}
                    aria-current={index === stepIndex ? "step" : undefined}
                    onClick={() => move(index)}
                  >
                    <span />
                  </button>
                ))}
              </div>
              <div className="tutorial-controls">
                <Button
                  variant="secondary"
                  disabled={stepIndex === 0}
                  onClick={() => move(stepIndex - 1)}
                >
                  Back
                </Button>
                <button
                  className="tutorial-text-button"
                  onClick={() => move(stepIndex + 1)}
                >
                  Skip step
                </button>
                <Button onClick={() => move(stepIndex + 1)}>
                  {stepIndex === 7 ? "Finish tour" : "Next"}
                  <Icon name="arrow" size={16} />
                </Button>
              </div>
              <p className="tutorial-keyboard">
                ← → move · Enter continues · Esc skips
              </p>
              {!persistent && (
                <p className="tutorial-storage-note" role="status">
                  Browser storage is unavailable. Progress is remembered for
                  this page session only.
                </p>
              )}
            </section>
          </div>,
          document.body,
        )}
      <Modal
        open={stage === "complete"}
        onClose={close}
        title="You're all set!"
      >
        <div className="tutorial-completion">
          <div className="tutorial-celebration" aria-hidden="true">
            {Array.from({ length: 12 }, (_, index) => (
              <i key={index} style={{ "--particle": index } as CSSProperties} />
            ))}
            <span>
              <Icon name="check" size={36} />
            </span>
          </div>
          <h3>Make your next decision a clearer one.</h3>
          <p>Your workspace is ready. Keep these shortcuts close:</p>
          <ul className="tutorial-tips">
            <li>
              <kbd>Ctrl / Cmd K</kbd>
              <span>Find a page or permitted record.</span>
            </li>
            <li>
              <Icon name="command" />
              <span>Use chart data tables to check exact figures.</span>
            </li>
            <li>
              <Icon name="bell" />
              <span>The bell holds your in-app notifications.</span>
            </li>
            <li>
              <Icon name="coverage" />
              <span>
                Replay this tutorial from your workspace or account settings.
              </span>
            </li>
          </ul>
          <div className="tutorial-welcome-actions">
            <Button onClick={close} autoFocus>
              Explore the workspace
              <Icon name="arrow" size={17} />
            </Button>
            <Button variant="secondary" onClick={start}>
              Replay tour
            </Button>
          </div>
        </div>
      </Modal>
      <Modal
        open={skipConfirm && stage !== "closed"}
        onClose={() => setSkipConfirm(false)}
        title="Skip the tutorial?"
      >
        <p>
          You can replay the tour at any time using Replay tutorial in the
          workspace or Account & access.
        </p>
        <div className="actions">
          <Button
            variant="secondary"
            onClick={() => setSkipConfirm(false)}
            autoFocus
          >
            Keep exploring
          </Button>
          <Button
            onClick={() => {
              save("skipped", stepIndex);
              close();
            }}
          >
            Confirm skip
          </Button>
        </div>
      </Modal>
    </>
  );
}
