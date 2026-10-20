"""제출 CSV를 submissions/날짜_시간_제목/ 폴더에 복사하고 제출 기록표에 한 줄을 추가한다.

폴더 안에는 같은 이름의 CSV와 메모용 README.md가 생기며, 관련 문서는 이 폴더에 함께 정리한다.

사용 예:
    python3 scripts/save_submission.py 만든파일.csv lgbm-baseline --cv 0.9512 --note "5-fold LightGBM 기본값"
    python3 scripts/save_submission.py datas/sample_submission.csv sample-submission --lb 0.5
"""

import argparse
import csv
import re
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUBMISSIONS = ROOT / "submissions"
LOG = SUBMISSIONS / "README.md"
TEST = ROOT / "datas" / "test.csv"

LOG_HEADER = """# 제출 기록

Kaggle에 제출한 파일과 점수를 시간순으로 남긴다. 제출마다 `YYYYMMDD_HHMM_제목/`(KST) 폴더를 만들고
그 안에 같은 이름의 CSV와 관련 문서를 둔다.
Public LB 점수는 제출 후 Kaggle에서 확인해 채운다.

| 일시 (KST) | 폴더 | 설명 | CV AUC | Public LB | 최종 선택 |
| --- | --- | --- | --- | --- | --- |
"""

NOTE_TEMPLATE = """# {name}

- 제출 일시 (KST): {when}
- 설명: {note}
- 원본 파일: `{source}`
- CV AUC: {cv}
- Public LB: {lb}

## 메모

"""


def check_format(path: Path) -> int:
    """sample_submission과 같은 형식인지 확인하고 행 수를 돌려준다."""
    with path.open(newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        if header != ["id", "satisfaction"]:
            raise SystemExit(f"열 이름이 id,satisfaction 이 아닙니다: {header}")
        ids = []
        for row in reader:
            value = float(row[1])
            if not 0.0 <= value <= 1.0:
                raise SystemExit(f"id {row[0]}의 확률이 0~1 범위를 벗어났습니다: {value}")
            ids.append(row[0])

    with TEST.open(newline="") as f:
        reader = csv.reader(f)
        next(reader)
        test_ids = [row[0] for row in reader]
    if ids != test_ids:
        raise SystemExit(f"id 목록이 test.csv와 다릅니다 (제출 {len(ids)}행, test {len(test_ids)}행)")
    return len(ids)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("csv", type=Path, help="제출할 CSV 경로")
    parser.add_argument("title", help="짧은 영문 제목 (예: lgbm-baseline)")
    parser.add_argument("--note", default="", help="무엇을 바꿨는지 한 줄 설명")
    parser.add_argument("--cv", default="", help="교차검증 AUC")
    parser.add_argument("--lb", default="", help="Public LB 점수 (알고 있으면)")
    args = parser.parse_args()

    title = re.sub(r"[^0-9A-Za-z가-힣_-]+", "-", args.title).strip("-")
    rows = check_format(args.csv)

    now = datetime.now()
    SUBMISSIONS.mkdir(exist_ok=True)
    name = f"{now:%Y%m%d_%H%M}_{title}"
    folder = SUBMISSIONS / name
    if folder.exists():
        raise SystemExit(f"이미 같은 이름의 폴더가 있습니다: {name}")
    folder.mkdir()
    dest = folder / f"{name}.csv"
    shutil.copy2(args.csv, dest)
    (folder / "README.md").write_text(NOTE_TEMPLATE.format(
        name=name, when=f"{now:%Y-%m-%d %H:%M}", note=args.note or title,
        source=args.csv, cv=args.cv, lb=args.lb), encoding="utf-8")

    if not LOG.exists():
        LOG.write_text(LOG_HEADER, encoding="utf-8")
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"| {now:%Y-%m-%d %H:%M} | [{name}]({name}/README.md) | {args.note or title} "
                f"| {args.cv} | {args.lb} |  |\n")

    print(f"저장: {folder.relative_to(ROOT)}/ ({rows}행)")
    print(f"기록: {LOG.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
