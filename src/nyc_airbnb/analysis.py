"""Pure analysis functions for cleaned Airbnb data."""
from __future__ import annotations

import pandas as pd

NO_DATA = "No valid data available for this analysis."


def _valid_price_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned["price"] = pd.to_numeric(cleaned["price"], errors="coerce")
    return cleaned.loc[cleaned["price"].notna() & (cleaned["price"] > 0)].copy()


def _valid_availability_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned["availability_365"] = pd.to_numeric(
        cleaned["availability_365"], errors="coerce"
    )
    return cleaned.loc[cleaned["availability_365"].notna()].copy()


def overall_summary(df: pd.DataFrame) -> dict[str, float | int | str]:
    """Return listing count plus overall price and availability statistics."""
    prices = _valid_price_data(df)["price"]
    availability = _valid_availability_data(df)["availability_365"]
    result: dict[str, float | int | str] = {"listing_count": int(len(df))}
    result["average_price"] = float(prices.mean()) if not prices.empty else NO_DATA
    result["median_price"] = float(prices.median()) if not prices.empty else NO_DATA
    result["average_availability"] = (
        float(availability.mean()) if not availability.empty else NO_DATA
    )
    result["median_availability"] = (
        float(availability.median()) if not availability.empty else NO_DATA
    )
    return result


def price_by_neighbourhood_group(df: pd.DataFrame) -> pd.DataFrame:
    """Return valid-price count, mean, and median for each actual group."""
    valid = _valid_price_data(df)
    if valid.empty:
        return pd.DataFrame(columns=["neighbourhood_group", "count", "mean", "median"])
    return (
        valid.groupby("neighbourhood_group", dropna=True)["price"]
        .agg(count="count", mean="mean", median="median")
        .reset_index()
        .sort_values("neighbourhood_group")
        .reset_index(drop=True)
    )


def price_by_room_type(df: pd.DataFrame) -> pd.DataFrame:
    """Return valid-price count, mean, and median for each actual room type."""
    valid = _valid_price_data(df)
    if valid.empty:
        return pd.DataFrame(columns=["room_type", "count", "mean", "median"])
    return (
        valid.groupby("room_type", dropna=True)["price"]
        .agg(count="count", mean="mean", median="median")
        .reset_index()
        .sort_values("room_type")
        .reset_index(drop=True)
    )


def availability_summary(df: pd.DataFrame) -> dict[str, float | int | str]:
    """Return the four required availability measures or a no-data result."""
    availability = _valid_availability_data(df)["availability_365"]
    if availability.empty:
        return {"message": NO_DATA}
    zero_count = int((availability == 0).sum())
    return {
        "average": float(availability.mean()),
        "median": float(availability.median()),
        "zero_count": zero_count,
        "zero_percentage": float(zero_count / len(availability) * 100),
    }
