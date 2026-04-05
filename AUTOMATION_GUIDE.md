# 자동 실행 가이드

이 저장소는 원본 노트북을 분석 기록으로 유지하면서, 재현성을 위해 별도의 실행 진입점도 함께 제공합니다.

## 변경 내용

- `run_pipeline.py`가 원본 노트북을 수정하지 않고 전체 흐름을 실행합니다.
- 실행된 노트북 사본은 `artifacts/executed_notebooks/`에 저장됩니다.
- 실행 로그는 `artifacts/logs/`에 저장됩니다.

## 로컬 실행

```bash
pip install -r requirements.txt
python run_pipeline.py
```

Windows 재현 실행:

```bash
python -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install pandas numpy matplotlib seaborn scipy scikit-learn statsmodels scikit-posthocs nbconvert nbclient ipykernel jupyter-core jupyter-client nbformat pywin32
.\.venv\Scripts\python run_pipeline.py --clear-artifacts --stop-on-error
```

선택 실행 명령:

```bash
python run_pipeline.py --clear-artifacts
python run_pipeline.py --stop-on-error
python run_pipeline.py --notebook 00_전처리_코드정리.ipynb --notebook 01_분석_RFM_코드정리.ipynb
```

## GitHub 정리 기준

- 원본 노트북은 `분석 과정/`에 유지
- 원본 CSV 파일은 Git에 포함하지 않음
- 생성된 노트북 사본과 로그는 `artifacts/` 아래에 관리
- 선별된 정적 결과 이미지는 `리테일_시각화_png/`에 유지
- 메인 README에 입력 파일명과 한 줄 실행 경로를 문서화
- 필수 입력 파일: `데이터셋/Online_Retail.csv`
- 생성 중간 CSV: `분석 과정/전처리_완료.csv`
