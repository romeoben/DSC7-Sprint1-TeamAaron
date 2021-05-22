import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

st.title('Analyzing Gaps in the Philippine Education System')
st.subheader('Data Science Fellowship Cohort 7 - Group 5')

prov = pd.read_csv("schools_prov.csv")
region = pd.read_csv("schools_region.csv")
shapefile = gpd.read_file('./Regions/Regions.shp')
mpr = region["MOOE_Diff"].sort_values()

shapefile.replace({'REGION' : {'Autonomous Region of Muslim Mindanao (ARMM)': 'ARMM', 
                               'Bicol Region (Region V)' : 'Region 05', 
                               'CALABARZON (Region IV-A)' : 'Region 04A', 
                               'Cagayan Valley (Region II)' : 'Region 02', 
                               'Caraga (Region XIII)' : 'CARAGA', 
                               'Central Luzon (Region III)' : 'Region 03', 
                               'Central Visayas (Region VII)' : 'Region 07', 
                               'Cordillera Administrative Region (CAR)' : 'CAR', 
                               'Davao Region (Region XI)' : 'Region 11', 
                               'Eastern Visayas (Region VIII)' : 'Region 08', 
                               'Ilocos Region (Region I)' : 'Region 01', 
                               'MIMAROPA (Region IV-B)' : 'Region 04B', 
                               'Metropolitan Manila' : 'NCR', 
                               'Northern Mindanao (Region X)' : 'Region 10', 
                               'SOCCSKSARGEN (Region XII)' : 'Region 12', 
                               'Western Visayas (Region VI)' : 'Region 06', 
                               'Zamboanga Peninsula (Region IX)' : 'Region 09'}}, inplace=True)

merged_data = pd.merge(shapefile, mpr, left_on="REGION", right_on=mpr.index, how="outer")

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
    st.subheader("2015 DepEd Enhanced Basic Education Information System (EBEIS) Data")
    st.write("1. Schools Masterlist Data")
    st.write("2. Rooms Data")
    st.write("3. Teachers Data")
    st.write("4. MOOE Data")
    st.subheader('Methodology')
    st.write("Data Cleaning")
    st.write("Exploratory Data Analysis")
    st.write("Clustering")
    st.write("Visualization")

def city_income():
    st.title('City Income vs School Resources')
    st.subheader("Urban areas have more educational resources.")
    st.write("Provincial Income Level vs Teacher Availability")
    fig = plt.figure(figsize=(8,6))
    plt.scatter(prov["Schools_Income"], prov["Schools_Teachers"])
    #plt.title("Provincial Income Level vs Teacher Availability", fontsize=14)
    plt.ylabel("Number of Teachers")
    plt.xlabel("Income Level (PHP 1*10^11)")
    st.pyplot(fig)
    st.write("Correlation coefficient: 0.86")
    
    st.write("Provincial Income Level vs Room Availability")
    fig = plt.figure(figsize=(8,6))
    plt.scatter(prov["Schools_Income"], prov["Schools_Rooms"])
    #plt.title("Provincial Income Level vs Room Availability", fontsize=14)
    plt.ylabel("Number of Rooms Available")
    plt.xlabel("Income Level (PHP 1*10^11)")
    st.pyplot(fig)
    st.write("Correlation coefficient: 0.88")
    
    st.write("Provincial Income Level vs Enrollment")
    fig = plt.figure(figsize=(8,6))
    plt.scatter(prov["Schools_Income"], prov["Schools_Enrollment"])
    #plt.title("Provincial Income Level vs Enrollment", fontsize=14)
    plt.ylabel("Enrolled Students")
    plt.xlabel("Income Level (PHP 1*10^11)")
    st.pyplot(fig)
    st.write("Correlation coefficient: 0.85")
    
    st.write("Provincial Income Level vs Mean Student-Teacher Ratio")
    fig = plt.figure(figsize=(8,6))
    plt.scatter(prov["Schools_Income"], prov["Student_Teacher_Ratio"])
    #plt.title("Provincial Income Level vs Mean Student-Teacher Ratio", fontsize=14)
    plt.ylabel("Student-Teacher Ratio")
    plt.xlabel("Income Level (PHP 1*10^11)")
    st.pyplot(fig)
    st.write("Correlation coefficient: 0.42")
    
    corr = prov[['Schools_Income', 'Schools_Teachers', 'Schools_Rooms', 'Student_Teacher_Ratio', 'Schools_Enrollment']].corr()
    
    st.write("City income is positively correlated with total number of enrollees, teachers and classrooms.")
    fig = plt.figure(figsize=(10,8))
    sns.set_theme(style="white")
    mask = np.triu(np.ones_like(corr, dtype=bool))
    #cmap = sns.light_palette("blue", as_cmap=True)
    sns.heatmap(corr, mask=mask, cmap="twilight", center=1, annot=True)
    st.pyplot(fig)

def boncodin():
    st.title('Actual MOOE vs Boncodin MOOE')
            
    st.image("mooe_diff.png", caption=None, width=None, use_column_width=None, clamp=False, channels='RGB', output_format='auto')
    st.write("Some schools receive less than the Boncodin MOOE, some more")
 
    st.write("Regional MOOE Differentials")
    fig = plt.figure(figsize=(10,6), dpi=200) 
    plt.barh(mpr.index, mpr.values) 
    #plt.title("Regional MOOE Differentials", fontsize = 16)
    plt.xlabel("MOOE Differential", fontsize=12)
    plt.xticks(range(0,250000000,25000000))
    st.pyplot(fig)
    st.write("NCR, Region 3, 4-A, 6, 5, 7 have higher MOOE differentials")
    st.write("CAR, CARAGA, Region 4-B, 9, 2 have lower MOOE differentials")
    
    variable = 'MOOE_Diff'
    
    st.write("Regions near the capital have higher MOOE differentials")
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
    st.write("We recommend a reevaluation of the Boncodin Formula, to incorporate certain factors important to the context, such as:")
    st.write("Travel time and cost from school to Division Office)")
    st.write("Poverty incidence")
    st.write("Vulnerability to natural and human-induced hazards")



list_of_pages = [
    "Background",
    "Points of Investigation",
    "What is MOOE?",
    "Data Sources and Methodology",
    "City Income vs School Resources",
    "Actual vs Boncodin MOOE",
    "Conclusion and Recommendations",
]

st.sidebar.title('Table of Contents')
selection = st.sidebar.radio("Go to", list_of_pages)

if selection == "Background":
    background()

elif selection == "Points of Investigation":
    point_of_investigation()

elif selection == "What is MOOE?":
    what_is_mooe()

elif selection == "Data Sources and Methodology":
    data_sources()

elif selection == "City Income vs School Resources":
    city_income()

elif selection == "Actual vs Boncodin MOOE":
    boncodin()

elif selection == "Conclusion and Recommendations":
    conclusion()