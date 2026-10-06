"use client";

import {
  useEffect,
  useId,
  useRef,
  useState,
  type ReactNode,
  type ButtonHTMLAttributes,
} from "react";

export function Button({
  variant = "primary",
  className = "",
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "secondary" | "danger";
}) {
  return <button className={`button ${variant} ${className}`} {...props} />;
}
export function Badge({
  children,
  tone = "neutral",
}: {
  children: ReactNode;
  tone?: "neutral" | "success" | "warning";
}) {
  return <span className={`badge ${tone}`}>{children}</span>;
}
export function Field({
  label,
  children,
  hint,
}: {
  label: string;
  children: ReactNode;
  hint?: string;
}) {
  return (
    <label className="field">
      <span>{label}</span>
      {children}
      {hint && <small>{hint}</small>}
    </label>
  );
}
export function StatePanel({
  title,
  children,
  kind = "empty",
  action,
}: {
  title: string;
  children: ReactNode;
  kind?: "empty" | "error" | "forbidden" | "partial";
  action?: ReactNode;
}) {
  return (
    <section
      className={`state-panel state-${kind}`}
      role={kind === "error" ? "alert" : undefined}
    >
      <span className="state-symbol" aria-hidden="true">
        {kind === "error" ? "!" : "◇"}
      </span>
      <h2>{title}</h2>
      <p>{children}</p>
      {action}
    </section>
  );
}
export function Skeleton({ label = "Loading workspace" }: { label?: string }) {
  return (
    <div role="status" className="skeleton">
      <span>{label}…</span>
      <div aria-hidden="true" />
      <div aria-hidden="true" />
      <div aria-hidden="true" />
    </div>
  );
}
export function MetricCard({
  label,
  value,
  detail,
}: {
  label: string;
  value: ReactNode;
  detail: string;
}) {
  return (
    <article className="metric-card">
      <p>{label}</p>
      <strong>{value}</strong>
      <small>{detail}</small>
    </article>
  );
}
export function Modal({
  open,
  onClose,
  title,
  children,
  drawer = false,
}: {
  open: boolean;
  onClose: () => void;
  title: string;
  children: ReactNode;
  drawer?: boolean;
}) {
  const ref = useRef<HTMLDialogElement>(null);
  const id = useId();
  useEffect(() => {
    const dialog = ref.current;
    if (!dialog || !open) return;
    const previous = document.activeElement as HTMLElement | null;
    dialog.showModal();
    const overflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      dialog.close();
      document.body.style.overflow = overflow;
      previous?.focus();
    };
  }, [open]);
  return (
    <dialog
      ref={ref}
      aria-labelledby={id}
      className={drawer ? "modal drawer" : "modal"}
      onCancel={(e) => {
        e.preventDefault();
        onClose();
      }}
    >
      <div className="dialog-heading">
        <h2 id={id}>{title}</h2>
        <Button
          variant="secondary"
          onClick={onClose}
          aria-label={`Close ${title}`}
        >
          ×
        </Button>
      </div>
      {children}
    </dialog>
  );
}
export type Confirmation = {
  title: string;
  description: string;
  confirm: () => Promise<void>;
};
export function ConfirmDialog({
  value,
  onClose,
}: {
  value: Confirmation | null;
  onClose: () => void;
}) {
  return (
    <Modal
      open={!!value}
      onClose={onClose}
      title={value?.title || "Confirm action"}
    >
      <p>{value?.description}</p>
      <div className="actions">
        <Button variant="secondary" autoFocus onClick={onClose}>
          Cancel
        </Button>
        <Button
          variant="danger"
          onClick={() => {
            const run = value?.confirm;
            onClose();
            void run?.();
          }}
        >
          Confirm change
        </Button>
      </div>
    </Modal>
  );
}
export type Column<T> = {
  key: string;
  label: string;
  render: (row: T) => ReactNode;
  sort?: (row: T) => string | number;
};
export function DataTable<T>({
  rows,
  columns,
  rowKey,
  caption,
  searchText,
  pageSize = 5,
  external = false,
}: {
  rows: T[];
  columns: Column<T>[];
  rowKey: (row: T) => string;
  caption: string;
  searchText: (row: T) => string;
  pageSize?: number;
  external?: boolean;
}) {
  const [query, setQuery] = useState("");
  const [page, setPage] = useState(0);
  const [sort, setSort] = useState({ key: "", descending: false });
  const [density, setDensity] = useState("comfortable");
  const column = columns.find((c) => c.key === sort.key);
  const filtered = rows.filter((r) =>
    searchText(r).toLowerCase().includes(query.toLowerCase()),
  );
  if (column?.sort)
    filtered.sort(
      (a, b) =>
        String(column.sort!(a)).localeCompare(
          String(column.sort!(b)),
          undefined,
          { numeric: true },
        ) * (sort.descending ? -1 : 1),
    );
  const pages = Math.max(1, Math.ceil(filtered.length / pageSize));
  const current = Math.min(page, pages - 1);
  return (
    <div className="data-table">
      <div className="table-tools">
        {!external && (
          <Field label={`Filter ${caption}`}>
            <input
              type="search"
              value={query}
              onChange={(e) => {
                setQuery(e.target.value);
                setPage(0);
              }}
              placeholder="Search loaded records…"
            />
          </Field>
        )}
        <Field label={`Density for ${caption}`}>
          <select value={density} onChange={(e) => setDensity(e.target.value)}>
            <option value="comfortable">Comfortable</option>
            <option value="compact">Compact</option>
          </select>
        </Field>
      </div>
      <div
        className="table-scroll"
        tabIndex={0}
        role="region"
        aria-label={`${caption} table`}
      >
        <table data-density={density}>
          <caption>
            {caption} · {filtered.length}{" "}
            {external ? "records on this page" : "matching loaded records"}
          </caption>
          <thead>
            <tr>
              {columns.map((c) => (
                <th
                  key={c.key}
                  scope="col"
                  aria-sort={
                    c.key === sort.key
                      ? sort.descending
                        ? "descending"
                        : "ascending"
                      : undefined
                  }
                >
                  {c.sort ? (
                    <button
                      className="sort-button"
                      onClick={() => {
                        setSort({
                          key: c.key,
                          descending: c.key === sort.key && !sort.descending,
                        });
                        setPage(0);
                      }}
                    >
                      {c.label} <span aria-hidden="true">↕</span>
                    </button>
                  ) : (
                    c.label
                  )}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filtered
              .slice(current * pageSize, (current + 1) * pageSize)
              .map((row) => (
                <tr key={rowKey(row)}>
                  {columns.map((c) => (
                    <td key={c.key}>{c.render(row)}</td>
                  ))}
                </tr>
              ))}
          </tbody>
        </table>
      </div>
      {filtered.length === 0 && (
        <p className="table-empty">
          No matching records. Try a different filter.
        </p>
      )}
      {!external && (
        <div className="pagination">
          <span>
            Page {current + 1} of {pages}
          </span>
          <div className="actions">
            <Button
              variant="secondary"
              disabled={current === 0}
              onClick={() => setPage(current - 1)}
            >
              Previous
            </Button>
            <Button
              variant="secondary"
              disabled={current === pages - 1}
              onClick={() => setPage(current + 1)}
            >
              Next
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
export function ChartFrame({
  title,
  description,
  children,
  table,
}: {
  title: string;
  description: string;
  children: ReactNode;
  table: ReactNode;
}) {
  return (
    <section className="panel chart-frame">
      <h2>{title}</h2>
      <p className="muted">{description}</p>
      <div aria-hidden="true">{children}</div>
      <details>
        <summary>View chart data table</summary>
        {table}
      </details>
    </section>
  );
}
