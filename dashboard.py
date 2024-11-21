import streamlit as st
import pandas as pd

st.header("2024 AHI 507 Streamlit Example")
st.subheader("We are going to go through a couple different examples of loading and visualization information into this dashboard")

st.text("""In this streamlit dashboard, we are going to focus on some recently released school learning modalities data from the NCES, for the years of 2021.""")

# ## https://healthdata.gov/National/School-Learning-Modalities-2020-2021/a8v3-a3m3/about_data
df = pd.read_csv("https://healthdata.gov/resource/a8v3-a3m3.csv?$limit=50000") ## first 1k 

## data cleaning 
df['week_recoded'] = pd.to_datetime(df['week'])
df['zip_code'] = df['zip_code'].astype(str)

df['week'].value_counts()

## box to show how many rows and columns of data we have: 
col1, col2, col3 = st.columns(3)
col1.metric("Columns", df.shape[1]) 
col2.metric("Rows", len(df))
col3.metric("Number of unique districts/schools:", df['district_name'].nunique())

## exposing first 1k of NCES 20-21 data
st.dataframe(df)



table = pd.pivot_table(df, values='student_count', index=['week'],
                       columns=['learning_modality'], aggfunc="sum")

table = table.reset_index()
table.columns

## line chart by week 
st.bar_chart(
    table,
    x="week",
    y="Hybrid",
)

st.bar_chart(
    table,
    x="week",
    y="In Person",
)

st.bar_chart(
    table,
    x="week",
    y="Remote",
)


## Starting on this line and below is my enhancement to the code
st.header("Dashboard overview")

st.markdown("""
## Add New Visulization
This dashboard visualizes data on school learning modalities in 2020-2021. 
You can explore the distribution of different learning modes (Hybrid, In Person, Remote) across weeks.
Replaced multiple bar chart with a consolidated line chart for better visulization over time and also a pie chart for those that like pies.

### Data Source
The data is sourced from the **National Center for Education Statistics (NCES)** and provides insights into learning trends during the pandemic.
""") 
import plotly.express as px

# Line chart with plotly
fig = px.line(
    table.melt(id_vars=["week"], var_name="Learning Modality", value_name="Student Count"),
    x="week",
    y="Student Count",
    color="Learning Modality",
    title="Student Learning Modalities Over Time",
)
st.plotly_chart(fig)


modality_totals = df.groupby("learning_modality")["student_count"].sum().reset_index()

fig_pie = px.pie(
    modality_totals, 
    values="student_count", 
    names="learning_modality",
    title="Proportion of Students by Learning Modality"
)
st.plotly_chart(fig_pie)

st.markdown("""
## Add New Interactive Component 
This will enable users to filer data by week if desiered.
""")

selected_week = st.selectbox("Select a Week:", options=df['week'].unique())

# Filter data based on the selected week
filtered_data = df[df['week'] == selected_week]
st.write(f"Data for week: {selected_week}")
st.dataframe(filtered_data)

## This allows users to choose whether they want to see the raw data
if st.checkbox("Show Raw Data"):
    st.dataframe(df)

st.markdown("""
## Improved Dashboard Layout
""")


# Split into two sections for better layout
col1, col2 = st.columns(2)

# Metrics
col1.metric("Total Rows", df.shape[0])
col2.metric("Unique Districts", df['district_name'].nunique())

# Pivot Table Summary
st.markdown("### Pivot Table Summary")
st.dataframe(table)


st.markdown("""
## Animated Visulization
This is my first attempt that a visulization with animation

""")

# Prepare data for animation
animation_data = df.groupby(['week_recoded', 'learning_modality'])['student_count'].sum().reset_index()

fig_animation = px.bar(
    animation_data,
    x="learning_modality",
    y="student_count",
    color="learning_modality",
    animation_frame="week_recoded",
    title="Student Counts by Learning Modality Over Time",
    labels={"student_count": "Student Count", "learning_modality": "Learning Modality"},
)
st.plotly_chart(fig_animation)




st.markdown("""
## Geographical Visulization
This is my first attempt that a geographical visualization

""")
# Aggregate data by zip code and modality
geo_data = df.groupby(['zip_code', 'learning_modality'])['student_count'].sum().reset_index()

# Sample latitude/longitude data (replace with real geolocation data)
geo_data['latitude'] = pd.to_numeric(geo_data['zip_code'].str[:2]) * 2  # Example: mock latitudes
geo_data['longitude'] = pd.to_numeric(geo_data['zip_code'].str[:2]) * -2  # Example: mock longitudes

# Plot geographic scatter map
fig_geo = px.scatter_geo(
    geo_data,
    lat="latitude",
    lon="longitude",
    color="learning_modality",
    size="student_count",
    hover_name="zip_code",
    title="Learning Modalities by Location",
)
st.plotly_chart(fig_geo)


st.markdown("""
## Heat Map
This is my first attempt that a heat map style visualization

""")



import seaborn as sns
import matplotlib.pyplot as plt

# Pivot data for heatmap
heatmap_data = pd.pivot_table(
    df, values="student_count", index="week_recoded", columns="learning_modality", aggfunc="sum"
)

# Plot heatmap
st.markdown("### Heatmap of Learning Modalities Over Time")
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(heatmap_data, cmap="coolwarm", annot=True, fmt=".0f", ax=ax)
ax.set_title("Student Counts by Learning Modality and Week")
st.pyplot(fig)

