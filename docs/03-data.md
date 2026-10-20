# 제공 데이터

확인일: **2026-10-20 (KST)**. 공식 정보는 변경될 수 있으므로 제출 전 링크된 원문을 확인한다.

| 파일 | 용도 | 행 수 | 열 수 | Kaggle 표시 크기 |
| --- | --- | ---: | ---: | ---: |
| [`train.csv`](https://www.kaggle.com/competitions/playground-series-s6e10/data?select=train.csv) | 학습용; `satisfaction` 포함 | 699,635 | 23 | 67.25 MB |
| [`test.csv`](https://www.kaggle.com/competitions/playground-series-s6e10/data?select=test.csv) | 예측 대상; `satisfaction` 없음 | 299,844 | 22 | 27.2 MB |
| [`sample_submission.csv`](https://www.kaggle.com/competitions/playground-series-s6e10/data?select=sample_submission.csv) | 제출 형식 예시 | 299,844 | 2 | 8.1 MB |

공식 Data 탭에는 CSV 3개, 전체 **102.54 MB**로 표시된다. 행 수는 Kaggle 데이터 탐색기의 분포 합계와 `id` 범위에서 확인했다. `train.csv`의 `id`는 `0`~`699634`, `test.csv` 및 예시 제출의 `id`는 `699635`~`999478`이다. CSV 원본은 [`datas/`](../datas/)에 보관되어 있다. [출처: Data](https://www.kaggle.com/competitions/playground-series-s6e10/data)

### 학습 데이터 열 목록

공식 데이터 탐색기에 나타나는 **실제 열 이름과 순서**다. `id`는 식별자, `satisfaction`은 목표 열이며 나머지 21개가 입력 특성이다. 열 이름을 바탕으로 한 한국어 설명은 이해를 돕기 위한 번역이며 Kaggle이 제공한 상세 변수 사전은 아니다. [출처: Data → train.csv](https://www.kaggle.com/competitions/playground-series-s6e10/data?select=train.csv)

| 순서 | 열 이름 | 간단한 의미 |
| ---: | --- | --- |
| 1 | `id` | 행 식별자 |
| 2 | `Age` | 나이 |
| 3 | `Flight Distance` | 비행 거리 |
| 4 | `Inflight wifi service` | 기내 와이파이 서비스 평가 |
| 5 | `Departure/Arrival time convenient` | 출발·도착 시간 편의성 평가 |
| 6 | `Ease of Online booking` | 온라인 예약 편의성 평가 |
| 7 | `Gate location` | 탑승구 위치 평가 |
| 8 | `Food and drink` | 음식·음료 평가 |
| 9 | `Online boarding` | 온라인 탑승 수속 평가 |
| 10 | `Seat comfort` | 좌석 편안함 평가 |
| 11 | `Inflight entertainment` | 기내 엔터테인먼트 평가 |
| 12 | `On-board service` | 기내 서비스 평가 |
| 13 | `Leg room service` | 다리 공간 평가 |
| 14 | `Baggage handling` | 수하물 처리 평가 |
| 15 | `Checkin service` | 체크인 서비스 평가 |
| 16 | `Cleanliness` | 청결도 평가 |
| 17 | `Departure Delay in Minutes` | 출발 지연 시간(분) |
| 18 | `Arrival Delay in Minutes` | 도착 지연 시간(분) |
| 19 | `Gender` | 성별 |
| 20 | `Customer Type` | 고객 유형 |
| 21 | `Type of Travel` | 여행 유형 |
| 22 | `Class` | 좌석 등급 |
| 23 | `satisfaction` | 만족 여부: `True` 또는 `False` |

Kaggle 데이터 탐색기에서 `satisfaction`의 분포는 **True 310,339건(약 44.36%)**, **False 389,296건(약 55.64%)**, 결측 0건으로 표시된다. 이 분포는 로컬 CSV에서도 일치했다. [출처: Data → train.csv](https://www.kaggle.com/competitions/playground-series-s6e10/data?select=train.csv)

### 로컬 CSV 대조 결과

2026-10-20에 [`datas/`](../datas/)의 세 파일 전체를 읽어 위 행·열 수와 목표 분포를 대조했다. 세 파일 각각에서 `id`는 고유하다. 빈 문자열로 표시된 값은 `Arrival Delay in Minutes`에만 있었으며, `train.csv` **292건**, `test.csv` **130건**이다. 이 수치는 로컬 CSV 확인 결과이며 Kaggle 페이지의 설명 문구는 아니다.

데이터 라이선스는 [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)이다. 대회 규칙에는 상업적·비상업적 이용이 허용된다고 적혀 있으며, 별도의 데이터 보안 및 재배포 조항도 있다. 데이터를 외부에 공유하려면 [전체 규칙](https://www.kaggle.com/competitions/playground-series-s6e10/rules)을 함께 확인한다. [출처: Data](https://www.kaggle.com/competitions/playground-series-s6e10/data), [Rules](https://www.kaggle.com/competitions/playground-series-s6e10/rules)
