import sqlite3
import time
import datetime
import random

conn = sqlite3.connect('database.db')

c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS stufTopot(unix Real, datestamp TEXT, keyword TEXT, value REAL)')

def data_entry():
    c.execute('INSERT INTO stufTopot VALUES(1214344,'','',5)')
    conn.commit()
    c.close()
    conn.close()


def dynamic_data_entry():
    unix = time.time()
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H-%M-%S'))
    keyword = ''
    value = random.randrange(0, 10)
    c.execute("INSERT INTO stufTopot VALUES(unix , datestamp , keyword , value ) VALUES(?, ?, ?, ?)",
              (unix, date, keyword, value))
    conn.commit()

for i in range(10):
    # dynamic_data_entry()
    time.sleep(1)
c.close()
conn.close()
