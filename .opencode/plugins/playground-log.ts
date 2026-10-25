import { appendFile, mkdir } from "node:fs/promises";
import { dirname, join } from "node:path";
import { Plugin } from "@opencode/plugin";

export default Plugin.define({
  id: "bootdev.playground-log",
  setup: async (ctx) => {
    const logPath = join(ctx.location.project.directory, "logs", "plugin-playground.log");

    await ctx.shell.hook("create.before", async (event) => {
      if (!event.command.includes("playground/server.py")) return;

      try {
        await mkdir(dirname(logPath), { recursive: true });
        await appendFile(logPath, `playground shell request: ${event.command}\n`);
      } catch (error) {
        console.error("could not write playground log:", error);
      }
    });
  },
});
