import streamlit as st
import pandas as pd
import plotly.express as px
from model import train_model, predict_life_expectancy
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

#task 4 in tab 1
#create a slider to select a certain year, filter the dataset accordingly
with tab1:
    st.subheader("Select Year")
    year = st.slider("Select year", min_value=int(data['year'].min()), max_value=int(data['year'].max()), value=int(data['year'].min()))
    filtered_data = data[data['year'] == year]
    #create 4 key metrics in 4 columns each with a description: 
    #col1: mean of life expectancy; 
    #col2: median of GDP per capita; 
    #col3: mean of headcount_ratio_upper_mid_income_povline; 
    #col4: Number of countries
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Mean Life Expectancy", value=filtered_data['Life Expectancy (IHME)'].mean())
    with col2:
        st.metric("Median GDP per Capita", value=filtered_data['GDP per capita'].median())
    with col3:
        st.metric("Mean Headcount Ratio", value=filtered_data['headcount_ratio_upper_mid_income_povline'].mean())
    with col4:
        st.metric("Number of Countries", value=filtered_data.shape[0])
    
    #task 5: create scatterplot
    st.subheader("GDP per Capita vs Life Expectancy")
    fig = px.scatter(filtered_data, x='GDP per capita', y='Life Expectancy (IHME)', 
                     hover_name='country', log_x=True, 
                     size='headcount_ratio_upper_mid_income_povline', 
                     color='country', 
                     title='GDP per Capita vs Life Expectancy',
                     labels={'GDP per capita': 'GDP per Capita (log scale)', 'Life Expectancy (IHME)': 'Life Expectancy'})
    st.plotly_chart(fig)
# task 6: create a random forest regression model to predict life expectancy based on GDP per capita, headcount ratio and year. Show the feature importance in a bar chart in the first tab
    st.subheader("Life Expectancy Prediction Model")

    model, features = train_model(data)

    # Input fields

    col1, col2, col3 = st.columns(3)

    with col1:

        gdp = st.slider("GDP per capita", min_value=float(data['GDP per capita'].min()), max_value=float(data['GDP per capita'].max()), value=float(data['GDP per capita'].mean()))

    with col2:

        headcount = st.slider("Headcount Ratio", min_value=float(data['headcount_ratio_upper_mid_income_povline'].min()), max_value=float(data['headcount_ratio_upper_mid_income_povline'].max()), value=float(data['headcount_ratio_upper_mid_income_povline'].mean()))

    with col3:

        pred_year = st.slider("Year", min_value=int(data['year'].min()), max_value=int(data['year'].max()), value=int(data['year'].max()))

    

    if st.button("Predict Life Expectancy"):

        pred = predict_life_expectancy(model, features, gdp, headcount, pred_year)

        st.success(f"Predicted Life Expectancy: {pred:.2f} years")

    

    # Feature importance

    st.subheader("Feature Importance")

    importances = model.feature_importances_

    fig_imp = px.bar(x=features, y=importances, title="Feature Importance for Life Expectancy Prediction")

    st.plotly_chart(fig_imp)
#task 7 in tab 1: create a map plot. use chatgpt or similar to create lat and lon values for each country (e.g. capital as reference)
    st.subheader("Global Life Expectancy Map")
    # Create a mapping of countries to their latitudes and longitudes (using capital cities as reference points)
    country_coords = {
        'United States': (38.8977, -77.0365),  # Washington, D.C.
        'China': (39.9042, 116.4074),  # Beijing
        'India': (28.6139, 77.2090),  # New Delhi
        'Brazil': (-15.8267, -47.9218),  # Brasília
        'Russia': (55.7558, 37.6173),  # Moscow
        'Germany': (52.5200, 13.4050),  # Berlin
        'United Kingdom': (51.5074, -0.1278),  # London
        'France': (48.8566, 2.3522),  # Paris
        'Japan': (35.6895, 139.6917),  # Tokyo
        'Mexico': (19.4326, -99.1332),  # Mexico City
        # Add more countries and their coordinates as needed
    }      
    # Merge the coordinates with the filtered data
    map_data = filtered_data.copy()
    map_data['lat'] = map_data['country'].map(lambda x: country_coords.get(x, (None, None))[0])
    map_data['lon'] = map_data['country'].map(lambda x: country_coords.get(x, (None, None))[1])
    # Create the map plot
    fig_map = px.scatter_geo(map_data, lat='lat', lon='lon', color='Life Expectancy (IHME)', size='GDP per capita',
                             hover_name='country')
    fig_map.update_layout(title='Global Life Expectancy Map', geo=dict(showland=True))
    st.plotly_chart(fig_map)    
