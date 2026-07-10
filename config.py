import os
from dotenv import load_dotenv

load_dotenv()


ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

CLAUDE_MODEL = os.getenv(
    "CLAUDE_MODEL",
    "claude-3-5-sonnet-latest"
)

DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    "attendance.db"
)

MAX_MESSAGES = int(
    os.getenv("MAX_MESSAGES", "10")
)
