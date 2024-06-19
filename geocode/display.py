#! /usr/bin/env streamlit run --server.runOnSave true
# Copyright 2024 John Hanley. MIT licensed.
import pandas as pd
import streamlit as st

from geocode.geocode1 import geocoded_csv


def display(size=3):
    st.title("Geocoded Addresses")
    df = pd.read_csv(geocoded_csv)
    st.map(df, size=size)


if __name__ == "__main__":
    display()
