from flask import Flask
from flask import render_template, request, redirect
import folium
import input_data
import sqlite3
from folium import FeatureGroup
from folium.plugins import MarkerCluster

app = Flask(__name__)
app.secret_key = 'super secret key'

con = sqlite3.connect('data_app.db')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS data_app
                (ID INTEGER PRIMARY KEY AUTOINCREMENT, qty_car number, address_warehouse text, address_city text, hour_start time, hour_stop time)''')
con.close()



@app.route('/',methods=["POST", "GET"])
def index():
    conn = sqlite3.connect('data_app.db')
    rows = conn.execute('SELECT * FROM data_app').fetchall()
    conn.close()

    input_data.create_dashboard()

    return render_template('main.html', rows=rows)

@app.route('/add_data',methods=["POST", "GET"])
def add_data():
    if request.method == "POST":
        qty_car = request.form["qty_car"]
        address_warehouse = request.form["address_warehouse"]
        address_city = request.form["address_city"]
        hour_start = request.form["hour_start"]
        hour_stop = request.form["hour_stop"]
        input_data.input_row(qty_car, address_warehouse, address_city, hour_start, hour_stop)

    return render_template('form.html')


@app.route('/delete/<int:id>',methods=["POST", "GET"])
def delete(id):

    input_data.delete_row(id)
    return redirect('/')

@app.route('/edit/<int:id>',methods=["POST", "GET"])
def edit(id):
    if request.method == "POST":
        qty_car = request.form["qty_car"]
        address_warehouse = request.form["address_warehouse"]
        address_city = request.form["address_city"]
        hour_start = request.form["hour_start"]
        hour_stop = request.form["hour_stop"]
        input_data.update_row(id, qty_car, address_warehouse, address_city, hour_start, hour_stop)

    conn = sqlite3.connect('data_app.db')
    rows = conn.execute(f'SELECT * FROM data_app where id = {id}').fetchall()
    conn.close()

    return render_template('form_edit.html', rows=rows)

if __name__ == "__main__":
    app.run(debug="True")
