import sqlite3
from geopy.geocoders import Nominatim
import pandas as pd
import folium

def input_row(qty_car, address_warehouse,  address_city, hour_start, hour_stop):
    con = sqlite3.connect('data_app.db')
    cur = con.cursor()
    cur.execute("INSERT INTO data_app (qty_car, address_warehouse,  address_city, hour_start, hour_stop) VALUES (?, ?, ?, ?, ?)", (qty_car, address_warehouse,  address_city, hour_start, hour_stop))
    con.commit()
    con.close()


def delete_row(id):
    con = sqlite3.connect('data_app.db')
    cur = con.cursor()
    cur.execute("delete from data_app where id=?", (id,))
    con.commit()
    con.close()

def update_row(id, qty_car, address_warehouse,  address_city, hour_start, hour_stop):
    con = sqlite3.connect('data_app.db')
    cur = con.cursor()
    print(id, qty_car, address_warehouse, address_city, hour_start, hour_stop)
    cur.execute(f"UPDATE data_app SET qty_car = '{qty_car}', address_warehouse = '{address_warehouse}', address_city = '{address_city}', hour_start = '{hour_start}', hour_stop = '{hour_stop}'  WHERE ID = {id}")

    con.commit()
    con.close()


def return_geo():
    con = sqlite3.connect('data_app.db')
    cur = con.cursor()
    cur.execute(
        f"SELECT DISTINCT address_warehouse FROM data_app")

    geolocator = Nominatim(user_agent="user_agent")
    location = geolocator.geocode("Łódź")
    m = folium.Map(location=[location.latitude, location.longitude],
                   tiles='OpenStreetMap',
                   zoom_start=7, width=1200,
                   height=600)
    coord = []
    for row in cur:

        location = geolocator.geocode(row[0])
        coord.append([location.latitude, location.longitude])
        folium.Marker(
            location=[location.latitude, location.longitude],
            popup=row[0],
            icon=folium.Icon(color="red"),
        ).add_to(m)

    if len(coord) > 0:
        folium.PolyLine(coord,
                        color='red',
                        dash_array='10').add_to(m)

    con.close()
    m.save("templates/map.html")
    coord = []

def create_dashboard():
    con = sqlite3.connect('data_app.db')
    cur = con.cursor()
    sql_2 = cur.execute(
        "SELECT DISTINCT address_warehouse FROM data_app order by address_warehouse")

    geolocator = Nominatim(user_agent="user_agent")
    location = geolocator.geocode("Łódź")
    m = folium.Map(location=[location.latitude, location.longitude],
                   tiles='OpenStreetMap',
                   zoom_start=7, width=1200,
                   height=600)
    coord_city = []
    table = []
    i = -1
    colors = ['orange', 'black', 'green', 'blue', 'yellow', 'pink']

    for iterate_sql in sql_2:
        table.append(iterate_sql[0])

    for row in table:
        i += 1
        warehouse = row
        location = geolocator.geocode(warehouse)
        coord_city.append([location.latitude, location.longitude])

        folium.Marker(
            location=[location.latitude, location.longitude],
            popup= f"Magazyn - {warehouse}",
            icon=folium.Icon(color="red"),
        ).add_to(m)


        sql = cur.execute(
            f"""SELECT DISTINCT address_city FROM data_app where address_warehouse = '{warehouse}'""")

        for city in sql:
            location_city = geolocator.geocode(city[0])
            coord_city.append([location_city.latitude, location_city.longitude])

            folium.Marker(
                location=[location_city.latitude, location_city.longitude],
                popup=city[0],
                icon=folium.Icon(color="gray"),
            ).add_to(m)

        coord_city.append([location.latitude, location.longitude])
        folium.PolyLine(coord_city, color=colors[i], dash_array='10').add_to(m)
        coord_city = []
    m.save("templates/map.html")



