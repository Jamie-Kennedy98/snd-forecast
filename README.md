The WASDE reports, which stands for World Agricultural Supply and Demand Estimates, are important agricultural reports published by the United States Department of Agriculture (USDA). These reports provide comprehensive forecasts of supply and demand for major crops (like corn, soybeans, wheat) and livestock (like cattle, pork, poultry). It has been shown that the release of the wasde report impacts the markets so if you can predict the upcoming wasde report you may be able to predict market movements and place trades based on this.
This project attempts to predict the upcoming wasde report in January 2024. The purpose of this project is to become more familiar with this domain and the data in this domain, the purpose is not to build the most accurate prediction. If that was the purpose I would consider other modelling approaches such as ARIMAX, LSTM, and different ML models while also including more data such as weather data.

I used the testing.ipynb notebook to write the code that goes to the USDA website and scrapes all of the past wasde reports contained in xls files, cleans and processes this data, explores and visulaises this data, and then builds different arima models for each of the supply components in the wasde report.
This code is wrapped in functions which are stored in extract_data.py, clean_data.py and arima_models.py and these functions are called in app.py to create a streamlit app to display the forecasts.

To re-produce the results clone this repositpory, install the requirements and run "streamlit run app.py"