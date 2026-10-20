# 20261020_1729_lgbm-baseline

> 한 줄 요약: 원본 특성만으로 LightGBM 5-fold 베이스라인을 만들었다.

| 항목 | 값 |
| --- | --- |
| 제출 일시 (KST) | 2026-10-20 17:29 |
| 이전 제출 | [20261020_1722_sample-submission](../20261020_1722_sample-submission/README.md) |
| CV AUC | 0.95886 |
| Public LB | 0.95849 (이전 대비 +0.45849) |
| 최종 선택 | |

## 무엇을 바꿨나 (이전 제출 대비)

- 처음으로 모델을 학습했다. 원본 특성 21개를 그대로 쓰고, 범주형 4개(Gender, Customer Type, Type of Travel, Class)만 category 타입으로 지정했다.
- LightGBM (`learning_rate=0.05`, `num_leaves=63`, early stopping 200), StratifiedKFold 5-fold. test 예측은 5개 fold 모델의 평균이다.
- 결측치(`Arrival Delay in Minutes` 422개)는 LightGBM의 기본 처리에 맡겼다.

## 결과와 배운 점

- fold별 AUC: 0.95905 / 0.95773 / 0.95959 / 0.95890 / 0.95913 (best_iteration 256~622). fold 간 차이가 작아 결과가 안정적이다.
- CV 0.95886, LB 0.95849로 차이가 0.0004에 그친다. **CV를 기준으로 실험을 판단해도 된다**는 근거가 됐다.

## 재현 방법

- 당시 코드: git `f1f486f`의 `src/lgbm_baseline.py` (이 폴더에 사본 `lgbm_baseline.py`)
  ```bash
  uv run python src/lgbm_baseline.py outputs/lgbm_baseline.csv
  ```
- 현재 코드로 재현: 아래 명령의 결과가 제출 파일과 바이트 단위로 같음을 확인했다 (2026-10-20).
  ```bash
  uv run python src/experiment.py --model lgbm --features base --lr 0.05
  # → outputs/lgbm_base_lr0.05/submission.csv
  ```
- 학습 시간: 약 2분 (Apple Silicon 10코어)

## 제출 파일 정보

CSV는 git에 넣지 않으므로, 다시 만든 파일이 같은지 아래 값으로 확인한다 (`shasum -a 256 파일.csv`).

| 항목 | 값 |
| --- | --- |
| 행 수 | 299,844 |
| SHA-256 | `e83c34d904b86565dd089329bf57be413af8e39617bfec47bb33c2021507d29d` |
| 예측 평균 / 최소 / 최대 | 0.4437 / 0.0036 / 0.9885 |
