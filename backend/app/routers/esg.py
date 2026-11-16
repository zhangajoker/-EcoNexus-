"""ESG carbon-sink asset dashboard (moved from main.py)."""

import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ESGAsset, ESGLog

router = APIRouter(prefix="/api", tags=["esg"])


@router.get("/esg/dashboard")
def get_esg_dashboard(db: Session = Depends(get_db)):
    assets = db.query(ESGAsset).filter(ESGAsset.id == 1).first()
    logs = db.query(ESGLog).order_by(ESGLog.id.desc()).all()
    total_poll = assets.pollution_interception if assets else 3105.0
    reduction_chart = [
        {"name": "水资源无效渗漏", "value": round(total_poll * 0.65, 1)},
        {"name": "无机氮磷肥流失", "value": round(total_poll * 0.20, 1)},
        {"name": "广谱杀虫剂超标", "value": round(total_poll * 0.10, 1)},
        {"name": "化学除草剂滥用", "value": round(total_poll * 0.05, 1)}
    ]
    now = datetime.datetime.now()
    months = [(now - datetime.timedelta(days=30 * i)).strftime('%b') for i in range(5, -1, -1)]
    base_emissions = [120, 132, 145, 160, 180, 210]
    reduction_factor = min((assets.co2_reduction / 5000), 0.6) if assets else 0
    actual_emissions = [int(b * (1 - reduction_factor * (i / 5))) for i, b in enumerate(base_emissions)]
    return {"assets": assets, "logs": logs, "charts": {"reduction": reduction_chart,
                                                       "trend": {"categories": months, "baseline": base_emissions,
                                                                 "actual": actual_emissions}}}
