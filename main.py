import warnings
import geopandas as gpd
import descartes
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from PIL import Image
import cluster

warnings.filterwarnings('ignore')
st.set_option('deprecation.showPyplotGlobalUse', False)

prov = pd.read_csv("schools_prov.csv")
region = pd.read_csv("schools_region.csv")
merged_data = gpd.read_file('./merged_data/merged_data.shp')
corr = prov[['Schools_Income', 'Schools_Teachers', 'Schools_Rooms', 'Student_Teacher_Ratio', 'Schools_Enrollment']].corr()


def project():
    st.title('Analyzing Gaps in the Philippine Education System')
    st.subheader('Data Science Fellowship Cohort 7 - Group 5')

    teacher_image = Image.open('teacher.jpg')

    col1, col2 = st.beta_columns([2, 1])
    with col1:
        st.image(
            teacher_image,
            caption='A teacher with her class of 59 students in a Quezon City public school. Source: The Guardian'
        )
    with col2:
        st.markdown(
            "In this **exploratory data analysis**, we aim to uncover the distribution of public education resources "
            "across the Philippines and identify critical deficiencies "
            "through an assessment of Maintenance and Other Operating Expenses (MOOE) "
            "allocation in the different regions."
        )
        st.write("")
        st.write("")


def background():
    st.title('Background')
    st.markdown(
        "The United Nations SDG4 aims to *ensure inclusive and equitable quality education\n"
        "and promote lifelong learning opportunities for all.*")

    st.write(
        "In the context of the Philippines, has this goal been properly translated into **reality**?", "",
        "To investigate this, we asked three critical questions: "
    )

    sdg4_image = Image.open('sdg4.jpg')
    
    col1, col2 = st.beta_columns(2)
    with col1:
        st.markdown(
            "**1. How are education resources distributed across the country?**"
        )
        st.markdown(    
            "**2. Are there any schools, regions, or areas with resource deficiencies?**"
        )
        st.markdown(    
            "**3. Are the perceived discrepancies in allocation justified for resource needs of these schools/regions?**"
        )
    with col2:
        st.image(sdg4_image, caption='Source: Think Sustainability')
        


def what_is_mooe():
    st.title('What is MOOE?')
    st.write("")
    mooe_image = Image.open('what_is_mooe.png')
    st.image(mooe_image)
    st.write("")
    mooe_computation = Image.open("mooe_computation.png")
    st.image(mooe_computation)

def data_method():
    st.title('Data Sources and Methodology')
    st.write("")
    data_sources = Image.open("data_sources.png")
    st.image(data_sources)
    st.write("")
    methodology = Image.open("methodology.png")
    st.image(methodology)


def methodology():
    st.title('Methodology')
    methodology = Image.open("methodology.png")
    st.image(methodology)


def city_income():
    st.title('City Income vs School Resources')
    st.subheader("Urban areas have more educational resources.")

    st.write("Provincial Income Level vs Teacher Availability")
    fig = plt.figure(figsize=(8, 6))

    plt.scatter(prov["Schools_Income"], prov["Schools_Teachers"])
    # plt.title("Provincial Income Level vs Teacher Availability", fontsize=14)
    plt.ylabel("Number of Teachers")
    plt.xlabel("Income Level (PHP 1*10^11)")
    st.pyplot(fig)
    st.write("Correlation coefficient: 0.86")

    st.write("Provincial Income Level vs Room Availability")
    fig = plt.figure(figsize=(8, 6))

    plt.scatter(prov["Schools_Income"], prov["Schools_Rooms"])
    # plt.title("Provincial Income Level vs Room Availability", fontsize=14)
    plt.ylabel("Number of Rooms Available")
    plt.xlabel("Income Level (PHP 1*10^11)")
    st.pyplot(fig)
    st.write("Correlation coefficient: 0.88")

    st.write("Provincial Income Level vs Enrollment")
    fig = plt.figure(figsize=(8, 6))

    plt.scatter(prov["Schools_Income"], prov["Schools_Enrollment"])
    # plt.title("Provincial Income Level vs Enrollment", fontsize=14)
    plt.ylabel("Enrolled Students")
    plt.xlabel("Income Level (PHP 1*10^11)")
    st.pyplot(fig)
    st.write("Correlation coefficient: 0.85")

    st.write("Provincial Income Level vs Mean Student-Teacher Ratio")
    fig = plt.figure(figsize=(8, 6))

    plt.scatter(prov["Schools_Income"], prov["Student_Teacher_Ratio"])
    # plt.title("Provincial Income Level vs Mean Student-Teacher Ratio", fontsize=14)
    plt.ylabel("Student-Teacher Ratio")
    plt.xlabel("Income Level (PHP 1*10^11)")
    st.pyplot(fig)
    st.write("Correlation coefficient: 0.42")
    
    st.write("City income is positively correlated with total number of enrollees, teachers and classrooms.")
    fig = plt.figure(figsize=(10, 8))

    sns.set_theme(style="white")
    mask = np.triu(np.ones_like(corr, dtype=bool))
    # cmap = sns.light_palette("blue", as_cmap=True)
    sns.heatmap(corr, mask=mask, cmap="twilight", center=1, annot=True)
    st.pyplot(fig)


