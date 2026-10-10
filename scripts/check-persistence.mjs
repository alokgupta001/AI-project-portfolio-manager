import { spawnSync } from "node:child_process";
const docker = process.env.PPM_DOCKER || "docker";
const api = process.env.PPM_API_URL || "http://127.0.0.1:8000";
const read = async () => {
  const response = await fetch(`${api}/api/v1/foundation`, { signal: AbortSignal.timeout(5000) });
  if (!response.ok) throw new Error("Foundation unavailable");
  return (await response.json()).instance_id;
};
const before = await read();
const objectWrite = spawnSync(docker, ["compose", "exec", "-T", "api", "python", "scripts/storage_probe.py", "write"], { stdio: "inherit" });
if (objectWrite.status !== 0) process.exit(objectWrite.status || 1);
const result = spawnSync(docker, ["compose", "restart", "postgres", "redis", "api", "worker", "dispatcher", "web"], { stdio: "inherit" });
if (result.status !== 0) process.exit(result.status || 1);
let restored = false;
for (let attempt = 0; attempt < 30; attempt++) {
  try {
    const health = await fetch(`${api}/api/v1/health/ready`, { signal: AbortSignal.timeout(5000) });
    if (health.ok) { restored = true; break; }
  } catch { /* Service may be restarting. */ }
  await new Promise(resolve => setTimeout(resolve, 1000));
}
if (!restored || (await read()) !== before) throw new Error("Persisted checkpoint did not survive restart");
const objectRead = spawnSync(docker, ["compose", "exec", "-T", "api", "python", "scripts/storage_probe.py", "verify"], { stdio: "inherit" });
if (objectRead.status !== 0) process.exit(objectRead.status || 1);
console.log("PASS: database checkpoint survived PostgreSQL/Redis/API/worker/dispatcher/web restart:", before);
