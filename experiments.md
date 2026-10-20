# 실험 기록

제출 여부와 관계없이 모든 실험의 교차검증(5-fold) 결과를 남긴다. `src/experiment.py`와 `src/blend.py`를 실행하면 한 줄씩 자동으로 추가된다.
예측 파일과 fold별 로그는 `outputs/<실험>/`(git 제외)에 있고, Kaggle에 낸 결과는 [제출 기록](submissions/README.md)에 따로 남긴다.

| 일시 (KST) | 실험 | 내용 | CV AUC | 시간 | 메모 |
| --- | --- | --- | --- | --- | --- |
| 2026-10-20 17:29 | `lgbm_base_lr0.05` | lgbm, features=base, lr=0.05 | 0.95886 | 117s | 첫 베이스라인. Public LB 0.95849 |
| 2026-10-20 17:42 | `lgbm_fe_lr0.05` | lgbm, features=fe, lr=0.05 | 0.95940 | 119s | 특성 추가 효과 +0.00054 |
| 2026-10-20 17:45 | `xgb_fe_lr0.05` | xgb, features=fe, lr=0.05 | 0.95922 | 144s |  |
| 2026-10-20 17:58 | `cat_fe_lr0.08` | cat, features=fe, lr=0.08 | 0.95917 | 824s |  |
| 2026-10-20 18:15 | `lgbm_fe_lr0.02` | lgbm, features=fe, lr=0.02 | 0.95947 | 961s |  |
| 2026-10-20 18:31 | `blend_lgbm_xgb_cat` | 순위 가중 앙상블: lgbm_fe_lr0.02=0.531, xgb_fe_lr0.05=0.172, cat_fe_lr0.08=0.297 | 0.95963 | 12s | Public LB 0.95910 |
