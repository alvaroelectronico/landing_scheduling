import gurobipy
from gurobipy import*

def fInputDataFromCsv():
    #for i in range(1,11):
    #    sPlanes.append('Plane'+str(i))
    #print (sPlanes)
    #Reading infoFlights.cvs
    inputFile = open('infoFlights.csv')
    for line in inputFile:
        line = line.strip()
        items = line.split(';')
        if items[0]=='': continue
        if not items[0] in sPlanes:
            sPlanes.append(items[0])
            pEarliestArrival[items[0]]=items[1]
            pTargetTime[items[0]] = items[2]
            pLatestArrival[items[0]] = items[3]
    print ('Planes:',sPlanes)
    print ('Earliest arrivals:', pEarliestArrival)
    print ('Latest arrivals:', pLatestArrival)
    print('Target arrivals:', pTargetTime)

    #Reading minSeparation.csv
    inputFile = open('minSeparation.csv')
    for line in inputFile:
        line = line.strip()
        items = line.split(';')
        if items[0] == '': continue
        pMinSeparation[items[0], items[1]]=items[2]
    print ('Min. separation:', pMinSeparation )

    # Reading penalties.csv
    inputFile = open('penalties.csv')
    for line in inputFile:
        line = line.strip()
        items = line.split(';')
        if items[0] == '': continue
        pEarlinessPenality[items[0]] = items[1]
        pLatenessPenality[items[0]] = items[2]
    print('Earliness penalty:', pEarlinessPenality)
    print('Latenetss enalty:', pLatenessPenality)

    return


#Definint sets
sPlanes = list()

#Defining input parameters
pEarliestArrival=dict()
pLatestArrival =dict()
pTargetTime = dict()
pMinSeparation = dict()
pEarlinessPenality = dict()
pLatenessPenality = dict()

#Reading input data from .csv files
fInputDataFromCsv()

#Creating the model
modelMinPenalty = gurobipy.Model('Min. penalty')

#************************************************************************************************************************************************************************************************************************************
#VARIABLES
#************************************************************************************************************************************************************************************************************************************
#Precedence variables
v01PlanePreceedsPlane = dict()
indexPlanPreceedsPlan = list()
for (iPlane, iPlane2)  in list(pMinSeparation.keys()):
    if iPlane == iPlane2: continue
    indexPlanPreceedsPlan.append((iPlane, iPlane2))
print ('Indices for v0PlanePreceedPlane:', indexPlanPreceedsPlan)
for (iPlane, iPlane2) in indexPlanPreceedsPlan:
    v01PlanePreceedsPlane[iPlane, iPlane2]  = modelMinPenalty.addVar(vtype=GRB.BINARY, name = "Plane_{}_preceeds_plane_{}".format(iPlane, iPlane2))

#Arrival time and penalty variables
vArrivalTime=dict()
vEarliness=dict()
vLateness=dict()
for iPlane in sPlanes:
    vArrivalTime[iPlane]=modelMinPenalty.addVar(vtype=GRB.CONTINUOUS, lb=0, name="Arrival_time_plane_{}".format(iPlane))
    vEarliness[iPlane] = modelMinPenalty.addVar(vtype=GRB.CONTINUOUS, lb=0, name="Earliness_{}".format(iPlane))
    vLateness[iPlane] = modelMinPenalty.addVar(vtype=GRB.CONTINUOUS, lb=0, name="Lateness_plane_{}".format(iPlane))
modelMinPenalty.update()

#************************************************************************************************************************************************************************************************************************************
#CONSTRAINTS
#************************************************************************************************************************************************************************************************************************************
#Time window constraints
for iPlane in sPlanes:
    modelMinPenalty.addConstr(vArrivalTime[iPlane], GRB.LESS_EQUAL, float(pLatestArrival[iPlane]), name="Latest_arrival_{}".format(iPlane))
    modelMinPenalty.addConstr(vArrivalTime[iPlane], GRB.GREATER_EQUAL, float(pEarliestArrival[iPlane]), name="Earliest_arrival_{}".format(iPlane))

#Single precedence
for (iPlane, iPlane2) in indexPlanPreceedsPlan:
    modelMinPenalty.addConstr(v01PlanePreceedsPlane[iPlane, iPlane2]+v01PlanePreceedsPlane[iPlane2, iPlane], GRB.EQUAL, 1, name = "Single_precedece_{}_{}".format(iPlane, iPlane2))

#Min distance
pBigM = 1000
for (iPlane, iPlane2) in indexPlanPreceedsPlan:
    modelMinPenalty.addConstr(vArrivalTime[iPlane]+float(pMinSeparation[iPlane, iPlane2]), GRB.LESS_EQUAL, vArrivalTime[iPlane2]+float(pBigM)*v01PlanePreceedsPlane[iPlane2, iPlane], name = "Plane_precedes_plane_{}_{}".format(iPlane2, iPlane))

#Penalties
for iPlane in sPlanes:
    modelMinPenalty.addConstr(vEarliness[iPlane], GRB.GREATER_EQUAL, vArrivalTime[iPlane]-float(pTargetTime[iPlane]), name="Earliness_penalty_{}".format(iPlane))
    modelMinPenalty.addConstr(vLateness[iPlane], GRB.GREATER_EQUAL, float(pTargetTime[iPlane])-vArrivalTime[iPlane], name="Earliness_penalty_{}".format(iPlane))

#************************************************************************************************************************************************************************************************************************************
#OBJECTIVE
#************************************************************************************************************************************************************************************************************************************
objFunction = LinExpr()
for iPlane in sPlanes:
    objFunction +=vEarliness[iPlane]*float(pEarlinessPenality[iPlane])+vLateness[iPlane]*float(pLatenessPenality[iPlane])
print ('Objective:', objFunction)
modelMinPenalty.setObjective(objFunction, GRB.MINIMIZE)


#************************************************************************************************************************************************************************************************************************************
#SOLVING AND GETTING THE SOLUTION
#************************************************************************************************************************************************************************************************************************************
modelMinPenalty.update()
modelMinPenalty.optimize()
try:
    modelMinPenalty.printAttr('X')
except:
    print('Something went wrong')

