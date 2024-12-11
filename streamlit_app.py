import streamlit as st
from bokeh.plotting import figure, show
import plotly.express as px
from bokeh.models import HoverTool, ColumnDataSource, Legend
from bokeh.io import output_notebook
from bokeh.layouts import column
import matplotlib.pyplot as plt
from bokeh.palettes import Category10
import pandas as pd
from bokeh.plotting import figure, show
from bokeh.models import HoverTool, ColumnDataSource, Legend
from bokeh.io import output_notebook
from bokeh.layouts import column
from bokeh.palettes import Category10
import bqplot as bq
import ipywidgets as widgets
st.title("🎈 Seungmin's Final Project")
st.write("""
Group member: Seungmin Cho, Group 39
The name of the dataset is "Police_arrests". I found this dataset from data.illinois.gov. Here is the link of this dataset: https://data.illinois.gov/dataset/police-arrests/resource/ca1dceb3-01f8-4a56-935b-7e3035ff60a4. 

This dataset is available on the Data.illinois.gov. However, the dataset's page does not specify a particular license or terms of use. In the absence of explicit licensing information, I assume that the data is intended for public access and use, as it is hosted on a government open data platform. 

This usually allows for activities such as downloading, analyzing, and sharing the data, provided that proper attribution is given and the data is not used for commercial purposes without permission. 

The Police_arrests' file size is approximately 39.4 MB. It contains 206,600 rows and 25 columns. Github's web interface supports file uploads up to 100 MB. So, I can directly upload the file to a Github repository without issues.
""")

#data = pd.read_csv("police_arrests.csv")
url = ("https://data.illinois.gov/dataset/1d18ecc0-3c7e-4507-b8cc-7a5e30359d44/resource/ca1dceb3-01f8-4a56-935b-7e3035ff60a4/download/police-arrests-upload_20191226.csv")
data= pd.read_csv(url)




st.title('Distribution of Age at Arrest')

filtered_ages = data[(data['age_at_arrest'] >= 0) & (data['age_at_arrest'] <= 100)]

fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(filtered_ages['age_at_arrest'], bins=50, edgecolor='k')
ax.set_title('Distribution of Age at Arrest (Ages 0-100)')
ax.set_xlabel('Age')
ax.set_ylabel('Frequency')
ax.grid(True)

st.pyplot(fig)

st.write("""
This histogram illustrates the distribution of arrests by age for individuals aged 0 to 100, showing that arrests are most frequent among younger individuals, peaking between the ages of 20 and 25. The frequency of arrests declines steadily with increasing age, reflecting a right-skewed distribution. Arrests are rare for those under 15 and above 60 years old, highlighting a trend where younger populations are more likely to experience incidents leading to arrests. 
This pattern may offer insights into behavioral and societal factors influencing arrest rates.
""")





#file_path = "police_arrests.csv"
data = pd.read_csv(url)

filtered_data = data[(data['age_at_arrest'] >= 0) & (data['age_at_arrest'] <= 80)]

def create_age_histogram(df):
    hist, bin_edges = pd.cut(df['age_at_arrest'], bins=16, retbins=True)
    counts = hist.value_counts(sort=False)
    bin_labels = [f"{int(edge.left)}-{int(edge.right)}" for edge in counts.index]

    fig, ax = plt.subplots()
    ax.bar(bin_labels, counts.values, color='skyblue')
    ax.set_xlabel('Age at Arrest (0–80)')
    ax.set_ylabel('Number of Arrests')
    ax.set_title('Age Distribution (0–80)')
    plt.xticks(rotation=45, ha='right')
    return fig

def create_crime_bar_chart(df):
    crime_counts = df['crime_category_description'].value_counts()
    top_10_crimes = crime_counts.head(10)

    fig, ax = plt.subplots()
    ax.bar(top_10_crimes.index, top_10_crimes.values, color='skyblue')
    ax.set_xlabel('Top 10 Crime Categories')
    ax.set_ylabel('Number of Arrests')
    ax.set_title('Top 10 Crime Categories')
    plt.xticks(rotation=45, ha='right')
    return fig

