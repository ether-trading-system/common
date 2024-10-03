from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from common.settings import get_db_config
import databases


dbhelper = get_db_config()
# PostgreSQL URL 설정
DATABASE_URL = f"postgresql+asyncpg://{dbhelper.user}:{dbhelper.pw}@{dbhelper.host}:{dbhelper.port}/{dbhelper.name}"
print(DATABASE_URL)
# SQLAlchemy 엔진 생성
engine = create_async_engine(DATABASE_URL)

# 세션로컬 생성 : DB 요청 보내기 위한 파이프라인 역할
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

database = databases.Database(DATABASE_URL)


async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()