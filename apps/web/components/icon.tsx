import type { CSSProperties } from "react";

const paths = {
  overview: "M3 3h7v7H3z M14 3h7v7h-7z M3 14h7v7H3z M14 14h7v7h-7z",
  projects:
    "M3 7V5a2 2 0 0 1 2-2h5l2 3h7a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7Z",
  portfolios: "M3 7h18v14H3z M8 7V3h8v4 M3 12h18 M10 12v3h4v-3",
  resources:
    "M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2 M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8 M22 21v-2a4 4 0 0 0-3-3.87 M16 3.13a4 4 0 0 1 0 7.75",
  assessments: "M9 3H5v18h14V3h-4 M9 2h6v4H9z M8 12l2 2 5-5 M8 18h8",
  command: "M3 3v18h18 M7 15l4-5 4 2 6-8",
  documents: "M14 2H4v20h16V8z M14 2v6h6 M8 12h8 M8 16h6",
  integrations: "M8 3v5 M16 3v5 M6 8h12v3a6 6 0 0 1-12 0V8Z M12 17v5",
  ai: "M12 3l2.5 6.5L21 12l-6.5 2.5L12 21l-2.5-6.5L3 12l6.5-2.5Z",
  agents:
    "M12 3v3 M10 3h4 M5 7h14v13H5z M2 11v5 M22 11v5 M9 11v2 M15 11v2 M9 17h6",
  history: "M3 12a9 9 0 1 0 3-6.7 M3 3v6h6 M12 7v5l3 2",
  help: "M21 12a9 9 0 1 0-18 0 9 9 0 0 0 18 0 M9.5 8a2.5 2.5 0 1 1 4 2c-1 .7-1.5 1-1.5 3 M12 17v.1",
  settings: "M4 3h16v18H4z M8 7h8 M8 12h8 M8 17h8 M11 5v4 M15 10v4 M10 15v4",
  account: "M20 21v-2a7 7 0 0 0-14 0v2 M13 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8",
  gallery: "M3 3h7v7H3z M14 3h7v7h-7z M3 14h7v7H3z M14 14h7v7h-7z",
  search: "M21 21l-6-6 M17 10a7 7 0 1 0-14 0 7 7 0 0 0 14 0",
  moon: "M21 13a9 9 0 0 1-10-10 9 9 0 1 0 10 10Z",
  sun: "M12 3V1 M12 23v-2 M3 12H1 M23 12h-2 M5 5 3 3 M21 21l-2-2 M5 19l-2 2 M21 3l-2 2 M16 12a4 4 0 1 0-8 0 4 4 0 0 0 8 0",
  bell: "M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9 M10 21h4",
  menu: "M3 6h18 M3 12h18 M3 18h18",
  arrow: "M4 12h16 M14 6l6 6-6 6",
  check: "M5 12l4 4L19 6",
  warning: "M12 3 2 21h20L12 3Z M12 9v5 M12 17v.1",
  coverage: "M12 3v9h9 M9 3.5a9 9 0 1 0 11.5 11.5",
  monitor: "M3 3h18v14H3z M12 17v4 M8 21h8",
  pulse: "M2 12h5l3-9 4 18 3-9h5",
} as const;

export type IconName = keyof typeof paths;
export function Icon({
  name,
  size = 20,
  style,
}: {
  name: IconName;
  size?: number;
  style?: CSSProperties;
}) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.7"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      focusable="false"
      style={style}
    >
      <path d={paths[name]} />
    </svg>
  );
}
