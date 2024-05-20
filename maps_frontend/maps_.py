import folium
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
from folium.plugins import HeatMap
from branca.element import Template, MacroElement
#add legends to the map
def add_legend(map_obj, legend_html):
    legend = folium.Element(legend_html)
    map_obj.get_root().html.add_child(legend)

#create a map to display the health data for different diseases
def create_choropleth(merged_gdf, disease, geoJSON, genre, color):
    disease_df = merged_gdf[merged_gdf['Disease']== disease]
    disease_df['lon'] = disease_df['geo_point_2d'].apply(lambda x: x['lon'])
    disease_df['lat'] = disease_df['geo_point_2d'].apply(lambda x: x['lat'])
    disease_ = disease_df.groupby('LGA').agg({genre: 'mean', 'lon': 'mean', 'lat': 'mean'}).reset_index()
    map = folium.Map(location=[-36.8103, 144.2700], zoom_start=8, max_bounds=True, min_zoom=6.8)
    
    folium.Choropleth(
        geo_data=geoJSON,
        name=f'{disease} Choropleth',
        data=disease_,
        columns=['LGA', genre],
        key_on='feature.properties.LGA',
        fill_color=color,
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f'{genre} of {disease} by LGA'
    ).add_to(map)

    for index, entry in disease_.iterrows():
        popup_text = f"LGA: {entry['LGA']} <br> {genre}: {entry[genre]}"
        folium.Marker(location=[entry['lat'], entry['lon']], popup=popup_text).add_to(map)

    folium.LayerControl().add_to(map)
 
    return map

def avg_avg_values(data):
    # Create a dictionary to store sum and count of values for each coordinate

    coord_values = {}

    # Iterate over data to calculate sum and count of values for each coordinate
    for lat, lon, val in data:
        if (lat, lon) not in coord_values:
            coord_values[(lat, lon)] = [val, 1]
        else:
            coord_values[(lat, lon)][0] += val
            coord_values[(lat, lon)][1] += 1

    # Calculate average value for each coordinate
    average_data = [[lat, lon, val_sum / val_count] for (lat, lon), (val_sum, val_count) in coord_values.items()]
    return (average_data)


