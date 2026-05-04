"""
Ombre — Autonomous AI Reasoning Data Infrastructure
One call. Full autonomy. Zero waste.

Enterprise: ombreaiq@gmail.com
License: BUSL-1.1
GitHub: https://github.com/ombreaiq/ombre
"""

__version__ = "1.0.0"
__author__  = "Ombre"
__email__   = "ombreaiq@gmail.com"
__license__ = "BUSL-1.1"

from ombre.storage.database import init_db


def start(host: str = "0.0.0.0", port: int = 8080):
    """
    Start Ombre — initializes database and launches dashboard.

    Usage:
        import ombre
        ombre.start()

    MCP Usage (in mcp config):
        {
          "mcpServers": {
            "ombre": {
              "command": "python3",
              "args": ["-m", "ombre.mcp.server"],
              "env": { "OMBRE_CLIENT_ID": "your-client-id" }
            }
          }
        }
    """
    print("""
 ██████╗ ███╗   ███╗██████╗ ██████╗ ███████╗
██╔═══██╗████╗ ████║██╔══██╗██╔══██╗██╔════╝
██║   ██║██╔████╔██║██████╔╝██████╔╝█████╗
██║   ██║██║╚██╔╝██║██╔══██╗██╔══██╗██╔══╝
╚██████╔╝██║ ╚═╝ ██║██████╔╝██║  ██║███████╗
 ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚═╝  ╚═╝╚══════╝

  Autonomous AI Reasoning Data Infrastructure  v1.0.0
  ombreaiq@gmail.com
""")

    init_db()

    from ombre.dashboard import run_dashboard
    run_dashboard(host=host, port=port)
    
