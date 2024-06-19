#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
import csv
from collections.abc import Generator
from pathlib import Path

import pandas as pd
from geopy import ArcGIS
from tqdm import tqdm

data_dir = Path(__file__).parent / "data"


def norm(addr: str) -> str:
    """Normalize address, for comparisons."""
    return addr.replace("'", "").upper().strip()


def _read_known_locations(output_csv: Path) -> set[str]:
    """Before we start appending to the output file, it helps to know what's already there."""
    known_locations: set[str] = set()
    if output_csv.exists():
        with open(output_csv, "r") as fin:
            sheet = csv.DictReader(fin)
            for row in sheet:
                # address = f"{norm(row["address"])}, {row["city"]} {row["st"]} {row["zip"]}"
                # For now we take advantage of e.g. 10 Main St not being in multiple cities.
                known_locations.add(norm(row["address"]))
    return known_locations


def geocode(output_csv: Path) -> Generator[dict[str, str | float], None, None]:
    """Adds lat, lon columns to df."""

    known_locations = _read_known_locations(output_csv)

    with open(output_csv, "w") as fout:
        fields = "address,city,st,zip,housenum,street,lat,lon"
        sheet = csv.DictWriter(fout, fieldnames=fields.split(","))
        if len(known_locations) == 0:
            sheet.writeheader()

        geolocator = ArcGIS()
        rows = pd.read_csv(data_dir / "resident_addr.csv").iterrows()
        for _, row in tqdm(rows):
            if norm(row.address) in known_locations:
                continue
            addr = f"{row.address}, {row.city}, {row.st} {row.zip}"
            if location := geolocator.geocode(addr):
                row = dict(row)
                row["address"] = norm(row["address"])
                row["lat"] = round(location.latitude, 5)
                row["lon"] = round(location.longitude, 5)
                sheet.writerow(row)
                fout.flush()  # for benefit of tail -f
                yield dict(row)
            else:
                print(f"Could not geocode {addr}")


def main(output_csv: Path = data_dir / "geocoded.csv") -> None:
    df = pd.DataFrame(geocode(output_csv))
    print(df)


if __name__ == "__main__":
    main()
