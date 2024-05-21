'''
-----------Team 48------------
| Name          | Student ID |
|---------------|------------|
| Yifei ZHANG   | 1174267    |
| Yibo HUANG    | 1380231    |
| Hanzhang SUN  | 1379790    |
| Liyang CHEN   | 1135879    |
| Yueyang WU    | 1345511    |
'''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import requests
import json
from match_url import epa, twitter, bom, health
import ipywidgets as widgets
from IPython.display import display, clear_output

def plot_data(start, end, city=None, disease=None, size=2000):


    data_epa = epa(start=start, end=end, city=city)
    data_health = health(disease=disease, phn=city)

    health_df = pd.DataFrame(data_health)
    
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
    if city:
        plt.title('Relationship between PM2.5 Levels and ASR in ' + city)
    else:
        plt.title('Relationship between PM2.5 Levels and ASR')
    plt.xlabel('PM2.5 Level')
    plt.ylabel('ASR')
    plt.grid(True)
    plt.show()

def plot_widget(start, end, city=None, disease=None, size=2000, epa_show=None, bom_show=None):
    city_textbox = widgets.Text(
        value=city if city is not None else '',
        description='City:',
        disabled=False
    )

    disease_textbox = widgets.Text(
        value=disease if disease is not None else 'COPD',
        description='Disease:',
        disabled=False
    )

    button = widgets.Button(description="Update Plot")

    def on_button_clicked(b):
        nonlocal city, disease
        city = city_textbox.value
        disease = disease_textbox.value
        clear_output(wait=True)
        display(city_textbox, disease_textbox, button)
        if epa_show == 1:
            plot_data(start=start, end=end, city=city, disease=disease, size=size)
        elif bom_show == 1:
            bom_health(start=start, end=end, size=size, city=city, disease=disease)


    button.on_click(on_button_clicked)

    display(city_textbox, disease_textbox, button)
    

def merge_bom_epa(bom_df, epa_df):

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

    # Focus on relevant columns only
    relevant_data = data[weather_cols + air_quality_cols]
    
    # Compute the correlation matrix
    corr_matrix = relevant_data.corr()

    # Plot
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
    plt.title('Correlation between Weather Conditions and Air Quality Indices')
    plt.show()


