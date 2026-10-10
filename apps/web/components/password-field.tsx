"use client";
import { useId, useState } from "react";

export function PasswordField({
  label,
  autoComplete,
  minLength = 1,
}: {
  label: string;
  autoComplete: "current-password" | "new-password";
  minLength?: number;
}) {
  const id = useId();
  const [visible, setVisible] = useState(false);
  return (
    <div>
      <label htmlFor={id}>{label}</label>
      <div className="password-control">
        <input
          id={id}
          name="password"
          type={visible ? "text" : "password"}
          required
          autoComplete={autoComplete}
          minLength={minLength}
          maxLength={72}
        />
        <button
          type="button"
          aria-controls={id}
          aria-label={visible ? "Hide password" : "Show password"}
          aria-pressed={visible}
          onClick={() => setVisible((v) => !v)}
        >
          <svg
            aria-hidden="true"
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7S2 12 2 12Z" />
            <circle cx="12" cy="12" r="3" />
            {visible && <path d="m3 3 18 18" />}
          </svg>
          {visible ? "Hide" : "Show"}
        </button>
      </div>
    </div>
  );
}
