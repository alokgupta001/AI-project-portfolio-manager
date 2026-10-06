import { spawnSync } from "node:child_process";
import { readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import openapiTS, { astToString } from "openapi-typescript";
const check = process.argv.includes("--check");
const python = process.env.PPM_PYTHON || (process.platform === "win32" ? ".venv/Scripts/python.exe" : ".venv/bin/python");
const result = spawnSync(python, ["scripts/export_openapi.py", ...(check ? ["--check"] : [])], { stdio: "inherit" });
if (result.status !== 0) process.exit(result.status || 1);
const schema = JSON.parse(readFileSync("packages/contracts/openapi.json", "utf8"));
const content = "// Generated from backend OpenAPI. Do not edit.\n" + astToString(await openapiTS(schema));
const target = resolve("packages/contracts/src/schema.d.ts");
if (check) {
  if (readFileSync(target, "utf8") !== content) throw new Error("TypeScript contract drift; run npm run contracts:generate");
} else writeFileSync(target, content);
console.log(check ? "OpenAPI and TypeScript contracts match." : "Contracts generated.");
