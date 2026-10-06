import { readFileSync, writeFileSync } from "node:fs";
const lock = JSON.parse(readFileSync("package-lock.json", "utf8"));
const packages = Object.entries(lock.packages)
  .filter(([path, value]) => path.includes("node_modules/") && !value.link)
  .map(([path, value]) => ({ path, version: value.version, declared_license: value.license || "Not declared" }))
  .sort((a, b) => a.path.localeCompare(b.path));
writeFileSync("docs/verification/npm-dependencies.json", JSON.stringify(packages, null, 2) + "\n");
console.log(`Recorded ${packages.length} npm lock entries and declared license metadata.`);
