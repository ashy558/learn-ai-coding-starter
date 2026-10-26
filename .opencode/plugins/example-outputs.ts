import { spawn } from "node:child_process";
import { readdir } from "node:fs/promises";
import { join } from "node:path";
import { Plugin } from "@opencode/plugin";

const TIMEOUT_MS = 30_000;
const KILL_GRACE_MS = 2_000;
const TIMEOUT_EXIT_CODE = 124;

interface SlopRun {
  stdout: string;
  exitCode: number;
}

function runSlop(projectRoot: string, file: string): Promise<SlopRun> {
  return new Promise((resolvePromise) => {
    const child = spawn("uv", ["run", "--no-active", "sloperator.py", file], {
      cwd: projectRoot,
      stdio: ["ignore", "pipe", "ignore"],
      detached: true,
    });

    let stdout = "";
    let timedOut = false;
    let settled = false;
    let timer: ReturnType<typeof setTimeout> | undefined;
    let graceTimer: ReturnType<typeof setTimeout> | undefined;

    const finish = (exitCode: number) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      if (graceTimer !== undefined) clearTimeout(graceTimer);
      resolvePromise({ stdout, exitCode });
    };

    timer = setTimeout(() => {
      timedOut = true;
      try {
        if (child.pid !== undefined) process.kill(-child.pid, "SIGKILL");
        else child.kill("SIGKILL");
      } catch {
        child.kill("SIGKILL");
      }
      graceTimer = setTimeout(() => finish(TIMEOUT_EXIT_CODE), KILL_GRACE_MS);
    }, TIMEOUT_MS);

    child.stdout?.setEncoding("utf8");
    child.stdout?.on("data", (chunk: string) => {
      stdout += chunk;
    });

    child.on("error", () => finish(-1));
    child.on("close", (code: number | null) => {
      finish(timedOut ? TIMEOUT_EXIT_CODE : (code ?? -1));
    });
  });
}

export default Plugin.define({
  id: "sloperator.example-outputs",
  setup: async (ctx) => {
    const projectRoot = ctx.location.project.directory;

    await ctx.tool.transform((tools) => {
      tools.add({
        name: "example_outputs",
        description:
          "Run every examples/*.slop program and return each filename, exit code, and first output line.",
        input: {
          type: "object",
          properties: {},
          additionalProperties: false,
        },
        options: { codemode: false },
        execute: async () => {
          const entries = await readdir(join(projectRoot, "examples"), {
            withFileTypes: true,
          });
          const files = entries
            .filter((entry) => entry.isFile() && entry.name.endsWith(".slop"))
            .map((entry) => entry.name)
            .sort();

          const examples = [];
          for (const name of files) {
            const result = await runSlop(projectRoot, join("examples", name));
            examples.push({
              name,
              exitCode: result.exitCode,
              firstLine: result.stdout.split(/\r?\n/, 1)[0],
            });
          }

          return { content: JSON.stringify({ examples }, null, 2) };
        },
      });
    });
  },
});
