import requests
from bs4 import BeautifulSoup
import xlrd
import pandas as pd
from tempfile import NamedTemporaryFile

def extract_from_wasde_report(file_url, sheet_name, header_range, data_range, date_cells):
    response = requests.get(file_url)
    response.raise_for_status()

    # Write the file temporarily to disk
    with NamedTemporaryFile(delete=False, suffix='.xls') as tmp:
        temp_file_name = tmp.name
        tmp.write(response.content)

    # Open the workbook and get the sheet
    workbook = xlrd.open_workbook(temp_file_name)
    worksheet = workbook.sheet_by_name(sheet_name)

    # Extract the date from the specified cells
    date_value = ' '.join([worksheet.cell_value(rowx, date_cells['col'] - 1) for rowx in range(date_cells['start_row'] - 1, date_cells['end_row'])])

    # Extract column headers
    headers = [worksheet.cell_value(rowx, header_range['start_col'] - 1) for rowx in range(header_range['start_row'] - 1, header_range['end_row'])]

    # Extract row data
    data_rows = [[worksheet.cell_value(rowx, data_range['start_col'] - 1) for rowx in range(data_range['start_row'] - 1, data_range['end_row'])]]

    # Prepend the date value to each row of data
    for row in data_rows:
        row.insert(0, date_value)

    # Create a DataFrame with an additional column for the date
    columns = ['Date'] + headers
    df = pd.DataFrame(data_rows, columns=columns)

    return df

def create_df():
    # Specify the ranges and sheet name
    header_range = {'start_row': 33, 'end_row': 49, 'start_col': 1}  # A33:A49 for headers
    data_range = {'start_row': 33, 'end_row': 49, 'start_col': 5}    # E33:E49 for data
    date_cells = {'start_row': 9, 'end_row': 10, 'col': 5}           # E9:E10 for the date

    # Specify the base URL and parameters
    base_url = 'https://usda.library.cornell.edu/concern/publications/3t945q76s'
    page_param = '?locale=en&page='

    # Specify the number of pages
    number_of_pages = 10 # Adjust as needed

    # List to store individual DataFrames
    data_frames = []

    for page in range(1, number_of_pages + 1):
        page_url = f"{base_url}{page_param}{page}#release-items"
        soup = BeautifulSoup(requests.get(page_url).text, 'html.parser')
        xls_links = soup.find_all('a', href=lambda x: (x and x.endswith('.xls')))

        for link in xls_links:
            file_url = link['href']
            df = extract_from_wasde_report(file_url, 'Page 12', header_range, data_range, date_cells)
            
            # Add the DataFrame to the list
            data_frames.append(df)

    # Concatenate all the DataFrames in the list
    all_data_df = pd.concat(data_frames, ignore_index=True)

    # Removing duplicate dates, keeping only the first occurrence
    all_data_df = all_data_df.drop_duplicates(subset='Date', keep='first')

    return all_data_df