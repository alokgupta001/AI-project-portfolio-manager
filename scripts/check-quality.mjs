import { spawnSync } from "node:child_process";
import { existsSync, mkdirSync, mkdtempSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("../", import.meta.url));
const options = new Set(process.argv.slice(2));
if ([...options].some((option) => !["--static", "--build"].includes(option))) {
  console.error("Usage: npm run check -- [--static] [--build]");
  process.exit(2);
}

const python =
  process.env.PPM_PYTHON ||
  join(
    root,
    ".venv",
    process.platform === "win32" ? "Scripts/python.exe" : "bin/python",
  );
const npmCli =
  process.env.npm_execpath ||
  join(dirname(process.execPath), "node_modules/npm/bin/npm-cli.js");
if (!existsSync(python) || !existsSync(npmCli)) {
  console.error(
    "Use npm with the existing project .venv (or set PPM_PYTHON). See LOCAL-DEVELOPMENT.md.",
  );
  process.exit(2);
}

// Windows sandbox TEMP can be inaccessible to pytest. Give this run its own
// ignored workspace directory; never reuse or delete an existing temp tree.
const tempParent = join(root, "artifacts", "local", "quality-temp");
mkdirSync(tempParent, { recursive: true });
const tempDir = mkdtempSync(join(tempParent, "run-"));

// Reuse installed tools and package scripts; never install, fix, migrate or reset.
const checks = [
  [
    "Python lint",
    python,
    ["-m", "ruff", "check", "services", "scripts", "tests"],
  ],
  [
    "Python format",
    python,
    ["-m", "ruff", "format", "--check", "services", "scripts", "tests"],
  ],
  [
    "Python types",
    python,
    ["-m", "mypy", "services/api/ppm_api", "services/worker/ppm_worker"],
  ],
  ["Source preservation", python, ["scripts/check_sources.py"]],
  ...[
    "contracts:check",
    "lint",
    "typecheck",
    "typecheck:browser",
    "format:check",
    "test:tooling",
  ].map((script) => [script, process.execPath, [npmCli, "run", script]]),
];
if (!options.has("--static")) {
  checks.push([
    "Backend unit tests",
    python,
    ["-m", "pytest", "-q", "--tb=short", "-m", "not integration"],
  ]);
}
if (options.has("--build")) {
  checks.push(["Frontend build", process.execPath, [npmCli, "run", "build"]]);
}

const results = [];
for (const [name, executable, args] of checks) {
  console.log(`\nRunning ${name}`);
  const started = Date.now();
  const result = spawnSync(executable, args, {
    cwd: root,
    stdio: "inherit",
    shell: false,
    env: {
      ...process.env,
      TEMP: tempDir,
      TMP: tempDir,
      TMPDIR: tempDir,
      PPM_AI_PROVIDER: "disabled",
      PPM_AI_REAL_CALLS_AUTHORIZED: "false",
      PPM_AI_CLOUD_ENABLED: "false",
      PPM_AI_OLLAMA_ENABLED: "false",
    },
  });
  if (result.error) console.error(result.error.message);
  results.push({
    name,
    status: result.status === 0 && !result.error ? "passed" : "failed",
    seconds: ((Date.now() - started) / 1000).toFixed(1),
  });
}
console.table(results);
process.exitCode = results.some(({ status }) => status === "failed") ? 1 : 0;
