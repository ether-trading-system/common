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
    nickname = Column(String)
    name = Column(String)
    
    profile_image = Column(String)
    thumbnail_image = Column(String)
    
    email_address = Column(String)
    connected_at = Column(Date)
    
    access_token = Column(String)
    token_type = Column(String)
    refresh_token = Column(String)
    expires_in = Column(Numeric)
    scope = Column(String)
    refresh_token_expires_in = Column(Numeric)
    
    create_date = Column(Date)
    create_by = Column(String)
    modify_date = Column(Date)
    modify_by = Column(String)


# Pydantic schema 정의
class UserLoginInfoCreate(BaseModel):
    service_type: str
    user_id: str
    nickname: str
    name: str
    profile_image: str
    thumbnail_image: str
    email_address: str
    connected_at: str
    access_token: str
    token_type: str
    refresh_token: str
    expires_in: float
    scope: str
    refresh_token_expires_in: float
    create_date: str
    create_by: str
    modify_date: str
    modify_by: str
    
class UserLoginInfoRead(UserLoginInfoCreate):
    pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 애플리케이션 시작 시 실행될 작업
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # 애플리케이션 종료 시 실행될 작업


# FastAPI 인스턴스 생성 시 lifespan 핸들러 설정
app = FastAPI(lifespan=lifespan)

@app.get("/users/", response_model=List[UserLoginInfoRead])
async def get_users(db: Session = Depends(get_db)):
    result = await db.execute(select(UserLoginInfo))
    users = result.scalars().all()
    
    return users


# 사용자 정보 등록
@app.post("/users/", response_model=UserLoginInfoRead)
async def create_user(user: UserLoginInfoCreate, db: Session = Depends(get_db)):
    db_user = UserLoginInfo(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    return db_user


# 사용자 정보 삭제
@app.delete("/users/{service_type}/{user_id}", response_model=str)
async def delete_user(service_type: str, user_id: str, db: Session = Depends(get_db)):
    db_user = db.query(UserLoginInfo).filter(UserLoginInfo.service_type == service_type, UserLoginInfo.user_id == user_id).first()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(db_user)
    await db.commit()
    
    return "User deleted successfully"


# main 함수 추가 및 실행
async def main():
    print("Starting FastAPI application...")
    uvicorn.run("postgresql:app", host="localhost", port=8000, log_level="info", reload=True)


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())