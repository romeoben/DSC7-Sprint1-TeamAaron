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
st.set_page_config(page_title='Analyzing Gaps in the Philippine Education System', layout="wide")
warnings.filterwarnings('ignore')
st.set_option('deprecation.showPyplotGlobalUse', False)

prov = pd.read_csv("schools_prov.csv")
region = pd.read_csv("schools_region.csv", index_col="school.region")
merged_data = gpd.read_file('./merged_data/merged_data.shp')
corr = prov[['Schools_Income', 'Schools_Teachers', 'Schools_Rooms', 'Student_Teacher_Ratio', 'Schools_Enrollment']].corr()


def project():
    st.title('Analyzing Gaps in the Philippine Education System')
    st.subheader('Data Science Fellowship Cohort 7 - Group 5')

    teacher_image = Image.open('teacher.jpg')

    col1, col2 = st.beta_columns(2)
    with col1:
        st.image(
            teacher_image,
            caption='A teacher with her class of 59 students in a Quezon City public school. Source: The Guardian'
        )
    with col2:
        st.markdown(
            "In this **exploratory data analysis**, we aim to uncover the distribution of public education resources "
            "across the Philippines and identify critical deficiencies "
            "through an assessment of **Maintenance and Other Operating Expenses (MOOE)** "
            "allocation in the different regions."
        )


def background():
    st.title('Background')
    st.markdown(
        "The United Nations SDG4 aims to *ensure inclusive and equitable quality education\n"
        "and promote lifelong learning opportunities for all.*")

    st.write(
        "In the context of the Philippines, has this goal been properly translated into **reality**? \n"
        "To investigate this, we asked three critical questions: "
    )

    sdg4_image = Image.open('sdg4.jpg')
    
    col1, col2 = st.beta_columns([1, 2])
    with col1:
        st.markdown(
            "1. **How are education resources distributed across the country?**"
        )
        st.markdown(    
            "2. **Are there any schools, regions, or areas with resource deficiencies?**"
        )
        st.markdown(    
            "3. **Are the perceived discrepancies in allocation justified for resource needs of these schools/regions?**"
        )
    with col2:
        st.image(sdg4_image, caption='Source: Think Sustainability')
        


def what_is_mooe():
    st.title('What is MOOE?')
    st.write("")
    col1, col2 = st.beta_columns(2)
    with col1:
        mooe_image = Image.open('what_is_mooe.png')
        st.image(mooe_image)
    with col2:
        mooe_computation = Image.open("mooe_computation.png")
        st.image(mooe_computation)

def data_method():
    st.title('Data Sources and Methodology')
    st.write("")
    col1, col2 = st.beta_columns(2)
    with col1:
        data_sources = Image.open("data_sources.png")
        st.image(data_sources)
    with col2:
        methodology = Image.open("methodology.png")
        st.image(methodology)


def methodology():
    st.title('Methodology')
    methodology = Image.open("methodology.png")
    st.image(methodology)


def city_income():
    st.title('City Income vs School Resources')
    st.subheader("Schools in cities with higher incomes have more educational resources.")
    st.write("")
    
    col1, col2 = st.beta_columns(2)
    with col1:
        st.write("City income was found to be positively correlated with total number of enrollees, teachers and classrooms.")
        fig = plt.figure(figsize=(10, 8))

        sns.set_theme(style="white")
        sns.set_context(context="paper",font_scale=1.7)
        mask = np.triu(np.ones_like(corr, dtype=bool))
        # cmap = sns.light_palette("blue", as_cmap=True)
        sns.heatmap(corr, mask=mask, cmap="twilight", center=1, annot=True)
        st.pyplot(fig)
    
    with col2:
        option = st.selectbox(
        'City Income vs:',
        ['Teacher Availability', 'Room Availability', 'Enrollment', 'Student-Teacher Ratio'])
        
        if option == "Teacher Availability":
            fig = plt.figure(figsize=(8, 6))

            plt.scatter(prov["Schools_Income"], prov["Schools_Teachers"])
            plt.ylabel("Number of Teachers")
            plt.xlabel("Income Level (PHP 1*10^11)")
            st.pyplot(fig)
            st.write("Correlation coefficient: 0.86")
        
        elif option == "Room Availability":
            fig = plt.figure(figsize=(8, 6))

            plt.scatter(prov["Schools_Income"], prov["Schools_Rooms"])
            plt.ylabel("Number of Rooms Available")
            plt.xlabel("Income Level (PHP 1*10^11)")
            st.pyplot(fig)
            st.write("Correlation coefficient: 0.88")
            
        elif option == "Enrollment":
            fig = plt.figure(figsize=(8, 6))

            plt.scatter(prov["Schools_Income"], prov["Schools_Enrollment"])
            plt.ylabel("Enrolled Students")
            plt.xlabel("Income Level (PHP 1*10^11)")
            st.pyplot(fig)
            st.write("Correlation coefficient: 0.85")
            
        elif option == "Student-Teacher Ratio":
            fig = plt.figure(figsize=(8, 6))

            plt.scatter(prov["Schools_Income"], prov["Student_Teacher_Ratio"])
            # plt.title("Provincial Income Level vs Mean Student-Teacher Ratio", fontsize=14)
            plt.ylabel("Student-Teacher Ratio")
            plt.xlabel("Income Level (PHP 1*10^11)")
            st.pyplot(fig)
            st.write("Correlation coefficient: 0.42")


