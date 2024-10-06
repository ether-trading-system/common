# common

> A common library for the project.

## Install

### poetry
```bash
poetry add git+https://github.com/ether-trading-system/common.git
```

아래와 같이 dependencies에 추가되면 정상 설치 입니다.
```
# pyproject.toml
[tool.poetry.dependencies]
...
common = {git = "https://github.com/ether-trading-system/common.git"}
```


### pip
```bash
pip install git+https://github.com/ether-trading-system/common.git
```

## Update

### poetry
```bash
poetry update common 
```


## Discord
디스코드 알림을 위한 모듈입니다.

### 설정
.env를 사용해 환경변수를 설정합니다.
채널을 추가하기 위해 아래 형식을 맞춰서 webhook을 등록해주세요

- `sample_topic`은 웹훅 대한 식별자 입니다. 원하는 웹훅을 식별하기 위한 key 정의해주세요.
- `name`은 웹훅의 이름을 정의해주세요. 채널에 메시지를 보낼 때 제목으로 사용됩니다.
- `url`은 웹훅의 URL을 정의해주세요. 웹훅을 통해 메시지를 보낼 수 있습니다.

```json
{
  "sample_topic": {
    "name": "sample",
    "url": "https://discord.com/api/webhooks/1274381556315852882/wyhFO7Xys5JlSi0Gypm9FppyGI_SstKXJcJ4rLLPoYP1VrcTsw-6hwTqMUAKeyuC2y5E"
  }
}
```

위 형식으로 정의된 json을 환경변수로 등록합니다.

```bash
COMMON_DISCORD='{ "sample_topic": { "name": "sample", "url": "https://discord.com/api/webhooks/1274381556315852882/wyhFO7Xys5JlSi0Gypm9FppyGI_SstKXJcJ4rLLPoYP1VrcTsw-6hwTqMUAKeyuC2y5E" } }'
```

### Usage

[`__test__ > discord.py`](__test__/discord.py) 파일을 참고해주세요.

```python
from common.discord import notify, notify_info, DiscordMessage, MessageColor

message = DiscordMessage(
    topic='sample_topic',
    title='title',
    message='message',
    data={'key': 'value'}
)

await notify(message, MessageColor.INFO)
await notify_info(message)
```


---
### [2024.10.06]
### SQLAlchemy를 이용한 비동기 PostgreSQL 접속(Created by 김대휘)

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