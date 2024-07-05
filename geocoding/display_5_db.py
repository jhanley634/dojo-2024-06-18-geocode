#! /usr/bin/env FLASK_DEBUG=1 python
# Copyright 2024 John Hanley. MIT licensed.
"""
Display a web page map of residences in southern San Mateo County.
"""
from functools import cache
from time import time
from typing import Any

import matplotlib
import matplotlib.pyplot as plt
import numpy.typing as npt
import pandas as pd
from flask import Flask
from linetimer import linetimer
from mpl_toolkits.basemap import Basemap

from geocoding.display_3_san_mateo import (
    _get_rows,
    get_san_mateo_basemap,
    light_brown,
    san_mateo_png,
    temp,
)
from geocoding.display_4_filter import _get_df, content_png, prettify, title

matplotlib.use("agg")  # headless
background_png = temp / "san_mateo_background.png"
app = Flask(__name__)


@app.route("/")  # type: ignore [misc]
def index() -> str:
    return str(
        prettify(
            title("map of San Mateo") + "<div style='font-size: 2em; margin: 3em;'>"
            "<hr><p>hello world</p><hr>"
            "<li><a href='/filtered_map/All'>All</a>"
            "<li><a href='/filtered_map/Menalto'>Menalto Ave</a>"
            "<li><a href='/filtered_map/Oconnor'>O'Connor St</a>"
        )
    )


@cache
def _get_background_image() -> npt.NDArray[Any]:
    if not background_png.exists():
        m = get_san_mateo_basemap()
        m.fillcontinents(color=light_brown, lake_color="aqua")
        plt.title("San Mateo")
        plt.close()
        r = plt.savefig(background_png)
        print(r, type(r))
    return plt.imread(background_png)


@app.route("/filtered_map/<street>")  # type: ignore [misc]
@linetimer()
def filtered_map(street: str) -> tuple[bytes, int, dict[str, str]]:
    street = street.title()
    if street == "All":
        street = ""  # empty string is in all addresses
    plt.title("San Mateo")
    fig, ax = plt.subplots()
    ax.imshow(_get_background_image())
    m = get_san_mateo_basemap()

    df = _get_df()
    df = df[df.addr.str.contains(street)]
    for _, row in df.iterrows():
        if street in row.addr:
            m.plot(row.x, row.y, "bo", markersize=3)
        else:
            m.plot(row.x, row.y, "k.", markersize=1)

    plt.savefig(san_mateo_png)
    plt.close()
    return san_mateo_png.read_bytes(), 200, content_png


def speed_test(street: str = "Oconnor") -> None:
    """Contrasts the speed of .iterrows() vs vectorized .str.contains()."""
    df = pd.DataFrame(_get_rows(Basemap()))
    t0 = time()

    # addrs = [row.addr for _, row in df.iterrows() if street in row.addr]
    # addrs = [row.addr for row in df.itertuples() if street in row.addr]  # 20x faster
    addrs = df[df.addr.str.contains(street)]  # 70x faster

    elapsed = time() - t0
    print(round(elapsed, 3))
    assert 3639 == len(df), len(df)
    assert 118 == len(addrs), len(addrs)


if __name__ == "__main__":
    app.run()
