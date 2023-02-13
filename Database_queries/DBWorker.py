import os
import psycopg2
from psycopg2 import Error
import pandas as pd
import Database_queries.config as config

class DBWorker:
    def __init__(self):
        pass

    # open connection to database
    def connect_to_db(self):
        conn = None

        try:
            conn = psycopg2.connect(
                host     = config.host,
                port     = config.port,
                database = config.database,
                user     = config.user,
                password = config.password
            )
            print("connected to database")

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    
        return conn

    # read rows from "fact" table
    def read_db_fact(self, conn):
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


    # function for inputting data to database table "fact"
    def write_to_fact(self, conn, data):
        try:        
            cur = conn.cursor()
            cur.execute(f"INSERT INTO fact (tid, lufttemperatur_celsius, vindhastighet_ms, price_area, spotprice_eur) VALUES {data};")
            conn.commit()
            print("Data inserted to database")
        except (Exception, Error) as error:
            print(error)
        finally:
            cur.close()
            conn.close()
            print("Connection closed")


if __name__ == '__main___':
    # Fill weather and price data to sql database table "fact"
    CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
    # create dataframe containing weather and price data
    fact_df = pd.read_csv(os.path.join(CURR_DIR_PATH, "..\data_el\merged\\nonull_elpriser_och_vader.csv"), sep=';')


    # create string containing all the data from fact_df. This will be used as argument when calling "write_to_fact" - function
    fact_data = ""

    for index, row in fact_df.iterrows():
        row_text = "('" + row[0] + "'," + str(row[4]) + "," + str(row[3]) + ",'" + row[1] + "'," + str(row[2]) + "),"
        fact_data = fact_data + "\n" + row_text
    fact_data = fact_data[:-1]
    #print(fact_data)


    # add the data to database
    db_worker = DBWorker()
    conn = db_worker.connect_to_db()
    db_worker.write_to_fact(conn, fact_data)


    ## check that the data can be fetched from database
    # conn = connect_to_db()
    # row_data = read_db_fact(conn)
    # print(row_data)
