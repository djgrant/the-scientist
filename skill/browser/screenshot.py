#!/usr/bin/env python3
"""
Browser interaction tool for web applications.

This tool maintains a persistent browser session via a Unix socket server,
allowing fast interactions without re-launching the browser each time.

Usage:
    python screenshot.py [command] [args...]

Commands:
    start                           Start the browser server (run first, blocks)
    stop                            Stop the browser server
    status                          Check if server is running
    
    screenshot [--wait N]           Take a screenshot
    click <selector>                Click an element  
    type <selector> <text>          Type text into an element
    press <key>                     Press a key (Enter, Tab, etc.)
    hover <selector>                Hover over an element
    scroll <direction> [amount]     Scroll up/down/left/right
    wait <seconds>                  Wait for specified seconds
    eval <js_code>                  Evaluate JavaScript in the page
    text <selector>                 Get text content of an element
    list <selector>                 List all matching elements
    goto <url>                      Navigate to a URL
    reload                          Reload the page

Examples:
    # First terminal: start the server
    python screenshot.py start
    
    # Second terminal: interact
    python screenshot.py screenshot --wait 3
    python screenshot.py click ".lesson-item"
    python screenshot.py type "input" "hello"
    python screenshot.py press Enter

Environment:
    BROWSER_URL     Base URL (default: http://localhost:5173)
    BROWSER_WIDTH   Viewport width (default: 1280)  
    BROWSER_HEIGHT  Viewport height (default: 800)

Screenshots are saved to .screenshots/screenshot.png (gitignored).
"""

import argparse
import json
import os
import socket
import sys
import time
import signal
from pathlib import Path

# Configuration
SCREENSHOTS_DIR = Path.cwd() / ".screenshots"
SOCKET_PATH = SCREENSHOTS_DIR / "browser.sock"
PID_FILE = SCREENSHOTS_DIR / "browser.pid"
DEFAULT_URL = os.environ.get("BROWSER_URL", "http://localhost:5173")
VIEWPORT_WIDTH = int(os.environ.get("BROWSER_WIDTH", "1280"))
VIEWPORT_HEIGHT = int(os.environ.get("BROWSER_HEIGHT", "800"))


def ensure_screenshots_dir():
    """Ensure the screenshots directory exists."""
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


def send_command(cmd: dict) -> dict:
    """Send a command to the browser server."""
    if not SOCKET_PATH.exists():
        print("Error: Browser server not running. Start it with: python screenshot.py start", file=sys.stderr)
        sys.exit(1)
    
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        sock.connect(str(SOCKET_PATH))
        sock.sendall(json.dumps(cmd).encode() + b'\n')
        
        # Read response
        response = b''
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk
            if b'\n' in response:
                break
        
        return json.loads(response.decode().strip())
    except ConnectionRefusedError:
        print("Error: Browser server not responding. Try restarting it.", file=sys.stderr)
        sys.exit(1)
    finally:
        sock.close()


def run_server():
    """Run the browser server."""
    from playwright.sync_api import sync_playwright
    
    ensure_screenshots_dir()
    
    # Clean up old socket
    if SOCKET_PATH.exists():
        SOCKET_PATH.unlink()
    
    # Write PID file
    PID_FILE.write_text(str(os.getpid()))
    
    print(f"Starting browser server...")
    print(f"Socket: {SOCKET_PATH}")
    print(f"URL: {DEFAULT_URL}")
    print(f"Viewport: {VIEWPORT_WIDTH}x{VIEWPORT_HEIGHT}")
    print()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
            device_scale_factor=1,
        )
        page = context.new_page()
        
        # Navigate to initial page
        print(f"Navigating to {DEFAULT_URL}...")
        page.goto(DEFAULT_URL, wait_until="domcontentloaded", timeout=30000)
        print("Page loaded.")
        
        # Create Unix socket server
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(str(SOCKET_PATH))
        server.listen(1)
        server.settimeout(1.0)  # Allow periodic checks
        
        def cleanup(signum=None, frame=None):
            print("\nShutting down...")
            server.close()
            if SOCKET_PATH.exists():
                SOCKET_PATH.unlink()
            if PID_FILE.exists():
                PID_FILE.unlink()
            browser.close()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, cleanup)
        signal.signal(signal.SIGTERM, cleanup)
        
        print("Server ready. Press Ctrl+C to stop.\n")
        
        while True:
            try:
                conn, addr = server.accept()
            except socket.timeout:
                continue
            except Exception as e:
                if "Bad file descriptor" in str(e):
                    break
                continue
            
            try:
                data = conn.recv(4096).decode().strip()
                if not data:
                    continue
                
                cmd = json.loads(data)
                result = handle_command(page, cmd)
                conn.sendall(json.dumps(result).encode() + b'\n')
            except Exception as e:
                conn.sendall(json.dumps({"error": str(e)}).encode() + b'\n')
            finally:
                conn.close()
        
        cleanup()


