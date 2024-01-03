"""Main file for Streamlit dashboard"""
import requests
from bs4 import BeautifulSoup
import xlrd
import pandas as pd
from tempfile import NamedTemporaryFile
import streamlit as st
import pandas as pd
from functions.extract_data import create_df
from functions.clean_data import clean_cols, convert_numerical, convert_to_date, adjust_month_to_marketing_year, new_date_cols
from functions.arima_models import prepare_for_modelling, imports_model, plot_imports, harvest_model, plot_harvest, yield_model, plot_yield
from statsmodels.tsa.arima.model import ARIMA
import warnings

st.title('Forecast of WASDE report')

########## get data  ##################
all_data_df = create_df()
df_cleaned = clean_cols(all_data_df)
df_cleaned = convert_numerical(df_cleaned)
df_cleaned = new_date_cols(df_cleaned)

# use csv file while developing to be faster
#df_cleaned = pd.read_csv("cleaned_data.csv")  

# prepare data for modelling
most_recent, df_cleaned = prepare_for_modelling(df_cleaned)


############## imports ########################
st.header('Analysis of Imports')
# do analysis for imports
imports_data, integrated_forecast, integrated_confidence_intervals = imports_model(df_cleaned)
# Generate the plot
plt = plot_imports(imports_data, integrated_forecast, integrated_confidence_intervals)

# Sample data
data = {
    "Date": ["Dec 2023/24 Proj.", "Jan 2023/24 Proj.", "Feb 2023/24 Proj.", "Mar 2023/24 Proj.", "Apr 2023/24 Proj."],
    "Forecasted": integrated_forecast,
    "Actual": [most_recent['Imports'], 0, 0, 0, 0],
    "Difference": [integrated_forecast[0]-most_recent['Imports'], 0, 0, 0, 0]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Transpose the DataFrame
df_transposed = df.T

# Convert transposed DataFrame to HTML without the index
html_transposed = df_transposed.to_html(header=False, index=True)

# Display the plot in Streamlit
st.pyplot(plt)
# Display the transposed DataFrame as HTML
st.markdown(html_transposed, unsafe_allow_html=True)

############## Area Harvested ########################
st.header('Analysis of Area Harvested')
# do analysis for imports
harvest_data, forecast_mean, confidence_intervals = harvest_model(df_cleaned)
# Generate the plot
plt = plot_harvest(harvest_data, forecast_mean, confidence_intervals)

# Sample data
data = {
    "Date": ["Dec 2023/24 Proj.", "Jan 2023/24 Proj.", "Feb 2023/24 Proj.", "Mar 2023/24 Proj.", "Apr 2023/24 Proj."],
    "Forecasted": forecast_mean,
    "Actual": [most_recent['Area_Harvested'], 0, 0, 0, 0],
    "Difference": [forecast_mean[0]-most_recent['Area_Harvested'], 0, 0, 0, 0]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Transpose the DataFrame
df_transposed = df.T

# Convert transposed DataFrame to HTML without the index
html_transposed = df_transposed.to_html(header=False, index=True)

# Display the plot in Streamlit
st.pyplot(plt)
# Display the transposed DataFrame as HTML
st.markdown(html_transposed, unsafe_allow_html=True)


############## Yield per Acre ########################
st.header('Analysis of Yield per Acre')
# do analysis for yield
yield_data, forecast_mean, confidence_intervals = yield_model(df_cleaned)
# Generate the plot
plt = plot_yield(yield_data, forecast_mean, confidence_intervals)

# Sample data
data = {
    "Date": ["Dec 2023/24 Proj.", "Jan 2023/24 Proj.", "Feb 2023/24 Proj.", "Mar 2023/24 Proj.", "Apr 2023/24 Proj."],
    "Forecasted": forecast_mean,
    "Actual": [most_recent['Yield_per_Acre'], 0, 0, 0, 0],
    "Difference": [forecast_mean[0]-most_recent['Yield_per_Acre'], 0, 0, 0, 0]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Transpose the DataFrame
df_transposed = df.T

# Convert transposed DataFrame to HTML without the index
html_transposed = df_transposed.to_html(header=False, index=True)

# Display the plot in Streamlit
st.pyplot(plt)
# Display the transposed DataFrame as HTML
st.markdown(html_transposed, unsafe_allow_html=True)

st.header('Predicted WASDE Report Jan 2023/24 Proj.')
# Data extracted from the provided image for the corn statistics table
data = {
    "": ["Area Planted", "Area Harvested", "Yield per Harvested Acre", "Beginning Stocks", "Production", 
         "Imports", "Supply, Total", "Feed and Residual", "Food, Seed & Industrial 2/", "Ethanol & by-products 3/",
         "Domestic, Total", "Exports", "Use, Total", "Ending Stocks", "Avg. Farm Price ($/bu) 4/"],
    "2021/22": [93.3, 85.3, 176.7, 1235, 15074, 24, 16333, 5726, 6757, 5320, 12483, 2472, 14956, 1377, 6],
    "2022/23 Est.": [88.6, 79.1, 173.4, 1377, 13715, 39, 15130, 5549, 6558, 5176, 12108, 1661, 13769, 1361, 6.54],
    "2023/24 Proj. Dec": [94.9, 87.1, 174.9, 1361, 15234, 25, 16621, 5650, 6740, 5325, 12390, 2100, 14490, 2131, 4.85],
    "2023/24 Proj. Jan": [94.9, 86.29, 174.7, 1361, 15075, 25, 16461, 5650, 6740, 5325, 12390, 2100, 14490, 2131, 4.85],
}

# Convert the data into a pandas DataFrame
corn_df = pd.DataFrame(data)
corn_df.set_index("", inplace=True)
# Calculate the difference
corn_df['Difference'] = (corn_df['2023/24 Proj. Jan'] - corn_df['2023/24 Proj. Dec']).round(1)

# Display the DataFrame with colored differences
st.dataframe(corn_df)
