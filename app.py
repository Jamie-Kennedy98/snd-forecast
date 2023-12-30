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

st.title('Forecast of WASDE report')

# all_data_df = create_df()
# df_cleaned = clean_cols(all_data_df)
# df_cleaned = convert_numerical(df_cleaned)
# df_cleaned = new_date_cols(df_cleaned)

# use csv file while developing to be faster
df_cleaned = pd.read_csv("cleaned_data.csv")  

st.write(df_cleaned) 
