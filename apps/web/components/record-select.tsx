"use client";
import { useEffect, useState } from "react";
import { usePilotApi } from "./pilot-api";

export function RecordSelect({
  transport,
  kind,
  label,
  value,
  onChange,
  name,
  required = false,
  refreshKey = 0,
}: {
  transport: typeof fetch;
  kind: string;
  label: string;
  value?: string;
  onChange?: (value: string) => void;
  name?: string;
  required?: boolean;
  refreshKey?: number;
}) {
  const api = usePilotApi(transport);
  const [q, setQ] = useState("");
  const [offset, setOffset] = useState(0);
  const [rows, setRows] = useState<{ id: string; name: string }[]>([]);
  const [next, setNext] = useState(false);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  useEffect(() => {
    let live = true;
    setBusy(true);
    setError("");
    const timer = setTimeout(() => {
      void api<
        | { items: { id: string; data: { name: string } }[]; total: number }
        | { id: string; name: string }[]
      >(
        `delivery/${kind}?` +
          new URLSearchParams({ q, offset: String(offset), limit: "25" }),
      )
        .then((p) => {
          if (live) {
            const items = Array.isArray(p)
              ? p
              : p.items.map((r) => ({ id: r.id, name: r.data.name }));
            setRows(items);
            setNext(
              Array.isArray(p) ? items.length === 25 : offset + 25 < p.total,
            );
          }
        })
        .catch((e) => {
          if (live) {
            setRows([]);
            setError(e.message);
          }
        })
        .finally(() => {
          if (live) setBusy(false);
        });
    }, 150);
    return () => {
      live = false;
      clearTimeout(timer);
    };
  }, [api, kind, q, offset, refreshKey]);
  return (
    <div className="reference-field">
      <label>
        Find {label.toLowerCase()}
        <input
          type="search"
          value={q}
          maxLength={160}
          onChange={(e) => {
            setQ(e.target.value);
            setOffset(0);
          }}
        />
      </label>
      <label>
        {label}
        <select
          name={name}
          required={required}
          value={value}
          onChange={(e) => onChange?.(e.target.value)}
        >
          <option value="">{required ? "Select…" : "None"}</option>
          {value && !rows.some((r) => r.id === value) && (
            <option value={value}>Current selection</option>
          )}
          {rows.map((r) => (
            <option key={r.id} value={r.id}>
              {r.name}
            </option>
          ))}
        </select>
      </label>
      {busy && <p role="status">Loading choices…</p>}
      {error && <p role="alert">{error}</p>}
      {!busy && !error && !rows.length && <p>No permitted choices match.</p>}
      <button
        type="button"
        disabled={!offset || busy}
        onClick={() => setOffset(offset - 25)}
      >
        Previous {label.toLowerCase()}
      </button>
      <button
        type="button"
        disabled={!next || busy}
        onClick={() => setOffset(offset + 25)}
      >
        Next {label.toLowerCase()}
      </button>
    </div>
  );
}