def visualize(data):
    city_to_senti_count = {}
    for i in range(len(data)):
        city = data[i]['full_name']
        sentiments = data[i]['sentiment']
        if city in city_to_senti_count:
            city_to_senti_count[city]["total_sentiment"] += sentiments
            city_to_senti_count[city]["count"] += 1
        else:
            city_to_senti_count[city] = {"total_sentiment": sentiments, "count": 1}
    
    city_to_avg_sentiment = {}
    for name, values in city_to_senti_count.items():
        avg_sentiment = values["total_sentiment"] / values["count"]
        city_to_avg_sentiment[name] = avg_sentiment
    senti_ments = list(city_to_avg_sentiment.values())

    mean_value = np.mean(senti_ments)
    median_value = np.median(senti_ments)
    plt.figure(figsize=(8, 6))

    # Create histogram
    plt.hist(senti_ments, bins=10, color='skyblue', edgecolor='black', alpha=0.7)

    # Add mean and median lines
    plt.axvline(mean_value, color='red', linestyle='dashed', linewidth=1, label='Mean')
    plt.axvline(median_value, color='green', linestyle='dashed', linewidth=1, label='Median')

    # Add legend and labels
    plt.legend()
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Histogram of Sentiment Data')

    # Show plot
    plt.show()
    
    # Define sentiment levels and corresponding colors
    sentiment_levels = {
        "Negative": (min(senti_ments), -0.05),
        "Neutral": (-0.05, 0.1),
        "Positive": (0.1, max(senti_ments))
    }

    color_map = {
        "Negative": "tomato",
        "Neutral": "burlywood",
        "Positive": "lightseagreen"
    }

    # Create a map centered around Victoria, Australia
    m = folium.Map(location=[-36.8103, 144.2700], zoom_start=6, max_bounds=True, min_zoom=6.8)

    # Geocode each city to get its coordinates
    geolocator = Nominatim(user_agent="city_sentiments_map")

    # Iterate over each city and its average sentiment
    for city, sentiment in city_to_avg_sentiment.items():
        try:
            # Get coordinates for the city
            location = geolocator.geocode(city + ", Victoria, Australia")
            if location:
                lat = location.latitude
                lon = location.longitude
                # Determine sentiment level
                for level, (min_val, max_val) in sentiment_levels.items():
                    if min_val <= sentiment < max_val:
                        color = color_map[level]
                        break
                else:
                    color = "slategray"  # If sentiment does not fall into any level
            
                # Add marker for the city with sentiment color
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=5,
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.7,
                    popup=f"{city}: {sentiment}"
                ).add_to(m)
            else:
                print(f"No coordinates found for {city}")
        except Exception as e:
            print(f"Error geocoding {city}: {e}")

    # Add legend
    legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; left: 50px; width: 215px; height: 120px; 
                    border:2px dark violet; z-index:9999; font-size:12px;
                    background-color: white;
                    ">
        <p style="margin:5px">&nbsp;<strong>Legend of Sentiments</strong></p>
        <p style="margin:5px">&nbsp;<i class="fa fa-circle" style="color:tomato"></i>&nbsp; Negative Sentiment (Below -0.05)</p>
        <p style="margin:5px">&nbsp;<i class="fa fa-circle" style="color:burlywood"></i>&nbsp; Neutral Sentiment (-0.05 to 0.1)</p>
        <p style="margin:5px">&nbsp;<i class="fa fa-circle" style="color:lightseagreen"></i>&nbsp; Positive Sentiment (Above 0.1)</p>
        <p style="margin:5px">&nbsp;<i class="fa fa-circle" style="color:slategrey"></i>&nbsp; Others</p>
        </div>
        '''

    add_legend(m, legend_html)

    # Set maximum bounds to prevent shrinking
    m.fit_bounds(m.get_bounds())
    
    return m
  


def heatmaps(epa_data):
    df = pd.DataFrame([epa_data[i] for i in range(len(epa_data))])
    # extract data with PM2.5
    pm25 = df[df['healthParameter'] == 'PM2.5']
    # extract data with particles
    particles = df[df['healthParameter'] == 'Particles']


    m = folium.Map(location=[-36.8103, 144.2700], zoom_start=6, max_bounds=True, min_zoom=6.8)

    # Create a list of tuples containing coordinates and average values
    heat_data1 = [[row['coordinates'][0], row['coordinates'][1], row['averageValue']] for index, row in particles.iterrows()]
    heat_data2 = [[row['coordinates'][0], row['coordinates'][1], row['averageValue']] for index, row in pm25.iterrows()]

    # calculate the average value of each coordinate
    data1 = avg_avg_values(heat_data1)
    data2 = avg_avg_values(heat_data2)

    fg1 = folium.FeatureGroup(name='Heatmap Particle Layer')
    fg2 = folium.FeatureGroup(name='Heatmap PM2.5 Layer')

    HeatMap(data1).add_to(fg1)
    HeatMap(data2).add_to(fg2)

    # Add feature groups to map
    fg1.add_to(m)
    fg2.add_to(m)

    # Add layer control to the map
    folium.LayerControl().add_to(m)

    # Add custom legend outside of the map
    legend_html= '''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 175px; height: 110px; 
                border:2px solid grey; z-index:9999; font-size:14px;
                background-color: white;
                ">
        <p style="margin:5px">&nbsp;<strong>Legend</strong></p>
        <p style="margin:5px">&nbsp;<span style="color:green">•</span>&nbsp; Low Value</p>
        <p style="margin:5px">&nbsp;<span style="color:orange">•</span>&nbsp; Medium Value</p>
        <p style="margin:5px">&nbsp;<span style="color:red">•</span>&nbsp; High Value</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    # Display the map
    return m

