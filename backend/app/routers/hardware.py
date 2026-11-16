"""Hardware telemetry ingestion (moved from main.py).

Fixes: the soil/water fields (soil_ph, soil_ec, water_ph, water_do,
water_turbidity) that ``SensorPayload`` already declared are now actually
written to the field record instead of being silently dropped; posting
telemetry for an unknown field id returns 404 instead of crashing.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import FieldNode
from app.schemas import SensorPayload

router = APIRouter(prefix="/api/hardware", tags=["hardware"])


def _apply_telemetry(field: FieldNode, payload: SensorPayload) -> None:
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


@router.post("/telemetry")
def receive_hardware_data(payload: SensorPayload, db: Session = Depends(get_db)):
    field = db.query(FieldNode).filter(FieldNode.id == payload.field_id).first()
    if field is None:
        raise HTTPException(status_code=404, detail="Field not found")
    _apply_telemetry(field, payload)
    db.commit()
    return {"status": "success"}


@router.post("/telemetry/bulk")
def receive_hardware_data_bulk(payloads: List[SensorPayload], db: Session = Depends(get_db)):
    for payload in payloads:
        field = db.query(FieldNode).filter(FieldNode.id == payload.field_id).first()
        if field:
            _apply_telemetry(field, payload)

    db.commit()
    return {"status": "success", "processed_count": len(payloads)}
