# 20261020_2153_blend-lgbm-xgb-cat

> 한 줄 요약: 파생 특성을 추가하고 LightGBM·XGBoost·CatBoost를 순위 가중 평균으로 앙상블했다.

| 항목 | 값 |
| --- | --- |
| 제출 일시 (KST) | 2026-10-20 21:53 |
| 이전 제출 | [20261020_1729_lgbm-baseline](../20261020_1729_lgbm-baseline/README.md) |
| CV AUC | 0.95963 (이전 대비 +0.00077) |
| Public LB | 0.95910 (이전 대비 +0.00061) |
| 최종 선택 | |

## 무엇을 바꿨나 (이전 제출 대비)

1. **파생 특성 추가** (`--features fe`)
   - 서비스 평점 13개 요약: 평균·최소·표준편차(0점은 '해당 없음'으로 보고 제외), 합계, 0점 개수, 5점 개수
   - 지연: 도착−출발 지연 차이, 최대 지연
   - 조합: 여행 목적 × 좌석 등급
   - 빈도: Age, Flight Distance, 출발 지연 값이 train+test에서 나온 횟수
2. **모델 3종:** LightGBM(lr 0.02), XGBoost(lr 0.05, depth 7), CatBoost(lr 0.08, depth 7)
3. **앙상블:** 각 모델의 OOF 예측을 순위로 바꾼 뒤, OOF AUC가 최대가 되는 가중치로 평균했다. 가중치: LightGBM 0.531, XGBoost 0.172, CatBoost 0.297

## 결과와 배운 점

| 실험 | CV AUC | 변화 |
| --- | --- | --- |
| 베이스라인 (LightGBM, 원본 특성) | 0.95886 | |
| LightGBM + 특성, lr 0.05 | 0.95940 | 특성 효과 +0.00054 |
| LightGBM + 특성, lr 0.02 | 0.95947 | lr 효과 +0.00007 |
| XGBoost + 특성, lr 0.05 | 0.95922 | |
| CatBoost + 특성, lr 0.08 | 0.95917 | |
| 3개 모델 동일 가중 평균 | 0.95960 | |
| **3개 모델 최적 가중** | **0.95963** | 최고 단일 모델 대비 +0.00016 |

- 가장 큰 효과는 **특성 추가**였다. lr을 낮춘 효과는 작고 학습 시간은 크게 늘었다.
- 단일 모델로는 LightGBM이 가장 좋았지만, 다른 모델을 섞자 점수가 더 올랐다.
- CV 상승분(+0.00077)과 LB 상승분(+0.00061)이 비슷해, CV가 계속 LB를 잘 따라간다.

## 재현 방법

- 당시 코드: git `a4b2c3c` (이 폴더에 사본 `experiment.py`, `blend.py`, 학습 로그 `run2.log`). 당시 `blend.py`는 `--name` 대신 `--out outputs/blend_lgbm_xgb_cat.csv`를 썼다.
- 현재 코드로 재현: 아래 명령의 결과가 제출 파일과 바이트 단위로 같음을 확인했다 (2026-10-20).
  ```bash
  uv run python src/experiment.py --model lgbm --features fe --lr 0.02   # 약 16분
  uv run python src/experiment.py --model xgb  --features fe --lr 0.05   # 약 2.5분
  uv run python src/experiment.py --model cat  --features fe --lr 0.08   # 약 14분
  uv run python src/blend.py lgbm_fe_lr0.02 xgb_fe_lr0.05 cat_fe_lr0.08 --name blend_lgbm_xgb_cat
  # → outputs/blend_lgbm_xgb_cat/submission.csv
  ```

## 제출 파일 정보

CSV는 git에 넣지 않으므로, 다시 만든 파일이 같은지 아래 값으로 확인한다 (`shasum -a 256 파일.csv`). 예측값은 순위 평균이라 0~1 범위에 고르게 퍼져 있다 (AUC에는 영향 없음).

| 항목 | 값 |
| --- | --- |
| 행 수 | 299,844 |
| SHA-256 | `e3589ffabb782b84441bcefefc086a0fca9850b51898428963b3fb4961d7df54` |
| 예측 평균 / 최소 / 최대 | 0.5000 / 0.0000 / 1.0000 |
