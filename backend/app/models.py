"""SQLAlchemy models. Column definitions are unchanged from the original
single-file implementation; only their location moved.

Added 2026-11-16 (foundations): TelemetryLog (append-only telemetry
history; FieldNode keeps only the latest values) and VisionTask
(persisted vision analysis results; previously in-memory only).
"""

from sqlalchemy import Column, Float, Integer, String, Text

from app.database import Base


class FieldNode(Base):
    __tablename__ = "field_nodes"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    status = Column(String)
    moisture = Column(Float)
    pestIndex = Column(String)
    spad = Column(Float)
    temp = Column(Float)
    n = Column(Integer)
    p = Column(Integer)
    k = Column(Integer)
    x = Column(Integer)
    y = Column(Integer)
    soil_ph = Column(Float, default=7.0)
    soil_ec = Column(Float, default=0.5)
    water_ph = Column(Float, default=7.0)
    water_do = Column(Float, default=6.5)
    water_turbidity = Column(Float, default=5.0)


class ESGAsset(Base):
    __tablename__ = "esg_assets"
    id = Column(Integer, primary_key=True, default=1)
    co2_reduction = Column(Float, default=1482.5)
    pollution_interception = Column(Float, default=3105.0)
    financial_rating = Column(String, default="AAA")
    carbon_revenue = Column(Float, default=118600.0)


class ESGLog(Base):
    __tablename__ = "esg_logs"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(String)
    category = Column(String)
    title = Column(String)
    description = Column(String)


class TaskLog(Base):
    __tablename__ = "task_logs"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    level = Column(String)
    title = Column(String)
    location = Column(String)
    confidence = Column(String)
    time = Column(String)
    analysis = Column(String)
    strategy = Column(String)
    pesticide_reduction = Column(String)
    action_name = Column(String)
    evidence_image = Column(String)
    status = Column(String, default="PENDING")


class TelemetryLog(Base):
    """One row per accepted telemetry report, newest last.

    FieldNode keeps only the latest values (the dashboard's live view);
    this table is the history behind it, for trend charts and later
    robot patrol analysis. Timestamps are server receipt time, in the
    same "%Y-%m-%d %H:%M:%S" format used elsewhere in the codebase.
    """

    __tablename__ = "telemetry_logs"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    field_id = Column(String, index=True)
    timestamp = Column(String)
    temp = Column(Float)
    moisture = Column(Float)
    n = Column(Integer)
    p = Column(Integer)
    k = Column(Integer)
    soil_ph = Column(Float)
    soil_ec = Column(Float)
    water_ph = Column(Float)
    water_do = Column(Float)
    water_turbidity = Column(Float)
    status = Column(String)


class VisionTask(Base):
    """Persisted vision analysis result, keyed by the task id handed out
    by POST /api/vision/analyze.

    The in-memory VISION_TASKS_STORE stays the fast path; this row is
    the write-through copy, so GET /api/vision/result keeps working
    after a backend restart. result_json holds the exact response dict
    (including the base64 annotated image for image tasks).
    """

    __tablename__ = "vision_tasks"
    task_id = Column(String, primary_key=True, index=True)
    field_id = Column(String)
    media_type = Column(String)
    status = Column(String)
    result_json = Column(Text)
    created_at = Column(String)
    updated_at = Column(String)