def handle_command(page, cmd: dict) -> dict:
    """Handle a command from the client."""
    action = cmd.get("action")
    output_path = str(SCREENSHOTS_DIR / "screenshot.png")
    
    try:
        if action == "screenshot":
            wait = cmd.get("wait", 0)
            if wait > 0:
                page.wait_for_timeout(int(wait * 1000))
            page.screenshot(path=output_path, full_page=cmd.get("full_page", False))
            return {"ok": True, "path": output_path}
        
        elif action == "click":
            page.click(cmd["selector"], timeout=5000)
            page.wait_for_timeout(300)
            page.screenshot(path=output_path)
            return {"ok": True, "path": output_path}
        
        elif action == "type":
            page.fill(cmd["selector"], cmd["text"], timeout=5000)
            page.wait_for_timeout(200)
            page.screenshot(path=output_path)
            return {"ok": True, "path": output_path}
        
        elif action == "press":
            page.keyboard.press(cmd["key"])
            page.wait_for_timeout(300)
            page.screenshot(path=output_path)
            return {"ok": True, "path": output_path}
        
        elif action == "hover":
            page.hover(cmd["selector"], timeout=5000)
            page.wait_for_timeout(200)
            page.screenshot(path=output_path)
            return {"ok": True, "path": output_path}
        
        elif action == "scroll":
            amount = cmd.get("amount", 300)
            direction = cmd["direction"].lower()
            scroll_map = {
                "up": (0, -amount),
                "down": (0, amount),
                "left": (-amount, 0),
                "right": (amount, 0),
            }
            if direction not in scroll_map:
                return {"error": f"Invalid direction: {direction}"}
            dx, dy = scroll_map[direction]
            page.mouse.wheel(dx, dy)
            page.wait_for_timeout(300)
            page.screenshot(path=output_path)
            return {"ok": True, "path": output_path}
        
        elif action == "wait":
            page.wait_for_timeout(int(cmd["seconds"] * 1000))
            page.screenshot(path=output_path)
            return {"ok": True, "path": output_path}
        
        elif action == "eval":
            result = page.evaluate(cmd["code"])
            return {"ok": True, "result": result}
        
        elif action == "text":
            text = page.text_content(cmd["selector"], timeout=5000)
            return {"ok": True, "text": text}
        
        elif action == "list":
            elements = page.query_selector_all(cmd["selector"])
            items = []
            for i, el in enumerate(elements):
                text = el.text_content() or ""
                text = " ".join(text.split())[:100]
                tag = el.evaluate("el => el.tagName.toLowerCase()")
                classes = el.evaluate("el => el.className")
                items.append({"index": i, "tag": tag, "class": classes, "text": text})
            return {"ok": True, "items": items}
        
        elif action == "goto":
            page.goto(cmd["url"], wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(500)
            page.screenshot(path=output_path)
            return {"ok": True, "path": output_path}
        
        elif action == "reload":
            page.reload(wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(500)
            page.screenshot(path=output_path)
            return {"ok": True, "path": output_path}
        
        elif action == "ping":
            return {"ok": True, "status": "running"}
        
        else:
            return {"error": f"Unknown action: {action}"}
    
    except Exception as e:
        return {"error": str(e)}


# CLI Commands

def cmd_start(args):
    """Start the browser server."""
    run_server()


def cmd_stop(args):
    """Stop the browser server."""
    if PID_FILE.exists():
        pid = int(PID_FILE.read_text().strip())
        try:
            os.kill(pid, signal.SIGTERM)
            print("Server stopped.")
        except ProcessLookupError:
            print("Server was not running.")
            if SOCKET_PATH.exists():
                SOCKET_PATH.unlink()
            PID_FILE.unlink()
    else:
        print("Server is not running.")


def cmd_status(args):
    """Check server status."""
    if not SOCKET_PATH.exists():
        print("Server is not running.")
        return
    
    try:
        result = send_command({"action": "ping"})
        if result.get("ok"):
            print("Server is running.")
        else:
            print("Server is not responding.")
    except:
        print("Server is not running.")


def cmd_screenshot(args):
    """Take a screenshot."""
    result = send_command({
        "action": "screenshot",
        "wait": args.wait,
        "full_page": args.full_page,
    })
    if result.get("ok"):
        print(f"Screenshot saved: {result['path']}")
    else:
        print(f"Error: {result.get('error')}", file=sys.stderr)
        sys.exit(1)


def cmd_click(args):
    """Click an element."""
    result = send_command({"action": "click", "selector": args.selector})
    if result.get("ok"):
        print(f"Clicked: {args.selector}")
        print(f"Screenshot saved: {result['path']}")
    else:
        print(f"Error: {result.get('error')}", file=sys.stderr)
        sys.exit(1)


def cmd_type(args):
    """Type text into an element."""
    result = send_command({"action": "type", "selector": args.selector, "text": args.text})
    if result.get("ok"):
        print(f"Typed into {args.selector}")
        print(f"Screenshot saved: {result['path']}")
    else:
        print(f"Error: {result.get('error')}", file=sys.stderr)
        sys.exit(1)


def cmd_press(args):
    """Press a key."""
    result = send_command({"action": "press", "key": args.key})
    if result.get("ok"):
        print(f"Pressed: {args.key}")
        print(f"Screenshot saved: {result['path']}")
    else:
        print(f"Error: {result.get('error')}", file=sys.stderr)
        sys.exit(1)


def cmd_hover(args):
    """Hover over an element."""
    result = send_command({"action": "hover", "selector": args.selector})
    if result.get("ok"):
        print(f"Hovering: {args.selector}")
        print(f"Screenshot saved: {result['path']}")
    else:
        print(f"Error: {result.get('error')}", file=sys.stderr)
        sys.exit(1)


def cmd_scroll(args):
    """Scroll the page."""
    result = send_command({
        "action": "scroll",
        "direction": args.direction,
        "amount": args.amount,
    })
    if result.get("ok"):
        print(f"Scrolled {args.direction}")
        print(f"Screenshot saved: {result['path']}")
    else:
        print(f"Error: {result.get('error')}", file=sys.stderr)
        sys.exit(1)


def cmd_wait(args):
    """Wait and take screenshot."""
    result = send_command({"action": "wait", "seconds": args.seconds})
    if result.get("ok"):
        print(f"Waited {args.seconds}s")
        print(f"Screenshot saved: {result['path']}")
    else:
        print(f"Error: {result.get('error')}", file=sys.stderr)
        sys.exit(1)


def cmd_eval(args):
    """Evaluate JavaScript."""
    result = send_command({"action": "eval", "code": args.code})
    if result.get("ok"):
        print(json.dumps(result["result"], indent=2, default=str))
    else:
        print(f"Error: {result.get('error')}", file=sys.stderr)
        sys.exit(1)


def cmd_text(args):
    """Get text content of an element."""
    result = send_command({"action": "text", "selector": args.selector})
    if result.get("ok"):
        print(result["text"])
    else:
        print(f"Error: {result.get('error')}", file=sys.stderr)
        sys.exit(1)


def cmd_list(args):
    """List matching elements."""
    result = send_command({"action": "list", "selector": args.selector})
    if result.get("ok"):
        items = result["items"]
        print(f"Found {len(items)} elements matching '{args.selector}':\n")
        for item in items:
            print(f"  [{item['index']}] <{item['tag']} class=\"{item['class']}\">")
            print(f"      Text: {item['text']}")
            print()
    else:
        print(f"Error: {result.get('error')}", file=sys.stderr)
        sys.exit(1)


def cmd_goto(args):
    """Navigate to a URL."""
    result = send_command({"action": "goto", "url": args.url})
    if result.get("ok"):
        print(f"Navigated to: {args.url}")
        print(f"Screenshot saved: {result['path']}")
    else:
        print(f"Error: {result.get('error')}", file=sys.stderr)
        sys.exit(1)


def cmd_reload(args):
    """Reload the page."""
    result = send_command({"action": "reload"})
    if result.get("ok"):
        print("Page reloaded")
        print(f"Screenshot saved: {result['path']}")
    else:
        print(f"Error: {result.get('error')}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Browser interaction tool for web applications",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Server commands
    p_start = subparsers.add_parser("start", help="Start the browser server")
    p_start.set_defaults(func=cmd_start)
    
    p_stop = subparsers.add_parser("stop", help="Stop the browser server")
    p_stop.set_defaults(func=cmd_stop)
    
    p_status = subparsers.add_parser("status", help="Check server status")
    p_status.set_defaults(func=cmd_status)
    
    # Interaction commands
    p_screenshot = subparsers.add_parser("screenshot", aliases=["ss"], help="Take a screenshot")
    p_screenshot.add_argument("--wait", "-w", type=float, default=0, help="Seconds to wait before screenshot")
    p_screenshot.add_argument("--full-page", "-f", action="store_true", help="Capture full page")
    p_screenshot.set_defaults(func=cmd_screenshot)
    
    p_click = subparsers.add_parser("click", help="Click an element")
    p_click.add_argument("selector", help="CSS selector")
    p_click.set_defaults(func=cmd_click)
    
    p_type = subparsers.add_parser("type", help="Type text into an element")
    p_type.add_argument("selector", help="CSS selector")
    p_type.add_argument("text", help="Text to type")
    p_type.set_defaults(func=cmd_type)
    
    p_press = subparsers.add_parser("press", help="Press a key")
    p_press.add_argument("key", help="Key to press (Enter, Tab, Escape, etc.)")
    p_press.set_defaults(func=cmd_press)
    
    p_hover = subparsers.add_parser("hover", help="Hover over an element")
    p_hover.add_argument("selector", help="CSS selector")
    p_hover.set_defaults(func=cmd_hover)
    
    p_scroll = subparsers.add_parser("scroll", help="Scroll the page")
    p_scroll.add_argument("direction", help="Direction: up, down, left, right")
    p_scroll.add_argument("amount", type=int, nargs="?", default=300, help="Pixels (default: 300)")
    p_scroll.set_defaults(func=cmd_scroll)
    
    p_wait = subparsers.add_parser("wait", help="Wait and take screenshot")
    p_wait.add_argument("seconds", type=float, help="Seconds to wait")
    p_wait.set_defaults(func=cmd_wait)
    
    p_eval = subparsers.add_parser("eval", help="Evaluate JavaScript")
    p_eval.add_argument("code", help="JavaScript code")
    p_eval.set_defaults(func=cmd_eval)
    
    p_text = subparsers.add_parser("text", help="Get element text")
    p_text.add_argument("selector", help="CSS selector")
    p_text.set_defaults(func=cmd_text)
    
    p_list = subparsers.add_parser("list", help="List matching elements")
    p_list.add_argument("selector", help="CSS selector")
    p_list.set_defaults(func=cmd_list)
    
    p_goto = subparsers.add_parser("goto", help="Navigate to URL")
    p_goto.add_argument("url", help="URL to navigate to")
    p_goto.set_defaults(func=cmd_goto)
    
    p_reload = subparsers.add_parser("reload", help="Reload the page")
    p_reload.set_defaults(func=cmd_reload)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Handle 'ss' alias
    if args.command == "ss":
        args.func = cmd_screenshot
    
    args.func(args)


if __name__ == "__main__":
    main()
