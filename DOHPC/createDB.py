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
                op TEXT,
                rw TEXT,
                type TEXT,
                url TEXT
            );
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS hp_data (
                DATE TEXT,
                R_D_Error TEXT,
                R_Info TEXT,
                R_D_I_Brand TEXT,
                R_D_I_Model TEXT,
                R_D_I_Duty TEXT,
                R_D_I_Firmware INTEGER,
                R_D_I_software TEXT,
                R_D_I_Serial INTEGER,
                R_U_I_Indoor_Software TEXT,
                R_U_I_Outdoor_Software TEXT,
                R_U_I_Model_Number TEXT,
                R_U_I_Indoor_Eeprom TEXT,
                R_U_I_User_Eeprom TEXT,
                R_U_I_Given_Name TEXT,
                R_U_S_Error_State INTEGER,
                R_U_S_Installer_State INTEGER,
                R_U_S_Warning_State INTEGER,
                R_U_S_Emergency_State INTEGER,
                R_U_S_TTOS INTEGER,
                R_U_S_WeatherDependentState TEXT,
                R_LeavingWaterTemperatureCurrent INTEGER,
                R_Heating_TargetTemperature INTEGER,
                R_Heating_IndoorTemperature INTEGER,
                R_Heating_OutdoorTemperature INTEGER,
                R_Heating_OperationPower TEXT,
                R_Heating_OperationMode TEXT,
                R_ChildLock_State INTEGER,
                R_ChildLock_Code INTEGER,
                R_Holiday_StartDate TEXT,
                R_Holiday_EndDate TEXT,
                R_Holiday_HolidayState INTEGER,
                R_Schedule_Active INTEGER,
                R_Schedule_Next_Start INTEGER,
                R_Schedule_Next_Target INTEGER,
                R_Schedule_Next_Day INTEGER,
                R_Schedule_List_ID BLOB,
                R_Schedule_List_ID_0 BLOB,
                R_Schedule_List_ID_1 BLOB,
                R_Schedule_List_ID_2 BLOB,
                R_Schedule_List_ID_3 BLOB,
                R_Schedule_List_ID_4 BLOB,
                R_Schedule_List_ID_5 BLOB,
                R_Device_ID TEXT
            );
        """)
        con.execute("CREATE UNIQUE INDEX daikinReturnValues ON hp_data (DATE);")
    sql = 'INSERT INTO rw_url (id, cnf, end, fr, key1, key2, key3, name, op, rw, type, url ) values(?,?,?,?,?,?,?,?,?,?,?,?)'
    data = [
        (1,  '',             '/la', '/',  'm2m:cin', 'con', '',                  'R_D_Error',                        '2', 'r', 'e', '/Error'),
        (2,  '',             '',    '/',  'm2m:cnt', 'lbl', '',                  'R_Info',                           '2', 'r', 'b', ''),
        (3,  '',             '',    '/',  'm2m:dvi', 'man', '',                  'R_D_I_Brand',                      '2', 'r', 'd', 'deviceInfo'),
        (4,  '',             '',    '/',  'm2m:dvi', 'mod', '',                  'R_D_I_Model',                      '2', 'r', 'd', 'deviceInfo'),
        (5,  '',             '',    '/',  'm2m:dvi', 'dty', '',                  'R_D_I_Duty',                       '2', 'r', 'd', 'deviceInfo'),
        (6,  '',             '',    '/',  'm2m:dvi', 'fwv', '',                  'R_D_I_Firmware',                   '2', 'r', 'd', 'deviceInfo'),
        (7,  '',             '',    '/',  'm2m:dvi', 'swv', '',                  'R_D_I_software',                   '2', 'r', 'd', 'deviceInfo'),
        (8,  '',             '',    '/',  'm2m:dvi', 'dlb', '',                  'R_D_I_Serial',                     '2', 'r', 'd', 'deviceInfo'),
        (9,  '',             '/la', '/',  'm2m:cin', 'con', '',                  'R_U_I_Indoor_Software',            '2', 'r', 'b', '/UnitInfo/Version/IndoorSoftware'),
        (10, '',             '/la', '/',  'm2m:cin', 'con', '',                  'R_U_I_Outdoor_Software',           '2', 'r', 'b', '/UnitInfo/Version/OutdoorSoftware'),
        (11, '',             '/la', '/',  'm2m:cin', 'con', '',                  'R_U_I_Model_Number',               '2', 'r', 'b', '/UnitInfo/ModelNumber'),
        (12, '',             '/la', '/',  'm2m:cin', 'con', '',                  'R_U_I_Indoor_Eeprom',              '2', 'r', 'b', '/UnitInfo/Version/IndoorSettings'),
        (13, '',             '/la', '/',  'm2m:cin', 'con', '',                  'R_U_I_User_Eeprom',                '2', 'r', 'b', '/UnitInfo/Version/RemoconSettings'),
        (14, '',             '/la', '/',  'm2m:cin', 'con', '',                  'R_U_I_Given_Name',                 '2', 'r', 'b', '/UnitIdentifier/Name'),
        (15, '',             '/la', '/',  'm2m:cin', 'con', '',                  'R_U_S_Error_State',                '2', 'r', 'b', '/UnitStatus/ErrorState'),
        (16, '',             '/la', '/',  'm2m:cin', 'con', '',                  'R_U_S_Installer_State',            '2', 'r', 'b', '/UnitStatus/InstallerState'),
        (17, '',             '/la', '/',  'm2m:cin', 'con', '',                  'R_U_S_Warning_State',              '2', 'r', 'b', '/UnitStatus/WarningState'),
        (18, '',             '/la', '/',  'm2m:cin', 'con', '',                  'R_U_S_Emergency_State',            '2', 'r', 'b', '/UnitStatus/EmergencyState'),
        (19, '',             '/la', '/',  'm2m:cin', 'con', '',                  'R_U_S_TTOS',                       '2', 'r', 'b', '/UnitStatus/TargetTemperatureOverruledState'),
        (20, '',             '/la', '/',  'm2m:cin', 'con', '',                  'R_U_S_WeatherDependentState',      '2', 'r', 'b', '/UnitStatus/WeatherDependentState'),
        (21, '',             '/la', '/',  'm2m:cin', 'con', '',                  'R_LeavingWaterTemperatureCurrent', '2', 'r', 'b', '/Sensor/LeavingWaterTemperatureCurrent'),
        (22, '',             '/la', '/',  'm2m:cin', 'con', '',                  'R_Heating_TargetTemperature',      '2', 'r', 'b', '/Operation/TargetTemperature'),
        (23, '',             '/la', '/',  'm2m:cin', 'con', '',                  'R_Heating_IndoorTemperature',      '2', 'r', 'b', '/Sensor/IndoorTemperature'),
        (24, '',             '/la', '/',  'm2m:cin', 'con', '',                  'R_Heating_OutdoorTemperature',     '2', 'r', 'b', '/Sensor/OutdoorTemperature'),
        (25, '',             '/la', '/',  'm2m:cin', 'con', '',                  'R_Heating_OperationPower',         '2', 'r', 'b', '/Operation/Power'),
        (26, '',             '/la', '/',  'm2m:cin', 'con', '',                  'R_Heating_OperationMode',          '2', 'r', 'b', '/Operation/OperationMode'),
        (27, '',             '/la', '/',  'm2m:cin', 'con', '',                  'R_ChildLock_State',                '2', 'r', 'b', '/ChildLock/LockedState'),
        (28, '',             '/la', '/',  'm2m:cin', 'con', '',                  'R_ChildLock_Code',                 '2', 'r', 'b', '/ChildLock/PinCode'),
        (29, '',             '/la', '/',  'm2m:cin', 'con', '',                  'R_Holiday_StartDate',              '2', 'r', 'b', '/Holiday/StartDate'),
        (30, '',             '/la', '/',  'm2m:cin', 'con', '',                  'R_Holiday_EndDate',                '2', 'r', 'b', '/Holiday/EndDate'),
        (31, '',             '/la', '/',  'm2m:cin', 'con', '',                  'R_Holiday_HolidayState',           '2', 'r', 'b', '/Holiday/HolidayState'),
        (32, '',             '/la', '/',  'm2m:cin', 'con', 'id',                'R_Schedule_Active',                '2', 'r', 'n', '/Schedule/Active'),
        (33, '',             '/la', '/',  'm2m:cin', 'con', 'StartTime',         'R_Schedule_Next_Start',            '2', 'r', 'n', '/Schedule/Next'),
        (34, '',             '/la', '/',  'm2m:cin', 'con', 'TargetTemperature', 'R_Schedule_Next_Target',           '2', 'r', 'n', '/Schedule/Next'),
        (35, '',             '/la', '/',  'm2m:cin', 'con', 'Day',               'R_Schedule_Next_Day',              '2', 'r', 'n', '/Schedule/Next'),
        (36, '',             '/la', '/',  'm2m:cin', 'con', '3',                 'R_Schedule_List_ID',               '2', 'r', 'n', '/Schedule/List/Heating'),
        (37, 'text/plain:0', '',    '/S', 'm2m:cin', 'con', '',                  'W_Heating_OperationPower',         '1', 'w', 'b', '/Operation/Power'),
        (38, 'text/plain:0', '',    '/S', 'm2m:cin', 'con', '',                  'W_TargetTemperature',              '1', 'w', 'b', '/Operation/TargetTemperature'),

    ]
    with con:
        con.executemany(sql, data)

    print("Show imported data:")
    with con:
        data = con.execute("SELECT * FROM rw_url")
        for row in data:
            print(row)

    print("Database populated")
