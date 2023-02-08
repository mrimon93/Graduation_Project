import os
import psycopg2
from psycopg2 import Error
import pandas as pd
import config


CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))

# open connection to database
def connect_to_db():
    conn = None

    try:
        conn = psycopg2.connect(
            host=config.host,
            database=config.database,
            user=config.user,
            password=config.password
        )
        print("connected to database")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
  
    return conn


# read rows from "fact" table
def read_db_fact(conn):
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM fact;")
        rows = cur.fetchall()
        return rows
    except (Exception, Error) as error:
        print(error)
    finally:
        cur.close()
        conn.close()
        print("Connection closed")

# read rows from "station" table
def read_db_station(conn):
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM station;")
        rows = cur.fetchall()
        return rows
    except (Exception, Error) as error:
        print(error)
    finally:
        cur.close()
        conn.close()
        print("Connection closed")


# function for inputting data to database table "station"
def write_to_station(conn, data):
    try:        
        cur = conn.cursor()
        cur.execute(f"INSERT INTO station VALUES {data};")
        conn.commit()
        print("Data added to database")
    except (Exception, Error) as error:
        print(error)
    finally:
        cur.close()
        conn.close()
        print("Connection closed")


# function for inputting data to database table "fact"
def write_to_fact(conn, data):
    try:        
        cur = conn.cursor()
        cur.execute(f"INSERT INTO fact (tid, station_id, lufttemperatur_celsius, vindhastighet_ms, price_area, spotprice_eur) VALUES {data};")
        conn.commit()
        print("Data inserted to database")
    except (Exception, Error) as error:
        print(error)
    finally:
        cur.close()
        conn.close()
        print("Connection closed")

# Fill data to database table "station" 
# create dataframe containing weather station keys and names
stations = pd.read_csv(f"{CURR_DIR_PATH}" + "\station_keys.csv", encoding = "ISO-8859-1")

# create string containing all station keys and names. This will be used as argument when calling write_to_station - function
station_data = ""

for index, row in stations.iterrows():
    row_text = "(" + str(row[0]) + ",'" + row[1] + "'),"
    station_data = station_data + "\n" + row_text

station_data = station_data[:-1]


# add station data to database table "station"
conn = connect_to_db()
write_to_station(conn, station_data)

# check that the data can be fetched from database
conn = connect_to_db()
row_data = read_db_station(conn)
print(row_data)
