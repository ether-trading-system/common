from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from common.settings import get_db_config

db_config = get_db_config()
# PostgreSQL URL 설정
DATABASE_URL = f"postgresql://postgres:1q2w3e4r!!@localhost:5432/nebula"
# DATABASE_URL = f"postgresql://{db_config.user}:{db_config.pw}@{db_config.host}:{db_config.port}/{db_config.name}"
print(db_config)
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