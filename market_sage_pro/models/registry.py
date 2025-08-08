from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Generator

import mlflow


@contextmanager
def start_run(name: str) -> Generator[None, None, None]:
    tracking_uri = os.environ.get("MLFLOW_TRACKING_URI", "file:./mlruns")
    mlflow.set_tracking_uri(tracking_uri)
    with mlflow.start_run(run_name=name):
        yield