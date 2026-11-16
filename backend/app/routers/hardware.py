"""Hardware telemetry ingestion (moved from main.py).

Fixes: the soil/water fields (soil_ph, soil_ec, water_ph, water_do,
water_turbidity) that ``SensorPayload`` already declared are now actually
written to the field record instead of being silently dropped; posting
telemetry for an unknown field id returns 404 instead of crashing.

Foundations 2026-11-16: every accepted report is also appended to the
TelemetryLog history table (FieldNode keeps only the latest values), and
GET /api/hardware/telemetry/history exposes that history, newest first.
"""

import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import FieldNode, TelemetryLog
from app.schemas import SensorPayload

router = APIRouter(prefix="/api/hardware", tags=["hardware"])


def _apply_telemetry(field: FieldNode, payload: SensorPayload) -> str:
    field.temp = payload.temp
    field.moisture = payload.moisture
    field.n = payload.n
    field.p = payload.p
    field.k = payload.k
    field.soil_ph = payload.soil_ph
    field.soil_ec = payload.soil_ec
    field.water_ph = payload.water_ph
    field.water_do = payload.water_do
    field.water_turbidity = payload.water_turbidity
    field.status = "生态预警" if (payload.moisture < 20 or payload.temp > 35) else "健康"
    return field.status


def _record_history(db: Session, payload: SensorPayload, status: str) -> None:
    db.add(TelemetryLog(
        field_id=payload.field_id,
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        temp=payload.temp,
        moisture=payload.moisture,
        n=payload.n,
        p=payload.p,
        k=payload.k,
        soil_ph=payload.soil_ph,
        soil_ec=payload.soil_ec,
        water_ph=payload.water_ph,
        water_do=payload.water_do,
        water_turbidity=payload.water_turbidity,
        status=status,
    ))


@router.post("/telemetry")
def receive_hardware_data(payload: SensorPayload, db: Session = Depends(get_db)):
    field = db.query(FieldNode).filter(FieldNode.id == payload.field_id).first()
    if field is None:
        raise HTTPException(status_code=404, detail="Field not found")
    status = _apply_telemetry(field, payload)
    _record_history(db, payload, status)
    db.commit()
    return {"status": "success"}


@router.post("/telemetry/bulk")
def receive_hardware_data_bulk(payloads: List[SensorPayload], db: Session = Depends(get_db)):
    for payload in payloads:
        field = db.query(FieldNode).filter(FieldNode.id == payload.field_id).first()
        if field:
            status = _apply_telemetry(field, payload)
            _record_history(db, payload, status)

    db.commit()
    return {"status": "success", "processed_count": len(payloads)}


@router.get("/telemetry/history")
def get_telemetry_history(field_id: str, limit: int = 100, db: Session = Depends(get_db)):
    field = db.query(FieldNode).filter(FieldNode.id == field_id).first()
    if field is None:
        raise HTTPException(status_code=404, detail="Field not found")
    limit = max(1, min(limit, 1000))
    rows = (
        db.query(TelemetryLog)
        .filter(TelemetryLog.field_id == field_id)
        .order_by(TelemetryLog.id.desc())
        .limit(limit)
        .all()
    )
    return {
        "status": "success",
        "field_id": field_id,
        "count": len(rows),
        "records": [
            {
                "timestamp": row.timestamp,
                "temp": row.temp,
                "moisture": row.moisture,
                "n": row.n,
                "p": row.p,
                "k": row.k,
                "soil_ph": row.soil_ph,
                "soil_ec": row.soil_ec,
                "water_ph": row.water_ph,
                "water_do": row.water_do,
                "water_turbidity": row.water_turbidity,
                "status": row.status,
            }
            for row in rows
        ],
    }
