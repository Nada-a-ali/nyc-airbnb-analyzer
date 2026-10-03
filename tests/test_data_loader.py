from pathlib import Path

import pandas as pd
import pytest

from nyc_airbnb.data_loader import clean_data, load_data, validate_required_columns

FIXTURE = Path(__file__).parent / "fixtures" / "small_airbnb.csv"


def test_load_and_clean_fixture():
    df = load_data(FIXTURE)
    assert len(df) == 9
    assert df.loc[0, "price"] == 100
    assert pd.isna(df.loc[5, "price"])


def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_data("does-not-exist.csv")


def test_required_columns_are_validated():
    with pytest.raises(ValueError, match="room_type"):
        validate_required_columns(["price", "availability_365", "neighbourhood_group"])


def test_cleaning_does_not_drop_rows_globally():
    raw = pd.DataFrame(
        {
            "price": [100, 0, -1, "bad", None],
            "availability_365": [1, 2, 3, 4, None],
            "neighbourhood_group": ["A"] * 5,
            "room_type": ["Private room"] * 5,
        }
    )
    cleaned = clean_data(raw)
    assert len(cleaned) == 5
    assert cleaned["price"].isna().sum() == 2
