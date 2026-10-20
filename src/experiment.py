"""모델과 특성 조합을 바꿔 가며 5-fold 실험을 돌리는 공용 스크립트.

실험 결과는 outputs/<이름>/ 에 저장하고, experiments.md 기록표에 한 줄을 추가한다.
    oof.npy         train 각 행에 대한 OOF 예측 (앙상블 가중치 찾기에 사용)
    pred.npy        test 예측 (fold 평균)
    submission.csv  제출 형식 CSV
    log.txt         fold별 점수 로그

실행 예:
    uv run python src/experiment.py --model lgbm --features fe --lr 0.05
    uv run python src/experiment.py --model cat --features fe --lr 0.08
    uv run python src/experiment.py --model lgbm --features base --lr 0.05   # 베이스라인
"""

import argparse
import shlex
import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold

ROOT = Path(__file__).resolve().parent.parent
EXPERIMENTS = ROOT / "experiments.md"
TARGET = "satisfaction"
SEED = 42
N_FOLDS = 5

CATEGORICAL = ["Gender", "Customer Type", "Type of Travel", "Class"]
RATINGS = [
    "Inflight wifi service", "Departure/Arrival time convenient", "Ease of Online booking",
    "Gate location", "Food and drink", "Online boarding", "Seat comfort",
    "Inflight entertainment", "On-board service", "Leg room service", "Baggage handling",
    "Checkin service", "Cleanliness",
]


def add_features(df: pd.DataFrame, full: pd.DataFrame) -> pd.DataFrame:
    """평점 요약·지연 관련 특성과 빈도(count) 특성을 추가한다. full은 train+test 전체."""
    df = df.copy()
    ratings = df[RATINGS]
    # 평점 0은 '해당 없음'으로 보고 평균 계산에서 뺀다
    rated = ratings.replace(0, np.nan)
    df["rating_mean"] = rated.mean(axis=1)
    df["rating_min"] = rated.min(axis=1)
    df["rating_std"] = rated.std(axis=1)
    df["rating_sum"] = ratings.sum(axis=1)
    df["rating_zero_count"] = (ratings == 0).sum(axis=1)
    df["rating_5_count"] = (ratings == 5).sum(axis=1)

    dep = df["Departure Delay in Minutes"]
    arr = df["Arrival Delay in Minutes"]
    df["delay_diff"] = arr - dep
    df["delay_max"] = np.maximum(dep, arr.fillna(dep))

    df["travel_class"] = (df["Type of Travel"].astype(str) + "_" + df["Class"].astype(str)).astype("category")

    # 합성 데이터에서는 값이 얼마나 자주 나오는지가 신호가 되는 경우가 많다
    for col in ["Age", "Flight Distance", "Departure Delay in Minutes"]:
        df[f"{col}_count"] = df[col].map(full[col].value_counts())
    return df


def load(features: str):
    train = pd.read_csv(ROOT / "datas" / "train.csv")
    test = pd.read_csv(ROOT / "datas" / "test.csv")
    y = train.pop(TARGET).astype(int)
    for col in CATEGORICAL:
        cats = sorted(set(train[col]) | set(test[col]))
        train[col] = pd.Categorical(train[col], categories=cats)
        test[col] = pd.Categorical(test[col], categories=cats)
    if features == "fe":
        full = pd.concat([train, test], ignore_index=True)
        train, test = add_features(train, full), add_features(test, full)
        cats = sorted(set(train["travel_class"]) | set(test["travel_class"]))
        train["travel_class"] = pd.Categorical(train["travel_class"], categories=cats)
        test["travel_class"] = pd.Categorical(test["travel_class"], categories=cats)
    cols = [c for c in train.columns if c != "id"]
    return train, test, y, cols


