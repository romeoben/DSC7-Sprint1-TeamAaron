import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

st.title('Analyzing Gaps in the Philippine Education System')
st.subheader('Data Science Fellowship Cohort 7 - Group 5')


def background():
    st.title('Background')
    st.write(
        "UN SDG4 aims to “ensure inclusive and equitable quality education\n"
        "and promote lifelong learning opportunities for all.”")


def point_of_investigation():
    st.title('Points of Investigation')
    st.write("How are education resources distributed across the country?")
    st.write("Are there any schools, regions, or areas with resource deficiencies?")
    st.write("Are the perceived discrepancies justified for resource needs?")

def what_is_mooe():
    st.title('What is MOOE?')
    st.subheader("Maintenance and Other Operating Expenses")
    st.write("-Refers to expenditures to support the operations of government agencies")
    st.write("For schools, MOOE supports learning programs and helps maintain a safe and healthy learning environment. ")
    st.subheader("How is it computed?")
    st.write("Boncodin Formula")
    st.write("School MOOE = α + (β x TC) + (γ x TT) + (δ x TE)")
    st.write("Where α, β, γ, δ = constants dependent on school type (elementary or secondary)\n TC = total classrooms\n TT = total teachers\n TE = total enrollees")
    
def data_sources():
    st.title('Data Sources and Methodology')
    st.write("2015 DepEd Enhanced Basic Education Information System (EBEIS)")
    st.write("1. Schools Masterlist Data")
    st.write("2. Rooms Data")
    st.write("3. Teachers Data")
    st.write("4. MOOE Data")
    st.subheader('Methodology')
    st.write("This is the methodology.")


def conclusion():
    st.title('Conclusion and Recommendations')
    st.subheader("What did we learn?")
    st.write("How are education resources distributed across the country?")
    st.write("MOOE allocation generally favors schools in higher-income cities, highlighting inequitable distribution.")
    st.write("Are there any schools, regions, or areas with resource deficiencies?")
    st.write("897 schools received less than the Boncodin MOOE.")
    st.write("Some regions require more rooms and teachers per student.")
    st.write("Are the perceived discrepancies justified for resource needs?")
    st.write("Not necessarily. Some regions have lower differentials but require more resources (CAR, Region 2).")
    st.subheader("What can we do?")





list_of_pages = [
    "Background",
    "Points of Investigation",
    "What is MOOE?",
    "Data Sources and Methodology",
    "Conclusion and Recommendations",
]

st.sidebar.title('Table of Contents')
selection = st.sidebar.radio("Go to", list_of_pages)

if selection == "Background":
    background()

elif selection == "Points of Investigation":
    point_of_investigation()

elif selection == "Data Sources and Methodology":
    data_sources()

elif selection == "Conclusion and Recommendations":
    Conclusion()