from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import db_models as models   # 변경된 파일명 import
import database_connection as database # 변경된 파일명 import

# 서버 시작 시 DB 테이블 자동 생성 (없을 경우)
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Pill Alimi API Server",
    description="약알리미 서비스를 위한 REST API Backend",
    version="1.0.0"
)

# 1. Root Endpoint (Health Check)
@app.get("/")
def read_root():
    return {"status": "active", "message": "Pill Alimi Backend Server Running"}

# 2. 의약품 검색 API
@app.get("/pills/")
def search_pills(
    name: str = None, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(database.get_db)
):
    """
    [검색 기능]
    - name: 약 이름에 포함된 문자열 검색 (LIKE Query)
    - skip, limit: 페이징 처리
    """
    query = db.query(models.Pill)

    # 검색어(name)가 존재하면 LIKE 검색 수행
    if name:
        query = query.filter(models.Pill.ITEM_NAME.like(f"%{name}%"))

    pills = query.offset(skip).limit(limit).all()
    return pills