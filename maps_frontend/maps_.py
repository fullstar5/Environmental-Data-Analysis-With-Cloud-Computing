import folium
import requests
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

