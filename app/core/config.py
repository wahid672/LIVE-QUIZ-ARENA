import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

APP_NAME = os.getenv("APP_NAME", "LIVE QUIZ ARENA")
QUESTION_FILE = BASE_DIR / os.getenv("QUESTION_FILE", "data/questions.json")
DEFAULT_ANSWER_DURATION = int(os.getenv("DEFAULT_ANSWER_DURATION", "15"))
DEFAULT_QUESTION_COUNT = int(os.getenv("DEFAULT_QUESTION_COUNT", "10"))
