from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# [보안] 깃허브 업로드용으로 민감 정보는 마스킹 처리했습니다.
# 실제 운영 환경에서는 환경변수(.env) 등을 활용하여 관리합니다.
DB_USER = "admin"
DB_PASSWORD = "YOUR_PASSWORD"  # 비밀번호 수정 필요
DB_HOST = "127.0.0.1"          # localhost
DB_PORT = "3306"
DB_NAME = "pill_db"

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 1. 연결 엔진 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_recycle=3600, # 연결 끊김 방지
)

# 2. 세션 생성 (DB 트랜잭션 관리)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. 모델의 기본 클래스 정의
Base = declarative_base()

# 4. Dependency Injection용 DB 세션 제너레이터
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()