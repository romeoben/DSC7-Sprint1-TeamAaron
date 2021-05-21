import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static 
import warnings
warnings.filterwarnings('ignore')

st.title('Analyzing Gaps in the Philippine Education System')
st.subheader('Group 5 - Cohort 7')


def background():
    st.title('Background')
    st.write(
        "SDG4 aims to “ensure inclusive and equitable quality education\n"
        "and promote lifelong learning opportunities for all.”")


def point_of_investigation():
    st.title('Point of Investigation')
    st.write("What correlations are of importance to further analyze?")
    st.write("What impact does MOOE spending have on school performance?")
    st.write("What schools, regions, or areas are vulnerable?")


def data_sources():
    st.title('Data Sources')
    st.write("All data were sourced from the Department of Education.")
    st.write("1. MOOE Data")
    st.write("2. Rooms Data")
    st.write("3. Teachers Data")
    st.write("4. Schools Master List Data")


def methodology():
    st.title('Methodology')
    st.write("This is the methodology.")


list_of_pages = [
    "background",
    "point_of_investigation",
    "data_sources",
    "methodology",
]

st.sidebar.title('Table of Contents')
selection = st.sidebar.radio("Go to", list_of_pages)

if selection == "background":
    background()

elif selection == "point_of_investigation":
    point_of_investigation()

elif selection == "data_sources":
    data_sources()

elif selection == "methodology":
    methodology()