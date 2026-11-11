<div align="center">
  <img src="https://raw.githubusercontent.com/kalil0321/reverse-api-engineer/main/assets/reverse-api-banner.jpg" alt="Reverse API Engineer Banner">
  <br><br>
  <a href="https://pypi.org/project/reverse-api-engineer/"><img src="https://img.shields.io/pypi/v/reverse-api-engineer?style=flat-square&color=red" alt="PyPI"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.11+-red?style=flat-square" alt="Python"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-red?style=flat-square" alt="License"></a>
</div>

<p align="center">
CLI tool that captures browser traffic and generates Python, JavaScript, or TypeScript API clients with an AI agent.<br>
No more manual reverse engineering—just browse, capture, and get clean API code.
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/kalil0321/reverse-api-engineer/main/assets/rae-autoscout.gif" alt="Agent Mode Demo">
  <br>
  <em>Agent mode</em>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/kalil0321/reverse-api-engineer/main/assets/reverse-api-engineer.gif" alt="Manual Mode Demo">
  <br>
  <em>Manual mode</em>
</p>

## Checkout status

This fork currently declares version **0.9.0** in [pyproject.toml](pyproject.toml). The source includes four engineering SDK backends and a `reverse-api-mcp` entry point. The PyPI installation commands below install the published distribution; use the [source setup](#setup) to run this checkout's implementation.

This documentation describes the local source. Live browser capture, provider authentication, generated-client correctness, and MCP client interoperability have not been verified by the documentation review. [CHANGELOG.md](CHANGELOG.md) records historical releases, not a current runtime contract; for example, the current JSON schema version is the integer `1`, despite the older `v2` release-note wording.

## Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Modes](#-usage-modes)
  - [Manual Mode](#manual-mode)
  - [Engineer Mode](#engineer-mode)
  - [Agent Mode](#agent-mode)
  - [Collector Mode](#collector-mode)
- [Configuration](#-configuration)
  - [Model Selection](#model-selection)
  - [Agent Configuration](#agent-configuration)
  - [SDK Selection](#sdk-selection)
- [CLI Commands](#-cli-commands)
- [MCP Server](#mcp-server)
- [Project Structure](#project-structure)
- [Examples](#-examples)
- [Development](#-development)
- [Contributing](#-contributing)

## ✨ Features

- 🌐 **Browser Automation**: Built on Playwright with stealth mode for realistic browsing
- 🤖 **Autonomous Agent Mode**: Fully automated browser interaction using AI agents via MCP (Playwright MCP or Chrome DevTools MCP)
- 📊 **HAR Recording**: Manual mode records browser traffic in HTTP Archive format
- 🧠 **AI-Powered Generation**: Uses the selected SDK/model to analyze traffic and generate API clients
- 🔍 **Collector Mode**: Data collection with automatic JSON/CSV export
- 🔌 **Multi-SDK Support**: Claude Agent SDK, OpenCode HTTP API, optional GitHub Copilot SDK, and Cursor SDK bridge
- 💻 **Interactive CLI**: Minimalist terminal interface with mode cycling (Shift+Tab)
- 📦 **Client Generation**: Prompts request error handling, type hints, and documentation; review and test generated clients before use
- 💾 **Session History**: All runs saved locally with full message logs
- 💰 **Cost Tracking**: Detailed token usage and cost estimation with cache support

### Limitations

- The selected engineering backend can execute code and write files locally; monitor its output
- Some websites employ advanced bot-detection that may limit capture or require manual interaction

## 🚀 Installation

### Using uv (recommended)
```bash
uv tool install reverse-api-engineer
```

### Using pip
```bash
pip install reverse-api-engineer
```

### Post-installation
Install Playwright browsers:
```bash
uv tool run --from reverse-api-engineer playwright install chromium
```

For a pip installation, run `python -m playwright install chromium` in the same Python environment. For a source checkout, use `uv run playwright install chromium`. Agent mode also invokes browser MCP packages through `npx`, so it needs Node.js/npm and may download packages on first use. Configure authentication for your chosen [SDK](#sdk-selection) before capturing or engineering.

### Pricing

Reverse API Engineer includes built-in pricing for the most common models (Claude 4.6, Gemini 3, GPT-4.1/5). Cost tracking uses a 2-tier fallback:
1. **Local pricing table** — built-in pricing for common models
2. **Default fallback** — Claude Sonnet 4.6 pricing for unknown models

If `litellm` is independently installed in your environment, an extended pricing lookup is auto-detected for 100+ additional models. We no longer ship a `[pricing]` extra; install `litellm` directly if you need that coverage.

## 🚀 Quick Start

Launch the interactive CLI:
```bash
reverse-api-engineer
```

The CLI has four modes (cycle with **Shift+Tab**):
- **manual**: Browser capture + AI generation
- **engineer**: Re-process existing captures
- **agent** (initial mode): Autonomous AI browser agent (default provider: `auto`, with MCP-based browser + real-time reverse engineering)
- **collector**: AI-powered web data collection (very minimalist version for now)

Example workflow:
```bash
$ reverse-api-engineer
# Select manual mode with Shift+Tab first
> fetch all apple jobs from their careers page

# Browser opens, navigate and interact
# Close browser when done
# AI generates an API client for review

# Scripts saved to: ./scripts/apple_jobs_api/
```

## 📖 Usage Modes

### Manual Mode

Full pipeline with manual browser interaction:

1. Start the CLI: `reverse-api-engineer`, then select **manual** with Shift+Tab
2. Enter task description (e.g., "Fetch Apple job listings")
3. Optionally provide starting URL
4. Browse and interact with the website
5. Close browser when done
6. AI automatically generates the API client

**Output locations:**
- `~/.reverse-api/runs/scripts/{run_id}/` (permanent storage)
- `./scripts/{descriptive_name}/` (synced live by default; copied at completion in manual/engineer mode when sync is disabled)
- `~/.reverse-api/runs/har/{run_id}/recording.har` (manual capture)

`output_dir` / `--output-dir` changes the HAR and script storage root; config and history remain in `~/.reverse-api/`. Use `manual --no-engineer` for capture only. HARs, message logs, and generated code can contain credentials or captured content; review them before sharing.

### Engineer Mode

Re-run AI generation on a previous capture:
```bash
# Switch to engineer mode (Shift+Tab) and enter run_id
# Or use command line:
reverse-api-engineer engineer <run_id>
```

### Agent Mode

Fully automated browser interaction using AI agents:

1. Start CLI and switch to agent mode (Shift+Tab)
2. Enter task description (e.g., "Click on the first job listing")
3. Include the destination in your task, or pass `--url` with the `agent` subcommand
4. Agent automatically navigates and interacts
5. The browser MCP provider captures or exposes network traffic (a HAR file is not guaranteed for every provider)
6. API client generated automatically

**Agent Provider Options:**

- **auto** (default): Uses `rae-playwright-mcp` browser automation with the selected SDK. Combines browser control and real-time reverse engineering in a single workflow.
- **chrome-mcp**: Uses [Chrome DevTools MCP](https://www.npmjs.com/package/chrome-devtools-mcp) to drive your real Chrome browser (with existing sessions, cookies, and auth). The CLI setup guidance specifies Chrome 146+ and Node.js 20.19+.

Change agent provider in `/settings` → "agent provider".

### Collector Mode

Web data collection using Claude Agent SDK:

1. Start CLI and switch to collector mode (Shift+Tab)
2. Enter a natural language prompt describing the data to collect (e.g., "Find 3 JS frameworks")
3. The agent uses WebFetch, WebSearch, and file tools to autonomously collect structured data
4. Data is automatically exported to JSON and CSV formats

**Output location:**
- `./collected/{folder_name}/` under the current working directory

The current Collector implementation does not create a second copy under `~/.reverse-api/runs/collected/`. Its `output_dir` argument controls message-log storage, but collection artifacts always use the current working directory via `get_collected_dir()`.

**Output files:**
- `items.jsonl` - Intermediate records written by the agent
- `data.json` - Collected data in JSON format
- `data.csv` - Collected data in CSV format
- `README.md` - Collection metadata and schema documentation

**Model Configuration:**
Collector mode uses the `collector_model` setting (default: `claude-sonnet-4-6`). This can be configured in `~/.reverse-api/config.json`.

Example workflow:
```bash
$ reverse-api-engineer
# Select collector mode with Shift+Tab first
> Find 3 JS frameworks

# Agent autonomously searches and collects data
# Data saved to: ./collected/js_frameworks/
```

## 🔧 Configuration

Settings stored in `~/.reverse-api/config.json`; defaults from [config.py](src/reverse_api/config.py):
```json
{
  "agent_provider": "auto",
  "claude_code_model": "claude-sonnet-4-6",
  "collector_model": "claude-sonnet-4-6",
  "cursor_model": "composer-2",
  "cursor_web_search": true,
  "cursor_setting_sources": null,
  "copilot_model": "gpt-5",
  "opencode_model": "claude-opus-4-6",
  "opencode_provider": "anthropic",
  "output_dir": null,
  "output_language": "python",
  "real_time_sync": true,
  "sdk": "claude"
}
```

### Model Selection

Choose from Claude 4.6 models for API generation:
- **Sonnet 4.6** (default): Balanced performance and cost
- **Opus 4.6**: Maximum capability for complex APIs
- **Haiku 4.5**: Fastest and most economical

Change in `/settings` or via CLI:
```bash
reverse-api-engineer manual --model claude-sonnet-4-6
```

If you use Opencode, look at the [models](https://models.dev).

### Agent Configuration

Configure AI agents for autonomous browser automation.

**Agent Providers:**
- **auto** (default): Playwright MCP browser automation with real-time reverse engineering. Uses the selected SDK with browser MCP tools. Combines browser control and API reverse engineering in a single unified workflow. Works with Claude (default), OpenCode, Copilot, or Cursor.
- **chrome-mcp**: Drives your real Chrome browser via [Chrome DevTools MCP](https://www.npmjs.com/package/chrome-devtools-mcp). Useful when you need existing sessions, cookies, or auth. The CLI setup guidance specifies Chrome 146+ and Node.js 20.19+; enable auto-connect at `chrome://inspect/#remote-debugging`.

`agent --headless` requests a hidden browser. With `chrome-mcp`, it removes `--autoConnect` and starts a separate headless browser instead of using an existing Chrome session.

The agent's reasoning model is the same as the SDK model — see [Model Selection](#model-selection).

Change in `/settings` → "agent provider"

### SDK Selection

- **Claude** (`sdk: "claude"`, default): Uses `claude-agent-sdk` and its Claude Code runtime/authentication. Default model: `claude-sonnet-4-6`.
- **OpenCode** (`sdk: "opencode"`): Calls a local HTTP server at `http://127.0.0.1:4096`; start it with `opencode serve` and configure the provider there. Default model: `claude-opus-4-6`, provider: `anthropic`. If server authentication is enabled, export `OPENCODE_SERVER_PASSWORD` and optionally `OPENCODE_SERVER_USERNAME` (default `opencode`).
- **Copilot** (`sdk: "copilot"`): Requires the optional Python SDK (`uv sync --extra copilot` from source, or `pip install 'reverse-api-engineer[copilot]'`) and an authenticated Copilot CLI. Default model: `gpt-5`.
- **Cursor** (`sdk: "cursor"`): Uses the bundled Node bridge in `src/reverse_api/cursor_bridge/`. Export `CURSOR_API_KEY` through your environment and make Node.js/npm available. On first use, the bridge runs `npm install --no-fund --no-audit` in its package directory if `@cursor/sdk` is missing, so that directory must be writable. Default model: `composer-2`.

`cursor_web_search: true` loads Cursor's project, user, plugins, and team setting sources; `false` loads project and user only. A nonempty `cursor_setting_sources` array overrides that choice. Collector mode always uses Claude and `collector_model`, regardless of `sdk`. Model IDs here are configured defaults, not a guarantee of current provider availability.

Change in `/settings` or edit `config.json` directly.

### Output Language

Control the programming language of generated API clients:
- **python** (default): Generate Python API clients
- **javascript**: Generate JavaScript API clients
- **typescript**: Generate TypeScript API clients

Change in `/settings` → "Output Language" or edit `config.json`:
```json
{
  "output_language": "typescript"
}
```

### Real-time Sync

Enable or disable real-time file synchronization during engineering sessions:
- **Enabled** (default): Files in the permanent run directory are copied to `./scripts/{descriptive_name}/` as they are generated
- **Disabled**: The agent still writes to the permanent run directory. Manual/engineer mode copies top-level output files locally at completion; agent mode does not make that final copy

When enabled, you can see files appear in real-time as the AI generates them. This is useful for monitoring progress and debugging.

Change in `/settings` → "Real-time Sync" or edit `config.json`:
```json
{
  "real_time_sync": false
}
```

## 💻 CLI Commands

Use these slash commands while in the CLI:
- `/settings` - Configure model, agent, SDK, and output directory
- `/history` - View past runs with costs
- `/messages <run_id>` - View detailed message logs
- `/help` - Show all commands
- `/exit` - Quit

### Scripted / Agent Usage

The CLI exposes `manual`, `agent`, `engineer`, `list`, `show`, and `run`. Collector is available through the interactive mode selector and MCP tool, not a `collector` subcommand. Running without a subcommand requires a TTY.

`agent` and `engineer` accept `--no-interactive` and `--json`; `list` and `show` accept `--json`; `run` accepts `--no-interactive` but not `--json`. Check `<command> --help` for each command's flags. `manual` remains interactive.

For `agent` and `engineer`, when `--json` is set: stdout contains exactly one JSON document (the final result), Rich logs and progress are diverted to stderr, and the process exits with a stable code.

```bash
# Run an autonomous agent capture and get a single JSON result on stdout
reverse-api-engineer agent \
  --prompt "capture the public jobs api" \
  --url https://example.com/jobs \
  --json | jq

# List runs / inspect a run as JSON (empty history -> [])
reverse-api-engineer list --json
reverse-api-engineer show <run_id> --json

# Re-engineer a capture with a replacement goal, without follow-up prompts
reverse-api-engineer engineer <run_id> --fresh --prompt "add pagination to the client" --json

# Inspect the JSON contract version
reverse-api-engineer --json-schema-version

# Run a generated Python script non-interactively
#   --no-interactive : never open the script-picker / install confirm
#   --auto-install   : install missing deps on retry without asking
reverse-api-engineer run <run_id> --file api_client.py \
  --no-interactive --auto-install -- --org acme
```

`agent --dry-run --prompt "capture the public jobs API"` emits JSON preflight checks without launching a browser or SDK. It checks configuration, environment-variable presence, Node/npx availability, and output-directory writability. It can create the output directory and writes then removes a probe file; it does not verify credentials, network access, or a successful capture.

#### `agent --json` output schema

| Field            | Type                | Notes                                                                  |
|------------------|---------------------|------------------------------------------------------------------------|
| `schema_version` | `int`               | Currently `1`. Bumped on breaking changes.                             |
| `status`         | `"ok"` \| `"error"` | Top-level result.                                                      |
| `run_id`         | `string` \| `null`  | Stable id for follow-up `show` / `engineer` / `run` calls.             |
| `prompt`         | `string`            | The prompt that was passed in.                                         |
| `url`            | `string` \| `null`  | Optional starting URL.                                                 |
| `mode`           | `string` \| `null`  | Provider used (`"auto"` for Playwright MCP, `"chrome-mcp"`).           |
| `har_path`       | `string` \| `null`  | Path to an existing HAR (`recording.har`), otherwise `null`.                   |
| `script_path`    | `string` \| `null`  | Reported client path when engineering ran; inspect the artifact before use.    |
| `usage`          | `object`            | Available normalized keys: `input_tokens`, `output_tokens`, `cache_read_tokens`, `cache_write_tokens`, `total_cost_usd`; SDK fields under `raw`. Empty when unavailable.|
| `error`          | `string` \| `null`  | Human-readable error message when `status == "error"`.                 |

`error_kind` is also present: `null` on success, otherwise one of `misuse`, `config_invalid`, `permission_denied`, `network`, `engine_failure`, `interrupted`, or `unknown`. `engineer --json` uses the same status/error/usage fields, adds `fresh`, and omits `url`, `mode`, and `har_path`.

#### Exit codes

| Code | Meaning                                                                   |
|------|---------------------------------------------------------------------------|
| `0`  | Success.                                                                  |
| `1`  | Runtime error (capture or engineering failed; details in `error`).        |
| `2`  | Misuse — required arg missing under `--no-interactive` / `--json`.        |

These result codes describe `agent --json` and `engineer --json`; Click argument-parsing errors can still print text to stderr. `agent --dry-run` returns `0` without check errors and `1` with any check error, including missing input.

`run` executes Python files in a shared environment under the configured run root (`~/.reverse-api/runs/.venv` by default), installing requirements as needed. JavaScript/TypeScript clients need their own runtime. For `run`, the exit code is the underlying script's return code on success, or `1` if no script was found, or non-zero if `--no-interactive` would otherwise have to prompt.

## MCP Server

The source defines the `reverse-api-mcp` console script in [pyproject.toml](pyproject.toml), implemented by [mcp_server.py](src/reverse_api/mcp_server.py). After source setup, a local MCP client can launch it over stdio with:

```json
{
  "mcpServers": {
    "reverse-api-engineer": {
      "command": "uv",
      "args": ["run", "--directory", "/absolute/path/to/reverse-api-engineer", "reverse-api-mcp"]
    }
  }
}
```

Replace the checkout path and make the selected SDK's authentication available to the child process. The server registers:

- `capture_api(prompt, url=None)`: calls the integrated capture/engineering workflow with `headless=True`. It uses the configured SDK but the helper's default `auto` provider, not the configured `agent_provider`.
- `collect_data(prompt)`: calls the Claude Collector workflow.

Both tools return text, not the CLI JSON schema. This is a thin wrapper: capture leaves the helper's `interactive=True` default in place, and workflow console output is not redirected away from stdio. Unattended operation and clean MCP transport output are therefore not established. At the 2026-11-11 documentation review, the local working tree contained uncommitted result/error-handling changes in `cli.py` and `mcp_server.py`; those changes are separate from this documentation update and are not release guarantees.

## Project Structure

- `src/reverse_api/`: CLI, configuration, session/message persistence, browser capture, SDK backends, Collector, and terminal UI.
- `src/reverse_api/prompts/`: runtime prompt templates; changing them changes agent behavior.
- `src/reverse_api/cursor_bridge/`: Node bridge and npm dependency lockfile.
- `tests/`: pytest tests using fixtures and SDK/subprocess mocks.
- `examples/`: checked-in generated clients for Apple, Ashby, AutoScout24, IKEA, Mintlify, and Uber. These are reference artifacts; their external APIs have not been revalidated.
- `assets/`: README illustrations and demos.
- `scripts/clean_build.sh`: build helper. Other files in `scripts/` are ignored generated/local content, not maintained source.
- `pyproject.toml` / `uv.lock`: Python package metadata, dependencies, tooling, and lockfile.

Runtime config and history live in `~/.reverse-api/`; captures, scripts, and logs are runtime data, not repository documentation.

## 💡 Examples

### Example: Reverse Engineering a Job Board API

```bash
$ reverse-api-engineer
# Select manual mode with Shift+Tab first
> fetch all apple jobs from their careers page

# Browser opens, you navigate and interact
# Close browser when done

# AI generates:
# - api_client.py (full API implementation)
# - README.md (documentation)
# - example_usage.py (usage examples)

# Scripts copied to: ./scripts/apple_jobs_api/
```

The generation prompts request:
- Authentication handling
- Clean function interfaces
- Type hints and docstrings
- Error handling
- Code that should be reviewed and tested against the intended API

## 🛠️ Development

### Setup
```bash
git clone https://github.com/ljen/reverse-api-engineer.git
cd reverse-api-engineer
uv sync --locked
uv run playwright install chromium
```

Python 3.11+ is supported by the package metadata; `.python-version` selects Python 3.13 for local uv development. `uv sync` installs the dev dependency group by default. See [CONTRIBUTING.md](CONTRIBUTING.md) for tests and tooling.

### Run
```bash
uv run reverse-api-engineer
```

### Build
```bash
uv build
```

The optional `./scripts/clean_build.sh` also removes `dist/`, `build/`, egg metadata, and Python caches recursively before building (including caches in a local virtual environment). See [RELEASING.md](RELEASING.md) for the manual release workflow.

## 🔐 Requirements

- Python 3.11+
- A configured/authenticated engineering SDK (see [SDK Selection](#sdk-selection))
- Playwright Chromium for manual capture; Node.js/npm for MCP-based agent capture
- Provider-specific runtime and browser prerequisites described above

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
