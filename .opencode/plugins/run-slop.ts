import { spawn } from "node:child_process";
import { isAbsolute, resolve } from "node:path";
import { Plugin } from "@opencode/plugin";

/** SlopLang programs can loop forever (`ralph`), so bound every run. */
const TIMEOUT_MS = 30_000;
/** Grace period after a timeout kill before reporting anyway. */
const KILL_GRACE_MS = 2_000;
/** Exit code reported when a run is killed for exceeding the timeout. */
const TIMEOUT_EXIT_CODE = 124;

interface SlopRun {
  stdout: string;
  stderr: string;
  exitCode: number;
}

/**
 * Runs `uv run --no-active sloperator.py <file>` from the project root.
 * `--no-active` skips the active virtualenv, so uv resolves the project
 * environment from the working directory instead of `VIRTUAL_ENV`.
 */
function runSlop(projectRoot: string, file: string): Promise<SlopRun> {
  return new Promise((resolvePromise) => {
    const child = spawn("uv", ["run", "--no-active", "sloperator.py", file], {
      cwd: projectRoot,
      stdio: ["ignore", "pipe", "pipe"],
      // Give uv its own process group so a timeout can kill it (detached) and
      // anything it spawns. Killing only uv can leave a child holding our
      // pipes open, in which case "close" never fires and we would hang.
      detached: true,
    });

    let stdout = "";
    let stderr = "";
    let timedOut = false;
    let settled = false;
    let timer: ReturnType<typeof setTimeout> | undefined;
    let graceTimer: ReturnType<typeof setTimeout> | undefined;

    const finish = (result: SlopRun) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      if (graceTimer !== undefined) clearTimeout(graceTimer);
      resolvePromise(result);
    };

    timer = setTimeout(() => {
      timedOut = true;
      stderr += `sloperator timed out after ${TIMEOUT_MS}ms and was killed\n`;
      try {
        if (child.pid !== undefined) process.kill(-child.pid, "SIGKILL");
        else child.kill("SIGKILL");
      } catch {
        child.kill("SIGKILL");
      }
      graceTimer = setTimeout(() => finish({ stdout, stderr, exitCode: TIMEOUT_EXIT_CODE }), KILL_GRACE_MS);
    }, TIMEOUT_MS);

    child.stdout?.setEncoding("utf8");
    child.stderr?.setEncoding("utf8");
    child.stdout?.on("data", (chunk: string) => {
      stdout += chunk;
    });
    child.stderr?.on("data", (chunk: string) => {
      stderr += chunk;
    });

    child.on("error", (error: Error) => {
      finish({ stdout, stderr: stderr + error.message, exitCode: -1 });
    });

    child.on("close", (code: number | null) => {
      finish({ stdout, stderr, exitCode: timedOut ? TIMEOUT_EXIT_CODE : (code ?? -1) });
    });
  });
}

export default Plugin.define({
  id: "sloperator.run-slop",
  setup: async (ctx) => {
    const projectRoot = ctx.location.project.directory;

    await ctx.tool.transform((tools) => {
      tools.add({
        name: "run_slop",
        description:
          "Run a SlopLang (.slop) program with the Sloperator interpreter. " +
          "Returns JSON with the program's stdout, stderr, and exit code. " +
          "Runs are killed after 30 seconds.",
        input: {
          type: "object",
          properties: {
            path: {
              type: "string",
              description:
                "Path to the .slop file, resolved against the project root when relative",
            },
          },
          required: ["path"],
          additionalProperties: false,
        },
        options: { codemode: false },
        execute: async (input) => {
          const { path } = input as { path: string };
          const file = isAbsolute(path) ? path : resolve(projectRoot, path);
          const result = await runSlop(projectRoot, file);
          return { content: JSON.stringify(result, null, 2) };
        },
      });
    });
  },
});
