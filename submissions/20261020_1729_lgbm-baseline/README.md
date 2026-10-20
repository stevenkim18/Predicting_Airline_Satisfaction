# 20261020_1729_lgbm-baseline

- 제출 일시 (KST): 2026-10-20 17:29
- 설명: LightGBM 5-fold, 원본 특성 그대로 (범주 4개는 category)
- 원본 파일: `outputs/lgbm_baseline.csv`
- CV AUC: 0.95886
- Public LB: 0.95849

## 메모

- 코드: 같은 폴더의 `lgbm_baseline.py` (실행: `uv run python src/lgbm_baseline.py outputs/lgbm_baseline.csv`)
- fold별 AUC: 0.95905 / 0.95773 / 0.95959 / 0.95890 / 0.95913 (best_iteration 256~622)
- 학습 시간: 약 2분 (M 시리즈 10코어)
