# from elasticsearch import Elasticsearch
from get_data import twitter, epa, bom, health
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import requests

def plot_data(start, end, city=None, disease=None, size=2000):

    epa_url = 'http://127.0.0.1:9090/epa'
    health_url = 'http://127.0.0.1:9090/health'

    params = {
        'start': start,
        'end': end,
        'size': size,
    }

    if city:
        params['city'] = city
    if disease:
        params['disease'] = disease

    epa = requests.get(epa_url, params=params)
    epa_data = epa.json()

    health = requests.get(health_url, params=params)
    health_data = health.json()

    # epa_data = epa(es, start=start, end=end, city=city, size=size)
    # health_data = health(es, lga=city, size=size)

    data_health = [item['_source'] for item in health_data]
    health_df = pd.DataFrame(data_health)
    
    data_epa = [item['_source'] for item in epa_data]
    epa_df = pd.DataFrame(data_epa)

    pm25_data = epa_df[epa_df['healthParameter'] == 'PM2.5']


    pm25_data = pm25_data[pm25_data['averageValue'] <= 13]

    breath_data = health_df[health_df['Disease'] == disease]

    # Find the minimum length between the two datasets
    min_length = min(len(pm25_data), len(breath_data))

    # Align data lengths for plotting
    pm25_data_aligned = pm25_data.head(min_length)
    breath_data_aligned = breath_data.head(min_length)

    plt.figure(figsize=(10, 6))
    plt.scatter(pm25_data_aligned['averageValue'], breath_data_aligned['ASR'], alpha=0.5)
    plt.title('Relationship between PM2.5 Levels and ASR in ' + city)
    plt.xlabel('PM2.5 Level')
    plt.ylabel('ASR')
    plt.grid(True)
    plt.show()


def merge_bom_epa(bom_df, epa_df):
    """
    Prepares and merges BOM and EPA dataframes based on the precise datetime information.

    Parameters:
    - bom_df: DataFrame containing BOM data with a 'local_date_time' column.
    - epa_df: DataFrame containing EPA data with 'hour' and 'date' columns.

    Returns:
    - Merged DataFrame on precise datetime information.
    """
    # Convert 'local_date_time' in BOM to datetime format
    bom_df['local_date_time'] = pd.to_datetime(bom_df['local_date_time'], format='%Y%m%d%H%M%S')
    bom_df['date'] = bom_df['local_date_time'].dt.date
    bom_df['hour'] = bom_df['local_date_time'].dt.hour

    # Convert 'hour' and 'date' in EPA to datetime format
    epa_df['hour'] = pd.to_datetime(epa_df['hour'], format='%H:%M:%S').dt.hour
    epa_df['date'] = pd.to_datetime(epa_df['date'], format='epa-air-quality-%Y-%m-%d').dt.date

    # Merge on the 'date' and 'hour' columns
    merged_df = pd.merge(bom_df, epa_df, on=['date', 'hour'], suffixes=('_bom', '_epa'))
    
    return merged_df

def create_heatmap(data, weather_cols, air_quality_cols):
    """
    Creates a heatmap showing the correlation between specified weather conditions and air quality indices.

    Parameters:
    - data: DataFrame with merged weather and air quality data.
    - weather_cols: List of column names related to weather conditions.
    - air_quality_cols: List of column names related to air quality indices.
    """
    # Focus on relevant columns only
    relevant_data = data[weather_cols + air_quality_cols]
    
    # Compute the correlation matrix
    corr_matrix = relevant_data.corr()

    # Plot the heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
    plt.title('Correlation between Weather Conditions and Air Quality Indices')
    plt.show()


