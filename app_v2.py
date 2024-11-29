import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


age_data = pd.read_csv('ages_test.csv')
core_details = pd.read_csv('core_details.csv')
core_proxies = pd.read_csv('core_proxies.csv')

############################# Writing 
st.title("Allan Hills ice core summary data")
st.write("Note: This is mostly preliminary, unpublished, and incomplete data.")

st.image("allan_hills.png")

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
core_details_filtered = core_details[core_details['Ice Core'].isin(unique_cores)]
    
st.write("Filtered data", filtered_data)
st.write("Summary data", core_details_filtered)


################# Plots

grouped_filtered_data = filtered_data.groupby("core")
grouped_core_proxies = core_proxies.groupby("core")

plot_choice = st.radio(
    "Select Plot Type:",
    ("Age", "CH4", "CO2", "dD", "d18O", "TAC")
    )

st.write("*Only 'Age' works with age and depth filters above*")

if plot_choice == "Age":
    for core, group in grouped_filtered_data:
        group = group.sort_values(by="TD")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(group["age"], group["TD"], label=f"Core {core}")
        ax.plot(group["age"], group["TD"], linestyle='-', color='grey', alpha=0.5)
        
        ax.set_xlabel("Age")
        ax.set_ylabel("Depth")
        ax.set_title(f"Depth vs. Age for {core}")
        ax.invert_yaxis()
        
        st.pyplot(fig)
        
elif plot_choice == "CH4":
    for core, group in grouped_core_proxies:
        if group[plot_choice].notna().any():
            group = group.sort_values(by="TD")
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(group["CH4"], group["TD"], label=f"Core {core}")
            ax.plot(group["CH4"], group["TD"], linestyle='-', color='grey', alpha=0.5)
            
            ax.set_xlabel("CH4")
            ax.set_ylabel("Depth")
            ax.set_title(f"CH4 vs. Depth for {core}")
            ax.invert_yaxis()
            
            st.pyplot(fig)
        else:
            st.write(f"No data available for {core}")

elif plot_choice == "CO2":
    for core, group in grouped_core_proxies:
        if group[plot_choice].notna().any():
            group = group.sort_values(by="TD")
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(group["CO2"], group["TD"], label=f"Core {core}")
            ax.plot(group["CO2"], group["TD"], linestyle='-', color='grey', alpha=0.5)
            
            ax.set_xlabel("CO2")
            ax.set_ylabel("Depth")
            ax.set_title(f"CO2 vs. Depth for {core}")
            ax.invert_yaxis()
            
            st.pyplot(fig)
        else:
            st.write(f"No data available for {core}")
        
elif plot_choice == "dD":
    for core, group in grouped_core_proxies:
        if group[plot_choice].notna().any():
            group = group.dropna(subset=["dD"])
            group = group.sort_values(by="TD")
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(group["dD"], group["TD"], label=f"Core {core}")
            ax.plot(group["dD"], group["TD"], linestyle='-', color='grey', alpha=0.5)
            
            ax.set_xlabel("dD")
            ax.set_ylabel("Depth")
            ax.set_title(f"dD vs. Depth for {core}")
            ax.invert_yaxis()
            
            st.pyplot(fig)
        else:
            st.write(f"No data available for {core}")
        
elif plot_choice == "d18O":
    for core, group in grouped_core_proxies:
        if group[plot_choice].notna().any():
            group = group.dropna(subset=["d18O"])
            group = group.sort_values(by="TD")
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(group["d18O"], group["TD"], label=f"Core {core}")
            ax.plot(group["d18O"], group["TD"], linestyle='-', color='grey', alpha=0.5)
            
            ax.set_xlabel("d18O")
            ax.set_ylabel("Depth")
            ax.set_title(f"d18O vs. Depth for {core}")
            ax.invert_yaxis()
            
            st.pyplot(fig)
        else:
            st.write(f"No data available for {core}")
        
elif plot_choice == "TAC":
    for core, group in grouped_core_proxies:
        if group[plot_choice].notna().any():
            group = group.sort_values(by="TD")
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(group["TAC"], group["TD"], label=f"Core {core}")
            ax.plot(group["TAC"], group["TD"], linestyle='-', color='grey', alpha=0.5)
            
            ax.set_xlabel("TAC")
            ax.set_ylabel("Depth")
            ax.set_title(f"TAC vs. Depth for {core}")
            ax.invert_yaxis()
            
            st.pyplot(fig)
        else:
            st.write(f"No data available for {core}")

