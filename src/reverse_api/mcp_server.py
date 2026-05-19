from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Reverse API Engineer")

def _init():
    from reverse_api.cli import run_auto_capture, run_collector
    return run_auto_capture, run_collector

@mcp.tool()
def capture_api(prompt: str, url: str | None = None) -> str:
    """Capture browser traffic and reverse engineer APIs autonomously.

    Args:
        prompt: Instruction for the autonomous agent.
        url: Optional starting URL.
    """
    run_auto_capture, _ = _init()
    result = run_auto_capture(prompt=prompt, url=url, headless=True)
    if result and not result.get("error"):
        return f"Successfully generated API client at {result.get('script_path')}"

    error_msg = result.get("error") if result else "Unknown error"
    return f"Failed to generate API client: {error_msg}"

@mcp.tool()
def collect_data(prompt: str) -> str:
    """Run AI-powered data collection with Collector class.

    Args:
        prompt: Instruction for what data to collect.
    """
    _, run_collector = _init()
    result = run_collector(prompt=prompt)
    if result and not result.get("error"):
        return f"Successfully collected data at {result.get('output_path')}"

    error_msg = result.get("error") if result else "Unknown error"
    return f"Failed to collect data: {error_msg}"

def main():
    mcp.run()

if __name__ == "__main__":
    main()
