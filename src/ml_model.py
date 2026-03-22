"""
src/ml_model.py — ThreatSense
Machine Learning classifier — Random Forest + Logistic Regression ensemble.

Usage:
  python -m src.ml_model --train
  python -m src.ml_model --predict "Your account is blocked. Act now."
  python -m src.ml_model --evaluate
"""

import json
import os
import sys
import pickle

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.feature_extractor import extract_features, FEATURE_NAMES

BASE_DIR      = os.path.join(os.path.dirname(__file__), "..")
TRAINING_PATH = os.path.join(BASE_DIR, "data", "training_data.json")
MODEL_PATH    = os.path.join(BASE_DIR, "data", "model.pkl")

LABEL_MAP     = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
LABEL_REVERSE = {0: "LOW", 1: "MEDIUM", 2: "HIGH"}


def load_training_data():
    """Load JSON training data → (X, y) arrays."""
    with open(TRAINING_PATH, "r") as f:
        records = json.load(f)
    X, y = [], []
    for rec in records:
        X.append(extract_features(rec["text"]))
        y.append(LABEL_MAP[rec["label"].upper()])
    return X, y


def train(verbose: bool = True) -> dict:
    """Train ThreatSense ML ensemble and save to disk."""
    from sklearn.ensemble      import RandomForestClassifier
    from sklearn.linear_model  import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline      import Pipeline
    from sklearn.model_selection import cross_val_score
    import numpy as np

    X, y = load_training_data()
    X = np.array(X)
    y = np.array(y)

    if verbose:
        print(f"ThreatSense ML — Training on {len(X)} samples  |  "
              f"LOW={y.tolist().count(0)} MEDIUM={y.tolist().count(1)} HIGH={y.tolist().count(2)}")

    rf = RandomForestClassifier(n_estimators=100, max_depth=8,
                                random_state=42, class_weight="balanced")
    lr = Pipeline([
        ("scaler", StandardScaler()),
        ("clf",    LogisticRegression(max_iter=500, random_state=42,
                                      class_weight="balanced")),
    ])

    rf_cv = cross_val_score(rf, X, y, cv=5, scoring="accuracy")
    lr_cv = cross_val_score(lr, X, y, cv=5, scoring="accuracy")

    if verbose:
        print(f"  Random Forest CV : {rf_cv.mean()*100:.1f}% ± {rf_cv.std()*100:.1f}%")
        print(f"  Logistic Reg CV  : {lr_cv.mean()*100:.1f}% ± {lr_cv.std()*100:.1f}%")

    rf.fit(X, y)
    lr.fit(X, y)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump({"rf": rf, "lr": lr}, f)

    if verbose:
        print(f"  Model saved → {MODEL_PATH}")
        importances = dict(zip(FEATURE_NAMES, rf.feature_importances_))
        top = sorted(importances.items(), key=lambda x: x[1], reverse=True)[:5]
        print("\n  Top 5 features:")
        for feat, imp in top:
            print(f"    {feat:20s} {imp:.3f}  {'█' * int(imp * 40)}")

    return {"rf_cv_mean": round(rf_cv.mean()*100, 1),
            "lr_cv_mean": round(lr_cv.mean()*100, 1), "n_samples": len(X)}


def _load_models():
    """Load saved ThreatSense ML model bundle."""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"No trained model at {MODEL_PATH}. Run: python main.py --train")
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


def predict(message: str) -> dict:
    """ThreatSense ML prediction for a single message."""
    import numpy as np
    bundle = _load_models()
    rf, lr = bundle["rf"], bundle["lr"]
    feats  = np.array([extract_features(message)])

    rf_pred  = LABEL_REVERSE[rf.predict(feats)[0]]
    lr_pred  = LABEL_REVERSE[lr.predict(feats)[0]]
    rf_proba = rf.predict_proba(feats)[0]
    lr_proba = lr.predict_proba(feats)[0]
    avg      = (rf_proba + lr_proba) / 2.0

    final_idx   = int(avg.argmax())
    final_label = LABEL_REVERSE[final_idx]
    confidence  = round(float(avg[final_idx]), 3)
    probs       = {LABEL_REVERSE[i]: round(float(avg[i]), 3) for i in range(3)}

    return {
        "ml_risk_level": final_label,
        "ml_confidence": confidence,
        "rf_prediction": rf_pred,
        "lr_prediction": lr_pred,
        "agreement":     rf_pred == lr_pred,
        "probabilities": probs,
    }


def evaluate(verbose: bool = True) -> dict:
    """Full ThreatSense ML evaluation with confusion matrix."""
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble        import RandomForestClassifier
    from sklearn.linear_model    import LogisticRegression
    from sklearn.preprocessing   import StandardScaler
    from sklearn.pipeline        import Pipeline
    from sklearn.metrics         import classification_report, confusion_matrix
    import numpy as np

    X, y = load_training_data()
    X, y = np.array(X), np.array(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y)

    rf = RandomForestClassifier(n_estimators=100, max_depth=8,
                                random_state=42, class_weight="balanced")
    lr = Pipeline([("scaler", StandardScaler()),
                   ("clf", LogisticRegression(max_iter=500, random_state=42,
                                              class_weight="balanced"))])
    rf.fit(X_train, y_train)
    lr.fit(X_train, y_train)

    avg    = (rf.predict_proba(X_test) + lr.predict_proba(X_test)) / 2.0
    y_pred = avg.argmax(axis=1)

    labels   = ["LOW", "MEDIUM", "HIGH"]
    report   = classification_report(y_test, y_pred, target_names=labels, output_dict=True)
    cm       = confusion_matrix(y_test, y_pred).tolist()
    accuracy = round(report["accuracy"] * 100, 1)

    if verbose:
        print(f"\n{'═'*52}")
        print(f"  ThreatSense ML Evaluation  (25% test split)")
        print(f"{'═'*52}")
        print(f"  Overall Accuracy : {accuracy}%")
        print(f"\n  Per-class metrics:")
        for lbl in labels:
            m = report[lbl]
            print(f"    {lbl:6s}  precision={m['precision']:.2f}  "
                  f"recall={m['recall']:.2f}  f1={m['f1-score']:.2f}")
        print(f"\n  Confusion Matrix (rows=actual, cols=predicted):")
        print(f"             LOW  MED  HIGH")
        for i, row in enumerate(cm):
            print(f"    {labels[i]:6s}  {row}")
        print(f"{'═'*52}")

    return {"accuracy": accuracy, "report": report, "confusion_matrix": cm}


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] == "--train":
        print("\n🤖 ThreatSense — Training ML model...\n")
        train(verbose=True)
        print("\n✅ Training complete.")
    elif args[0] == "--predict":
        msg    = " ".join(args[1:]) if len(args) > 1 else input("Message: ")
        result = predict(msg)
        print(f"\n🤖 ThreatSense ML : {result['ml_risk_level']}")
        print(f"   Confidence     : {result['ml_confidence']*100:.1f}%")
        print(f"   Probabilities  : {result['probabilities']}")
    elif args[0] == "--evaluate":
        evaluate(verbose=True)
