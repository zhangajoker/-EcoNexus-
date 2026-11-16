"""EcoNexus API entrypoint (thin composition root).

Run from the backend directory:
    uvicorn main:app --host 127.0.0.1 --port 8000

All behaviour lives in the ``app`` package: configuration in
``app.config``, models in ``app.models``, endpoints in ``app.routers`` and
the vision pipeline in ``app.services.vision``.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import STATIC_DIR
from app.database import init_db
from app.routers import ai, dashboard, esg, fields, hardware, tasks, vision, weather

init_db()

app = FastAPI(title="EcoNexus API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

for _router in (fields.router, esg.router, weather.router, dashboard.router,
                vision.router, tasks.router, hardware.router, ai.router):
    app.include_router(_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000)
