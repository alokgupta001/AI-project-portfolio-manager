import { spawnSync } from "node:child_process";
import { mkdirSync, writeFileSync, existsSync, unlinkSync } from "node:fs";
import { resolve } from "node:path";

const docker = process.env.PPM_DOCKER || "docker";
const args = ["compose", "-f", "compose.yaml", "-f", "compose.documents.yaml", "-f", "compose.identity-test.yaml"];
const env = {...process.env, PPM_WEB_PORT:"3001", PPM_API_PORT:"8001", PPM_POSTGRES_PORT:"15433",
  PPM_REDIS_PORT:"16380", PPM_WEB_ORIGIN:"http://localhost:3001",
  PPM_WEB_URL:"http://localhost:3001", PPM_API_URL:"http://127.0.0.1:8001"};
function run(command, parameters, capture=false, input=undefined) {
  const result=spawnSync(command,parameters,{env,encoding:"utf8",stdio:capture?"pipe":"inherit", input});
  if(result.status!==0) {
    if(capture && result.stderr) process.stderr.write(result.stderr);
    throw new Error(`Acceptance command failed: ${command} (exit ${result.status})`);
  }
  return result.stdout;
}
try {
  run(docker,[...args,"up","--build","-d","--wait"]);
  run(docker,[...args,"--profile","test","build","test"]);
  const fixture=JSON.parse(run(docker,[...args,"--profile","test","run","--rm","test","python","scripts/browser_identity_fixture.py"],true));
  // Seed specialist data for the default full suite as well as focused runs.
  run(docker,[...args,"stop","dispatcher"]);
  Object.assign(fixture, JSON.parse(run(docker,[...args,"--profile","test","run","--rm","-T","test","python","scripts/browser_agent_fixture.py"],true,JSON.stringify(fixture))));
  run(docker,[...args,"start","dispatcher"]);
  mkdirSync("artifacts/local",{recursive:true});
  env.PPM_IDENTITY_FIXTURE=resolve("artifacts/local/identity-fixture.json");
  writeFileSync(env.PPM_IDENTITY_FIXTURE,JSON.stringify(fixture),{mode:0o600});
  run(process.execPath,["node_modules/@playwright/test/cli.js","test",...process.argv.slice(2)]);
} finally {
  if (env.PPM_IDENTITY_FIXTURE && existsSync(env.PPM_IDENTITY_FIXTURE)) unlinkSync(env.PPM_IDENTITY_FIXTURE);
  // Preserve named volumes; never delete local/test data as an implicit cleanup step.
  run(docker,[...args,"down"]);
}
