import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import warnings
import matplotlib.pyplot as plt

def prepare_for_modelling(df_cleaned):
    # Convert the 'projected_dates' column to datetime for accurate sorting
    df_cleaned['projected_dates'] = pd.to_datetime(df_cleaned['projected_dates'], errors='coerce')
    # train on all data apart from most recent wasde report
    # Removing the most recent row
    most_recent = df_cleaned.iloc[0]
    df_cleaned = df_cleaned.iloc[1:]

    return most_recent, df_cleaned

def imports_model(df_cleaned):
    # focus on imports column
    imports_data = df_cleaned[['Marketing_Year_Month', 'Imports']].copy()

    imports_data['Marketing_Year_Month'] = pd.to_datetime(imports_data['Marketing_Year_Month'], errors='coerce')
    # Sort the data based on dates
    imports_data = imports_data.sort_values(by='Marketing_Year_Month')

    # Set the index
    imports_data.set_index('Marketing_Year_Month', inplace=True)

    # Differencing the series
    imports_diff = imports_data['Imports'].diff()

    # Removing NaN values created by differencing
    imports_diff = imports_diff.dropna()

    # Fitting an ARIMA(1,1,1) model to the differenced series
    # Suppressing warnings for model fitting
    warnings.filterwarnings("ignore")

    model = ARIMA(imports_diff, order=(1, 1, 1))
    model_fit = model.fit()

    # Trying different ARIMA configurations to find a better fitting model
    # We will vary p and q from 0 to 2 and keep d as 1 since we have already differenced the series once

    best_aic = float("inf")
    best_bic = float("inf")
    best_order = None
    best_model = None

    # Iterating over different values of p and q
    for p in range(3):
        for q in range(3):
            try:
                # Fitting the ARIMA model
                model = ARIMA(imports_diff, order=(p, 1, q))
                model_fit = model.fit()

                # Checking if the current model has a lower AIC and BIC than the best so far
                if model_fit.aic < best_aic and model_fit.bic < best_bic:
                    best_aic = model_fit.aic
                    best_bic = model_fit.bic
                    best_order = (p, 1, q)
                    best_model = model_fit
            except:
                continue

    # Proceeding with forecasting using the best model (ARIMA(0,1,1))

    # Number of steps to forecast
    n_steps = 5

    # Forecasting the next few steps
    forecast = best_model.get_forecast(steps=n_steps)

    # Extracting forecast mean and confidence intervals
    forecast_mean = forecast.predicted_mean

    # Correcting the approach to get the confidence intervals
    confidence_intervals = forecast.conf_int()

    # Integrating the forecasts back to the original scale
    # The last known value of the original non-differenced 'Imports' series
    last_value = imports_data['Imports'].iloc[-1]

    # Integrating the forecasts
    integrated_forecast = last_value + forecast_mean.cumsum()

    # Integrating the confidence intervals
    integrated_confidence_intervals = confidence_intervals.cumsum() + last_value

    # Adjusting the forecast index to align with the original data's timeline

    # Getting the last date from the original data
    last_date = imports_data.index[-1]

    # Generating new forecast dates starting from the day after the last date
    forecast_dates = pd.date_range(start=last_date, periods=n_steps + 1, freq='M')[1:]

    # Assigning the new dates to the forecast and confidence intervals
    integrated_forecast.index = forecast_dates
    integrated_confidence_intervals.index = forecast_dates

    return imports_data, integrated_forecast, integrated_confidence_intervals

def plot_imports(imports_data, integrated_forecast, integrated_confidence_intervals):
    # Re-plotting the forecast with the corrected dates
    plt.figure(figsize=(12, 6))

    # Plotting the original 'Imports' data
    plt.plot(imports_data['Imports'], color='blue', label='Original Data')

    # Plotting the forecast
    plt.plot(integrated_forecast, color='red', marker='o', label='Forecast')

    # Plotting the confidence intervals
    plt.fill_between(integrated_confidence_intervals.index, 
                    integrated_confidence_intervals['lower Imports'], 
                    integrated_confidence_intervals['upper Imports'], 
                    color='pink', alpha=0.3, label='Confidence Interval')

    plt.title('Forecast of Imports with Confidence Intervals')
    plt.xlabel('Date')
    plt.ylabel('Imports')
    plt.legend()
    plt.grid(True)
    
    return plt

