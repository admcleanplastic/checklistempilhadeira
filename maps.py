import streamlit as st
import folium
from geopy.geocoders import Nominatim
import sqlite3
from streamlit_folium import folium_static

def geocode_address(address):
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode(address)
    if location:
        latitude = location.latitude
        longitude = location.longitude
        return latitude, longitude
    return None, None

def get_cities_from_database():
    conn = sqlite3.connect('novo.db')  # Substitua 'novo.db' pelo caminho correto do seu banco de dados
    cursor = conn.cursor()
    cursor.execute('SELECT cidade_origem FROM entrada')
    result = cursor.fetchall()
    cities = [row[0] for row in result]
    conn.close()
    return cities

def main():
    # Obter as cidades do banco de dados
    cities = get_cities_from_database()

    # Criar o mapa
    m = folium.Map(location=[0, 0], zoom_start=2)

    # Geocodificar e adicionar marcadores para as cidades
    for city in cities:
        latitude, longitude = geocode_address(city)
        if latitude and longitude:
            folium.Marker(location=[latitude, longitude], popup=city).add_to(m)

    # Obter o código HTML do mapa folium
    folium_map = folium_static(m)

    # Exibir o mapa como um HTML embutido usando a função st.markdown
    st.markdown(folium_map, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
