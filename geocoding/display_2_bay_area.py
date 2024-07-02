#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
"""
Display a map of the San Francisco Bay Area,
with a scale indication plotted at the location of the Hacker Dojo.

This is straight from the Basemap tutorial,
plus some we plot some residences.
"""
import csv
from collections.abc import Generator
from random import randrange

import matplotlib.pyplot as plt
import numpy as np
from geocode import data_dir
from mpl_toolkits.basemap import Basemap

dojo = (-122.049020, 37.3963152)  # 855 W Maude Ave, Mtn. View


def display_bay_area_map() -> None:
    m = Basemap(
        projection="merc",
        urcrnrlat=38,
        llcrnrlat=37.2,
        lat_ts=37,
        llcrnrlon=-122.6,
        urcrnrlon=-121.8,
        resolution="h",
    )
    m.drawcoastlines()
    m.fillcontinents(color="coral", lake_color="aqua")
    m.drawcounties()
    m.drawmapscale(*dojo, *dojo, 10, barstyle="fancy")

    m.drawparallels(np.arange(30.0, 50.0, 0.1))
    m.drawmeridians(np.arange(-130.0, -110.0, 0.1))
    m.drawmapboundary(fill_color="aqua")
    plt.title("SF Bay Area")
    _show_residences(m)
    plt.show()


def _show_residences(m: Basemap, threshold: int = 1) -> None:
    for lon, lat, addr, _ in get_residences():
        x, y = m(lon, lat)
        m.plot(x, y, "bo", markersize=3)
        if randrange(100) < threshold:
            plt.text(x, y, addr)


def get_residences() -> Generator[tuple[float, float, str, str], None, None]:
    with open(data_dir / "geocoded.csv") as fin:
        sheet = csv.DictReader(fin)
        for row in sheet:
            lon, lat = map(float, (row["lon"], row["lat"]))
            yield lon, lat, _title(row["address"]), row["zip"]


def _title(s: str) -> str:
    words = s.split()
    return " ".join(map(str.title, words))


if __name__ == "__main__":
    display_bay_area_map()
