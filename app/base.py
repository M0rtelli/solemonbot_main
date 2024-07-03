import sqlite3
import config
import app.localdata.load as localdata

def init():
    global conn, cursor
    print("[BD]: Connecting...")
    try: 
        conn = sqlite3.connect(config.sql_data_path)
        print("[BD]: Connected successful.")
    except Exception as exc:
        print("[BD]: Ошибка подключения к базе данных")
        print(f"[BD]: {exc}")

    cursor = conn.cursor()

    localdata.loadMarketPlaceAllAd()
    localdata.LoadUsers()