import streamlit as st
import pandas as pd
st.header("Worldwide Analysis of Quality of Life and Economic Factors")
st.markdown("### This app enables you to explore the relationships between poverty, life expectancy, and GDP across various countries and years. Use the panels to select options and interact with the data.")

#create 3 tabs called "Global Overview", "Country Deep Dive", "Data Explorer"
tab1, tab2, tab3 = st.tabs(["Global Overview", "Country Deep Dive", "Data Explorer"])
url = "https://raw.githubusercontent.com/JohannaViktor/streamlit_practical/refs/heads/main/global_development_data.csv"
data = pd.read_csv(url)
#show the dataset in the 3rd tab

#include a multiselectbox to select the country names in 3rd tab
with tab3:
    st.subheader("Select Countries")
    countries = data['country'].unique()
    selected_countries = st.multiselect("Select countries to display", options=countries, default=countries[:5])
    filtered_data = data[data['country'].isin(selected_countries)]
    st.dataframe(filtered_data)
    st.subheader("Select Year Range")
    min_year = int(data['year'].min())
    max_year = int(data['year'].max())
    year_range = st.slider("Select year range", min_value=min_year, max_value=max_year, value=(min_year, max_year))
    filtered_data = filtered_data[(filtered_data['year'] >= year_range[0]) & (filtered_data['year'] <= year_range[1])]
    st.dataframe(filtered_data)
#make the filtered dataset downloadablewith a download button in the 3rd tab
with tab3:
    st.subheader("Download Filtered Data")
    csv = filtered_data.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download CSV", data=csv, file_name='filtered_data.csv', mime='text/csv')

