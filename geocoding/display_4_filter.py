#! /usr/bin/env FLASK_DEBUG=1 python
# Copyright 2024 John Hanley. MIT licensed.
"""
Display a web page map of residences in southern San Mateo County.
"""
from functools import cache
from time import time

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from bs4 import BeautifulSoup
from flask import Flask

from geocoding.display_3_san_mateo import (
    _get_rows,
    get_san_mateo_basemap,
    light_brown,
    san_mateo_png,
)

matplotlib.use("agg")  # headless
app = Flask(__name__)


@app.route("/")  # type: ignore [misc]
def index() -> str:
    return prettify(
        title("map of San Mateo") + "<div style='font-size: 2em; margin: 3em;'>"
        "<hr><p>hello world</p><hr>"
        "<ul><li><a href='/cached_map'>San Mateo Map</a>"
        "<li><a href='/filtered_map/All'>All</a>"
        "<li><a href='/filtered_map/Menalto'>Menalto Ave</a>"
        "<li><a href='/filtered_map/Oconnor'>O'Connor St</a>"
    )


content_png = {"Content-Type": "image/png"}


@app.route("/cached_map")  # type: ignore [misc]
def cached_map() -> tuple[bytes, int, dict[str, str]]:
    return san_mateo_png.read_bytes(), 200, content_png


@cache
def _get_df() -> pd.DataFrame:
    return pd.DataFrame(_get_rows(get_san_mateo_basemap()))


@app.route("/filtered_map/<street>")  # type: ignore [misc]
def filtered_map(street: str) -> tuple[bytes, int, dict[str, str]]:
    street = street.title()
    if street == "All":
        street = ""  # empty string is in all addresses
    m = get_san_mateo_basemap()
    m.fillcontinents(color=light_brown, lake_color="aqua")
    plt.title("San Mateo")

    df = _get_df()
    xs = []
    ys = []
    t0 = time()
    for row in df.itertuples():
        assert isinstance(row.addr, str)
        if street in row.addr:
            xs.append(row.x)
            ys.append(row.y)
        else:
            m.plot(row.x, row.y, "k.", markersize=1)
    m.plot(xs, ys, "bo", markersize=3)
    print(f"Filtered {len(df)} rows in {time() - t0:.3f} sec.")

    plt.savefig(san_mateo_png)
    plt.close()
    return san_mateo_png.read_bytes(), 200, content_png


def title(text: str) -> str:
    return f"<!DOCTYPE html><html lang='en'><head><title>{text}</head><body>"


def prettify(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    return soup.prettify(formatter="html5")


if __name__ == "__main__":
    app.run()
