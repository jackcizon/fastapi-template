"""run uvicorn server

<SHELL>: poetry run python scripts/run_server.py
"""

import os
import sys
from pathlib import Path

import uvicorn

root_dir = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(root_dir))
sys.path.insert(0, os.path.join(root_dir, 'src'))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
