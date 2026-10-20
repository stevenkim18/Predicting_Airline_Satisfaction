"""제출 CSV를 submissions/날짜_시간_제목/ 폴더에 복사하고 제출 기록표에 한 줄을 추가한다.

CSV는 git에 넣지 않으므로 폴더의 README.md가 제출의 기록이 된다. README에는 요약표,
이전 제출 대비 변화, 재현 방법(git 커밋·실험 로그), 파일 지문(SHA-256)이 자동으로 채워지고,
'무엇을 바꿨나'와 '결과와 배운 점'은 제출 후 직접 채운다.

사용 예:
    uv run python src/save_submission.py outputs/lgbm_fe_lr0.02/submission.csv lgbm-fe --cv 0.95947 --note "특성 추가"
"""

import argparse
import csv
import hashlib
import re
import shutil
import subprocess
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

> 한 줄 요약: {note}

| 항목 | 값 |
| --- | --- |
| 제출 일시 (KST) | {when} |
| 이전 제출 | {prev_link} |
| CV AUC | {cv} |
| Public LB | {lb} |
| 최종 선택 | |

## 무엇을 바꿨나 (이전 제출 대비)

- (작성)

## 결과와 배운 점

- (작성)

## 재현 방법

- 코드 버전: git `{commit}`{dirty}
- 원본 파일: `{source}`
{log}
## 제출 파일 정보

CSV는 git에 넣지 않으므로, 다시 만든 파일이 같은지 아래 값으로 확인한다 (`shasum -a 256 파일.csv`).

| 항목 | 값 |
| --- | --- |
| 행 수 | {rows:,} |
| SHA-256 | `{sha256}` |
| 예측 평균 / 최소 / 최대 | {mean:.4f} / {min:.4f} / {max:.4f} |
"""


def check_format(path: Path) -> list[float]:
    """sample_submission과 같은 형식인지 확인하고 예측값 목록을 돌려준다."""
    with path.open(newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        if header != ["id", "satisfaction"]:
            raise SystemExit(f"열 이름이 id,satisfaction 이 아닙니다: {header}")
        ids, values = [], []
        for row in reader:
            value = float(row[1])
            if not 0.0 <= value <= 1.0:
                raise SystemExit(f"id {row[0]}의 확률이 0~1 범위를 벗어났습니다: {value}")
            ids.append(row[0])
            values.append(value)

    with TEST.open(newline="") as f:
        reader = csv.reader(f)
        next(reader)
        test_ids = [row[0] for row in reader]
    if ids != test_ids:
        raise SystemExit(f"id 목록이 test.csv와 다릅니다 (제출 {len(ids)}행, test {len(test_ids)}행)")
    return values


def previous_submission() -> tuple[str, str]:
    """기록표 마지막 행의 (폴더 이름, CV AUC)를 돌려준다. 없으면 빈 문자열."""
    if not LOG.exists():
        return "", ""
    rows = [line for line in LOG.read_text(encoding="utf-8").splitlines() if re.match(r"\| \d{4}-", line)]
    if not rows:
        return "", ""
    cells = [c.strip() for c in rows[-1].strip("|").split("|")]
    name = re.search(r"\[(.+?)\]", cells[1]).group(1)
    return name, cells[3]


def git_state() -> tuple[str, str]:
    """(HEAD 커밋 해시, 커밋되지 않은 코드 변경이 있으면 경고 문구)."""
    try:
        commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                                capture_output=True, text=True, check=True).stdout.strip()
        changed = subprocess.run(["git", "status", "--porcelain", "src", "pyproject.toml", "uv.lock"],
                                 cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "알 수 없음", ""
    return commit, " (주의: 이 시점에 커밋되지 않은 코드 변경이 있었음. 제출 기록 커밋에 함께 포함할 것)" if changed else ""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("csv", type=Path, help="제출할 CSV 경로")
    parser.add_argument("title", help="짧은 영문 제목 (예: lgbm-baseline)")
    parser.add_argument("--note", default="", help="무엇을 바꿨는지 한 줄 설명")
    parser.add_argument("--cv", default="", help="교차검증 AUC")
    parser.add_argument("--lb", default="", help="Public LB 점수 (알고 있으면)")
    args = parser.parse_args()

    title = re.sub(r"[^0-9A-Za-z가-힣_-]+", "-", args.title).strip("-")
    values = check_format(args.csv)

    now = datetime.now()
    SUBMISSIONS.mkdir(exist_ok=True)
    name = f"{now:%Y%m%d_%H%M}_{title}"
    folder = SUBMISSIONS / name
    if folder.exists():
        raise SystemExit(f"이미 같은 이름의 폴더가 있습니다: {name}")

    prev_name, prev_cv = previous_submission()
    cv = args.cv or "-"
    try:
        cv += f" (이전 대비 {float(args.cv) - float(prev_cv):+.5f})"
    except ValueError:
        pass
    commit, dirty = git_state()
    src = args.csv.resolve()
    source = src.relative_to(ROOT) if src.is_relative_to(ROOT) else src

    # outputs/<실험>/submission.csv 에서 왔다면 그 실험 로그(실행 명령 포함)를 README에 남긴다
    exp_log = args.csv.resolve().parent / "log.txt"
    log = f"- 실험 로그 (`{exp_log.relative_to(ROOT)}`):\n  ```\n" + "".join(
        f"  {line}\n" for line in exp_log.read_text(encoding="utf-8").splitlines()
    ) + "  ```\n" if exp_log.exists() and exp_log.is_relative_to(ROOT) else ""

    folder.mkdir()
    dest = folder / f"{name}.csv"
    shutil.copy2(args.csv, dest)
    (folder / "README.md").write_text(NOTE_TEMPLATE.format(
        name=name, when=f"{now:%Y-%m-%d %H:%M}", note=args.note or title,
        prev_link=f"[{prev_name}](../{prev_name}/README.md)" if prev_name else "없음 (첫 제출)",
        cv=cv, lb=args.lb, commit=commit, dirty=dirty, source=source, log=log,
        rows=len(values), sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),
        mean=sum(values) / len(values), min=min(values), max=max(values),
    ), encoding="utf-8")

    if not LOG.exists():
        LOG.write_text(LOG_HEADER, encoding="utf-8")
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"| {now:%Y-%m-%d %H:%M} | [{name}]({name}/README.md) | {args.note or title} "
                f"| {args.cv} | {args.lb} |  |\n")

    print(f"저장: {folder.relative_to(ROOT)}/ ({len(values)}행)")
    print(f"기록: {LOG.relative_to(ROOT)}")
    print("README의 '무엇을 바꿨나'와 '결과와 배운 점'을 채워 주세요.")


if __name__ == "__main__":
    main()