def plot_air_quality_and_sentiment(epa_df, twitter_df, city):

    if len(twitter_df) > len(epa_df):
        twitter_df = twitter_df.iloc[:len(epa_df)]
    else:
        twitter_df = twitter_df.reindex(epa_df.index)


    twitter_df = twitter_df.reset_index(drop=True)
    epa_df = epa_df.reset_index(drop=True)

    # Concatenate the dataframes
    concatenated_df = pd.concat([epa_df, twitter_df], axis=1)

    # Extract the date from the concatenated dataframe
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
    ax1.set_ylabel('Air Pollution Index', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Create a second y-axis to plot the average sentiment scores
    ax2 = ax1.twinx()
    sns.lineplot(data=avg_values_per_date, x='date', y='sentiment', ax=ax2, color='red', label='Average Sentiment')
    ax2.set_ylabel('Average Sentiment', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    plt.title('Average Air Pollution Index (pm 2.5) and Average Sentiment per Date in '+ city)
    ax1.set_xlabel('Date')

    # Combine legends and place them outside the plot
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left', bbox_to_anchor=(0, 1))

    plt.xticks(rotation=45)
    plt.show()

def bom_health(start, end, size=2000, city=None, disease=None):

    data_bom = bom(start=start, end=end, size=size)
    data_health = health(lga=city, size=size)

    health_df = pd.DataFrame(data_health)
    health_df = health_df[health_df['Disease'] == disease]
    
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
    
    # Plot
    plt.figure(figsize=(14, 8))
    bars = plt.bar(health_df['avg_temperature'], health_df['ASR'], color='skyblue', edgecolor='black', width=0.08)
    plt.xlabel('Average Daily Temperature (°C)', fontsize=12)
    plt.ylabel('Disease ASR', fontsize=12)
    plt.title('Comparison of Disease ASR under Different Temperature Conditions', fontsize=14)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)

def bom_merge_data(bom_df, health_df):

    # Convert local_date_time to datetime and extract the date
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

    # Merge dataframes
    merged_df = pd.merge(daily_avg_temp, health_df, left_index=True, right_index=True)

    return merged_df

def bom_heatmap(merged_df):

    heatmap_df = merged_df[['date', 'avg_temperature', 'ASR']].copy()
    heatmap_df['day'] = heatmap_df['date'].apply(lambda x: x.day)

    # Create pivot tables
    pivot_table_asr = heatmap_df.pivot_table(index='day', values='ASR', aggfunc='mean')
    pivot_table_temp = heatmap_df.pivot_table(index='day', values='avg_temperature', aggfunc='mean')

    # Plot heatmap
    fig, ax = plt.subplots(figsize=(14, 8))

    # Plot ASR heatmap
    sns.heatmap(pivot_table_asr, cmap="YlOrRd", annot=False, cbar_kws={'label': 'ASR'}, ax=ax)

    # Plot temperature heatmap
    sns.heatmap(pivot_table_temp, cmap="coolwarm", annot=False, cbar_kws={'label': 'Temperature (°C)'}, alpha=0.6, ax=ax)

    # Add ASR and temperature annotations
    for i in range(len(pivot_table_asr)):
        for j in range(len(pivot_table_asr.columns)):
            asr_value = pivot_table_asr.iloc[i, j]
            temp_value = pivot_table_temp.iloc[i, j]
            ax.text(j + 0.5, i + 0.5, f"{asr_value:.1f}", color='black', ha='center', va='center', fontsize=10)
            ax.text(j + 0.5, i + 0.7, f"{temp_value:.1f}", color='blue', ha='center', va='center', fontsize=8, alpha=0.7)


    ax.set_title('Calendar Heatmap of ASR and Temperature in May')
    ax.set_xlabel('May')
    ax.set_ylabel('Day')

    plt.show()

def twitter_plot(option, twitter_df, city='Melbourne'):

    with open('language_to_country.json', 'r') as file:
        language_to_country = json.load(file)
    
    if option == 1:
        city_sentiment = twitter_df.groupby('full_name')['sentiment'].mean().reset_index()

        plt.figure(figsize=(20, 10))
        sns.barplot(x='full_name', y='sentiment', data=city_sentiment)
        plt.title('Average Sentiment by City')
        plt.xlabel('City')
        plt.ylabel('Average Sentiment')
        plt.xticks(rotation=90, ha='center', fontsize=8)
        plt.tight_layout()
        plt.show()
        
    elif option == 2:

        language_sentiment = twitter_df.groupby('language')['sentiment'].mean().reset_index()
        
        language_sentiment['country'] = language_sentiment['language'].map(language_to_country) + ' (' + language_sentiment['language'] + ')'
        
        plt.figure(figsize=(18, 8))
        sns.barplot(x='country', y='sentiment', data=language_sentiment)
        plt.title('Average Sentiment by Language/Country')
        plt.xlabel('Country')
        plt.ylabel('Average Sentiment')
        plt.xticks(rotation=45, ha='right')
        plt.show()

    elif option == 3:
 
        city_data = twitter_df[(twitter_df['full_name'] == city) & (twitter_df['language'] != 'en')]
    
        language_distribution = city_data['language'].value_counts(normalize=True) * 100
    
        top_10_languages = language_distribution.nlargest(10)
    
        other_percentage = language_distribution[~language_distribution.index.isin(top_10_languages.index)].sum()
    
        language_distribution = pd.concat([top_10_languages, pd.Series({'Other': other_percentage})])
    
        plt.figure(figsize=(10, 6))
        colors = plt.get_cmap('tab20').colors 
        language_distribution.plot.pie(autopct='%1.1f%%', startangle=140, colors=colors, legend=False)
        plt.title(f'Top 10 Language Distribution in {city} (excluding English)')
        plt.ylabel('')
        plt.show()

    elif option == 4:

        twitter_df = twitter_df[twitter_df['language'] != 'en']
    
        most_frequent_languages = twitter_df.groupby('full_name')['language'].agg(lambda x: x.value_counts().idxmax()).reset_index()
    
        most_frequent_languages.columns = ['city', ' most frequent language (exclude en)']
    
        return most_frequent_languages
    else:
        print("Invalid option.")

