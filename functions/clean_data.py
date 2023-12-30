import pandas as pd
# get a datetime column
from datetime import datetime

def clean_cols(df):
    # Remove columns that have 'Unnamed' in their name
    df_cleaned = df.loc[:, ~df.columns.str.contains('Unnamed')]
    df_cleaned = df_cleaned.loc[:, df_cleaned.columns != '']
    # Renaming columns 
    df_cleaned = df_cleaned.rename(columns={
        'Date': 'Date',
        'Area Planted': 'Area_Planted',
        'Area Harvested': 'Area_Harvested',
        'Yield per Harvested Acre': 'Yield_per_Acre',
        'Beginning Stocks': 'Beginning_Stocks',
        'Production': 'Production',
        'Imports': 'Imports',
        '    Supply, Total': 'Total_Supply',
        'Feed and Residual': 'Feed_and_Residual',
        'Food, Seed & Industrial 2/': 'Food_Seed_and_Industrial_Use',
        '   Ethanol & by-products 3/': 'Ethanol_and_By_products',
        '    Domestic, Total': 'Total_Domestic_Use',
        'Exports': 'Exports',
        '    Use, Total': 'Total_Use',
        'Ending Stocks': 'Ending_Stocks',
        'Avg. Farm Price ($/bu)  4/': 'Avg_Farm_Price'
    })
    return df_cleaned

# def convert_numerical(df_cleaned):
#     # Convert Numerical Columns
#     # Function to clean numeric values and remove asterisks or other non-numeric characters
#     def clean_numeric(x):
#         try:
#             return pd.to_numeric(x.replace('*', '').strip())
#         except ValueError:
#             return pd.NA

#     # Apply the cleaning function to all columns except 'Date'
#     for col in df_cleaned.columns:
#         if col not in ['Date']:
#             df_cleaned[col] = df_cleaned[col].astype(str).apply(clean_numeric)

#     return df_cleaned

def convert_numerical(df_cleaned):
    # Function to clean numeric values and remove asterisks or other non-numeric characters
    def clean_numeric(x):
        try:
            # Ensure that x is a string before applying string methods
            if isinstance(x, str):
                return pd.to_numeric(x.replace('*', '').strip())
            else:
                return pd.to_numeric(x)
        except ValueError:
            return pd.NA

    # Apply the cleaning function to all columns except 'Date'
    for col in df_cleaned.columns:
        if col != 'Date':
            # Apply clean_numeric to each element of the column
            df_cleaned[col] = df_cleaned[col].apply(clean_numeric)

    return df_cleaned


# Function to convert the strings into datetime objects
def convert_to_date(string):
    year, month_str = string.split(" Proj. ")
    # Since the year is in the format "2023/24", we'll take the first year for simplicity
    year = year.split("/")[0]
    # Convert month string to a datetime object and format it
    date = datetime.strptime(f"{year} {month_str}", "%Y %b")
    return date

# Function to adjust the month to the marketing year
def adjust_month_to_marketing_year(month):
    # May as the first month, June as second, and so forth
    return (month - 5) % 12 + 1

def new_date_cols(df_cleaned):
    # Apply the function to the DataFrame
    df_cleaned['projected_dates'] = df_cleaned['Date'].apply(convert_to_date)

    # Apply the functions to adjust the year and month
    df_cleaned['Adjusted_Year'] = df_cleaned['projected_dates'].dt.year
    df_cleaned['Adjusted_Month'] = df_cleaned['projected_dates'].dt.month.apply(adjust_month_to_marketing_year)

    # Create a column for the adjusted year and month
    df_cleaned['Marketing_Year_Month'] = df_cleaned.apply(lambda row: datetime(year=row['Adjusted_Year'], 
                                                                    month=row['Adjusted_Month'], 
                                                                    day=1), axis=1)
    
    return df_cleaned