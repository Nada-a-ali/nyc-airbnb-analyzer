"""Command-line interface for the NYC Airbnb analyzer."""
from __future__ import annotations

from pathlib import Path

from .analysis import (
    availability_summary,
    overall_summary,
    price_by_neighbourhood_group,
    price_by_room_type,
)
from .data_loader import load_data

MENU = """
NYC Airbnb Price & Availability Analyzer

1. Overall summary
2. Price by neighbourhood group
3. Summary by room type
4. Availability summary
5. Exit
"""


def _dataset_path() -> Path:
    return Path(__file__).resolve().parents[2] / "data" / "AB_NYC_2019.csv"


def _print_overall(df) -> None:
    result = overall_summary(df)
    print(f"Listings: {result['listing_count']}")
    for label, key in [
        ("Average price", "average_price"),
        ("Median price", "median_price"),
        ("Average availability", "average_availability"),
        ("Median availability", "median_availability"),
    ]:
        value = result[key]
        print(f"{label}: {value if isinstance(value, str) else f'{value:.2f}'}")


def _print_grouped(title: str, result) -> None:
    print(f"\n{title}")
    if result.empty:
        print("No valid price data available for this analysis.")
        return
    print(
        result.to_string(
            index=False,
            formatters={"mean": "{:.2f}".format, "median": "{:.2f}".format},
        )
    )


def _print_availability(df) -> None:
    result = availability_summary(df)
    if "message" in result:
        print(result["message"])
        return
    print(f"Average availability: {result['average']:.2f}")
    print(f"Median availability: {result['median']:.2f}")
    print(f"Zero-availability listings: {result['zero_count']}")
    print(f"Zero-availability percentage: {result['zero_percentage']:.2f}%")


def run_cli(dataset_path: str | Path | None = None) -> None:
    """Run the interactive analyzer."""
    df = load_data(dataset_path or _dataset_path())
    while True:
        print(MENU)
        choice = input("Select an option: ").strip()
        if choice == "1":
            _print_overall(df)
        elif choice == "2":
            _print_grouped(
                "Price by neighbourhood group",
                price_by_neighbourhood_group(df),
            )
        elif choice == "3":
            _print_grouped("Price by room type", price_by_room_type(df))
        elif choice == "4":
            _print_availability(df)
        elif choice == "5":
            print("Goodbye!")
            return
        else:
            print("Invalid choice. Please select an option from 1 to 5.")


if __name__ == "__main__":
    run_cli()
