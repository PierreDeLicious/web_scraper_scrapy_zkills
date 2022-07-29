from sqlite3 import dbapi2
from contextlib import closing
import os
import pandas as pd

_db_conn_path = os.path.abspath('/Users/80932462/repos/web_scraper/data/raw/db_zkill.db')
_reports_path = os.path.abspath('/Users/80932462/repos/web_scraper/data/reports/')

columns = ['pilot_km_id', 'pilot_name', 'pilot_ship', 'pilot_corporation', 'pilot_alliance', 'km_id', 'km_system', 'km_region', 'km_time', 'km_is_main']

df_pilots_km = pd.DataFrame(columns=columns)

try:
    with closing(dbapi2.connect(_db_conn_path, isolation_level=None)) as db_connection:
        query = "SELECT * FROM km_pilot_with_kill_mail"
        df_pilots_km = pd.DataFrame(db_connection.cursor().execute(query), columns=columns)
except dbapi2.Error as exc:
    print("Comdb2 exception encountered: %s" % exc)

print('df_pilots_km has a size of: ' + str(df_pilots_km.size) + ' with the following cols: ' + ', '.join(df_pilots_km.columns))

df_pilots_km['Day'] = df_pilots_km['km_time']

df_pilots_km['km_time'] = pd.to_datetime(df_pilots_km['km_time'])
df_pilots_km['day_of_week'] = df_pilots_km['km_time'].dt.day_name()
df_pilots_km['hour_of_day'] = df_pilots_km['km_time'].dt.hour

df_pilots_km['km_id'] = df_pilots_km['km_id'].astype(str)

df_active_pilots_during_peek_hours = df_pilots_km[(df_pilots_km['hour_of_day'] >= 19) & (df_pilots_km['hour_of_day'] <= 22)]

print('df_active_pilots_during_peek_hours has a size of: ' + str(df_active_pilots_during_peek_hours.size))
print(df_active_pilots_during_peek_hours.head())

df_results = df_active_pilots_during_peek_hours.groupby(['pilot_alliance', 'pilot_corporation'])['pilot_name'].nunique().sort_values(ascending=False)

print(df_results.sort_values(ascending=False))

with pd.ExcelWriter(_reports_path+'/most_active_corps.xlsx') as writer:
    df_results.to_excel(writer, sheet_name='most_active_corpos')
    df_pilots_km.to_excel(writer, sheet_name='data')