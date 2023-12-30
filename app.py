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
from functions.arima_models import prepare_for_modelling, imports_model, plot_imports
from statsmodels.tsa.arima.model import ARIMA
import warnings

st.title('Forecast of WASDE report')

########## get data  ##################
# all_data_df = create_df()
# df_cleaned = clean_cols(all_data_df)
# df_cleaned = convert_numerical(df_cleaned)
# df_cleaned = new_date_cols(df_cleaned)

# use csv file while developing to be faster
df_cleaned = pd.read_csv("cleaned_data.csv")  

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
    "Date": ["Dec 2022/23 Proj.", "Jan 2022/23 Proj.", "Feb 2022/23 Proj.", "Mar 2022/23 Proj.", "Apr 2022/23 Proj."],
    "Forecasted": integrated_forecast,
    "Actual": [most_recent['Imports'], 0, 0, 0, 0],
    "Difference": [most_recent['Imports']-integrated_forecast[0], 0, 0, 0, 0]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Transpose the DataFrame
df_transposed = df.T

# Convert transposed DataFrame to HTML without the index
html_transposed = df_transposed.to_html(header=False, index=True)

# Add custom styling for the 'Difference' column
html_transposed = html_transposed.replace('<td>0.052775</td>', '<td style="color: green;">0.052775</td>')
for i in range(4):
    html_transposed = html_transposed.replace('<td>0</td>', '<td style="color: red;">0</td>', 1)

# Display the plot in Streamlit
st.pyplot(plot_imports(imports_data, integrated_forecast, integrated_confidence_intervals))
# Display the transposed DataFrame as HTML
st.markdown(html_transposed, unsafe_allow_html=True)


