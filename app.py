import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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
core_details_filtered = core_details[core_details['core'].isin(unique_cores)]
    
st.write("Filtered data", filtered_data)
st.write("Summary data", core_details_filtered)

########### Summary data

# Widgets to select age threshold
# age_threshold = st.slider("Select Age Threshold", min_value=0.0, max_value=5.0, value=0.8, step=0.1)
# 
# ########### Calculations ###########
# 
# def calculate_depth_percentage(age_data, core_details, age_threshold):
#     # Convert 'depth' to numeric and drop missing values
#     core_details["depth"] = pd.to_numeric(core_details["Depth"], errors="coerce")
#     core_details = core_details.dropna(subset=["Depth"])
# 
#     # Get the maximum depth for each core
#     max_depths = core_details.groupby("core")["Depth"].max()
# 
#     # Filter rows where age is greater than the threshold
#     age_data["is_above_threshold"] = age_data["age"] > age_threshold
# 
#     # Group by core and calculate required sums
#     core_summaries = (
#         age_data.groupby("core")
#         .apply(
#             lambda group: pd.Series({
#                 "total_depth_sum": group["TD"].sum(),
#                 "depth_above_threshold": group.loc[group["is_above_threshold"], "TD"].sum(),
#                 "max_depth": max_depths.get(group.name, None),  # Get max depth for the core
#             })
#         )
#         .reset_index()
#     )
# 
#     # Safeguard against division by zero
#     core_summaries["percentage_above_threshold"] = (
#         core_summaries["depth_above_threshold"] / core_summaries["max_depth"] * 100
#     ).fillna(0)  # Replace NaN with 0 for cores without valid max_depth
# 
#     return core_summaries
# 
# def calculate_age_percentage(age_data, age_threshold):
#     core_summaries = (
#         age_data.groupby("core")
#         .apply(
#             lambda group: pd.Series({
#                 "total_points": len(group),
#                 "points_above_threshold": len(group[group["age"] > age_threshold]),
#             })
#         )
#         .reset_index()
#     )
# 
#     # Calculate percentages
#     core_summaries["percentage_above_threshold"] = (
#         core_summaries["points_above_threshold"] / core_summaries["total_points"] * 100
#     )
# 
#     return core_summaries
# 
# depth_summary = calculate_depth_percentage(age_data, core_details, age_threshold)
# age_summary = calculate_age_percentage(age_data, age_threshold)

################# Plots

#depth x age plots for unique core ids in filtered_data

import matplotlib.pyplot as plt
import streamlit as st

# Group data by 'core' to create individual plots for each core
grouped = filtered_data.groupby("core")

# Loop through each group and create a separate plot for each core
for core, group in grouped:
    # Sort by depth (TD) to ensure the line goes in the correct order
    group = group.sort_values(by="TD")

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot the scatter points
    ax.scatter(group["age"], group["TD"], label=f"Core {core}")
    
    # Plot the line connecting the dots, in order of depth
    ax.plot(group["age"], group["TD"], linestyle='-', color='blue', alpha=0.5)
    
    # Add labels and title
    ax.set_xlabel("Age")
    ax.set_ylabel("Depth")
    ax.set_title(f"Depth vs. Age for Core {core}")
    ax.invert_yaxis()  # Invert the y-axis to show depth descending
    
    # Show the plot in Streamlit
    st.pyplot(fig)



################## depth minimum for age groups

# 
# depth_thresholds = [0.8, 1, 2, 3, 4, 5, 6]
# 
# # Prepare a list to hold the rows for the summary table
# summary_rows = []
# 
# # Group data by core
# grouped = filtered_data.groupby("core")
# 
# # Process each core
# for core, group in grouped:
#     # Initialize a row for this core
#     row = {"core": core}
#     for threshold in depth_thresholds:
#         # Filter rows where TD > threshold
#         filtered_group = group[(group["TD"] > (threshold - 1)) & (group["TD"] > threshold)]
#         
#         # Find the minimum depth where TD > threshold
#         min_depth = filtered_group["TD"].min() if not filtered_group.empty else np.nan
#         
#         # Count the number of data points where TD > threshold
#         points_above_threshold = filtered_group.shape[0]  # Number of rows
#         
#         # Add data for this threshold to the row
#         row[f"min depth > {threshold}"] = min_depth
#         row[f"points > {threshold} Ma"] = points_above_threshold
#     
#     # Append the row to the list of rows
#     summary_rows.append(row)
# 
# 
# 
# 
# 
# summary_table = pd.DataFrame(result)
# st.write("The minimum depth (m) at which each age (Ma) is found and the number of data points at each age grouping", summary_table)

########### Display Results ###########

# Display Depth-Based Percentage
# st.header("Percentage Above Age Threshold (By Depth)")
# st.dataframe(depth_summary)

# Display Age Points-Based Percentage
# st.header("Percentage Above Age Threshold (By Data Points)")
# st.dataframe(age_summary)

