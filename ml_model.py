import os
from typing import Dict, List

import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


class HealthSuggestionModel:
    """
    Trains a simple KNN classifier to map health features to a suggestion
    string found in the dataset's `health_suggestion` column.
    """

    def __init__(self):
        self.pipeline: Pipeline | None = None
        self.feature_columns: List[str] = [
            "age",
            "gender_num",
            "height_cm",
            "weight_kg",
            "bmi",
            "sleep_hours",
            "water_liters",
            "exercise_minutes",
        ]

    @staticmethod
    def _gender_to_num(gender: str) -> int:
        g = (gender or "").strip().lower()
        if g == "male":
            return 0
        if g == "female":
            return 1
        return 2

    def fit_from_csv(self, csv_path: str) -> "HealthSuggestionModel":
        df = pd.read_csv(csv_path)

        # Normalize column names presence and derive gender_num
        df["gender_num"] = df["gender"].astype(str).str.lower().map(
            {"male": 0, "female": 1}
        ).fillna(2).astype(int)

        # Ensure required columns exist
        missing = [c for c in self.feature_columns if c not in df.columns]
        if missing:
            raise ValueError(f"Missing columns in CSV: {missing}")

        X = df[self.feature_columns].values
        y = df["health_suggestion"].astype(str).values

        # Simple, robust pipeline
        self.pipeline = Pipeline(
            steps=[
                ("scaler", StandardScaler()),
                ("knn", KNeighborsClassifier(n_neighbors=3)),
            ]
        )
        self.pipeline.fit(X, y)
        return self

    def predict_suggestion(self, data: Dict) -> str:
        if self.pipeline is None:
            raise RuntimeError("Model not trained. Call fit_from_csv first.")

        # Build a single-row feature vector aligned with training columns
        gender_num = self._gender_to_num(data.get("gender", ""))
        features = np.array([
            [
                float(data.get("age", 0)),
                float(gender_num),
                float(data.get("height", 0)),
                float(data.get("weight", 0)),
                float(data.get("bmi", 0)),
                float(data.get("sleep", 0)),
                float(data.get("water", 0)),
                float(data.get("exercise", 0)),
            ]
        ])

        pred = self.pipeline.predict(features)
        return str(pred[0])


# Singleton-style loader
_model: HealthSuggestionModel | None = None


def get_model() -> HealthSuggestionModel:
    global _model
    if _model is None:
        csv_path = os.path.join(os.path.dirname(__file__), "health_training_dataset.csv")
        model = HealthSuggestionModel()
        model.fit_from_csv(csv_path)
        _model = model
    return _model


