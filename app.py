import streamlit as st
from bokeh.plotting import figure, show

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
The name of the dataset is "Police_arrests". I found this dataset from data.illinois.gov. Here is the link of this dataset: https://data.illinois.gov/dataset/police-arrests/resource/ca1dceb3-01f8-4a56-935b-7e3035ff60a4. 

This dataset is available on the Data.illinois.gov. However, the dataset's page does not specify a particular license or terms of use. In the absence of explicit licensing information, I assume that the data is intended for public access and use, as it is hosted on a government open data platform. 

This usually allows for activities such as downloading, analyzing, and sharing the data, provided that proper attribution is given and the data is not used for commercial purposes without permission. 

The Police_arrests' file size is approximately 39.4 MB. It contains 206,600 rows and 25 columns. Github's web interface supports file uploads up to 100 MB. So, I can directly upload the file to a Github repository without issues.
""")

data = pd.read_csv("police_arrests.csv")

plt.figure(figsize=(10, 6))
filtered_ages = data[(data['age_at_arrest'] >= 0) & (data['age_at_arrest'] <= 100)]
plt.hist(filtered_ages['age_at_arrest'], bins=50, edgecolor='k')
plt.title('Distribution of Age at Arrest (Ages 0-100)')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()


file_path = "police_arrests.csv"
data = pd.read_csv(file_path)

filtered_data = data[(data['age_at_arrest'] >= 0) & (data['age_at_arrest'] <= 80)]

race_options = ['All'] + list(filtered_data['arrestee_race'].unique())
race_dropdown = widgets.Dropdown(
    options=race_options,
    value='All',
    description='Race:',
)

def create_age_histogram(df):
    hist, edges = pd.cut(df['age_at_arrest'], bins=16, retbins=True)
    counts = hist.value_counts(sort=False)
    bin_edges = [f"{int(edge.left)}-{int(edge.right)}" for edge in counts.index]

    x_scale = bq.OrdinalScale()
    y_scale = bq.LinearScale()
    bars = bq.Bars(
        x=bin_edges,
        y=counts.values,
        colors=['skyblue'] * len(counts), 
        scales={'x': x_scale, 'y': y_scale},
        tooltip=bq.Tooltip(fields=['x', 'y'], labels=['Age Range', 'Count']),
    )
    ax_x = bq.Axis(scale=x_scale, label='Age at Arrest (0–80)', grid_lines='none')
    ax_y = bq.Axis(scale=y_scale, orientation='vertical', label='Number of Arrests')
    return bq.Figure(marks=[bars], axes=[ax_x, ax_y], title='Age Distribution (0–80)'), bars

def create_crime_bar_chart(df):
    crime_counts = df['crime_category_description'].value_counts()

    top_10_crimes = crime_counts.head(10)
    x_scale = bq.OrdinalScale()
    y_scale = bq.LinearScale()
    bars = bq.Bars(
        x=top_10_crimes.index,
        y=top_10_crimes.values,
        colors=['skyblue'] * len(top_10_crimes), 
        scales={'x': x_scale, 'y': y_scale},
        tooltip=bq.Tooltip(fields=['x', 'y'], labels=['Crime Category', 'Count']),
    )
    ax_x = bq.Axis(scale=x_scale, label='Top 10 Crime Categories', grid_lines='none')
    ax_y = bq.Axis(scale=y_scale, orientation='vertical', label='Number of Arrests')
    return bq.Figure(marks=[bars], axes=[ax_x, ax_y], title='Top 10 Crime Categories'), bars

age_hist_figure, age_bars = create_age_histogram(filtered_data)
crime_bar_figure, crime_bars = create_crime_bar_chart(filtered_data)

def update_graphs(change):
    selected_race = race_dropdown.value
    global age_hist_figure, age_bars, crime_bar_figure, crime_bars

    if selected_race == 'All':
        filtered_race_data = filtered_data
    else:
        filtered_race_data = filtered_data[filtered_data['arrestee_race'] == selected_race]

    hist, edges = pd.cut(filtered_race_data['age_at_arrest'], bins=16, retbins=True)
    counts = hist.value_counts(sort=False)
    bin_edges = [f"{int(edge.left)}-{int(edge.right)}" for edge in counts.index]
    age_bars.x = bin_edges
    age_bars.y = counts.values

    crime_counts = filtered_race_data['crime_category_description'].value_counts().head(10)
    crime_bars.x = crime_counts.index
    crime_bars.y = crime_counts.values

race_dropdown.observe(update_graphs, names='value')

dashboard = widgets.VBox([
    race_dropdown,
    widgets.Label("Interactive Arrest Data Visualization", style={'font-size': '20px'}),
    age_hist_figure,
    crime_bar_figure
])

dashboard



file_path = "police_arrests.csv" 
data = pd.read_csv(file_path)

def create_gender_crime_chart(df):
    gender_counts = df['arrestee_sex'].value_counts()
    
    x_scale_gender = bq.OrdinalScale()
    y_scale_gender = bq.LinearScale()
    gender_bars = bq.Bars(
        x=gender_counts.index,
        y=gender_counts.values,
        scales={'x': x_scale_gender, 'y': y_scale_gender},
        colors=['#ff9999', '#66b3ff'], 
        tooltip=bq.Tooltip(fields=['x', 'y'], labels=['Gender', 'Count']),
    )
    gender_bars.interactions = {'click': 'select'} 
    ax_x_gender = bq.Axis(scale=x_scale_gender, label='Gender', grid_lines='none')
    ax_y_gender = bq.Axis(scale=y_scale_gender, orientation='vertical', label='Number of Arrests')
    gender_chart = bq.Figure(
        marks=[gender_bars],
        axes=[ax_x_gender, ax_y_gender],
        title='Gender Distribution'
    )

    crime_counts = df['crime_category_description'].value_counts().head(10)

    x_scale_crime = bq.OrdinalScale()
    y_scale_crime = bq.LinearScale()
    crime_bars = bq.Bars(
        x=crime_counts.index,
        y=crime_counts.values,
        scales={'x': x_scale_crime, 'y': y_scale_crime},
        colors=['orange'] * len(crime_counts),
        tooltip=bq.Tooltip(fields=['x', 'y'], labels=['Crime Category', 'Count']),
    )
    ax_x_crime = bq.Axis(scale=x_scale_crime, label='Crime Category', grid_lines='none')
    ax_y_crime = bq.Axis(scale=y_scale_crime, orientation='vertical', label='Number of Arrests')
    crime_chart = bq.Figure(
        marks=[crime_bars],
        axes=[ax_x_crime, ax_y_crime],
        title='Crime Types for Selected Gender'
    )

    return gender_chart, gender_bars, crime_chart, crime_bars

gender_chart, gender_bars, crime_chart, crime_bars = create_gender_crime_chart(data)

def update_crime_chart(change):
    selected_indices = gender_bars.selected
    if selected_indices:
        selected_gender = gender_bars.x[selected_indices[0]]
        filtered_data = data[data['arrestee_sex'] == selected_gender]
        crime_counts = filtered_data['crime_category_description'].value_counts().head(10)
    else:
        crime_counts = data['crime_category_description'].value_counts().head(10)

    crime_bars.x = crime_counts.index
    crime_bars.y = crime_counts.values
    crime_chart.title = f'Crime Types for Selected Gender: {selected_gender if selected_indices else "All"}'

gender_bars.observe(update_crime_chart, names='selected')

dashboard = widgets.VBox([
    widgets.Label("Gender and Crime Distribution", style={'font-size': '20px'}),
    gender_chart,
    crime_chart,
])
dashboard



arrests_by_race_year = data.groupby(['year_of_arrest', 'arrestee_race']).size().reset_index(name='Arrests')

p = figure(
    title="Arrests by Race Over Time",
    x_axis_label="Year of Arrest",
    y_axis_label="Number of Arrests",
    width=900,  
    height=500,  
    tools="pan,box_zoom,reset,save"
)

palette = Category10[10]
race_colors = {race: palette[i % len(palette)] for i, race in enumerate(arrests_by_race_year['arrestee_race'].unique())}

legend_items = []

for race in arrests_by_race_year['arrestee_race'].unique():
    race_data = arrests_by_race_year[arrests_by_race_year['arrestee_race'] == race]
    source = ColumnDataSource(race_data)
    
    line = p.line(
        x='year_of_arrest',
        y='Arrests',
        source=source,
        legend_label=race,
        line_width=2,
        name=race,
        color=race_colors[race] 
    )
    
    legend_items.append((race, [line]))
    
    hover = HoverTool(
        tooltips=[
            ("Year", "@year_of_arrest"),
            ("Race", "@arrestee_race"),
            ("Arrests", "@Arrests")
        ],
        renderers=[line]
    )
    p.add_tools(hover)

p.legend.visible = False

legend = Legend(items=legend_items, location="center")
legend.orientation = "horizontal"
legend.label_text_font_size = "10pt"
legend.title = "Arrestee Race"
legend.title_text_font_size = "12pt"

p.add_layout(legend, 'below')

output_notebook()
show(p)
