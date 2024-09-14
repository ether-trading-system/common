from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from common.utils.postgresql_helper import get_db

from sqlalchemy import Column, Integer, String
from common.utils.postgresql_helper import Base
from pydantic import BaseModel

# T_USER 테이블 모델 정의
class User(Base):
    __tablename__ = 't_user'
    __table_args__ = {'schema': 'public'}

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, index=True)

class UserSchema(BaseModel):
    user_id: int
    user_name: str


app = FastAPI()
client = TestClient(app)

@app.get("/", response_model=list[UserSchema])
async def get_postgresql(db: Session = Depends(get_db)):
    users = db.query(User).all()
    print(type(users))

    return users



def test_get_postgresql():
    response = client.get("/")
    assert response.status_code == 200
    # 반환된 사용자 목록이 올바르게 직렬화되었는지 확인
    
    data = response.json()

    return data