"""여러 실험의 예측을 순위(rank) 가중 평균으로 섞는다. 가중치는 OOF AUC가 가장 높아지도록 찾는다.

AUC는 예측값의 순서만 보므로, 모델마다 다른 확률 스케일을 순위로 바꿔 맞춘 뒤 평균한다.
결과는 outputs/<이름>/ 에 저장하고 experiments.md 기록표에 한 줄을 추가한다.

실행 예:
    uv run python src/blend.py lgbm_fe_lr0.02 xgb_fe_lr0.05 cat_fe_lr0.08 --name blend_lgbm_xgb_cat
"""

import argparse
import shlex
import sys
import time

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import rankdata
from sklearn.metrics import roc_auc_score

from experiment import ROOT, TARGET, record


def to_rank(x: np.ndarray) -> np.ndarray:
    return rankdata(x) / len(x)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("names", nargs="+", help="outputs/ 아래 실험 폴더 이름")
    parser.add_argument("--name", help="결과 폴더 이름 (기본: blend_ + 실험 이름들)")
    parser.add_argument("--note", default="", help="experiments.md에 남길 메모")
    args = parser.parse_args()
    name = args.name or "blend_" + "+".join(args.names)
    start = time.time()

    y = pd.read_csv(ROOT / "datas" / "train.csv", usecols=[TARGET])[TARGET].astype(int).to_numpy()
    test_id = pd.read_csv(ROOT / "datas" / "test.csv", usecols=["id"])["id"]
    oofs = np.column_stack([to_rank(np.load(ROOT / "outputs" / n / "oof.npy")) for n in args.names])
    preds = np.column_stack([to_rank(np.load(ROOT / "outputs" / n / "pred.npy")) for n in args.names])

    # 섞은 실험들의 실행 명령도 함께 남겨, 이 로그만으로 전체를 재현할 수 있게 한다
    log = []
    for n in args.names:
        first = (ROOT / "outputs" / n / "log.txt").read_text(encoding="utf-8").splitlines()[:1]
        log.append(first[0] if first and first[0].startswith("$") else f"# {n}: 실행 명령 기록 없음")
    log.append(f"$ uv run python src/blend.py {shlex.join(sys.argv[1:])}")
    log += [f"{n:24s} OOF AUC {roc_auc_score(y, col):.5f}" for n, col in zip(args.names, oofs.T)]

    def loss(w):
        w = np.abs(w) / np.abs(w).sum()
        return -roc_auc_score(y, oofs @ w)

    k = len(args.names)
    res = minimize(loss, np.full(k, 1 / k), method="Nelder-Mead", options={"xatol": 1e-3, "fatol": 1e-6})
    w = np.abs(res.x) / np.abs(res.x).sum()
    auc = roc_auc_score(y, oofs @ w)
    weights = ", ".join(f"{n}={v:.3f}" for n, v in zip(args.names, w))

    log.append(f"{'equal weights':24s} OOF AUC {roc_auc_score(y, oofs.mean(axis=1)):.5f}")
    log.append(f"{'optimized weights':24s} OOF AUC {auc:.5f}  {weights}")
    print("\n".join(log))

    out = ROOT / "outputs" / name
    out.mkdir(parents=True, exist_ok=True)
    np.save(out / "oof.npy", oofs @ w)
    np.save(out / "pred.npy", preds @ w)
    pd.DataFrame({"id": test_id, TARGET: preds @ w}).to_csv(out / "submission.csv", index=False)
    (out / "log.txt").write_text("\n".join(log) + "\n", encoding="utf-8")
    record(name, f"순위 가중 앙상블: {weights}", auc, time.time() - start, args.note)
    print(f"저장: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
