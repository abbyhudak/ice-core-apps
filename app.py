import streamlit as st
import pandas as pd
import numpy as np


age_data = pd.read_csv('ages_test.csv')
core_details = pd.read_csv('core_details.csv')

########### Filters

# Age filter
age_ranges = np.arange(0, 7, 0.5)
age_filter = st.slider("Select age range (optional)", min_value=0.0, max_value=7.0, value=(0.0, 7.0), step=0.5)

#Depth filter
depth_ranges = np.arange(0, 250, 10)
depth_filter = st.slider("Select depth range (optional)", min_value=0, max_value=250, value=(0, 250), step=10)

########### Data filtering
filtered_data = age_data

# Apply age filter if selected
if age_filter is not None:
    filtered_data = filtered_data[
        (filtered_data['age'] >= age_filter[0]) & (filtered_data['age'] <= age_filter[1])
    ]

# Apply depth filter if selected
if depth_filter is not None:
    filtered_data = filtered_data[
        (filtered_data['TD'] >= depth_filter[0]) & (filtered_data['TD'] <= depth_filter[1])
    ]
    
unique_cores = filtered_data['core'].unique()
    
st.write("Filtered data", filtered_data)
st.write("Summary data", core_details)

########### Summary data

### Unique core IDs with these criteria

### Percent core > 800 kyr

# by depth 
#Find percentage of core that is > 0.8 age by summing the depths in which this is true divided by the total depth from core_details['depth']


# by age points
#Find percentage of core that is > 0.8 age by summing the number of data points in age_data where this is true divided by total data points



# Streamlit App Title
st.title("Core Data Analysis")

# Widgets to select age threshold
age_threshold = st.slider("Select Age Threshold", min_value=0.0, max_value=5.0, value=0.8, step=0.1)

########### Calculations ###########

def calculate_depth_percentage(age_data, core_details, age_threshold):
    # Convert 'depth' to numeric and drop missing values
    core_details["depth"] = pd.to_numeric(core_details["Depth"], errors="coerce")
    core_details = core_details.dropna(subset=["Depth"])

    # Get the maximum depth for each core
    max_depths = core_details.groupby("core")["Depth"].max()

    # Filter rows where age is greater than the threshold
    age_data["is_above_threshold"] = age_data["age"] > age_threshold

    # Group by core and calculate required sums
    core_summaries = (
        age_data.groupby("core")
        .apply(
            lambda group: pd.Series({
                "total_depth_sum": group["TD"].sum(),
                "depth_above_threshold": group.loc[group["is_above_threshold"], "TD"].sum(),
                "max_depth": max_depths.get(group.name, None),  # Get max depth for the core
            })
        )
        .reset_index()
    )

    # Safeguard against division by zero
    core_summaries["percentage_above_threshold"] = (
        core_summaries["depth_above_threshold"] / core_summaries["max_depth"] * 100
    ).fillna(0)  # Replace NaN with 0 for cores without valid max_depth

    return core_summaries
  
def calculate_age_percentage(age_data, age_threshold):
    core_summaries = (
        age_data.groupby("core")
        .apply(
            lambda group: pd.Series({
                "total_points": len(group),
                "points_above_threshold": len(group[group["age"] > age_threshold]),
            })
        )
        .reset_index()
    )

    # Calculate percentages
    core_summaries["percentage_above_threshold"] = (
        core_summaries["points_above_threshold"] / core_summaries["total_points"] * 100
    )

    return core_summaries

depth_summary = calculate_depth_percentage(age_data, core_details, age_threshold)
age_summary = calculate_age_percentage(age_data, age_threshold)

########### Display Results ###########

# Display Depth-Based Percentage
st.header("Percentage Above Age Threshold (By Depth)")
st.dataframe(depth_summary)

# Display Age Points-Based Percentage
st.header("Percentage Above Age Threshold (By Data Points)")
st.dataframe(age_summary)