def boncodin():
    st.title('Actual MOOE vs Boncodin MOOE')

    st.image("mooe_diff.png", caption=None, width=None, use_column_width=None, clamp=False, channels='RGB',
             output_format='auto')
    st.write("Some schools receive less than the Boncodin MOOE, some more")
    
    mpr = region["MOOE_Diff"].sort_values()
    st.subheader("Regional MOOE Differentials")
    fig = plt.figure(figsize=(10, 6), dpi=200)
    plt.barh(mpr.index, mpr.values)
    # plt.title("Regional MOOE Differentials", fontsize = 16)
    plt.xlabel("MOOE Differential", fontsize=12)
    plt.xticks(range(0, 250000000, 25000000))
    st.pyplot(fig)
    st.write("NCR, Region 3, 4-A, 6, 5, 7 have higher MOOE differentials.")
    st.write("CAR, CARAGA, Region 4-B, 9, 2 have lower MOOE differentials.")

    variable = 'MOOE_Diff'

    vmin, vmax = merged_data['MOOE_Diff'].min(), merged_data['MOOE_Diff'].max()
    fig, ax = plt.subplots(1, figsize=(15, 10))
    merged_data.plot(column=variable, cmap='PuBu', linewidth=0.8, ax=ax, edgecolor='0.8', vmin=vmin, vmax=vmax)
    sm = plt.cm.ScalarMappable(cmap='PuBu', norm=plt.Normalize(vmin=vmin, vmax=vmax))
    cbar = fig.colorbar(sm)
    st.pyplot()


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
    st.write(
        "We recommend a reevaluation of the Boncodin Formula, to incorporate certain factors important to the context, such as:")
    st.write("Travel time and cost from school to Division Office)")
    st.write("Poverty incidence")
    st.write("Vulnerability to natural and human-induced hazards")


list_of_pages = [
    "The Project",
    "Background",
    "What is MOOE?",
    "Data Sources and Methodology",
    "City Income vs School Resources",
    "Gaps in School Resources",
    "Actual vs Boncodin MOOE",
    "Clustering",
    "Conclusion and Recommendations",
]

st.sidebar.title('Table of Contents')
selection = st.sidebar.radio("Go to", list_of_pages)

if selection == "The Project":
    project()

elif selection == "Background":
    background()

elif selection == "Points of Investigation":
    point_of_investigation()

elif selection == "What is MOOE?":
    what_is_mooe()

elif selection == "Data Sources and Methodology":
    data_method()

elif selection == "City Income vs School Resources":
    city_income()

elif selection == "Gaps in School Resources":
    cluster.gaps()

elif selection == "Actual vs Boncodin MOOE":
    boncodin()

elif selection == "Clustering":
    cluster.clustering()

elif selection == "Conclusion and Recommendations":
    conclusion()