def plot_air_quality_and_sentiment(epa_df, twitter_df, city):
    """
    Plots the average air quality index and average sentiment per date.
    
    Parameters:
    - epa_df: DataFrame containing EPA data
    - twitter_df: DataFrame containing Twitter sentiment data
    
    The function assumes that the EPA data contains 'date' and 'averageValue' columns,
    and the Twitter data contains 'date' and 'sentiment' columns. The 'language' column
    in the Twitter data will be dropped.
    """
    if len(twitter_df) > len(epa_df):
        twitter_df = twitter_df.iloc[:len(epa_df)]
    else:
        twitter_df = twitter_df.reindex(epa_df.index)


    twitter_df = twitter_df.reset_index(drop=True)
    epa_df = epa_df.reset_index(drop=True)

    # Concatenate the dataframes
    concatenated_df = pd.concat([epa_df, twitter_df], axis=1)

    # Extract the date from the concatenated dataframe (EPA data column)
    concatenated_df['date'] = pd.to_datetime(concatenated_df['date'], format='epa-air-quality-%Y-%m-%d').dt.date

    # Calculate the average sentiment and averageValue per date
    avg_values_per_date = concatenated_df.groupby('date').agg({
        'sentiment': 'mean',
        'averageValue': 'mean'
    }).reset_index()

    # Plot the data with dual y-axes
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot average air quality index on the first y-axis
    sns.lineplot(data=avg_values_per_date, x='date', y='averageValue', ax=ax1, color='blue', label='Average Air Pollution Index')
    ax1.set_ylabel('Air Quality Index', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Create a second y-axis to plot the average sentiment scores
    ax2 = ax1.twinx()
    sns.lineplot(data=avg_values_per_date, x='date', y='sentiment', ax=ax2, color='red', label='Average Sentiment')
    ax2.set_ylabel('Average Sentiment', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    # Add title and labels
    plt.title('Average Air Pollution Index and Average Sentiment per Date in '+ city)
    ax1.set_xlabel('Date')

    # Combine legends and place them outside the plot
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left', bbox_to_anchor=(0, 1))

    # Rotate date labels for better readability
    plt.xticks(rotation=45)

    # Show the plot
    plt.show()

def bom_health(es, start, end, size=2000, city=None, disease=None):
    """
    Prepares and merges BOM and health dataframes based on the order of records.
    Calculates daily average temperature and plots a bar chart comparing disease ASR under different temperature conditions.
    
    Parameters:
    - bom_df: DataFrame containing BOM data with a 'local_date_time' column.
    - health_df: DataFrame containing health data without date column.
    
    Returns:
    - Merged DataFrame on the order of records.
    """

    bom_data = bom(es, start=start, end=end, size=size)
    health_data = health(es, lga=city, size=size)

    data_health = [item['_source'] for item in health_data]

    health_df = pd.DataFrame(data_health)
    health_df = health_df[health_df['Disease'] == disease]
    
    data_bom = [item['_source'] for item in bom_data]
    bom_df = pd.DataFrame(data_bom)

    # Convert 'local_date_time' in BOM to datetime format
    bom_df['local_date_time'] = pd.to_datetime(bom_df['local_date_time'], format='%Y%m%d%H%M%S')
    bom_df['date'] = bom_df['local_date_time'].dt.date

    # Calculate daily average temperature
    daily_avg_temp = bom_df.groupby('date')['apparent_temperature'].mean().reset_index()
    daily_avg_temp.columns = ['date', 'avg_temperature']
    
    # Determine the minimum length to merge on
    min_length = min(len(daily_avg_temp), len(health_df))
    
    # Truncate both dataframes to the minimum length
    daily_avg_temp = daily_avg_temp.iloc[:min_length]
    health_df = health_df.iloc[:min_length]
    
    # Add date and avg_temperature information to health data
    health_df['date'] = daily_avg_temp['date'].values
    health_df['avg_temperature'] = daily_avg_temp['avg_temperature'].values
    
    # Plot a bar chart comparing disease ASR under different temperature conditions
    plt.figure(figsize=(14, 8))
    bars = plt.bar(health_df['avg_temperature'], health_df['ASR'], color='skyblue', edgecolor='black', width=0.08)
    plt.xlabel('Average Daily Temperature (°C)', fontsize=12)
    plt.ylabel('Disease ASR', fontsize=12)
    plt.title('Comparison of Disease ASR under Different Temperature Conditions', fontsize=14)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)