def main():
    st.title("Interactive Arrest Data Visualization")

    race_options = ['All'] + list(filtered_data['arrestee_race'].unique())
    selected_race = st.selectbox('Select Race:', race_options)

    if selected_race != 'All':
        filtered_race_data = filtered_data[filtered_data['arrestee_race'] == selected_race]
    else:
        filtered_race_data = filtered_data

    st.subheader("Age Distribution (0–80)")
    age_histogram_fig = create_age_histogram(filtered_race_data)
    st.pyplot(age_histogram_fig)

    st.subheader("Top 10 Crime Categories")
    crime_bar_chart_fig = create_crime_bar_chart(filtered_race_data)
    st.pyplot(crime_bar_chart_fig)

if __name__ == "__main__":
    main()

st.write("""
The accompanying dashboard is designed to enable users to explore the dataset interactively. One primary feature of the dashboard is its ability to display gender distribution and the corresponding crime types. 
Users can select specific genders by clicking on bars in the gender distribution graph, dynamically filtering the crime types graph to reflect the selected gender's associated crime categories. Another feature allows users to analyze age distributions and the top 10 crime categories for each race. By selecting a specific race from an interactive option button, users can visualize the age group distribution and crime categories associated with that race. These functionalities offer insights into how demographic variables, such as race and gender, correlate with different types of criminal activity.
""")



def create_gender_chart(df):
    gender_counts = df['arrestee_sex'].value_counts()

    fig, ax = plt.subplots()
    bars = ax.bar(gender_counts.index, gender_counts.values, color=['#ff9999', '#66b3ff'])
    ax.set_xlabel('Gender')
    ax.set_ylabel('Number of Arrests')
    ax.set_title('Gender Distribution')

    for i, v in enumerate(gender_counts.values):
        ax.text(i, v + 1, str(v), ha='center')

    return fig

def create_crime_chart(df):
    crime_counts = df['crime_category_description'].value_counts().head(10)

    fig, ax = plt.subplots()
    bars = ax.bar(crime_counts.index, crime_counts.values, color='orange')
    ax.set_xlabel('Crime Category')
    ax.set_ylabel('Number of Arrests')
    ax.set_title('Crime Types for Selected Gender')
    plt.xticks(rotation=45, ha='right')

    for i, v in enumerate(crime_counts.values):
        ax.text(i, v + 1, str(v), ha='center')

    return fig

def create_race_year_chart(df):
    arrests_by_race_year = df.groupby(['year_of_arrest', 'arrestee_race']).size().reset_index(name='Arrests')

    fig = px.line(
        arrests_by_race_year,
        x='year_of_arrest',
        y='Arrests',
        color='arrestee_race',
        title='Arrests by Race Over Time',
        labels={'year_of_arrest': 'Year of Arrest', 'Arrests': 'Number of Arrests', 'arrestee_race': 'Arrestee Race'},
        hover_data={'year_of_arrest': True, 'arrestee_race': True, 'Arrests': True}
    )

    fig.update_layout(legend_title_text='Arrestee Race')
    return fig

def main():
    st.title("Gender, Crime, and Arrest Trends")

    gender_options = ['All'] + list(data['arrestee_sex'].unique())
    selected_gender = st.selectbox('Select Gender:', gender_options, key='gender_selectbox')

    if selected_gender != 'All':
        filtered_data = data[data['arrestee_sex'] == selected_gender]
    else:
        filtered_data = data

    st.subheader("Gender Distribution")
    gender_chart_fig = create_gender_chart(data)
    st.pyplot(gender_chart_fig)

    st.subheader(f"Crime Types for Selected Gender: {selected_gender if selected_gender != 'All' else 'All'}")
    crime_chart_fig = create_crime_chart(filtered_data)
    st.pyplot(crime_chart_fig)

    st.subheader("Arrests by Race Over Time")
    race_year_chart_fig = create_race_year_chart(data)
    st.plotly_chart(race_year_chart_fig)

if __name__ == "__main__":
    main()

st.write("""

This line graph provides a contextual visualization of arrest trends by race over time, spanning from around 1990 to 2015. It shows that arrests are highest for White individuals, followed by Black and Hispanic individuals, with arrest rates peaking in the early 2000s for both White and Black groups before gradually declining. Hispanic arrests follow a similar pattern at slightly lower levels, while Asian and American Indian/Alaskan groups show consistently low arrest rates over time. The "UNKNOWN" category reflects unclassified arrests, which remain minimal but steady. This contextual visualization highlights racial disparities and trends in arrest rates, offering insights into how they have evolved over time.
""")

