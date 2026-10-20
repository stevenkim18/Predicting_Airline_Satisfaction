"""여러 실험의 예측을 순위(rank) 가중 평균으로 섞는다. 가중치는 OOF AUC가 가장 높아지도록 찾는다.

AUC는 예측값의 순서만 보므로, 모델마다 다른 확률 스케일을 순위로 바꿔 맞춘 뒤 평균한다.

실행 예:
    uv run python src/blend.py lgbm_fe_lr0.02 xgb_fe_lr0.05 cat_fe_lr0.08 --out outputs/blend.csv
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import rankdata
from sklearn.metrics import roc_auc_score

ROOT = Path(__file__).resolve().parent.parent


def to_rank(x: np.ndarray) -> np.ndarray:
    return rankdata(x) / len(x)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("names", nargs="+", help="outputs/ 아래 실험 폴더 이름")
    parser.add_argument("--out", type=Path, default=ROOT / "outputs" / "blend.csv")
    args = parser.parse_args()

    y = pd.read_csv(ROOT / "datas" / "train.csv", usecols=["satisfaction"])["satisfaction"].astype(int).to_numpy()
    test_id = pd.read_csv(ROOT / "datas" / "test.csv", usecols=["id"])["id"]
    oofs = np.column_stack([to_rank(np.load(ROOT / "outputs" / n / "oof.npy")) for n in args.names])
    preds = np.column_stack([to_rank(np.load(ROOT / "outputs" / n / "pred.npy")) for n in args.names])

    for n, col in zip(args.names, oofs.T):
        print(f"{n:24s} OOF AUC {roc_auc_score(y, col):.5f}")

    def loss(w):
        w = np.abs(w) / np.abs(w).sum()
        return -roc_auc_score(y, oofs @ w)

    k = len(args.names)
    res = minimize(loss, np.full(k, 1 / k), method="Nelder-Mead", options={"xatol": 1e-3, "fatol": 1e-6})
    w = np.abs(res.x) / np.abs(res.x).sum()

    print(f"{'equal weights':24s} OOF AUC {roc_auc_score(y, oofs.mean(axis=1)):.5f}")
    print(f"{'optimized weights':24s} OOF AUC {-res.fun:.5f}  " + ", ".join(f"{n}={v:.3f}" for n, v in zip(args.names, w)))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame({"id": test_id, "satisfaction": preds @ w}).to_csv(args.out, index=False)
    print(f"저장: {args.out}")


if __name__ == "__main__":
    main()
