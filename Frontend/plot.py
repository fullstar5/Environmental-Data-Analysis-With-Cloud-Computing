# from elasticsearch import Elasticsearch
from get_data import twitter, epa, bom, health
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_data(es, start, end, city, size):
    # Fetch data
    epa_data = epa(es, start=start, end=end, city=city, size=size)
    health_data = health(es, lga=city, size=size)

    # Convert to DataFrame
    data_health = [item['_source'] for item in health_data]
    health_df = pd.DataFrame(data_health)
    
    data_epa = [item['_source'] for item in epa_data]
    epa_df = pd.DataFrame(data_epa)

    # Visualization: PM2.5 vs ASR
    pm25_data = epa_df[epa_df['healthParameter'] == 'PM2.5']
    pm25_data_aligned = pm25_data.head(len(health_df))  # Align data lengths for demonstration

    plt.figure(figsize=(10, 6))
    plt.scatter(pm25_data_aligned['averageValue'], health_df['ASR'][:len(pm25_data_aligned)], alpha=0.5)
    plt.title('Relationship between PM2.5 Levels and ASR in ' + city)
    plt.xlabel('PM2.5 Level')
    plt.ylabel('ASR')
    plt.grid(True)
    plt.show()

# def merge_bom_epa(bom_df, epa_df):
#     """
#     Prepares and merges BOM and EPA dataframes based on the hour of the day.

#     Parameters:
#     - bom_df: DataFrame containing BOM data with a 'local_date_time' column.
#     - epa_df: DataFrame containing EPA data with an 'hour' column.

#     Returns:
#     - Merged DataFrame on hourly precision.
#     """
#     # Convert 'local_date_time' from BOM to datetime and extract the hour for merging
#     bom_df['hour'] = pd.to_datetime(bom_df['local_date_time'], format='%Y%m%d%H%M%S').dt.hour

#     # Convert 'hour' in EPA to datetime, and extract the hour
#     epa_df['hour'] = pd.to_datetime(epa_df['hour'], format='%H:%M:%S').dt.hour

#     # Merge on the 'hour' column
#     merged_df = pd.merge(bom_df, epa_df, on='hour', suffixes=('_bom', '_epa'))
    
#     return merged_df

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
    sns.lineplot(data=avg_values_per_date, x='date', y='averageValue', ax=ax1, color='blue', label='Average Air Quality Index')
    ax1.set_ylabel('Air Quality Index', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Create a second y-axis to plot the average sentiment scores
    ax2 = ax1.twinx()
    sns.lineplot(data=avg_values_per_date, x='date', y='sentiment', ax=ax2, color='red', label='Average Sentiment')
    ax2.set_ylabel('Average Sentiment', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    # Add title and labels
    plt.title('Average Air Quality Index and Average Sentiment per Date in '+ city)
    ax1.set_xlabel('Date')

    # Combine legends and place them outside the plot
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left', bbox_to_anchor=(0, 1))

    # Rotate date labels for better readability
    plt.xticks(rotation=45)

    # Show the plot
    plt.show()

