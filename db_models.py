from sqlalchemy import Column, Integer, String, Text
from database_connection import Base

class Pill(Base):
    """
    [MySQL Table Schema Definition]
    - Table Name: medicine_pill_info
    """
    __tablename__ = "medicine_pill_info"

    # 1. Primary Key
    ITEM_SEQ = Column(String(50), primary_key=True, index=True, comment="품목일련번호")

    # 2. Major Search Columns (Index Applied 🚀)
    # 실제 DB의 VARCHAR 길이와 맞춰주고, 검색 속도를 위해 index=True 설정
    ITEM_NAME = Column(String(300), index=True, comment="품목명") 
    ENTP_NAME = Column(String(200), index=True, comment="업체명")

    # 3. Basic Info
    ENTP_SEQ = Column(String(50), comment="업체일련번호")
    CHART = Column(Text, comment="성상")
    ITEM_IMAGE = Column(Text, comment="큰제품이미지")
    
    # 4. Visual Identification info
    PRINT_FRONT = Column(Text, comment="표시(앞)")
    PRINT_BACK = Column(Text, comment="표시(뒤)")
    DRUG_SHAPE = Column(String(100), comment="의약품제형")
    COLOR_CLASS1 = Column(String(50), comment="색상앞")
    COLOR_CLASS2 = Column(String(50), comment="색상뒤")
    LINE_FRONT = Column(String(100), comment="분할선(앞)")
    LINE_BACK = Column(String(100), comment="분할선(뒤)")
    
    # 5. Dimensions
    LENG_LONG = Column(String(50), comment="크기(장축)")
    LENG_SHORT = Column(String(50), comment="크기(단축)")
    THICK = Column(String(50), comment="크기(두께)")
    
    # 6. Classification & Codes
    IMG_REGIST_TS = Column(String(50))
    CLASS_NO = Column(String(50), comment="분류번호")
    CLASS_NAME = Column(Text, comment="분류명")
    ETC_OTC_NAME = Column(String(50), comment="전문/일반")
    ITEM_PERMIT_DATE = Column(String(50), comment="품목허가일자")
    FORM_CODE_NAME = Column(String(50), comment="제형코드명")
    
    # 7. Analysis Codes & Others
    MARK_CODE_FRONT_ANAL = Column(Text)
    MARK_CODE_BACK_ANAL = Column(Text)
    MARK_CODE_FRONT_IMG = Column(Text)
    MARK_CODE_BACK_IMG = Column(Text)
    
    ITEM_ENG_NAME = Column(Text)
    CHANGE_DATE = Column(String(50))
    MARK_CODE_FRONT = Column(Text)
    MARK_CODE_BACK = Column(Text)
    EDI_CODE = Column(String(50))
    BIZRNO = Column(String(50))
    STD_CD = Column(String(50), comment="표준코드")