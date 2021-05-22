import warnings
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from PIL import Image
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from math import pi
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import MinMaxScaler

rooms_schools4 = pd.read_csv("Nilly_data.csv")

def gaps():
    st.title('ACROSS THE COUNTRY, CAN WE IDENTIFY REGIONS WITH GAPS?')
    st.write("In terms of educational resources")
    
    st.subheader("REGIONS REQUIRING MORE ROOMS")
    region_rooms_ratio = rooms_schools4.groupby("school.region")['rooms_students'].mean()
    region_rooms_ratio = region_rooms_ratio.replace([np.inf, -np.inf], np.nan)
    region_rooms_ratio = region_rooms_ratio.sort_values()
    fig = plt.figure(figsize=(10,6)) 
    plt.barh(region_rooms_ratio.index, region_rooms_ratio.values,height=0.8,left=0,align='edge') 
    plt.title("Region: Room Utilization.", fontsize=16)
    plt.xlabel("number of students per one room", fontsize=12)
    st.pyplot(fig)
    st.write("According to the World Bank [1], less students per classroom is associated with better student performance.")
    st.write("Additionally, House Bill 473 [2] states that the standard class size is 35.")
    
    st.subheader("REGIONS REQUIRING MORE TEACHERS")
    region_teacher_student_ratio = rooms_schools4.groupby("school.region")['student_teacher'].mean()
    region_teacher_student_ratio = region_teacher_student_ratio.sort_values()
    fig = plt.figure(figsize=(10,6)) 
    plt.barh(region_teacher_student_ratio.index, region_teacher_student_ratio.values,height=0.8,left=0,align='edge') 
    plt.title("Region: Student Teacher ratio", fontsize=16)
    plt.xlabel("number of students per one teacher", fontsize=12)
    st.pyplot(fig)
    st.write("In 2018, DepEd [3] set parameters for Student-Teacher ratios: for Grades 1-2, it is 1:30, Grade 3-4, 1:35, and Grades 5-10, 1:40.")
    st.write("This brings us to an average of 1:35 - which is the ideal.")
    
   
def clustering():
    st.title('WITH GREATER RESOURCE NEED…')
    st.subheader('COMES COMES GREATER MOOE DIFFERENTIAL?')
    st.write("Justifying resource allocation per region using K-Means Clustering")
    
    region_urban_rooms_ratio = rooms_schools4.groupby(["school.urban", "school.region"])["rooms_students"].mean()
    
    region_schools = rooms_schools4.groupby(["school.region"])[["rooms_students", "student_teacher", "mooe_diff"]].agg(
    rooms_students=("rooms_students", 'mean'), 
    student_teacher=("student_teacher", 'mean'),
    mooe_diff=("mooe_diff", 'mean')
    )
    region_schools = region_schools.drop(region_schools.index[0])
    
    index_name = (region_schools[(region_schools["rooms_students"]==0.0) |
                             (region_schools["student_teacher"]==0.0) |
                             (region_schools["mooe_diff"] == 0.0)].index)
    
    region_schools_final = region_schools.drop(index_name)
    
    ##standardize the features
    # Removing (statistical) outliers for student teacher
    Q1 = region_schools_final['rooms_students'].quantile(0.05)
    Q3 = region_schools_final['rooms_students'].quantile(0.95)
    IQR = Q3 - Q1
    region_schools_final = (region_schools_final[(region_schools_final['rooms_students'] >= Q1 - 1.5*IQR) & 
                           (region_schools_final['rooms_students'] <= Q3 + 1.5*IQR)])
    #quartile is 0.25 and quantile is 0.05
    
    region_schools_final.dropna(inplace=True)
    

    #takes out discrepancies
    scaler = StandardScaler()
    region_schools_scaled = scaler.fit_transform(region_schools_final)
    
    #using KMeans

    #setting up your model
    model = KMeans(n_clusters=4) #hyperparameters in the parenthesis
    model.fit(region_schools_scaled) #fitting -> training
    cluster_labels = model.predict(region_schools_scaled)
    
    #applying kmeans to the dataset / creating the kmeans classifier
    kmeans = KMeans(n_clusters=3, init='k-means++', max_iter=300, n_init=10, random_state=0)
    kmeans.fit(region_schools_scaled)
    cluster_labels = kmeans.predict(region_schools_scaled)   
    region_schools_final['Cluster_Labels'] = cluster_labels
    region_schools_final['Cluster_Labels'].value_counts()
    
    #using DBSCAN
    dbs = DBSCAN(eps=0.33, min_samples=3)
    dbs_labels = dbs.fit_predict(region_schools_scaled)   
    region_schools_final['DBS_Labels'] = dbs_labels
    region_schools_final['DBS_Labels'].value_counts()
    
    ##RADAR CHART##
    scaler = MinMaxScaler()
    df_minmax = scaler.fit_transform(region_schools_final)
    df_minmax = pd.DataFrame(df_minmax, index=region_schools_final.index, columns=region_schools_final.columns)
    df_minmax['Cluster_Labels'] = cluster_labels
    df_clusters = df_minmax.set_index("Cluster_Labels")
    df_clusters = df_clusters.groupby("Cluster_Labels").mean().reset_index()
    # df_clusters
    
    my_dpi=100
    fig = plt.figure(figsize=(1000/my_dpi, 1000/my_dpi), dpi=my_dpi)
    plt.subplots_adjust(hspace=0.5)

     #Create a color palette:
    my_palette = plt.cm.get_cmap("Set2", len(df_clusters.index))

    for row in range(0, len(df_clusters.index)):
        make_spider(row=row, 
                    title='Segment '+(df_clusters['Cluster_Labels'][row]).astype(str), 
                    color=my_palette(row))
    
    st.pyplot(fig)
    
    st.subheader('SEGMENT 0')
    st.write("low room utilization (0)")
    st.write("low student teacher ratio (0)")
    st.write("low MOOE diff (-0.25)")
    
    st.subheader('SEGMENT 1')
    st.write("high room utilization (0.75)")
    st.write("medium student teacher ratio (0.25)")
    st.write("high MOOE diff (0.75)")
    
    st.subheader('SEGMENT 2')
    st.write("low room utilization (0.25)")
    st.write("high student teacher ratio (0.5)")
    st.write("low MOOE diff (-0.25)")
    
def make_spider(row, title, color):
        # number of variable
        categories=list(df_clusters)[1:]
        N = len(categories)

        # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]

        # Initialise the spider plot
        ax = plt.subplot(3,3,row+1, polar=True )

        # If you want the first axis to be on top:
        ax.set_theta_offset(pi / 3.5)
        ax.set_theta_direction(-1)

        # Draw one axe per variable + add labels labels yet
        plt.xticks(angles[:-1], categories, color='grey', size=8)

        # Draw ylabels
        ax.set_rlabel_position(0)
        #plt.yticks([-2, -1, 0, 1, 2], [-2,-1, 0, 1, 2], color="grey", size=7) #for sscaled
        # plt.ylim(-2.5,2.5)
        plt.yticks([-0.25, 0, 0.25, 0.5, 0.75, 1], [-0.25, 0, 0.25, 0.5,0.75, 1], color="grey", size=7) #formmscaled
        plt.ylim(-0.25,1)

        # Ind1
        values=df_clusters.loc[row].drop('Cluster_Labels').values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, color=color, linewidth=2, linestyle='solid')
        ax.fill(angles, values, color=color, alpha=0.4)

        # Add a title
        plt.title(title, size=14, color=color, y=1.1)