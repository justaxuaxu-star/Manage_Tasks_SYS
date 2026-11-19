import os
from pathlib import Path

import uvicorn
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")
port = int(os.getenv("API_PORT", "8001"))

uvicorn.run("backend.main:app", host="127.0.0.1", port=port, reload=True)