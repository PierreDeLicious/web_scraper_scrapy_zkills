import sqlite3
import os

_db_conn_path = os.path.abspath('/Users/80932462/repos/web_scraper/data/raw/db_zkill.db')

if os.path.isfile(_db_conn_path):
    os.remove(_db_conn_path)
    print(_db_conn_path + ' removed!')

db_connection = sqlite3.connect(_db_conn_path)
db_cursor = db_connection.cursor()

db_cursor.execute('''
        CREATE TABLE IF NOT EXISTS kill_mail 
        (   [km_id] TEXT NOT NULL, 
            [km_system] TEXT NOT NULL, 
            [km_region] TEXT NOT NULL, 
            [km_time] TEXT NOT NULL,
            PRIMARY KEY (km_id))
        ''')

db_cursor.execute('''
          CREATE TABLE IF NOT EXISTS km_pilot_with_kill_mail
          ( [pilot_km_id] TEXT NOT NULL,
            [pilot_name] TEXT NOT NULL, 
            [pilot_ship] TEXT NOT NULL, 
            [pilot_corporation] TEXT NOT NULL, 
            [pilot_alliance] TEXT NOT NULL,
            [km_id] TEXT NOT NULL,
            [km_system] TEXT NOT NULL, 
            [km_region] TEXT NOT NULL, 
            [km_time] TEXT NOT NULL, 
            [km_is_main] BOOLEAN NOT NULL,
            PRIMARY KEY (pilot_km_id))
          ''')

db_connection.commit()
db_connection.close()
