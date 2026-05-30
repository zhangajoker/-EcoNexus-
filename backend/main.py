from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# ==================== 1. 数据库配置 (SQLAlchemy) ====================
SQLALCHEMY_DATABASE_URL = "sqlite:///./econexus.db"
# check_same_thread=False 是 SQLite 配合 FastAPI 需要的特有配置
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ==================== 2. 数据表模型定义 ====================
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

# 在本地创建表结构
Base.metadata.create_all(bind=engine)

# ==================== 3. FastAPI 实例与中间件 ====================
app = FastAPI(title="EcoNexus API", description="天衍·生境 农业数字孪生中枢")

# 配置 CORS，允许 Vue 前端 (默认5173端口) 跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应改为前端的真实域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 获取数据库会话的依赖函数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==================== 4. 核心业务路由 ====================

@app.on_event("startup")
def startup_populate_data():
    """系统启动时，检查并注入初始的物理节点数据"""
    db = SessionLocal()
    if db.query(FieldNode).count() == 0:
        mock_data = [
            FieldNode(id="F-001", name="A区-核心稻田", status="健康", moisture=45.0, pestIndex="低", spad=42.1, temp=26.5, n=142, p=35, k=120, x=220, y=160),
            FieldNode(id="F-002", name="B区-试验田", status="高危", moisture=32.0, pestIndex="高", spad=38.5, temp=28.2, n=98, p=20, k=85, x=620, y=340),
            FieldNode(id="F-003", name="C区-果林套种", status="健康", moisture=55.0, pestIndex="无", spad=45.0, temp=25.1, n=160, p=40, k=135, x=780, y=140),
            FieldNode(id="F-004", name="D区-育秧温室", status="预警", moisture=60.0, pestIndex="中", spad=40.2, temp=29.0, n=155, p=45, k=140, x=380, y=480)
        ]
        db.add_all(mock_data)
        db.commit()
    db.close()

@app.get("/api/fields")
def get_all_fields(db: Session = Depends(get_db)):
    """API: 获取全域态势感知的节点阵列数据"""
    return db.query(FieldNode).all()