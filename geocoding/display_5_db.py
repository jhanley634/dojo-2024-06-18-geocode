#! /usr/bin/env FLASK_DEBUG=1 python
# Copyright 2024 John Hanley. MIT licensed.
"""
Display a web page map of residences in southern San Mateo County.
"""
import pickle
from functools import cache
from time import time

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask
from matplotlib.axes._axes import Axes
from matplotlib.figure import Figure
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
pickled_bg = temp / "san_mateo_background.pkl"
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
def _get_background_image() -> tuple[Figure, Axes]:
    pickled_bg.unlink(missing_ok=True)
    if not pickled_bg.exists():
        m = get_san_mateo_basemap()
        m.fillcontinents(color=light_brown, lake_color="aqua")
        for row in _get_df().itertuples():
            m.plot(row.x, row.y, "k.", markersize=1)
        plt.savefig(background_png)
        fig, ax = plt.subplots()
        assert isinstance(fig, Figure)
        assert isinstance(ax, Axes)
        # plt.close()
        with open(pickled_bg, "wb") as fout:
            pickle.dump((fig, ax), fout)

    with open(pickled_bg, "rb") as fin:
        fig, ax = pickle.load(fin)
        assert isinstance(fig, Figure)
        assert isinstance(ax, Axes)
        return fig, ax


@app.route("/filtered_map/<street>")  # type: ignore [misc]
def filtered_map(street: str) -> tuple[bytes, int, dict[str, str]]:
    street = street.title()
    if street == "All":
        street = ""  # empty string is in all addresses
    fig, ax = _get_background_image()
    ax.set_title("San Mateo")
    m = get_san_mateo_basemap()
    print(ax.get_xlim(), ax.get_ylim())
    xs = range(400)
    ax.plot(xs, xs, "--", linewidth=5, color="firebrick")

    df = _get_df()
    df = df[df.addr.str.contains(street)]
    coords = []
    for row in df.itertuples():
        if street in row.addr:
            coords.append((row.x, row.y))

    m.plot(
        [x for x, _ in coords],
        [y for _, y in coords],
        "bo",
        markersize=3,
    )
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
