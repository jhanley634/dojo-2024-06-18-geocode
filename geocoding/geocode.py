#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
"""
Geocode residential addresses, appending lat, lon columns to a csv file.

Consumes data/resident_addr.csv, produces geocoded.csv.

We continuously append geocoded results to the output .CSV,
so that we can CTRL/C and restart the process without losing any work.
We deliberately discard less than 1% of results, based on address hash,
so there's always at least a little work for the API client to do.
"""
import csv
import zlib
from collections.abc import Generator
from pathlib import Path
from time import sleep

import pandas as pd
from geopy import ArcGIS
from tqdm import tqdm

data_dir = Path(__file__).parent / "data"


def _unit_hash(s: str) -> float:
    """Returns a value on the unit interval: [0, 1)."""
    return zlib.crc32(s.encode()) / 2**32


def sorted_subset(csv: Path, frac: float = 0.995) -> pd.DataFrame:
    """Returns a subset of the csv, sorted by address."""
    df = pd.read_csv(csv)
    df = df.sort_values(["street", "housenum"])
    df["hash"] = df.address.apply(_unit_hash)
    df = df[df["hash"] < frac]
    df = df.drop(columns=["hash"])
    return df


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

    def _locations_to_lookup(i_row: tuple[int, pd.Series]) -> bool:
        i, row = i_row
        if i == 0:
            # Always lookup at least one row, so we have a non-empty dataframe.
            return True
        return row.address not in known_locations  # Is it interesting? Then look it up.

    with open(output_csv, "a") as fout:
        fields = "address,city,st,zip,housenum,street,lat,lon"
        sheet = csv.DictWriter(fout, fieldnames=fields.split(","), lineterminator="\n")
        if len(known_locations) == 0:
            sheet.writeheader()

        geolocator = ArcGIS()
        df = pd.read_csv(data_dir / "resident_addr.csv")
        rows = filter(_locations_to_lookup, df.iterrows())
        for _, row in tqdm(rows):
            if norm(row.address) in known_locations:
                continue
            sleep(1.2)
            addr = f"{row.address}, {row.city}, {row.st} {row.zip}"
            if location := geolocator.geocode(addr):
                row["zip"] = location.address.split()[-1]
                int(row.zip)  # verify it's valid

                known_locations.add(norm(row.address))  # e.g. apt 3 + apt 4
                row["address"] = norm(row.address)
                row["lat"] = round(location.latitude, 5)
                row["lon"] = round(location.longitude, 5)
                row = dict(row)
                sheet.writerow(row)
                fout.flush()  # for benefit of tail -f
                yield dict(row)
            else:
                print(f"Could not geocode {addr}")


def main(output_csv: Path = data_dir / "geocoded.csv") -> None:

    if output_csv.exists():
        # Ensure that we always have at least a _little_ lookup work to do.
        df = sorted_subset(output_csv)  # discards a handful of rows (9 rows)
        df.to_csv(output_csv, index=False)

    df = pd.DataFrame(geocode(output_csv))
    print(df)


if __name__ == "__main__":
    main()
