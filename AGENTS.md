# 작업 지침

이 저장소는 Kaggle **Predicting Airline Satisfaction (Playground Series S6E10)** 참가 자료를 관리한다.

- `README.md`는 문서 목차, `docs/`는 대회 정보, `datas/`는 Kaggle에서 받은 CSV 원본, `src/`는 코드, `outputs/`는 실험 산출물(git 제외)이다.
- CSV 파일(`*.csv`)은 git에 넣지 않는다.
- `datas/`의 원본 파일은 수정하지 않는다. 분석 결과나 파생 파일은 별도 경로에 저장한다.
- 일정·평가·규칙을 수정할 때는 [Kaggle 공식 대회 페이지](https://www.kaggle.com/competitions/playground-series-s6e10/overview)를 확인하고 문서에 출처 링크와 확인일을 남긴다.
- 웹페이지 문장을 길게 복제하지 말고, 원문 섹션 이름과 링크를 보존하며 내용을 정확히 요약한다. 확인되지 않은 내용은 추정으로 표시한다.
- 데이터 수치나 열 구성을 적을 때는 가능하면 `datas/`의 실제 CSV로 검증한다. 대용량 CSV를 문서나 도구 출력에 통째로 표시하지 않는다.
- `docs/` 구조를 바꾸면 `README.md`와 `docs/00-official-source-map.md`의 링크도 함께 갱신한다.
- Kaggle에 제출하는 CSV는 `uv run python src/save_submission.py <csv> <제목>`으로 `submissions/YYYYMMDD_HHMM_제목/` 폴더(KST)에 같은 이름의 CSV와 메모 README.md로 보관하고, 그 제출과 관련된 문서도 해당 폴더에 정리하며, `submissions/README.md` 기록표에 설명·CV AUC를 남긴다. CSV는 git에 넣지 않으므로 제출 폴더의 README.md가 그 제출의 유일한 기록이다. 저장 직후 README의 '무엇을 바꿨나 (이전 제출 대비)'와 '결과와 배운 점'을 채우고, Public LB 점수를 사용자가 알려주면 `submissions/README.md` 기록표와 해당 폴더 README 요약표 양쪽에 이전 대비 변화와 함께 채운다. 기존 제출본 CSV는 수정하거나 지우지 않는다.
- 실험은 `src/experiment.py`·`src/blend.py`로 돌리며, 결과는 `outputs/<실험>/`에 저장되고 `experiments.md`에 자동 기록된다. 다른 방법으로 실험했다면 `experiments.md`에 직접 한 줄을 남긴다.
