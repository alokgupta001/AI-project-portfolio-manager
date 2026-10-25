"use client";
import { useEffect, useState, type ReactNode } from "react";
import { usePathname } from "next/navigation";
import { Button, Modal, Badge } from "./ui";

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
      onClick={toggle}
      aria-label={`Switch to ${theme === "light" ? "dark" : "light"} theme`}
    >
      <span aria-hidden="true">{theme === "light" ? "◐" : "☀"}</span>
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
        P
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
  children,
  transport,
  name,
  role,
  organizationControl,
}: {
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
  const destinations = [
    { name: "Workspace overview", href: "/", icon: "◈" },
    { name: "Projects", href: "/projects", icon: "▤" },
    { name: "Maturity assessments", href: "/assessments", icon: "◉" },
    { name: "Command center", href: "/command-center", icon: "◈" },
    { name: "History & baselines", href: "/ml", icon: "▤" },
    { name: "Integrations & jobs", href: "/integrations", icon: "◇" },
    { name: "Document library", href: "/documents", icon: "▤" },
    { name: "AI operations & evidence", href: "/ai", icon: "◇" },
    { name: "Agents & recommendations", href: "/agents", icon: "◇" },
    { name: "Resource planning", href: "/resources", icon: "▦" },
    { name: "Portfolios", href: "/portfolios", icon: "▦" },
    ...(role === "Admin"
      ? [{ name: "Organization setup", href: "/organization", icon: "◇" }]
      : []),
    { name: "Account & access", href: "/account", icon: "◎" },
    ...(role === "Admin"
      ? [{ name: "Organization members", href: "/account#members", icon: "♙" }]
      : []),
    { name: "Component gallery", href: "/design-system", icon: "▦" },
  ];
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
      <p className="nav-label">WORKSPACE</p>
      <nav aria-label="Primary navigation">
        {destinations.map((d) => (
          <a
            key={d.href}
            href={d.href}
            aria-current={path === d.href ? "page" : undefined}
          >
            <span aria-hidden="true">{d.icon}</span>
            {d.name}
          </a>
        ))}
      </nav>
      <p className="nav-label">COMING NEXT</p>
      <ul className="future-nav">
        {futureModules.map((d) => (
          <li key={d.name}>
            <span>{d.name}</span>
            <span className="future-label">Planned</span>
          </li>
        ))}
      </ul>
      <div className="sidebar-bottom">
        <Badge>Local workspace</Badge>
        <p>
          Built in stages.
          <br />
          Only available modules are active.
        </p>
        <a href="/system">Service diagnostics ↗</a>
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
            ☰
          </Button>
          <div className="organization-control">{organizationControl}</div>
          <div className="top-actions">
            <Button
              variant="secondary"
              className="search-trigger"
              onClick={() => {
                setQuery("");
                setPalette(true);
              }}
              aria-label="Search workspace commands"
            >
              <span aria-hidden="true">⌕</span>
              <span className="search-label">Go to a page…</span>
              <kbd>Ctrl K</kbd>
            </Button>
            <ThemeControl />
            <Button
              variant="secondary"
              aria-label="Open notifications"
              onClick={() => setNotifications(true)}
            >
              ♧
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
