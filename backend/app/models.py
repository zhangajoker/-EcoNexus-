"""SQLAlchemy models. Column definitions are unchanged from the original
single-file implementation; only their location moved."""

from sqlalchemy import Column, Float, Integer, String

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
