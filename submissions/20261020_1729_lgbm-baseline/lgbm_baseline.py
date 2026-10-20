"""LightGBM 5-fold 베이스라인: OOF AUC를 출력하고 test 예측을 제출 형식 CSV로 저장한다.

실행:
    uv run python src/lgbm_baseline.py outputs/lgbm_baseline.csv
"""

import sys
from pathlib import Path

import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold

ROOT = Path(__file__).resolve().parent.parent
TARGET = "satisfaction"
CATEGORICAL = ["Gender", "Customer Type", "Type of Travel", "Class"]
SEED = 42

PARAMS = {
    "objective": "binary",
    "metric": "auc",
    "learning_rate": 0.05,
    "num_leaves": 63,
    "min_child_samples": 50,
    "feature_fraction": 0.8,
    "bagging_fraction": 0.8,
    "bagging_freq": 1,
    "lambda_l2": 1.0,
    "seed": SEED,
    "verbose": -1,
}


def load():
    train = pd.read_csv(ROOT / "datas" / "train.csv")
    test = pd.read_csv(ROOT / "datas" / "test.csv")
    y = train.pop(TARGET).astype(int)
    # train과 test에서 같은 범주 코드를 쓰도록 범주 목록을 맞춘다
    for col in CATEGORICAL:
        cats = sorted(set(train[col]) | set(test[col]))
        train[col] = pd.Categorical(train[col], categories=cats)
        test[col] = pd.Categorical(test[col], categories=cats)
    features = [c for c in train.columns if c != "id"]
    return train, test, y, features


def main(out_path: Path) -> None:
    train, test, y, features = load()
    oof = np.zeros(len(train))
    pred = np.zeros(len(test))

    folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    for fold, (tr_idx, va_idx) in enumerate(folds.split(train, y)):
        dtrain = lgb.Dataset(train.iloc[tr_idx][features], y.iloc[tr_idx])
        dvalid = lgb.Dataset(train.iloc[va_idx][features], y.iloc[va_idx])
        model = lgb.train(
            PARAMS, dtrain, num_boost_round=10000, valid_sets=[dvalid],
            callbacks=[lgb.early_stopping(200, verbose=False)],
        )
        oof[va_idx] = model.predict(train.iloc[va_idx][features], num_iteration=model.best_iteration)
        pred += model.predict(test[features], num_iteration=model.best_iteration) / folds.n_splits
        print(f"fold {fold}: AUC {roc_auc_score(y.iloc[va_idx], oof[va_idx]):.5f} "
              f"(best_iteration {model.best_iteration})", flush=True)

    print(f"OOF AUC: {roc_auc_score(y, oof):.5f}")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame({"id": test["id"], TARGET: pred}).to_csv(out_path, index=False)
    print(f"저장: {out_path}")


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "outputs" / "lgbm_baseline.csv")
