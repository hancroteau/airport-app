"""
Hannah Croteau
CS230-6
Data: New England Airports

Description:
This program uses features to display New England airport data based on
user input through a navigation sidebar and elevation slider.
This data is visualized through a 2d map, bar chart, pie chart,
line chart, and a table that displays the filtered data by elevation
and latitude. This information is helpful to explore the distribution
of New England airports and can provide insights into its characteristics.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Load dataset using pandas
def load_data():
    df = pd.read_csv('new_england_airports.csv')
    return df

# Code for 2d map based on code from ChatGPT. See accompany AI report submitted with python file.
def show_map(df):
    #[PY2] Function creates a 2D map of New England airports using latitude and longitude

    st.write("Displaying a 2D map of New England Airports")

    # [VIZ1] Create a 2D map
    fig = go.Figure(data=go.Scattergeo(
        lon=df["longitude_deg"],
        lat=df["latitude_deg"],
        hoverinfo='text',
        mode='markers',
        marker=dict(
            size=5,
            color='red',
            opacity=0.8,
            symbol='circle',
        )
    ))

    # Customize the map
    fig.update_layout(
        title='2D Map of New England Airports',
        geo=dict(
            projection_type='mercator',
            scope='north america',
            showland=True,
            landcolor='rgb(243, 243, 243)',
            countrycolor='rgb(204, 204, 204)',
            coastlinecolor='rgb(204, 204, 204)',
            lakecolor='rgb(255, 255, 255)'
        ),
    )

    st.plotly_chart(fig)  # [ST2] Displays map with Plotly in Streamlit

# Function creates a bar chart showing the number of airports by state
def create_airports_by_state_bar_chart(df):
    #[PY3] Function to create a bar chart for the number of airports by state

    # Count airports by state
    state_counts = df['iso_region'].value_counts()

    # [VIZ2] Create the bar chart
    plt.figure(figsize=(12, 6))
    state_counts.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title("Number of Airports by State")
    plt.xlabel("State")
    plt.ylabel("Number of Airports")
    plt.xticks(rotation=45)

    # Customize grid lines and colors
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # [ST3] Displaying the bar chart using Streamlit
    st.pyplot(plt)

def create_elevation_trend_line_chart(df):
    #[VIZ3] Function creates a line chart for the average elevation of airports in each state

    # Group the data by state and calculate average elevation
    elevation_trend = df.groupby('iso_region')['elevation_ft'].mean()

    # Create a line chart for the elevation trend
    plt.figure(figsize=(12, 6))
    elevation_trend.plot(kind='line', color='green', marker='o', linewidth=2)
    plt.title("Average Elevation of Airports by State")
    plt.xlabel("State")
    plt.ylabel("Average Elevation (ft)")
    plt.xticks(rotation=45)

    # [ST4] Displays line chart using Streamlit
    st.pyplot(plt)

def create_airports_by_state_pie_chart(df):
    # [VIZ4] Function to create a pie chart for the distribution of airports by state

    # Count airports by state
    state_counts = df['iso_region'].value_counts()

    # Each state is associated with its own unique color to make it visually appealing
    colors = plt.cm.Paired(range(len(state_counts)))

    # Create pie chart
    plt.figure(figsize=(8, 8))
    state_counts.plot(kind='pie', autopct='%1.1f%%', colors=colors)
    plt.title("Distribution of Airports by State")

    # [ST5] Displays the pie chart using Streamlit
    st.pyplot(plt)

def filter_data(df):
    # [PY4] Function to display data based on user-selected state and elevation range

    # [DA1] Filter options to only return unique values
    states = df['iso_region'].unique()
    state_filter = st.selectbox("Select a State:", states)  # [ST1] Dropdown filter for state

    # Elevation filter using Streamlit slider
    min_elev = int(df['elevation_ft'].min())
    max_elev = int(df['elevation_ft'].max())
    # [DA3] This uses the min and max to create the elevation range
    # [ST2] Slider filter for elevation
    elevation_filter = st.slider("Select Elevation Range:", min_elev, max_elev, (min_elev, max_elev))

    # [DA4] Apply filters to the dataset based on conditions of state and elevation
    filtered_df = df[(df['iso_region'] == state_filter) &
                     (df['elevation_ft'] >= elevation_filter[0]) &
                     (df['elevation_ft'] <= elevation_filter[1])]

    return filtered_df, state_filter, elevation_filter

def display_summary_statistics(filtered_df):
    # [DA5] Function displays the average elevation of the filtered airports

    # Calculate the average elevation of the filtered airports
    average_elevation = filtered_df['elevation_ft'].mean()
    # [ST4] Displaying summary statistic
    st.write(f"Average elevation of the filtered airports: {average_elevation:.2f} ft")

def display_filtered_data(filtered_df, state_filter, elevation_filter):
    # [PY5] Function displays filtered airport data

    # [ST4] Display filtered data table
    st.write(f"Displaying {len(filtered_df)} airports in {state_filter} with elevation range {elevation_filter[0]} ft to {elevation_filter[1]} ft.")
    st.dataframe(filtered_df)

def sort_data(filtered_df):
    # [PY6] Function to sort filtered data by either elevation or latitude

    # [ST1] Dropdown for sorting options
    sort_by = st.selectbox("Sort by:", ["Elevation", "Latitude"])
    # [DA2] Sort by elevation
    if sort_by == "Elevation":
        sorted_df = filtered_df.sort_values(by="elevation_ft", ascending=False)
    else:
    # [DA2] Sort by latitude
        sorted_df = filtered_df.sort_values(by="latitude_deg", ascending=False)

    return sorted_df, sort_by

def main():
    # [PY7] Main function to execute the Streamlit app
    df = load_data()

    # [ST4] Creates sidebar to flip through data
    page = st.sidebar.selectbox("Select a Page", ["Home", "Map", "Bar Chart", "Line Chart", "Pie Chart", "Filter Data"])

    if page == "Home":
        # Display the homepage
        # [ST3] Page title
        st.title("Learn more about New England airports!")
        st.write("Select a page from the sidebar to explore the data.")

    elif page == "Map":
        # Display the 2d map of airports
        st.title("Learn more about New England airports!")
        show_map(df)

    elif page == "Bar Chart":
        # Display the bar chart of airports by state
        st.title("Learn more about New England airports!")
        create_airports_by_state_bar_chart(df)

    elif page == "Line Chart":
        # Display the line chart for average elevation by state
        st.title("Learn more about New England airports!")
        create_elevation_trend_line_chart(df)

    elif page == "Pie Chart":
        # Display the pie chart for airport distribution by state
        st.title("Learn more about New England airports!")
        create_airports_by_state_pie_chart(df)

    elif page == "Filter Data":
        # Filter data and display the filtered airports
        st.title("Learn more about New England airports!")
        filtered_df, state_filter, elevation_filter = filter_data(df)
        display_filtered_data(filtered_df, state_filter, elevation_filter)

        # Display summary statistics
        # [DA5] Display summary statistics
        display_summary_statistics(filtered_df)

        # Sort data by user selection and display
        sorted_df, sort_by = sort_data(filtered_df)
        st.write(f"### Sorted Airports by {sort_by}:")
        st.dataframe(sorted_df)

if __name__ == "__main__":
    main()
