#! /usr/bin/env streamlit run --server.runOnSave true
# Copyright 2024 John Hanley. MIT licensed.
import pandas as pd
import streamlit as st

from geocode import data_dir


def display(size: int = 2) -> None:
    st.title("Geocoded Addresses")
    df = pd.read_csv(data_dir / "geocoded.csv")
    st.map(df, size=size)


if __name__ == "__main__":
    display()
