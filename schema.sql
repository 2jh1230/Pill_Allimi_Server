-- -----------------------------------------------------
-- Database: pill_db
-- Optimization: 검색 성능 향상을 위한 B-Tree Index 적용 (ITEM_NAME, ENTP_NAME)
-- -----------------------------------------------------

CREATE DATABASE IF NOT EXISTS `pill_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `pill_db`;

DROP TABLE IF EXISTS `medicine_pill_info`;

CREATE TABLE `medicine_pill_info` (
  -- PK: 품목일련번호
  `ITEM_SEQ` varchar(50) NOT NULL COMMENT '품목일련번호(PK)',
  
  -- 주요 검색 컬럼 (인덱스 적용 대상)
  `ITEM_NAME` varchar(300) DEFAULT NULL COMMENT '품목명',
  `ENTP_NAME` varchar(200) DEFAULT NULL COMMENT '업체명',
  
  -- 상세 정보
  `ENTP_SEQ` varchar(50) DEFAULT NULL,
  `CHART` text COMMENT '성상',
  `ITEM_IMAGE` varchar(1000) DEFAULT NULL,
  `PRINT_FRONT` varchar(100) DEFAULT NULL,
  `PRINT_BACK` varchar(100) DEFAULT NULL,
  `DRUG_SHAPE` varchar(100) DEFAULT NULL,
  `COLOR_CLASS1` varchar(100) DEFAULT NULL,
  `COLOR_CLASS2` varchar(100) DEFAULT NULL,
  `LINE_FRONT` varchar(100) DEFAULT NULL,
  `LINE_BACK` varchar(100) DEFAULT NULL,
  `LENG_LONG` varchar(50) DEFAULT NULL,
  `LENG_SHORT` varchar(50) DEFAULT NULL,
  `THICK` varchar(50) DEFAULT NULL,
  `IMG_REGIST_TS` varchar(50) DEFAULT NULL,
  `CLASS_NO` varchar(50) DEFAULT NULL,
  `CLASS_NAME` varchar(100) DEFAULT NULL,
  `ETC_OTC_NAME` varchar(50) DEFAULT NULL,
  `ITEM_PERMIT_DATE` varchar(50) DEFAULT NULL,
  `FORM_CODE_NAME` varchar(100) DEFAULT NULL,
  
  -- 식별 마크 및 코드
  `MARK_CODE_FRONT_ANAL` varchar(200) DEFAULT NULL,
  `MARK_CODE_BACK_ANAL` varchar(200) DEFAULT NULL,
  `MARK_CODE_FRONT_IMG` varchar(1000) DEFAULT NULL,
  `MARK_CODE_BACK_IMG` varchar(1000) DEFAULT NULL,
  `ITEM_ENG_NAME` varchar(300) DEFAULT NULL,
  `CHANGE_DATE` varchar(50) DEFAULT NULL,
  `MARK_CODE_FRONT` varchar(50) DEFAULT NULL,
  `MARK_CODE_BACK` varchar(50) DEFAULT NULL,
  `EDI_CODE` varchar(50) DEFAULT NULL,
  `BIZRNO` varchar(50) DEFAULT NULL,
  `STD_CD` text,
  
  -- 제약 조건 및 인덱스 설정
  PRIMARY KEY (`ITEM_SEQ`),
  KEY `idx_item_name` (`ITEM_NAME`),  -- [최적화] 약 이름 검색 속도 향상
  KEY `idx_entp_name` (`ENTP_NAME`)   -- [최적화] 업체명 필터링 속도 향상
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;