# 제출 기록

Kaggle에 제출한 파일과 점수를 시간순으로 남긴다. 제출마다 `YYYYMMDD_HHMM_제목/`(KST) 폴더를 만들고
그 안에 같은 이름의 CSV와 관련 문서를 둔다.
Public LB 점수는 제출 후 Kaggle에서 확인해 채운다.

| 일시 (KST) | 폴더 | 설명 | CV AUC | Public LB | 최종 선택 |
| --- | --- | --- | --- | --- | --- |
| 2026-10-20 17:22 | [20261020_1722_sample-submission](20261020_1722_sample-submission/README.md) | sample_submission.csv 그대로 제출 (제출 형식 확인용) | - | 0.5 |  |
| 2026-10-20 17:29 | [20261020_1729_lgbm-baseline](20261020_1729_lgbm-baseline/README.md) | LightGBM 5-fold, 원본 특성 그대로 (범주 4개는 category) | 0.95886 | 0.95849 |  |
| 2026-10-20 21:53 | [20261020_2153_blend-lgbm-xgb-cat](20261020_2153_blend-lgbm-xgb-cat/README.md) | 특성 추가 + LightGBM·XGBoost·CatBoost 순위 가중 앙상블 | 0.95963 | 0.95910 |  |
