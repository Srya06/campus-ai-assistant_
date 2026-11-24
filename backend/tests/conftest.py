import os
import sys
import asyncio
import pytest

# Fix AnyIO / Starlette TestClient event loop policy on Windows
if sys.platform == "win32":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass

os.environ["TESTING"] = "1"
os.environ["DATABASE_URL"] = "sqlite:///./campus_assistant.db"
