from input_data import *
from pulp import *
import pandas as pd

# Input data
inputOption = 0 # 0 csv, 1 xlsx
info_path =[ "..\input_data\\",
 "..\input_data\input_landing_scheduling.xlsx"]
sFlights, pEarliestArrival, pLatestArrival, pTargetTime, pEarlinessPenalty, pTardinessPenalty, pMinSeparation = \
read_input_data(inputOption, info_path[inputOption])

import pandas as pd
data = {'Target': list(pTargetTime.values()),
        'Earliest': list(pEarliestArrival.values()),
        'Latest': list(pLatestArrival.values()),
        'Earl. pen.': list(pEarlinessPenalty.values()),
        'Tard. pen.': list(pTardinessPenalty.values())
         }
df = pd.DataFrame(data, index=sFlights)
print(df)


modelPulp = LpProblem("Landing", LpMinimize)

sFlight1Flight2 = [(f, f2) for f in sFlights for f2 in sFlights if f != f2]
print('Indices for v01FlightPreceedsFlight', sFlight1Flight2)
pM = 1000

# Arrival time and penalty variables
v01FlightPreceedsFlight = LpVariable.dicts('FlightPreceedsFlight',
                                           sFlight1Flight2,
                                           cat=LpBinary)
vArrivalTime = LpVariable.dicts("Arrival", sFlights, lowBound=0, upBound=None,
                                cat=LpContinuous)
vEarliness = LpVariable.dicts("Earliness", sFlights, lowBound=0, upBound=None,
                              cat=LpContinuous)
vTardiness = LpVariable.dicts("Tardiness", sFlights, lowBound=0, upBound=None,
                              cat=LpContinuous)
vTotalPenalty = LpVariable("Total penalty", lowBound=0, cat=LpContinuous)

# CONSTRAINTS
# Time window constraints
for f in sFlights:
    modelPulp += vArrivalTime[f] <= pLatestArrival[f], "Latest" + str(f)

for f in sFlights:
    modelPulp += vArrivalTime[f] >= pEarliestArrival[f], "Earliest" + str(f)

# Earliness and Tardiness computation
for f in sFlights:
    modelPulp += vTardiness[f] >= vArrivalTime[f] - pTargetTime[f], "Tardiness" + str(f)

for f in sFlights:
    modelPulp += vEarliness[f] >= pTargetTime[f] - vArrivalTime[f], "Earliness" + str(f)

# Precedence constraints
for (f, f2) in sFlight1Flight2:
    modelPulp += v01FlightPreceedsFlight[f, f2] + v01FlightPreceedsFlight[f2, f] == 1, "Precedence" + str(
        f) + "-" + str(f2)

# Min. separation
for (f, f2) in sFlight1Flight2:
    modelPulp += vArrivalTime[f2] >= vArrivalTime[f] + pMinSeparation[f, f2] - pM * (
                1 - v01FlightPreceedsFlight[f, f2]), "MinSeparation" + str(f) + "-" + str(f2)

# Total penalty computation
modelPulp += vTotalPenalty == sum(vTardiness[f] * pTardinessPenalty[f] +
                                  vEarliness[f] * pEarlinessPenalty[f] for f in sFlights), "Total penalty"

# OBJECTIVE FUNCTION
modelPulp += vTotalPenalty

# SOLVING
modelPulp.solve()
#print(value(modelPulp.objective))


df['Arrival'] = [vArrivalTime[f].varValue for f in sFlights]
df['Earliness'] = [vEarliness[f].varValue for f in sFlights]
df['Tardiness'] = [vTardiness[f].varValue for f in sFlights]
df.sort_values('Arrival', inplace=True)
print ("Total penalty cost %s" %(vTotalPenalty.varValue))
print(df)

for c in modelPulp.constraints.values():
  print(c)

for v in modelPulp.variables():
    print(v.name, "=", v.varValue)
