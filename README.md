# 8조 리테일 – 온라인 리테일 RFM 분석

**파레토 73.5% 검증 + R·F 기반 4세그먼트(충성·신규·이탈위험·이탈) 및 이탈위험 집중 전략**을 도출한 온라인 리테일 고객 분석 프로젝트입니다.

---

## 목적

- **고객 가치 불균형 검증**: 파레토 법칙 (상위 20% 고객 = 73.5% 매출)
- **R·F 기반 세그먼트 분류**: 충성(R≥4 & F≥4), 신규(R≥4 & F<4), 이탈위험(R<4 & F≥4), 이탈(R<4 & F<4)
- M(Monetary)은 **결과 변수**이므로 분류 기준에서 제외, 순환 논리 방지
- 세그먼트별 차별화 마케팅 전략 수립 (충성·이탈위험 집중 투자 권장)

## 데이터

- **원본**: `데이터셋/Online_Retail.csv`
- **전처리**: 00_전처리_코드정리 실행 → `분석 과정/전처리_완료.csv`
- **분석 대상**: 회원(CustomerID 유효) 기준 고객 수·**회원만의 거래 건수** (전처리 후 회원 필터 적용)

### 데이터셋 출처

- **UCI Machine Learning Repository – Online Retail**  
  [Online Retail (UCI)](https://archive.ics.uci.edu/dataset/352/online+retail)  
  UK 기반 온라인 리테일 거래 데이터(2010-12 ~ 2011-09). Python에서는 `pip install ucimlrepo` 후 `fetch_ucirepo(id=352)`로 불러올 수 있습니다.  
  논문: Chen, D. et al. (2012), "Data mining for the online retail industry: A case study of RFM model-based customer segmentation using data mining", *Journal of Database Marketing and Customer Strategy Management*, Vol. 19, No. 3.

## 시작하기

1. **환경 설정**  
   `pip install -r requirements.txt`

2. **데이터 준비**  
   [UCI Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail)에서 CSV를 다운로드한 뒤 `데이터셋/Online_Retail.csv`로 저장합니다.  
   `분석 과정/`을 작업 디렉터리로 두면 00번 노트북이 `../데이터셋/Online_Retail.csv`를 참조합니다.

3. **실행 순서**  
   `분석 과정/`을 작업 디렉터리로 둔 상태에서 순서대로 실행:  
   `00_전처리_코드정리.ipynb` → `01_분석_RFM_코드정리.ipynb` → `02_통계검정_코드정리.ipynb` → `03_시각화_코드정리.ipynb`

## 폴더 구조

| 폴더/파일 | 설명 |
|-----------|------|
| `분석 과정/` | 00_전처리_코드정리, 01_분석_RFM_코드정리, 02_통계검정_코드정리, 03_시각화_코드정리 |
| `데이터셋/` | Online_Retail.csv(원본), 전처리_완료.csv(00 실행 후 분석 과정/에 생성) |
| `docs/` | [한페이지_요약.md](./docs/한페이지_요약.md) |

## 실행 순서·산출물

| 순서 | 노트북 | 내용·산출 |
|------|--------|-----------|
| 1 | `00_전처리_코드정리.ipynb` | 취소·비정상 StockCode 제거 등 → `전처리_완료.csv` |
| 2 | `01_분석_RFM_코드정리.ipynb` | R·F 4세그먼트, 파레토, 상위/전체 세그먼트 요약 |
| 3 | `02_통계검정_코드정리.ipynb` | ANOVA·Kruskal-Wallis·Tukey·Dunn, 효과크기 η², Monetary 분포 |
| 4 | `03_시각화_코드정리.ipynb` | 요일 히트맵·박스플롯·파레토·도넛·ARPU·월별 매출 |

## 핵심 인사이트 (발표용)

- 상위 20% 고객이 매출의 **73.5%** 차지
- 상위 20% 내부에서 이탈위험+충성 = 고객 91.7%, 매출 95.7% → 이 두 그룹에 마케팅 집중 권장
- 통계 검정: ANOVA·사후검정 유의, **효과크기 η²**로 세그먼트가 매출(로그) 변동에서 차지하는 비중 확인 (02 노트북)
- 10–11월 이탈위험 고객 매출 **-84.2%** 감소 → 재구매 유도 전략 필요  
  (계산 근거: 2011년 10월·11월 이탈 위험 세그먼트 매출을 (11월 매출 − 10월 매출) / 10월 매출 × 100 으로 계산, 03 노트북에서 산출)

## 발표 자료

- [PPT_Retail.md](./PPT_Retail.md) – 10분 발표용 슬라이드 가이드·시각화 체크리스트·발표 스크립트

## 한계·향후

- 데이터 기간이 2010-12 ~ 2011-09로 제한되어 있어, 최근 시즌·다른 채널 확장 시 재검증 필요
- R·F 구간(4단 분할) 및 세그먼트 경계는 도메인에 맞게 조정 가능

## 더 읽기

- [docs/한페이지_요약.md](./docs/한페이지_요약.md) – 문제·접근·결과·한계 요약
