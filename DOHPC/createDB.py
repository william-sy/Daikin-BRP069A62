# This file is here to initiate a sqlite DB
import sqlite3 as sl
def createDatabase(dbFileName):
    con = sl.connect(dbFileName)

    with con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS rw_url (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                cnf TEXT,
                end TEXT,
                fr TEXT,
                key1 TEXT,
                key2 TEXT,
                key3 TEXT,
                name TEXT,
                op INTEGER,
                rw TEXT,
                type TEXT,
                url TEXT
            );
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS temp_data (
                name TEXT,
                info TEXT
            );
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS temp_data (
                date DATE, 
                tempOUT INTEGER,
                tempIN INTEGER,
                tempWATER INTEGER,
                tempTARGET INTERGER
            );
        """)


    sql = 'INSERT INTO DURLS (id, cnf, end, fr, key1, key2, key3, name, op, rw, type, url ) values(?,?,?,?,?,?,?,?,?,?,?,?)'
    data = [
        (1, '', 'la', '/', 'm2m:cin', 'con', '', 'R_D_Error', 2, 'r', 'r', '/Error'),
        (2, '', '', '/', 'm2m:cnt', 'lbl', '', 'R_Info', 2, 'r', 'b', ''),
        (3, '', '', '/', 'm2m:dvi', 'man', '', 'R_D_I_Brand', 2, 'r', 'd', 'deviceInfo'),
        (4, '', '', '', 'm2m:', 'con', '', '', 2, 'r', 'r', ''),
        (2, '', '', '', 'm2m:', 'con', '', '', 2, 'r', 'r', ''),
        (2, '', '', '', 'm2m:', 'con', '', '', 2, 'r', 'r', ''),
    ]
    with con:
        con.executemany(sql, data)

    print("Show imported data:")
    with con:
        data = con.execute("SELECT * FROM DURLS")
        for row in data:
            print(row)

print("Database populated")
