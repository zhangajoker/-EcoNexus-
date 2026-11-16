"""SQLAlchemy engine, session factory and one-time database seeding."""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create tables and seed the four demo fields + ESG asset (once)."""
    # Imported here so model classes register on Base before create_all,
    # without creating an import cycle (models imports Base from here).
    from app.models import ESGAsset, FieldNode

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if not db.query(FieldNode).first():
            nodes = [
                FieldNode(id="F-001", name="A区核心试验田", status="健康", moisture=42.8, temp=25.0, n=40, p=20, k=30, x=150,
                          y=100),
                FieldNode(id="F-002", name="B区果林试验区", status="生态预警", moisture=28.5, temp=28.4, n=25, p=15, k=45,
                          x=450, y=200),
                FieldNode(id="F-003", name="C区轮作休耕地", status="健康", moisture=35.0, temp=24.0, n=35, p=30, k=40, x=300,
                          y=400),
                FieldNode(id="F-004", name="D区智慧温室群", status="健康", moisture=55.2, temp=22.5, n=45, p=25, k=35, x=600,
                          y=350),
            ]
            db.add_all(nodes)

        if not db.query(ESGAsset).first():
            db.add(ESGAsset(id=1, co2_reduction=1482.5, pollution_interception=3105.0, financial_rating="AAA",
                            carbon_revenue=118600.0))
        db.commit()
    finally:
        db.close()
