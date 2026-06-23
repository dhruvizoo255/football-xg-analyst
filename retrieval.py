import joblib
import pandas as pd
import numpy as np
from pathlib import Path

ROOT_DIR = Path(__file__).parent

shots_df = pd.read_csv(
    ROOT_DIR / "data" / "shots_df.csv"
)

nn = joblib.load(
    ROOT_DIR / "models" / "nearest_shots.pkl"
) 
def get_similar_shots(
    x,
    y,
    n_neighbors=5
):
    distance = np.sqrt(
        (120 - x) ** 2 +
        (40 - y) ** 2
    )

    distances, indices = nn.kneighbors(
        [[x, y, distance]],
        n_neighbors=n_neighbors
    )

    similar = shots_df.iloc[
        indices[0]
    ].copy()

    columns = [
        "player",
        "team",
        "outcome",
        "statsbomb_xg",
        "x",
        "y"
    ]

    return similar[
        columns
    ]