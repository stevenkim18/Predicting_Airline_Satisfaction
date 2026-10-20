# 추가 자료와 확인 범위

확인일: **2026-10-20 (KST)**. 공식 정보는 변경될 수 있으므로 제출 전 링크된 원문을 확인한다.

아래 영역은 참가자가 계속 게시하거나 순위가 바뀌는 자료다. 이 문서는 공식 고정 정보와 **2026-10-20에 확인한 자료 위치**를 정리한다.

| 영역 | 링크 | 무엇을 볼 수 있나 |
| --- | --- | --- |
| Overview | [대회 소개](https://www.kaggle.com/competitions/playground-series-s6e10/overview) | 과제, 평가, 일정, 시상, 인용 |
| Data | [데이터 설명·탐색기](https://www.kaggle.com/competitions/playground-series-s6e10/data) | 공식 파일, 열, 라이선스 |
| Code | [공개 노트북](https://www.kaggle.com/competitions/playground-series-s6e10/code) | 참가자 코드와 분석 |
| Models | [모델 목록](https://www.kaggle.com/competitions/playground-series-s6e10/models) | 대회 관련 모델 |
| Discussion | [토론 게시판](https://www.kaggle.com/competitions/playground-series-s6e10/discussion) | 질문, 실험 결과, 공지 |
| Leaderboard | [공개 순위](https://www.kaggle.com/competitions/playground-series-s6e10/leaderboard) | 현재 Public 점수와 최종 Private 순위 |
| Rules | [공식 규칙](https://www.kaggle.com/competitions/playground-series-s6e10/rules) | 참가·제출·공유·시상 조건 |

### 토론에서 바로 찾아볼 만한 글

아래는 게시판에서 확인한 **제목과 링크만** 기록했다. 게시글의 실험 결과나 점수를 독립 검증한 것은 아니다.

- [Simple LightGBM baseline: CV 0.95839 / LB 0.95803](https://www.kaggle.com/competitions/playground-series-s6e10/discussion/750195)
- [Six measured facts about this dataset (and what each one changes)](https://www.kaggle.com/competitions/playground-series-s6e10/discussion/745932)
- [Tabular Foundation Models (TFMs) - Intro, Dataset, and Starter!](https://www.kaggle.com/competitions/playground-series-s6e10/discussion/746363)
- [How well does 5-fold CV track the public LB here?](https://www.kaggle.com/competitions/playground-series-s6e10/discussion/749255)
- [How big does a public-LB gain have to be?](https://www.kaggle.com/competitions/playground-series-s6e10/discussion/750480)

## 참가 전 확인할 항목

1. Kaggle에서 [규칙·마감](https://www.kaggle.com/competitions/playground-series-s6e10/rules) 변경 여부를 확인한다.
2. [Data 탭](https://www.kaggle.com/competitions/playground-series-s6e10/data)에서 공식 CSV를 내려받고 `train`/`test`의 열·결측·값을 직접 검증한다.
3. 검증 기준은 ROC AUC로 맞추고, 제출 파일은 `sample_submission.csv`의 `id` 순서와 `id,satisfaction` 헤더를 따른다.
4. 공개 리더보드가 테스트의 약 20%만 반영한다는 점을 고려해 검증 결과와 함께 모델을 판단한다.

### 확인 범위

이 문서의 행 수·열 이름·목표 분포는 처음에 Kaggle 웹 데이터 탐색기에서 확인했다. 이후 사용자가 공식 CSV 3개를 [`datas/`](../datas/)에 보관했고, 행·열 수와 목표 분포, `id`의 고유성, 빈 필드 수를 파일 전체에서 대조했다. 범주값과 중복 특성 행의 분석은 아직 수행하지 않았다. Code, Models, Discussion의 모든 사용자 게시물을 정적 문서로 복제하지 않았으며 위 링크에서 최신 목록을 확인할 수 있다.

추가로 분석할 만한 정보는 범주형 열의 실제 값, 숫자 열의 분포, 중복 특성 행, 검증 분할과 재현 가능한 모델 기준점이다. 이 항목은 Kaggle 대회 페이지 원문 보관과는 별도 분석 작업이다.
