import os

# Qlib's recorder (qrun / R.start) uses MLflow's local file store (./mlruns).
# Recent MLflow releases refuse the file store unless explicitly allowed, which
# makes every backtest fail with "No result file found". Opt in by default; the
# variable is inherited by the qrun subprocess. Users can still override it.
os.environ.setdefault("MLFLOW_ALLOW_FILE_STORE", "true")
