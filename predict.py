import joblib
import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).parent

MODEL_PATH = ROOT_DIR / "models" / "logistic_xg.pkl"

model = joblib.load(MODEL_PATH)


def predict_xg(
    x,
    y,
    body_part,
    technique,
    shot_type,
    play_pattern,
    under_pressure,
    first_time
):
    input_df = pd.DataFrame(
        [{
            "x": x,
            "y": y,
            "body_part": body_part,
            "technique": technique,
            "shot_type": shot_type,
            "play_pattern": play_pattern,
            "under_pressure": under_pressure,
            "first_time": first_time
        }]
    )

    probability = model.predict_proba(input_df)[0][1]

    return float(probability)