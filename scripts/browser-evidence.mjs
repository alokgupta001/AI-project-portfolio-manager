import {
  copyFileSync,
  existsSync,
  mkdirSync,
  mkdtempSync,
  readFileSync,
  readdirSync,
  writeFileSync,
} from "node:fs";
import { dirname, join, resolve } from "node:path";

// Older browser specs render into docs/verification. Preserve the working bytes,
// including uncommitted evidence; never restore from Git HEAD.
export function preserveBrowserEvidence(projectRoot) {
  const root = resolve(projectRoot);
  const source = join(root, "docs", "verification");
  const parent = join(root, "artifacts", "local", "browser-evidence");
  mkdirSync(parent, { recursive: true });
  const archive = mkdtempSync(join(parent, "run-"));
  const files = [];
  function walk(directory, prefix = "") {
    if (!existsSync(directory)) return;
    for (const entry of readdirSync(directory, { withFileTypes: true })) {
      const relative = join(prefix, entry.name);
      const path = join(directory, entry.name);
      if (entry.isSymbolicLink()) {
        throw new Error(
          `Cannot preserve symlinked browser evidence: ${relative}`,
        );
      }
      if (entry.isDirectory()) walk(path, relative);
      else if (entry.isFile()) {
        const backup = join(archive, "originals", relative);
        mkdirSync(dirname(backup), { recursive: true });
        copyFileSync(path, backup);
        files.push(relative);
      }
    }
  }
  walk(source);
  writeFileSync(join(archive, "files.json"), JSON.stringify(files, null, 2));
  let restored = false;
  return {
    archive,
    restore() {
      if (restored) return;
      const changed = [];
      for (const relative of files) {
        const path = join(source, relative);
        const backup = join(archive, "originals", relative);
        const original = readFileSync(backup);
        if (existsSync(path) && readFileSync(path).equals(original)) continue;
        if (existsSync(path)) {
          const fresh = join(archive, "fresh", relative);
          mkdirSync(dirname(fresh), { recursive: true });
          copyFileSync(path, fresh);
        }
        mkdirSync(dirname(path), { recursive: true });
        writeFileSync(path, original);
        changed.push(relative);
      }
      writeFileSync(
        join(archive, "restored.json"),
        JSON.stringify(changed, null, 2),
      );
      restored = true;
      console.log(
        `Preserved ${changed.length} historical browser artifacts; fresh evidence: ${archive}`,
      );
    },
  };
}
