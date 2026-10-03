import math

import pandas as pd

from nyc_airbnb.analysis import (
    availability_summary,
    overall_summary,
    price_by_neighbourhood_group,
    price_by_room_type,
)
from nyc_airbnb.data_loader import load_data

FIXTURE = "tests/fixtures/small_airbnb.csv"


def test_overall_summary_uses_only_positive_prices():
    result = overall_summary(load_data(FIXTURE))
    # Valid prices: 100, 200, 50, 1000, 75
    assert result["listing_count"] == 9
    assert result["average_price"] == 285.0
    assert result["median_price"] == 100.0
    assert result["average_availability"] == 93.125
    assert result["median_availability"] == 35.0


def test_grouped_price_statistics():
    df = load_data(FIXTURE)
    groups = price_by_neighbourhood_group(df).set_index("neighbourhood_group")
    assert groups.loc["Manhattan", "count"] == 2
    assert groups.loc["Manhattan", "mean"] == 75
    assert groups.loc["Manhattan", "median"] == 75
    assert groups.loc["Queens", "count"] == 2
    assert groups.loc["Queens", "mean"] == 537.5

    rooms = price_by_room_type(df).set_index("room_type")
    assert rooms.loc["Private room", "count"] == 4
    assert rooms.loc["Private room", "median"] == 87.5


def test_availability_summary():
    result = availability_summary(load_data(FIXTURE))
    assert result["zero_count"] == 2
    assert math.isclose(result["zero_percentage"], 25.0)


def test_no_valid_price_data():
    df = pd.DataFrame(
        {
            "price": [0, -1, "bad", None],
            "availability_365": [1, 2, 3, 4],
            "neighbourhood_group": ["A"] * 4,
            "room_type": ["Private room"] * 4,
        }
    )
    result = overall_summary(df)
    assert result["average_price"] == "No valid data available for this analysis."
    assert result["median_price"] == "No valid data available for this analysis."
    assert price_by_neighbourhood_group(df).empty


def test_no_valid_availability_data():
    df = pd.DataFrame(
        {
            "price": [10],
            "availability_365": [None],
            "neighbourhood_group": ["A"],
            "room_type": ["Private room"],
        }
    )
    assert availability_summary(df) == {
        "message": "No valid data available for this analysis."
    }


def test_empty_data_does_not_crash():
    df = pd.DataFrame(
        columns=["price", "availability_365", "neighbourhood_group", "room_type"]
    )
    result = overall_summary(df)
    assert result["listing_count"] == 0
    assert "No valid" in result["average_price"]


def test_extreme_positive_price_is_retained():
    df = pd.DataFrame(
        {
            "price": [10, 10000],
            "availability_365": [0, 10],
            "neighbourhood_group": ["A", "A"],
            "room_type": ["Private room", "Private room"],
        }
    )
    result = overall_summary(df)
    assert result["average_price"] == 5005
    assert result["median_price"] == 5005
