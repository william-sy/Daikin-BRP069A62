def ConvertPipe(string):
    li = list(string.split("|"))
    return li
def ConvertSemi(string):
    li = list(string.split(";"))
    return li
def CC(string):
    li = list(string.split(","))
    return li[0]
def CT(string):
    li = list(string.split(","))
    return li[1]

def showHPDetails(daikinIP, dbFileName, daikinUrlError, daikinUrlBase, daikingUrlDisc, daikinDevices):
    import sqlite3 as sl
    LL  = "###################################################################################################"
    LS = "#"
    con = sl.connect(dbFileName)
    with con:
        hp_details = con.execute("SELECT * from hp_data order by DATE DESC limit 1")
    for row in hp_details:
        print(LL)
        print(f"{LS} Data last refreshed at:")
        print(f"{row[0][:4]}-{row[0][4:6]}-{row[0][6:8]} {row[0][8:10]}:{row[0][10:12]}")
        print(f"{LL}\n")
        print(f"\n{LL}")
        print(f"{LS} Device and Software info:")
        print(f"{LL}\n")
        print(f"Errors: {row[1]}, Error State: {row[15]}, Installer State: {row[16]}, Warning State: {row[17]} , Emergency State: {row[18]}")
        print(f"Device Function: {row[2]}")
        print(f"Brand: {row[3]} Model: {row[4]} Type: {row[5]}")
        print(f"Controller firmware: {row[6]}, Controller software: {row[7]} Controller SerialNR: {row[8]}")
        print(f"HP indoor software: {row[9]}, HP outdoor software: {row[10]}, HP modelnumber: {row[11]}")
        print(f"HP unit indoor eprom: {row[12]}, HP unit user eprom: {row[13]}")
        print(f"\n{LL}")
        print(f"{LS} Heating and temperature info (thermostat):")
        print(f"{LL}\n")
        print(f"User wanted different temperature than schedule: {row[19]}")
        print("Note: over ruledstate might be broken since last firmware.")
        print(f"User given name to setup: {row[14]}, Sytem is set up to be: {row[20]}")
        print(f"\n{LS} At time of last recording:")
        print(f"System leaving water temperature: {row[21]}, wanted temperature: {row[22]}")
        print(f"Indoor temperature: {row[23]}, outdoor temperature: {row[24]}")
        print(f"The system was/is: {row[25]}, And operation mode is: {row[26]}")



        print(f"\n{LS} Child lock:")
        print(f"Child lock state is currently: {row[27]}, With pincode {row[28]}")
        print(f"\n{LS} Holiday status:")
        print(f"Holiday state to start at: {row[29]}, end at {row[30]}, and is currently: {row[31]}")
        print("Note, This can be in the past")

        print(f"\n{LS} Schedule Info:")
        print(f"Current active schedule: {row[36]}, Next Schedule change at: {row[33]}, To temperature: {row[34]}, Day: {row[35]} (array?)")

        print(f"\n{LS} Schedules:")
        # This is default and can only be set lower.
        numberOfSchedules = 5
        # This is tied to the database
        rowNumberSchedule = 37
        if numberOfSchedules >= 6:
            print("More schedules wanted than there are available.")
        else:
            while numberOfSchedules >= 0:
                S0 = ConvertPipe(row[rowNumberSchedule])
                SSP = ConvertSemi(S0[2])
                #SSDT = ConvertComma(SSP[0])
                print(f"\nName of schedule: {S0[0]}, Is schedule editable: {S0[1]}")
                print(f"|Row|Monday----|Tuesday---|Wednesday-|Thursday--|Friday----|Saturday--|Sunday----|")
                print(f"|---|Time-|Temp|Time-|Temp|Time-|Temp|Time-|Temp|Time-|Temp|Time-|Temp|Time-|Temp|")
                print(f"|-1-|{CC(SSP[0]):<5}|{CT(SSP[0]):<4}|{CC(SSP[6]):<5}|{CT(SSP[6]):<4}|{CC(SSP[12]):<5}|{CT(SSP[12]):<4}|{CC(SSP[18]):<5}|{CT(SSP[18]):<4}|{CC(SSP[24]):<5}|{CT(SSP[24]):<4}|{CC(SSP[30]):<5}|{CT(SSP[30]):<4}|{CC(SSP[36]):<5}|{CT(SSP[36]):<4}|")
                print(f"|-2-|{CC(SSP[1]):<5}|{CT(SSP[1]):<4}|{CC(SSP[7]):<5}|{CT(SSP[7]):<4}|{CC(SSP[13]):<5}|{CT(SSP[13]):<4}|{CC(SSP[19]):<5}|{CT(SSP[19]):<4}|{CC(SSP[25]):<5}|{CT(SSP[25]):<4}|{CC(SSP[31]):<5}|{CT(SSP[31]):<4}|{CC(SSP[37]):<5}|{CT(SSP[37]):<4}|")
                print(f"|-3-|{CC(SSP[2]):<5}|{CT(SSP[2]):<4}|{CC(SSP[8]):<5}|{CT(SSP[8]):<4}|{CC(SSP[14]):<5}|{CT(SSP[14]):<4}|{CC(SSP[20]):<5}|{CT(SSP[20]):<4}|{CC(SSP[26]):<5}|{CT(SSP[26]):<4}|{CC(SSP[32]):<5}|{CT(SSP[32]):<4}|{CC(SSP[38]):<5}|{CT(SSP[38]):<4}|")
                print(f"|-4-|{CC(SSP[3]):<5}|{CT(SSP[3]):<4}|{CC(SSP[9]):<5}|{CT(SSP[9]):<4}|{CC(SSP[15]):<5}|{CT(SSP[15]):<4}|{CC(SSP[21]):<5}|{CT(SSP[21]):<4}|{CC(SSP[27]):<5}|{CT(SSP[27]):<4}|{CC(SSP[33]):<5}|{CT(SSP[33]):<4}|{CC(SSP[39]):<5}|{CT(SSP[39]):<4}|")
                print(f"|-5-|{CC(SSP[4]):<5}|{CT(SSP[4]):<4}|{CC(SSP[10]):<5}|{CT(SSP[10]):<4}|{CC(SSP[16]):<5}|{CT(SSP[16]):<4}|{CC(SSP[22]):<5}|{CT(SSP[22]):<4}|{CC(SSP[28]):<5}|{CT(SSP[28]):<4}|{CC(SSP[34]):<5}|{CT(SSP[34]):<4}|{CC(SSP[40]):<5}|{CT(SSP[40]):<4}|")
                print(f"|-6-|{CC(SSP[5]):<5}|{CT(SSP[5]):<4}|{CC(SSP[11]):<5}|{CT(SSP[11]):<4}|{CC(SSP[17]):<5}|{CT(SSP[17]):<4}|{CC(SSP[23]):<5}|{CT(SSP[23]):<4}|{CC(SSP[29]):<5}|{CT(SSP[29]):<4}|{CC(SSP[35]):<5}|{CT(SSP[35]):<4}|{CC(SSP[41]):<5}|{CT(SSP[41]):<4}|")
                rowNumberSchedule += 1
                numberOfSchedules -= 1
