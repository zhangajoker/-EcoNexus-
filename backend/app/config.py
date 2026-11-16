"""Central configuration for the EcoNexus backend.

All environment-dependent values live here. ``backend/.env`` is loaded from
an explicit path (next to this package's parent directory) so behaviour does
not depend on the working directory the server is launched from.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BACKEND_DIR.parent

load_dotenv(BACKEND_DIR / ".env")

# Keep direct outbound calls (LLM / weather) off any local proxy, as before.
os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""

STATIC_DIR = BACKEND_DIR / "static"
TEMP_UPLOADS_DIR = BACKEND_DIR / "temp_uploads"
STATIC_DIR.mkdir(exist_ok=True)
TEMP_UPLOADS_DIR.mkdir(exist_ok=True)


def _resolve_sqlite_url(url: str) -> str:
    """Resolve a relative sqlite URL against the backend dir, not the cwd."""
    prefix = "sqlite:///"
    if url.startswith(prefix):
        path = url[len(prefix):]
        if path.startswith("./"):
            return prefix + str(BACKEND_DIR / path[2:])
        if not os.path.isabs(path) and ":" not in path[:3]:
            return prefix + str(BACKEND_DIR / path)
    return url


DATABASE_URL = _resolve_sqlite_url(
    os.getenv("DATABASE_URL", "sqlite:///./econexus_v3.db")
)

# YOLO weights: resolved against the project root. Env overrides are
# honoured when set; the defaults are the weights the system already used.
MODEL_PATHS = {
    "pest_detect_pt": os.getenv(
        "YOLO_VISION_MODEL_PATH",
        str(
            PROJECT_ROOT
            / "runs"
            / "detect"
            / "runs"
            / "detect"
            / "tianyan_pest_v2_robust-5"
            / "weights"
            / "best.pt"
        ),
    ),
    "disease_classify_pt": os.getenv(
        "YOLO_DISEASE_MODEL_PATH",
        str(
            PROJECT_ROOT
            / "runs"
            / "classify"
            / "runs"
            / "classify"
            / "tianyan_disease_v2_regional-4"
            / "weights"
            / "best.pt"
        ),
    ),
}

LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.deepseek.com/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-chat")

# Public base URL used when building evidence (image/video) URLs.
# Override with the machine's LAN address (e.g. http://192.168.1.10:8000)
# so phones and robots on the LAN can open the links; the default keeps
# the previous loopback behaviour. Trailing slashes are stripped.
PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "http://127.0.0.1:8000").rstrip("/")


# NOTE: the coordinates below are Beijing's (kept verbatim from the original
# code to preserve behaviour). The frontend does not call this endpoint; it
# fetches Open-Meteo directly with browser geolocation.
WEATHER_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=39.9042&longitude=116.4074"
    "&current=temperature_2m,relative_humidity_2m,weather_code"
)
