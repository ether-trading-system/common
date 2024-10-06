## [2024.10.06] SQLAlchemy를 이용한 비동기 PostgreSQL 접속

### root 디렉토리에 환경변수 추가
```bash
# .env
DB_HOST='host명'
DB_PORT=5432
DB_NAME='postgres'
DB_USER='postgres'
DB_PW='1q2w3e4r!!'
```
⭐ 접두사 `DB_` 필수 입력

### `commmon/utils/postgresql_helper.py` 
```python
# common/utils/postgresql_helper.py

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
```
1. postgresql 비동기 접속을 위한 접속 URL 설정 (`postgresql+asyncpg://...`)
2. 비동기 연결을 위한 엔진 설정
3. 의존성 주입을 위한 get_db


### FastAPI에서의 사용
```python
# __test__/postgresql.py
import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import Column, String, Date, Numeric

from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.future import select
from common.utils.postgresql_helper import get_db, engine  # common 모듈에서 DB 연결 가져오기
from pydantic import BaseModel
from typing import List
import uvicorn
from contextlib import asynccontextmanager

# 현재 파일 경로로 작업 디렉토리 변경
os.chdir(os.path.dirname(os.path.abspath(__file__)))

Base = declarative_base()


# Model 정의
class UserLoginInfo(Base):
    __tablename__ = "user_login_info"
    
    service_type = Column(String, primary_key=True)
    user_id = Column(String, primary_key=True)
    # 이하 생략
    # .
    # .
    # .


# Pydantic schema 정의
class UserLoginInfoCreate(BaseModel):
    service_type: str
    user_id: str
    # 이하 생략
    # .
    # .
    # .
    
class UserLoginInfoRead(UserLoginInfoCreate):
    pass

# 예제
@app.post("/users/", response_model=UserLoginInfoRead)
async def create_user(user: UserLoginInfoCreate, db: Session = Depends(get_db)):
    db_user = UserLoginInfo(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    return db_user
```

1. Base class를 사용해서 정의한 model, schema 생성
2. `declarative_base()` 를 이용한 테이블 매핑
3. (필요시) `@asynccontextmanager`를 이용한 FastAPI lifespan 설정.(테이블 생성 등)
4. 필요한 API 작성<br/>
  a. 비동기 방식으로 작성<br/>
  b. Depends를 이용한 db 의존성 주입<br/>
  c. pydantic 스키마를 이용한 유효성 체크 & 데이터 직렬화( `model_dump()` )<br/>
  d. 트랜잭션 작업 후 commit(or rollback) & refresh