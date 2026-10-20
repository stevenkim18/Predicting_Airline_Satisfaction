# Predicting Airline Satisfaction

Kaggle [Playground Series - Season 6, Episode 10](https://www.kaggle.com/competitions/playground-series-s6e10/overview) 참가 자료를 주제별로 정리했습니다. 공식 페이지 확인일은 **2026-10-20 (KST)**입니다.

| 문서 | 필요한 내용 |
| --- | --- |
| [공식 페이지 원문 목차](docs/00-official-source-map.md) | Kaggle 원문 섹션과 이 저장소의 대응 문서 |
| [대회 소개와 일정](docs/01-overview-and-timeline.md) | 과제, 시리즈 설명, 주최·시상, 마감 시각, 공식 인용 |
| [평가와 제출](docs/02-evaluation-and-submission.md) | ROC AUC, 제출 CSV 형식, 공개·비공개 리더보드 |
| [제공 데이터](docs/03-data.md) | 공식 파일 3개, 행·열 수, 전체 열 이름, 목표값 분포, 라이선스 |
| [참가 규칙](docs/04-rules.md) | 팀·제출 제한, 외부 데이터와 도구, 공유, 순위·수상 조건 |
| [추가 자료와 확인 범위](docs/05-resources.md) | Kaggle 탭 링크, 관련 토론, 아직 확인하지 못한 항목 |

제출 전에는 [공식 일정](https://www.kaggle.com/competitions/playground-series-s6e10/overview)과 [규칙](https://www.kaggle.com/competitions/playground-series-s6e10/rules)의 최신 내용을 다시 확인하세요.

`docs/`는 대회 페이지의 섹션 구성과 내용을 한국어로 정리하고 원문 링크를 보존합니다.

## 폴더 구조

```
├── docs/          대회 정보 정리
├── datas/         Kaggle 원본 CSV 3개 (수정 금지, git 제외)
├── src/           코드
│   ├── experiment.py       모델·특성 조합별 5-fold 실험
│   ├── blend.py            여러 실험의 순위 가중 앙상블
│   └── save_submission.py  제출 CSV 형식 검사 후 submissions/에 보관
├── experiments.md 모든 실험의 CV 기록표
├── submissions/   Kaggle에 낸 제출본 (제출 1건 = 폴더 1개)
└── outputs/       실험 산출물 (git 제외)
```

CSV 파일은 용량과 대회 데이터 재배포 제한 때문에 git에 넣지 않습니다. 새 환경에서는 [Data 탭](https://www.kaggle.com/competitions/playground-series-s6e10/data)에서 CSV 3개를 받아 `datas/`에 둡니다.

## 실행 환경

[uv](https://docs.astral.sh/uv/)로 관리합니다. `uv sync`로 패키지를 설치합니다.

```bash
uv run python src/experiment.py --model lgbm --features fe --lr 0.02   # 실험 → outputs/lgbm_fe_lr0.02/
uv run python src/blend.py lgbm_fe_lr0.02 xgb_fe_lr0.05 cat_fe_lr0.08 --name blend_lgbm_xgb_cat
```

실험마다 `outputs/<이름>/`에 OOF 예측(`oof.npy`), test 예측(`pred.npy`), 제출 형식 CSV, fold별 로그가 생기고 [실험 기록](experiments.md)에 한 줄이 추가됩니다.

## 제출 기록

Kaggle에 낸 제출본은 [`submissions/`](submissions/README.md) 아래에 제출마다 `YYYYMMDD_HHMM_제목/`(KST) 폴더를 만들어 CSV와 관련 문서를 함께 보관하고, [제출 기록표](submissions/README.md)에 설명·CV·Public LB 점수를 남깁니다. 새 제출본은 아래 명령으로 형식을 검사한 뒤 저장합니다.

```bash
uv run python src/save_submission.py outputs/<실험>/submission.csv 짧은-제목 --cv 0.95 --note "무엇을 바꿨는지"
```
