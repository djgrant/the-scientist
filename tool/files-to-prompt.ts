import { tool } from "@opencode-ai/plugin"

export default tool({
  description: `Generate a prompt containing file contents from the repository using files-to-prompt CLI.
  
Use this tool after you have identified the relevant files the user wants to include in their prompt.
The tool will format the files and either copy to clipboard or write to a file.

Prerequisites: files-to-prompt must be installed (pip install files-to-prompt)`,

  args: {
    paths: tool.schema
      .array(tool.schema.string())
      .describe("List of file or directory paths to include in the prompt"),
    format: tool.schema
      .enum(["cxml", "markdown", "plain"])
      .default("cxml")
      .describe("Output format: cxml (Claude XML), markdown (fenced code blocks), or plain (--- separators)"),
    output: tool.schema
      .enum(["clipboard", "file"])
      .default("clipboard")
      .describe("Where to send output: clipboard or file"),
    outputPath: tool.schema
      .string()
      .optional()
      .describe("File path for output when output='file'. Defaults to prompts/{timestamp}.xml in the current project"),
    extensions: tool.schema
      .array(tool.schema.string())
      .optional()
      .describe("Only include files with these extensions (e.g. ['ts', 'js'])"),
    ignore: tool.schema
      .array(tool.schema.string())
      .optional()
      .describe("Patterns to ignore (e.g. ['*.test.ts', 'node_modules'])"),
  },

  async execute(args) {
    const { paths, format, output, outputPath, extensions, ignore } = args

    if (!paths || paths.length === 0) {
      return "Error: No paths provided. Please specify files or directories to include."
    }

    // Build the files-to-prompt command
    const cmdParts = ["files-to-prompt"]

    // Add paths
    cmdParts.push(...paths.map((p) => `"${p}"`))

    // Add format flag
    if (format === "cxml") {
      cmdParts.push("--cxml")
    } else if (format === "markdown") {
      cmdParts.push("--markdown")
    }
    // plain format is the default, no flag needed

    // Add extension filters
    if (extensions && extensions.length > 0) {
      for (const ext of extensions) {
        cmdParts.push(`-e ${ext}`)
      }
    }

    // Add ignore patterns
    if (ignore && ignore.length > 0) {
      for (const pattern of ignore) {
        cmdParts.push(`--ignore "${pattern}"`)
      }
    }

    const filesToPromptCmd = cmdParts.join(" ")

    // Determine output destination
    let finalCmd: string
    let outputFile: string | null = null

    if (output === "file") {
      // Generate default path if not provided
      const timestamp = new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19)
      const ext = format === "markdown" ? "md" : format === "cxml" ? "xml" : "txt"
      outputFile = outputPath || `prompts/${timestamp}.${ext}`

      // Ensure prompts directory exists
      finalCmd = `mkdir -p "$(dirname "${outputFile}")" && ${filesToPromptCmd} -o "${outputFile}"`
    } else {
      // Copy to clipboard - cross-platform
      const clipboardCmd = await getClipboardCommand()
      if (!clipboardCmd) {
        return "Error: No clipboard utility found. Install xclip (Linux), or use --output file instead."
      }
      finalCmd = `${filesToPromptCmd} | ${clipboardCmd}`
    }

    // Execute the command
    try {
      const result = await Bun.$`bash -c ${finalCmd}`.text()

      // Build success message
      const fileCount = paths.length
      const formatName =
        format === "cxml" ? "Claude XML" : format === "markdown" ? "Markdown" : "plain text"

      if (output === "clipboard") {
        return `Successfully generated prompt in ${formatName} format from ${fileCount} path(s) and copied to clipboard.

Paths included:
${paths.map((p) => `  - ${p}`).join("\n")}

The prompt is now in your clipboard, ready to paste.`
      } else {
        return `Successfully generated prompt in ${formatName} format from ${fileCount} path(s).

Paths included:
${paths.map((p) => `  - ${p}`).join("\n")}

Output written to: ${outputFile}`
      }
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error)

      // Check for common issues
      if (errorMsg.includes("command not found") || errorMsg.includes("not found")) {
        return `Error: files-to-prompt is not installed.

Install it with: pip install files-to-prompt

Then try again.`
      }

      return `Error executing files-to-prompt: ${errorMsg}`
    }
  },
})

async function getClipboardCommand(): Promise<string | null> {
  // Try each clipboard utility
  const utilities = [
    { cmd: "pbcopy", check: "which pbcopy" }, // macOS
    { cmd: "xclip -selection clipboard", check: "which xclip" }, // Linux (X11)
    { cmd: "xsel --clipboard --input", check: "which xsel" }, // Linux (X11 alternative)
    { cmd: "wl-copy", check: "which wl-copy" }, // Linux (Wayland)
    { cmd: "clip.exe", check: "which clip.exe" }, // WSL
  ]

  for (const util of utilities) {
    try {
      await Bun.$`bash -c ${util.check}`.quiet()
      return util.cmd
    } catch {
      // Utility not available, try next
    }
  }

  return null
}