def fit_predict(model: str, lr: float, X_tr, y_tr, X_va, y_va, X_te):
    """한 fold를 학습하고 (검증 예측, test 예측, 반복 횟수)를 돌려준다."""
    if model == "lgbm":
        import lightgbm as lgb
        params = {
            "objective": "binary", "metric": "auc", "learning_rate": lr,
            "num_leaves": 63, "min_child_samples": 50, "feature_fraction": 0.8,
            "bagging_fraction": 0.8, "bagging_freq": 1, "lambda_l2": 1.0,
            "seed": SEED, "verbose": -1,
        }
        booster = lgb.train(
            params, lgb.Dataset(X_tr, y_tr), num_boost_round=20000,
            valid_sets=[lgb.Dataset(X_va, y_va)],
            callbacks=[lgb.early_stopping(200, verbose=False)],
        )
        it = booster.best_iteration
        return booster.predict(X_va, num_iteration=it), booster.predict(X_te, num_iteration=it), it

    if model == "xgb":
        import xgboost as xgb
        params = {
            "objective": "binary:logistic", "eval_metric": "auc", "eta": lr,
            "max_depth": 7, "min_child_weight": 5, "subsample": 0.8,
            "colsample_bytree": 0.8, "lambda": 1.0, "tree_method": "hist",
            "max_cat_to_onehot": 1, "seed": SEED,
        }
        dtr = xgb.DMatrix(X_tr, y_tr, enable_categorical=True)
        dva = xgb.DMatrix(X_va, y_va, enable_categorical=True)
        booster = xgb.train(
            params, dtr, num_boost_round=20000, evals=[(dva, "valid")],
            early_stopping_rounds=200, verbose_eval=False,
        )
        rng = (0, booster.best_iteration + 1)
        dte = xgb.DMatrix(X_te, enable_categorical=True)
        return booster.predict(dva, iteration_range=rng), booster.predict(dte, iteration_range=rng), booster.best_iteration

    if model == "cat":
        from catboost import CatBoostClassifier
        cat_cols = [c for c in X_tr.columns if isinstance(X_tr[c].dtype, pd.CategoricalDtype)]
        to_str = lambda X: X.astype({c: str for c in cat_cols})
        clf = CatBoostClassifier(
            iterations=20000, learning_rate=lr, depth=7, eval_metric="AUC",
            od_type="Iter", od_wait=200, random_seed=SEED, thread_count=-1, verbose=False,
            allow_writing_files=False,
        )
        clf.fit(to_str(X_tr), y_tr, cat_features=cat_cols, eval_set=(to_str(X_va), y_va), use_best_model=True)
        return clf.predict_proba(to_str(X_va))[:, 1], clf.predict_proba(to_str(X_te))[:, 1], clf.get_best_iteration()

    raise ValueError(model)


def record(name: str, desc: str, auc: float, seconds: float, note: str) -> None:
    """experiments.md 기록표에 실험 결과 한 줄을 추가한다."""
    with EXPERIMENTS.open("a", encoding="utf-8") as f:
        f.write(f"| {datetime.now():%Y-%m-%d %H:%M} | `{name}` | {desc} | {auc:.5f} | {seconds:.0f}s | {note} |\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=["lgbm", "xgb", "cat"], default="lgbm")
    parser.add_argument("--features", choices=["base", "fe"], default="fe")
    parser.add_argument("--lr", type=float, default=0.05)
    parser.add_argument("--name", help="결과 폴더 이름 (기본: 모델_특성_lr)")
    parser.add_argument("--note", default="", help="experiments.md에 남길 메모")
    args = parser.parse_args()
    name = args.name or f"{args.model}_{args.features}_lr{args.lr}"

    train, test, y, cols = load(args.features)
    oof = np.zeros(len(train))
    pred = np.zeros(len(test))
    start = time.time()
    log = [f"$ uv run python src/experiment.py {shlex.join(sys.argv[1:])}"]

    def say(msg: str) -> None:
        print(msg, flush=True)
        log.append(msg)

    folds = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=SEED)
    for fold, (tr_idx, va_idx) in enumerate(folds.split(train, y)):
        va_pred, te_pred, it = fit_predict(
            args.model, args.lr,
            train.iloc[tr_idx][cols], y.iloc[tr_idx],
            train.iloc[va_idx][cols], y.iloc[va_idx], test[cols],
        )
        oof[va_idx] = va_pred
        pred += te_pred / N_FOLDS
        say(f"[{name}] fold {fold}: AUC {roc_auc_score(y.iloc[va_idx], va_pred):.5f} "
            f"(iter {it}, {time.time() - start:.0f}s)")

    auc = roc_auc_score(y, oof)
    seconds = time.time() - start
    out = ROOT / "outputs" / name
    out.mkdir(parents=True, exist_ok=True)
    np.save(out / "oof.npy", oof)
    np.save(out / "pred.npy", pred)
    pd.DataFrame({"id": test["id"], TARGET: pred}).to_csv(out / "submission.csv", index=False)
    say(f"[{name}] OOF AUC: {auc:.5f} ({seconds:.0f}s) → {out.relative_to(ROOT)}")
    (out / "log.txt").write_text("\n".join(log) + "\n", encoding="utf-8")
    record(name, f"{args.model}, features={args.features}, lr={args.lr}", auc, seconds, args.note)


if __name__ == "__main__":
    main()
