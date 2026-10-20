# 20261020_2153_blend-lgbm-xgb-cat

- 제출 일시 (KST): 2026-10-20 21:53
- 설명: 특성 추가 + LightGBM·XGBoost·CatBoost 순위 가중 앙상블
- 원본 파일: `outputs/blend_lgbm_xgb_cat.csv`
- CV AUC: 0.95963
- Public LB: 0.95910

## 메모

- 코드: 같은 폴더의 `experiment.py`(모델 학습), `blend.py`(앙상블). 학습 로그는 `run2.log`
- 재현:
  ```bash
  uv run python src/experiment.py --model lgbm --features fe --lr 0.02
  uv run python src/experiment.py --model xgb  --features fe --lr 0.05
  uv run python src/experiment.py --model cat  --features fe --lr 0.08
  uv run python src/blend.py lgbm_fe_lr0.02 xgb_fe_lr0.05 cat_fe_lr0.08 --out outputs/blend_lgbm_xgb_cat.csv
  ```
- 추가 특성(`--features fe`): 평점 평균·최소·표준편차·합계(0점은 '해당 없음'으로 보고 평균에서 제외), 0점·5점 개수, 도착−출발 지연 차이, 최대 지연, 여행 목적×좌석 등급 조합, Age·Flight Distance·출발 지연의 train+test 빈도

| 실험 | OOF AUC |
| --- | --- |
| 베이스라인 (LightGBM, 원본 특성) | 0.95886 |
| LightGBM + 특성, lr 0.05 | 0.95940 |
| LightGBM + 특성, lr 0.02 | 0.95947 |
| XGBoost + 특성, lr 0.05 | 0.95922 |
| CatBoost + 특성, lr 0.08 | 0.95917 |
| 3개 모델 동일 가중 평균 | 0.95960 |
| **3개 모델 최적 가중 (0.531 / 0.172 / 0.297)** | **0.95963** |
