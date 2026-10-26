import { appendFile, mkdir } from "node:fs/promises"
import { join } from "node:path"
import { Plugin } from "@opencode/plugin"

export default Plugin.define({
  id: "edit-log",
  async setup(ctx) {
    const logDirectory = join(ctx.location.project.directory, "logs")
    const logPath = join(logDirectory, "plugin-tools.log")

    await ctx.tool.hook("execute.after", async (event) => {
      if (
        event.status !== "completed" ||
        !["edit", "write", "patch"].includes(event.tool)
      ) {
        return
      }

      try {
        await mkdir(logDirectory, { recursive: true })
        await appendFile(
          logPath,
          `${JSON.stringify({ tool: event.tool, status: "completed" })}\n`,
          "utf8",
        )
      } catch (error) {
        console.error("Failed to append to logs/plugin-tools.log:", error)
      }
    })
  },
})
