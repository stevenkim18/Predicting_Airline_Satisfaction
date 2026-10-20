# 평가와 제출

확인일: **2026-10-20 (KST)**. 공식 정보는 변경될 수 있으므로 제출 전 링크된 원문을 확인한다.

## 평가 방식

- 평가값은 예측 확률과 실제 정답 사이의 **ROC AUC**다. 확률의 순위가 중요하며, `True`/`False` 또는 0/1로 결정한 최종 분류값 대신 확률을 제출한다. [출처: Overview → Evaluation](https://www.kaggle.com/competitions/playground-series-s6e10/overview)
- 테스트의 모든 `id`에 대해 `id,satisfaction` 두 열과 헤더를 포함한다. 열 이름의 대소문자와 철자를 그대로 사용한다. [출처: Overview → Submission File](https://www.kaggle.com/competitions/playground-series-s6e10/overview)

## 리더보드

공개 리더보드는 테스트 데이터의 **약 20%**, 최종 순위를 정하는 비공개 리더보드는 나머지 **약 80%**를 사용한다. 공개 순위와 최종 순위가 달라질 수 있다. [출처: Leaderboard](https://www.kaggle.com/competitions/playground-series-s6e10/leaderboard)

## 제출 파일

제출 파일 형식 예시:

```csv
id,satisfaction
699635,0.2
699636,0.3
699637,0.1
```

`sample_submission.csv`는 형식 확인용 예시 파일이다. 데이터 탐색기에는 모든 `satisfaction` 값이 약 `0.44357272006117476`으로 표시된다. 이를 학습된 예측으로 해석하지 않는다. [출처: Data → sample_submission.csv](https://www.kaggle.com/competitions/playground-series-s6e10/data?select=sample_submission.csv)

제출 직전에는 테스트 `id` 299,844개와 제출 파일의 `id`가 일치하는지, 결측·중복 `id`가 없는지, 확률값이 0~1 범위인지 확인한다. 이는 공식 형식을 지키기 위한 작업 체크 항목이다.
