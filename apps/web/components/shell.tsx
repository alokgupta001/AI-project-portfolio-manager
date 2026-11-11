"use client";
import { useEffect, useState, type ReactNode } from "react";
import { usePathname } from "next/navigation";
import { Button, Modal, Badge } from "./ui";
import { Icon, type IconName } from "./icon";
import { Tutorial } from "./tutorial";

export function ThemeControl() {
  const [theme, setTheme] = useState("light");
  useEffect(() => {
    setTheme(document.documentElement.dataset.theme || "light");
  }, []);
  function toggle() {
    const next = theme === "light" ? "dark" : "light";
    setTheme(next);
    document.documentElement.dataset.theme = next;
    try {
      localStorage.setItem("ppm-theme", next);
    } catch {
      /* Theme still works in memory when storage is unavailable. */
    }
  }
  return (
    <Button
      variant="secondary"
      className="theme-control"
      data-theme-state={theme}
      onClick={toggle}
      aria-label={`Switch to ${theme === "light" ? "dark" : "light"} theme`}
    >
      <Icon name={theme === "light" ? "moon" : "sun"} />
      <span className="theme-label">
        {theme === "light" ? "Dark" : "Light"}
      </span>
    </Button>
  );
}
export const futureModules = [
  {
    name: "AI PMO copilot",
    sprint: "14",
    detail: "Ask questions grounded in your organization's data.",
  },
];
export function Brand() {
  return (
    <a className="brand" href="/">
      <span className="brand-mark" aria-hidden="true">
        <Icon name="command" size={24} />
      </span>
      <span>
        Enterprise PPM<small>INTELLIGENCE WORKSPACE</small>
      </span>
    </a>
  );
}
export function AuthFrame({ children }: { children: ReactNode }) {
  return (
    <div className="auth-layout">
      <aside className="auth-story">
        <Brand />
        <div>
          <p className="eyebrow">CLARITY. ALIGNMENT. IMPACT.</p>
          <h2>
            A clearer view.
            <br />A stronger portfolio.
          </h2>
          <p>One workspace for your people, delivery and decisions.</p>
          <div className="orbit-art" aria-hidden="true">
            <span />
            <span />
            <span />
            <b>P</b>
          </div>
        </div>
        <p className="muted">Your organization's next chapter starts here.</p>
      </aside>
      <div className="auth-content">
        <div className="auth-top">
          <a href="/">Workspace</a>
          <ThemeControl />
        </div>
        {children}
      </div>
    </div>
  );
}
import { RecordSearch, PersonalFeed } from "./pilot";
export function Shell({
  userId,
  organizationId,
  children,
  transport,
  name,
  role,
  organizationControl,
}: {
  userId: string;
  organizationId: string;
  children: ReactNode;
  transport: typeof fetch;
  name: string;
  role: string;
  organizationControl: ReactNode;
}) {
  const path = usePathname();
  const [menu, setMenu] = useState(false);
  const [palette, setPalette] = useState(false);
  const [notifications, setNotifications] = useState(false);
  const [query, setQuery] = useState("");
  const groups: {
    name: string;
    items: { name: string; href: string; icon: IconName }[];
  }[] = [
    {
      name: "Plan & deliver",
      items: [
        { name: "Workspace overview", href: "/", icon: "overview" },
        { name: "Projects", href: "/projects", icon: "projects" },
        { name: "Portfolios", href: "/portfolios", icon: "portfolios" },
        { name: "Resource planning", href: "/resources", icon: "resources" },
        {
          name: "Maturity assessments",
          href: "/assessments",
          icon: "assessments",
        },
        { name: "Command center", href: "/command-center", icon: "command" },
      ],
    },
    {
      name: "Evidence & intelligence",
      items: [
        { name: "Document library", href: "/documents", icon: "documents" },
        {
          name: "Integrations & jobs",
          href: "/integrations",
          icon: "integrations",
        },
        { name: "AI operations & evidence", href: "/ai", icon: "ai" },
        { name: "Agents & recommendations", href: "/agents", icon: "agents" },
        { name: "History & baselines", href: "/ml", icon: "history" },
      ],
    },
    {
      name: "Workspace",
      items: [
        ...(role === "Admin"
          ? [
              {
                name: "Organization setup",
                href: "/organization",
                icon: "settings" as const,
              },
            ]
          : []),
        { name: "Account & access", href: "/account", icon: "account" },
        ...(role === "Admin"
          ? [
              {
                name: "Organization members",
                href: "/account#members",
                icon: "resources" as const,
              },
            ]
          : []),
        { name: "Component gallery", href: "/design-system", icon: "gallery" },
      ],
    },
  ];
  const destinations = groups.flatMap((group) => group.items);
  const results = destinations.filter((d) =>
    d.name.toLowerCase().includes(query.toLowerCase()),
  );
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setPalette((v) => !v);
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, []);
  const navigation = (
    <>
      <nav aria-label="Primary navigation">
        {groups.map((group) => (
          <div className="nav-group" key={group.name}>
            <p className="nav-label">{group.name}</p>
            {group.items.map((d) => (
              <a
                key={d.href}
                href={d.href}
                onClick={() => setMenu(false)}
                aria-current={
                  !d.href.includes("#") &&
                  (path === d.href ||
                    (d.href !== "/" && path.startsWith(d.href + "/")))
                    ? "page"
                    : undefined
                }
              >
                <Icon name={d.icon} size={18} />
                <span className="nav-text">{d.name}</span>
              </a>
            ))}
          </div>
        ))}
      </nav>
      <div className="sidebar-bottom">
        <Badge>Local workspace</Badge>
        <a href="/system">
          <Icon name="pulse" size={17} />
          Service diagnostics <span aria-hidden="true">↗</span>
        </a>
      </div>
    </>
  );
  return (
    <div className="app-shell">
      <a className="skip-link" href="#main-content">
        Skip to main content
      </a>
      <aside className="sidebar">
        <Brand />
        {navigation}
      </aside>
      <div className="shell-body">
        <header className="topbar">
          <Button
            variant="secondary"
            className="mobile-menu"
            onClick={() => setMenu(true)}
            aria-label="Open navigation"
          >
            <Icon name="menu" />
          </Button>
          <div className="organization-control">{organizationControl}</div>
          <div className="top-actions">
            <Tutorial
              userId={userId}
              organizationId={organizationId}
              role={role}
            />
            <Button
              variant="secondary"
              className="search-trigger"
              onClick={() => {
                setQuery("");
                setPalette(true);
              }}
              aria-label="Search workspace commands"
            >
              <Icon name="search" size={18} />
              <span className="search-label">Go to a page…</span>
              <kbd>Ctrl K</kbd>
            </Button>
            <ThemeControl />
            <Button
              variant="secondary"
              aria-label="Open notifications"
              onClick={() => setNotifications(true)}
            >
              <Icon name="bell" />
            </Button>
            <a
              className="avatar"
              href="/account"
              aria-label={`Account for ${name}`}
            >
              {name.slice(0, 1).toUpperCase()}
            </a>
          </div>
        </header>
        <main id="main-content" tabIndex={-1} className="workspace-content">
          <nav className="breadcrumbs" aria-label="Breadcrumb">
            <a href="/">Workspace</a>
            <span aria-hidden="true">/</span>
            <span aria-current="page">
              {path === "/"
                ? "Overview"
                : path === "/design-system"
                  ? "Component gallery"
                  : path.startsWith("/agents")
                    ? "Agents & recommendations"
                    : path.startsWith("/ai")
                      ? "AI operations & evidence"
                      : path.startsWith("/documents")
                        ? "Document library"
                        : path.startsWith("/integrations")
                          ? "Integrations & jobs"
                          : path.startsWith("/ml")
                            ? "History & baselines"
                            : path.startsWith("/command-center")
                              ? "Command center"
                              : path.startsWith("/assessments")
                                ? "Maturity assessments"
                                : path.startsWith("/resources")
                                  ? "Resource planning"
                                  : path.startsWith("/projects")
                                    ? "Projects"
                                    : path.startsWith("/portfolios")
                                      ? "Portfolios"
                                      : path === "/organization"
                                        ? "Organization setup"
                                        : "Account & access"}
            </span>
          </nav>
          {children}
          <footer className="workspace-footer">
            <span>Enterprise PPM · Local development</span>
            <span>Portfolio & delivery · Local workspace</span>
          </footer>
        </main>
      </div>
      <Modal
        open={menu}
        onClose={() => setMenu(false)}
        title="Navigation"
        drawer
      >
        {navigation}
      </Modal>
      <Modal
        open={notifications}
        onClose={() => setNotifications(false)}
        title="Notifications"
        drawer
      >
        {notifications && <PersonalFeed transport={transport} notifications />}
      </Modal>
      <Modal
        open={palette}
        onClose={() => setPalette(false)}
        title="Workspace commands"
      >
        <p className="muted">
          Search available pages, or find permitted projects, work, risks and
          assessments below.
        </p>
        <label className="field">
          Find a page
          <input
            autoFocus
            type="search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "ArrowDown") {
                e.preventDefault();
                document
                  .querySelector<HTMLAnchorElement>(
                    "dialog[open] .command-results a",
                  )
                  ?.focus();
              }
            }}
          />
        </label>
        <nav
          className="command-results"
          aria-label="Available commands"
          onKeyDown={(e) => {
            const links = Array.from(e.currentTarget.querySelectorAll("a"));
            const index = links.indexOf(
              document.activeElement as HTMLAnchorElement,
            );
            if (["ArrowDown", "ArrowUp"].includes(e.key)) {
              e.preventDefault();
              links[
                (index + (e.key === "ArrowDown" ? 1 : -1) + links.length) %
                  links.length
              ]?.focus();
            }
          }}
        >
          {results.map((d) => (
            <a key={d.href} href={d.href} onClick={() => setPalette(false)}>
              {d.name}
              <span aria-hidden="true">↗</span>
            </a>
          ))}
        </nav>
        {results.length === 0 && <p>No available pages match your search.</p>}
        {palette && <RecordSearch transport={transport} />}
        <p className="muted">↑ ↓ to move · Enter to open · Esc to close</p>
      </Modal>
    </div>
  );
}
