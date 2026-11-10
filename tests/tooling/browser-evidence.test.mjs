import assert from "node:assert/strict";
import {
  mkdirSync,
  mkdtempSync,
  readFileSync,
  unlinkSync,
  writeFileSync,
} from "node:fs";
import { join, resolve } from "node:path";
import { test } from "node:test";
import { preserveBrowserEvidence } from "../../scripts/browser-evidence.mjs";

function fixture() {
  const parent = resolve("artifacts/local/tooling-tests");
  mkdirSync(parent, { recursive: true });
  const root = mkdtempSync(join(parent, "evidence-"));
  const folder = join(root, "docs/verification");
  mkdirSync(folder, { recursive: true });
  return { root, folder };
}

test("restores exact uncommitted binary evidence and retains the fresh render", () => {
  const { root, folder } = fixture();
  const path = join(folder, "existing.png");
  const original = Buffer.from([0, 255, 12, 90]);
  const fresh = Buffer.from([1, 2, 3, 4]);
  writeFileSync(path, original);
  const evidence = preserveBrowserEvidence(root);
  writeFileSync(path, fresh);
  evidence.restore();
  assert.deepEqual(readFileSync(path), original);
  assert.deepEqual(
    readFileSync(join(evidence.archive, "fresh/existing.png")),
    fresh,
  );
});

test("restores deleted nested evidence even when a browser run throws", () => {
  const { root, folder } = fixture();
  mkdirSync(join(folder, "nested"));
  const path = join(folder, "nested/results.json");
  writeFileSync(path, '{"prior":true}\r\n');
  const evidence = preserveBrowserEvidence(root);
  assert.throws(() => {
    try {
      unlinkSync(path);
      throw new Error("browser failed");
    } finally {
      evidence.restore();
    }
  }, /browser failed/);
  assert.equal(readFileSync(path, "utf8"), '{"prior":true}\r\n');
});

test("does not discard new evidence or overwrite subsequent work on a second restore", () => {
  const { root, folder } = fixture();
  const path = join(folder, "prior.json");
  writeFileSync(path, "before");
  const evidence = preserveBrowserEvidence(root);
  writeFileSync(join(folder, "new.json"), "new evidence");
  evidence.restore();
  writeFileSync(path, "later edit");
  evidence.restore();
  assert.equal(readFileSync(path, "utf8"), "later edit");
  assert.equal(readFileSync(join(folder, "new.json"), "utf8"), "new evidence");
});
