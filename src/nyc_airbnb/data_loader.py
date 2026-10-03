"""Load, validate, and clean the Airbnb dataset."""
from pathlib import Path
from typing import Iterable

import pandas as pd

REQUIRED_COLUMNS = {
    "price",
    "availability_365",
    "neighbourhood_group",
    "room_type",
}


def load_data(path: str | Path) -> pd.DataFrame:
    """Load the CSV and apply the project's documented cleaning rules."""
    csv_path = Path(path)
    if not csv_path.is_file():
        raise FileNotFoundError(f"Dataset not found: {csv_path}")

    df = pd.read_csv(csv_path)
    validate_required_columns(df.columns)
    return clean_data(df)


def validate_required_columns(columns: Iterable[str]) -> None:
    """Raise ValueError when required analysis columns are missing."""
    missing = sorted(REQUIRED_COLUMNS - set(columns))
    if missing:
        raise ValueError(f"Dataset is missing required columns: {', '.join(missing)}")


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with numeric analysis fields normalized.

    Price is numeric-coerced; price validity is applied by analysis functions.
    Availability is numeric-coerced and missing values remain missing so that
    availability analysis can use only valid observations. Other columns are
    not globally filtered.
    """
    validate_required_columns(df.columns)
    cleaned = df.copy()
    cleaned["price"] = pd.to_numeric(cleaned["price"], errors="coerce")
    cleaned["availability_365"] = pd.to_numeric(
        cleaned["availability_365"], errors="coerce"
    )
    return cleaned