def boncodin():
    st.title('Actual MOOE vs Boncodin MOOE')
    col1, col2 = st.beta_columns([1,2])
    with col1:
        st.subheader("At a Glance")
        st.image("mooe_diff.png", caption=None, width=None, use_column_width=None, clamp=False, channels='RGB',
                 output_format='auto')
        st.write("**Some schools receive less than the Boncodin MOOE, some more.**")
        option = st.selectbox(
        'Select Visualization:',
        ['Bar chart', 'Heatmap'])
        
    
    with col2:
        st.subheader("MOOE Differentials by Region")
        
        if option == "Bar chart":
        
            mpr = region["MOOE_Diff"].sort_values()
            fig = plt.figure(figsize=(10, 6), dpi=200)
            plt.barh(mpr.index, mpr.values)
            # plt.title("Regional MOOE Differentials", fontsize = 16)
            plt.xlabel("MOOE Differential", fontsize=12)
            plt.xticks(range(0, 250000000, 25000000))
            st.pyplot(fig)
        
        elif option == "Heatmap":
        
            variable = 'MOOE_Diff'

            vmin, vmax = merged_data['MOOE_Diff'].min(), merged_data['MOOE_Diff'].max()
            fig, ax = plt.subplots(1, figsize=(8, 6), dpi=200)
            merged_data.plot(column=variable, cmap='PuBu', linewidth=0.8, ax=ax, edgecolor='0.8', vmin=vmin, vmax=vmax)
            sm = plt.cm.ScalarMappable(cmap='PuBu', norm=plt.Normalize(vmin=vmin, vmax=vmax))
            cbar = fig.colorbar(sm)
            st.pyplot()
        st.write("")
        st.write("NCR, Region 3, 4-A, 6, 5, 7 have **higher** MOOE differentials.")
        st.write("CAR, CARAGA, Region 4-B, 9, 2 have **lower** MOOE differentials.")

def conclusion():
    st.title('Conclusion and Recommendations')
    st.write("## What did we learn?")
    st.write("### How are education resources distributed across the country?")
    st.write("- MOOE allocation generally favors schools in higher-income cities, highlighting inequitable distribution.")
    st.write("### Are there any schools, regions, or areas with resource deficiencies?")
    st.write("- 897 schools received less than the Boncodin MOOE.")
    st.write("- Some regions require more rooms and teachers per student.")
    st.write("### Are the perceived discrepancies justified for resource needs?")
    st.write("- Not necessarily. Some regions have lower MOOE differentials but require more resources (CAR, Region 2).")
    st.write("## What can we do?")
    st.write(
        "### We recommend a reevaluation of the Boncodin Formula, to incorporate certain factors important to the context, such as:")
    st.write("- Travel time and cost from school to Division Office)")
    st.write("- Poverty incidence")
    st.write("- Vulnerability to natural and human-induced hazards")

def referenecs():
    st.title('References:')
    
    st.subheader('[1] Building Better Learning Environments in the Philippines')
    st.write("World Bank Group. (2016). Building Better Learning Environments in the Philippines. Philippines education note,no. 4;. World Bank, Washington, DC. © World Bank. https://openknowledge.worldbank.org/handle/10986/24744 License: CC BY 3.0 IGO.")
    
    st.write("[2] House Bill No. 473: An Act Regulating Class Size in All Public Schools and Appointing Funds Therefor")
    st.write("Tinio, A. L., & Castro, F. L. (2016, June 30). House Bill No. 473: An Act Regulating Class Size in All Public Schools and Appointing Funds Therefor. House Bill No. 473. https://www.congress.gov.ph/legisdocs/basic_17/HB00473.pdf.")
    
    st.subheader("[3] Class-size affects students' learning : DepEd. Philippine News Agency RSS")
    st.write("Montemayor, M. T. (2018, March 19). Class-size affects students' learning : DepEd. Philippine News Agency RSS. https://www.pna.gov.ph/articles/1029281. ")

    st.subheader('[4] DepEd EBEIS (2015)')
    st.write("")    

    st.subheader('[5] Comparing the DISADVANTAGE INDEX (DI) with GEOGRAPHICALLY ISOLATED AND DISADVANTAGED AREAS (GIDA)')
    st.write("Comparing the DISADVANTAGE INDEX (DI) with GEOGRAPHICALLY ISOLATED AND DISADVANTAGED AREAS (GIDA). DepEd, 2015.")      
    
    st.subheader('[6] Computation of Public Schools MOOE')
    st.write("Llego, M. A. (2015). Computation of Public Schools MOOE. https://www.teacherph.com/computation-public-schools-mooe/")  
    
    
    
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
