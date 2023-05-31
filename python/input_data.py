import pandas as pd
import xlrd

def read_from_csv(folder_path):
    df_info_flights = pd.read_csv(folder_path + 'infoFlights.csv', sep=';')
    sFlights = [i for i in df_info_flights.loc[:, 'Flight']]
    #pEarliestArrival = {i: 1 for i in df_info_flights.loc[:, 'EarliestArrival']}
    pEarliestArrival = {df_info_flights.loc[i, "Flight"]:
                            df_info_flights.loc[i, "EarliestArrival"] for i in range(0, df_info_flights.shape[0])}
    pLatestArrival = {df_info_flights.loc[i, "Flight"]:
                           df_info_flights.loc[i, "LatestArrival"] for i in range(0, df_info_flights.shape[0])}
    pTargetTime = {df_info_flights.loc[i, "Flight"]:
                       df_info_flights.loc[i, "TargetTime"] for i in range(0, df_info_flights.shape[0])}

    df_min_separation = pd.read_csv(folder_path + 'minSeparation.csv', sep=';')
    pMinSeparation = {(df_min_separation.loc[i, "Flight1"], df_min_separation.loc[i, "Flight2"]):
                          df_min_separation.loc[i, "Separation"] for i in range(0, df_min_separation.shape[0])}

    df_penalties = pd.read_csv(folder_path + 'penalties.csv', sep=';')
    pEarlinessPenalty = {df_penalties.loc[i, "Flight"]: df_penalties.loc[i, "EarlinessPenalty"]
                         for i in range(0, df_penalties.shape[0])}
    pTardinessPenalty = {df_penalties.loc[i, "Flight"]: df_penalties.loc[i, "TardinessPenalty"]
                         for i in range(0, df_penalties.shape[0])}
    return sFlights, pEarliestArrival, pLatestArrival, pTargetTime, pEarlinessPenalty, pTardinessPenalty, pMinSeparation

def read_from_xlsx(file_path):
    wb = xlrd.open_workbook(file_path)
    sheet = wb.sheet_by_name("infoFlights")
    pEarliestArrival = {sheet.cell_value(r, 0): sheet.cell_value(r, 1)
                    for r in range(1, sheet.nrows)}
    pTargetTime  = {sheet.cell_value(r, 0): sheet.cell_value(r, 2)
                    for r in range(1, sheet.nrows)}
    pLatestArrival = {sheet.cell_value(r, 0): sheet.cell_value(r, 2)
                   for r in range(1, sheet.nrows)}

    sheet = wb.sheet_by_name("minSeparation")
    pMinSeparation = {(sheet.cell_value(r, 0), sheet.cell_value(r, 1)): sheet.cell_value(r, 2)
                        for r in range(1, sheet.nrows)}

    sheet = wb.sheet_by_name("penalties")
    pEarlinessPenalty = {sheet.cell_value(r, 0): sheet.cell_value(r, 1)
                   for r in range(1, sheet.nrows)}
    pTardinessPenalty = {sheet.cell_value(r, 0): sheet.cell_value(r, 2)
                         for r in range(1, sheet.nrows)}

    return sFlights, pEarliestArrival, pLatestArrival, pTargetTime, pEarlinessPenalty, pTardinessPenalty, pMinSeparation

def read_input_data(option, path_info):
    if option == 0:
      sFlights, pEarliestArrival, pLatestArrival, pTargetTime, pEarlinessPenalty, pTardinessPenalty, pMinSeparation = \
      read_from_csv(path_info)
    elif option == 1:
      sFlights, pEarliestArrival, pLatestArrival, pTargetTime, pEarlinessPenalty, pTardinessPenalty, pMinSeparation = \
      read_from_xlsx(path_info)
    return sFlights, pEarliestArrival, pLatestArrival, pTargetTime, pEarlinessPenalty, pTardinessPenalty, pMinSeparation