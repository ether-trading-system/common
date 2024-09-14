from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from common.settings import get_db_config


dbhelper = get_db_config()
# PostgreSQL URL 설정
DATABASE_URL = f"postgresql://{dbhelper.user}:{dbhelper.pw}@{dbhelper.host}:{dbhelper.port}/{dbhelper.name}"

# SQLAlchemy 엔진 생성
engine = create_engine(DATABASE_URL)

# 세션로컬 생성 : DB 요청 보내기 위한 파이프라인 역할
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Base 클래스 생성(모든 모델이 상속할 기본 클래스)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()