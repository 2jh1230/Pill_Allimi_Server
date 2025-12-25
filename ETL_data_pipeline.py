import requests
import pandas as pd
from sqlalchemy import create_engine, text
import json

# 1. DB 연결 설정 (ETL 전용 Connection)
# [보안] 실제 운영 시 환경변수로 관리
DB_CONNECTION_STR = 'mysql+pymysql://admin:YOUR_PASSWORD@127.0.0.1:3306/pill_db'
db_connection = create_engine(DB_CONNECTION_STR)

# 2. 공공데이터포털 API 설정
BASE_URL = "http://apis.data.go.kr/1471000/MdcinGrnIdntfcInfoService03/getMdcinGrnIdntfcInfoList03"
SERVICE_KEY = "YOUR_OPEN_API_SERVICE_KEY"  # [보안] API 키 마스킹 처리

def run_etl_pipeline():
    """
    Extract: 공공데이터 API 호출
    Transform: 데이터 정제 및 결측치(NaN) 처리
    Load: MySQL DB 적재 (Bulk Insert & Ignore Duplicates)
    """
    page_no = 1
    num_of_rows = 100
    total_count = 0

    # Bulk Insert 쿼리 (INSERT IGNORE로 중복 데이터 발생 시 오류 없이 Skip)
    insert_query = text("""
        INSERT IGNORE INTO medicine_pill_info (
            ITEM_SEQ, ITEM_NAME, ENTP_SEQ, ENTP_NAME, CHART,
            ITEM_IMAGE, PRINT_FRONT, PRINT_BACK, DRUG_SHAPE,
            COLOR_CLASS1, COLOR_CLASS2, LINE_FRONT, LINE_BACK,
            LENG_LONG, LENG_SHORT, THICK, IMG_REGIST_TS,
            CLASS_NO, CLASS_NAME, ETC_OTC_NAME, ITEM_PERMIT_DATE,
            FORM_CODE_NAME, MARK_CODE_FRONT_ANAL, MARK_CODE_BACK_ANAL,
            MARK_CODE_FRONT_IMG, MARK_CODE_BACK_IMG, ITEM_ENG_NAME,
            CHANGE_DATE, MARK_CODE_FRONT, MARK_CODE_BACK, EDI_CODE,
            BIZRNO, STD_CD
        ) VALUES (
            :ITEM_SEQ, :ITEM_NAME, :ENTP_SEQ, :ENTP_NAME, :CHART,
            :ITEM_IMAGE, :PRINT_FRONT, :PRINT_BACK, :DRUG_SHAPE,
            :COLOR_CLASS1, :COLOR_CLASS2, :LINE_FRONT, :LINE_BACK,
            :LENG_LONG, :LENG_SHORT, :THICK, :IMG_REGIST_TS,
            :CLASS_NO, :CLASS_NAME, :ETC_OTC_NAME, :ITEM_PERMIT_DATE,
            :FORM_CODE_NAME, :MARK_CODE_FRONT_ANAL, :MARK_CODE_BACK_ANAL,
            :MARK_CODE_FRONT_IMG, :MARK_CODE_BACK_IMG, :ITEM_ENG_NAME,
            :CHANGE_DATE, :MARK_CODE_FRONT, :MARK_CODE_BACK, :EDI_CODE,
            :BIZRNO, :STD_CD
        )
    """)

    print(">>> ETL 파이프라인 가동 시작...")

    while True:
        params = {
            'serviceKey': SERVICE_KEY,
            'pageNo': page_no,
            'numOfRows': num_of_rows,
            'type': 'json'
        }

        try:
            response = requests.get(BASE_URL, params=params)

            if response.status_code != 200:
                print(f"[Error] API Status Code: {response.status_code}")
                break

            try:
                data = response.json()
            except json.JSONDecodeError:
                print(f"[Error] JSON Parsing Failed. Check Response.")
                break

            body = data.get('body')
            if not body:
                break

            items = body.get('items')
            if not items:
                print(f"수집 종료 (Total Saved: {total_count}건)")
                break

            # Data Transformation (Pandas)
            df = pd.DataFrame(items)
            
            # MySQL 적재를 위해 NaN 값을 None(NULL)으로 변환
            df = df.where(pd.notnull(df), None)

            # Dictionary List 변환
            data_list = df.to_dict(orient='records')

            # Data Load (Transaction 관리)
            with db_connection.begin() as connection:
                connection.execute(insert_query, data_list)
                
            count = len(df)
            total_count += count
            print(f"Page {page_no} Processed. ({count} rows saved)")

            page_no += 1

        except Exception as e:
            print(f"[System Error] {e}")
            break

if __name__ == "__main__":
    run_etl_pipeline()