def harvest_model(df_cleaned):
    # focus on area harvested column
    harvest_data = df_cleaned[['Marketing_Year_Month', 'Area_Harvested']].copy()

    harvest_data['Marketing_Year_Month'] = pd.to_datetime(harvest_data['Marketing_Year_Month'], errors='coerce')
    # Sort the data based on dates
    harvest_data = harvest_data.sort_values(by='Marketing_Year_Month')

    # Set the index
    harvest_data.set_index('Marketing_Year_Month', inplace=True)

    # Fitting an ARIMA(1,0,1) model to the differenced series
    # Suppressing warnings for model fitting
    warnings.filterwarnings("ignore")

    model = ARIMA(harvest_data, order=(1, 0, 1))
    model_fit = model.fit()

    # Trying different ARIMA configurations to find a better fitting model
    # We will vary p and q from 0 to 2 and keep d as 0 since we have already differenced the series once

    best_aic = float("inf")
    best_bic = float("inf")
    best_order = None
    best_model = None

    # Iterating over different values of p and q
    for p in range(3):
        for q in range(3):
            try:
                # Fitting the ARIMA model
                model = ARIMA(harvest_data, order=(p, 0, q))
                model_fit = model.fit()

                # Checking if the current model has a lower AIC and BIC than the best so far
                if model_fit.aic < best_aic and model_fit.bic < best_bic:
                    best_aic = model_fit.aic
                    best_bic = model_fit.bic
                    best_order = (p, 0, q)
                    best_model = model_fit
            except:
                continue

    # Number of steps to forecast
    n_steps = 5

    # Forecasting the next few steps
    forecast = best_model.get_forecast(steps=n_steps)

    # Extracting forecast mean and confidence intervals
    forecast_mean = forecast.predicted_mean

    # Correcting the approach to get the confidence intervals
    confidence_intervals = forecast.conf_int()

    # Adjusting the forecast index to align with the original data's timeline

    # Getting the last date from the original data
    last_date = harvest_data.index[-1]

    # Generating new forecast dates starting from the day after the last date
    forecast_dates = pd.date_range(start=last_date, periods=n_steps + 1, freq='M')[1:]

    # Assigning the new dates to the forecast and confidence intervals
    forecast_mean.index = forecast_dates
    confidence_intervals.index = forecast_dates

    return harvest_data, forecast_mean, confidence_intervals

def plot_harvest(harvest_data, forecast_mean, confidence_intervals):
    plt.figure(figsize=(12, 6))

    # Plotting the original 'Imports' data
    plt.plot(harvest_data['Area_Harvested'], color='blue', label='Original Data')

    # Plotting the forecast
    plt.plot(forecast_mean, color='red', marker='o', label='Forecast')

    # Plotting the confidence intervals
    plt.fill_between(confidence_intervals.index, 
                    confidence_intervals['lower Area_Harvested'], 
                    confidence_intervals['upper Area_Harvested'], 
                    color='pink', alpha=0.3, label='Confidence Interval')

    plt.title('Forecast of Area_Harvested with Confidence Intervals')
    plt.xlabel('Date')
    plt.ylabel('Area_Harvested')
    plt.legend()
    plt.grid(True)

    return plt

def yield_model(df_cleaned):
    # focus on area harvested column
    yield_data = df_cleaned[['Marketing_Year_Month', 'Yield_per_Acre']].copy()

    yield_data['Marketing_Year_Month'] = pd.to_datetime(yield_data['Marketing_Year_Month'], errors='coerce')
    # Sort the data based on dates
    yield_data = yield_data.sort_values(by='Marketing_Year_Month')

    # Set the index
    yield_data.set_index('Marketing_Year_Month', inplace=True)

    # Fitting an ARIMA(1,0,1) model to the differenced series
    # Suppressing warnings for model fitting
    warnings.filterwarnings("ignore")

    model = ARIMA(yield_data, order=(1, 0, 1))
    model_fit = model.fit()

    # Trying different ARIMA configurations to find a better fitting model
    # We will vary p and q from 0 to 2 and keep d as 0 since we have already differenced the series once

    best_aic = float("inf")
    best_bic = float("inf")
    best_order = None
    best_model = None

    # Iterating over different values of p and q
    for p in range(3):
        for q in range(3):
            try:
                # Fitting the ARIMA model
                model = ARIMA(yield_data, order=(p, 0, q))
                model_fit = model.fit()

                # Checking if the current model has a lower AIC and BIC than the best so far
                if model_fit.aic < best_aic and model_fit.bic < best_bic:
                    best_aic = model_fit.aic
                    best_bic = model_fit.bic
                    best_order = (p, 0, q)
                    best_model = model_fit
            except:
                continue

    # Number of steps to forecast
    n_steps = 5

    # Forecasting the next few steps
    forecast = best_model.get_forecast(steps=n_steps)

    # Extracting forecast mean and confidence intervals
    forecast_mean = forecast.predicted_mean

    # Correcting the approach to get the confidence intervals
    confidence_intervals = forecast.conf_int()

    # Adjusting the forecast index to align with the original data's timeline

    # Getting the last date from the original data
    last_date = yield_data.index[-1]

    # Generating new forecast dates starting from the day after the last date
    forecast_dates = pd.date_range(start=last_date, periods=n_steps + 1, freq='M')[1:]

    # Assigning the new dates to the forecast and confidence intervals
    forecast_mean.index = forecast_dates
    confidence_intervals.index = forecast_dates

    return yield_data, forecast_mean, confidence_intervals

def plot_yield(yield_data, forecast_mean, confidence_intervals):
    plt.figure(figsize=(12, 6))

    # Plotting the original data
    plt.plot(yield_data['Yield_per_Acre'], color='blue', label='Original Data')

    # Plotting the forecast
    plt.plot(forecast_mean, color='red', marker='o', label='Forecast')

    # Plotting the confidence intervals
    plt.fill_between(confidence_intervals.index, 
                    confidence_intervals['lower Yield_per_Acre'], 
                    confidence_intervals['upper Yield_per_Acre'], 
                    color='pink', alpha=0.3, label='Confidence Interval')

    plt.title('Forecast of Yield_Per_Acre with Confidence Intervals')
    plt.xlabel('Date')
    plt.ylabel('Yield_Per_Acre')
    plt.legend()
    plt.grid(True)

    return plt








    



    
