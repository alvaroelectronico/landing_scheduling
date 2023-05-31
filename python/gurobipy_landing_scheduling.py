# import gurobipy
from input_data import*
# from gurobipy import *
from pulp import *


def fSolveWithGuropby():
    # Creating the model
    modelMinPenalty = gurobipy.Model('Min. penalty')

    # ************************************************************************************************************************************************************************************************************************************
    # VARIABLES
    # ************************************************************************************************************************************************************************************************************************************
    # Precedence variables
    v01PlanePreceedsPlane = dict()
    indexPlanPreceedsPlan = list()
    for (iPlane, iPlane2) in list(pMinSeparation.keys()):
        if iPlane == iPlane2: continue
        indexPlanPreceedsPlan.append((iPlane, iPlane2))
    print('Indices for v0PlanePreceedPlane:', indexPlanPreceedsPlan)
    for (iPlane, iPlane2) in indexPlanPreceedsPlan:
        v01PlanePreceedsPlane[iPlane, iPlane2] = modelMinPenalty.addVar(vtype=GRB.BINARY,
                                                                        name="Plane_{}_preceeds_plane_{}".format(iPlane,
                                                                                                                 iPlane2))

    # Arrival time and penalty variables
    vArrivalTime = dict()
    vEarliness = dict()
    vLateness = dict()
    for iPlane in sPlanes:
        vArrivalTime[iPlane] = modelMinPenalty.addVar(vtype=GRB.CONTINUOUS, lb=0,
                                                      name="Arrival_time_plane_{}".format(iPlane))
        vEarliness[iPlane] = modelMinPenalty.addVar(vtype=GRB.CONTINUOUS, lb=0, name="Earliness_{}".format(iPlane))
        vLateness[iPlane] = modelMinPenalty.addVar(vtype=GRB.CONTINUOUS, lb=0, name="Lateness_plane_{}".format(iPlane))
    modelMinPenalty.update()

    # ************************************************************************************************************************************************************************************************************************************
    # CONSTRAINTS
    # ************************************************************************************************************************************************************************************************************************************
    # Time window constraints
    for iPlane in sPlanes:
        modelMinPenalty.addConstr(vArrivalTime[iPlane], GRB.LESS_EQUAL, float(pLatestArrival[iPlane]),
                                  name="Latest_arrival_{}".format(iPlane))
        modelMinPenalty.addConstr(vArrivalTime[iPlane], GRB.GREATER_EQUAL, float(pEarliestArrival[iPlane]),
                                  name="Earliest_arrival_{}".format(iPlane))

    # Single precedence
    for (iPlane, iPlane2) in indexPlanPreceedsPlan:
        modelMinPenalty.addConstr(v01PlanePreceedsPlane[iPlane, iPlane2] + v01PlanePreceedsPlane[iPlane2, iPlane],
                                  GRB.EQUAL, 1, name="Single_precedece_{}_{}".format(iPlane, iPlane2))

    # Min distance
    pBigM = 1000
    for (iPlane, iPlane2) in indexPlanPreceedsPlan:
        modelMinPenalty.addConstr(vArrivalTime[iPlane] + float(pMinSeparation[iPlane, iPlane2]), GRB.LESS_EQUAL,
                                  vArrivalTime[iPlane2] + float(pBigM) * v01PlanePreceedsPlane[iPlane2, iPlane],
                                  name="Plane_precedes_plane_{}_{}".format(iPlane2, iPlane))

    # Penalties
    for iPlane in sPlanes:
        modelMinPenalty.addConstr(vEarliness[iPlane], GRB.GREATER_EQUAL,
                                  vArrivalTime[iPlane] - float(pTargetTime[iPlane]),
                                  name="Earliness_penalty_{}".format(iPlane))
        modelMinPenalty.addConstr(vLateness[iPlane], GRB.GREATER_EQUAL,
                                  float(pTargetTime[iPlane]) - vArrivalTime[iPlane],
                                  name="Earliness_penalty_{}".format(iPlane))

    # ************************************************************************************************************************************************************************************************************************************
    # OBJECTIVE
    # ************************************************************************************************************************************************************************************************************************************
    objFunction = LinExpr()
    for iPlane in sPlanes:
        objFunction += vEarliness[iPlane] * float(pEarlinessPenality[iPlane]) + vLateness[iPlane] * float(
            pLatenessPenality[iPlane])
    print('Objective:', objFunction)
    modelMinPenalty.setObjective(objFunction, GRB.MINIMIZE)

    # ************************************************************************************************************************************************************************************************************************************
    # SOLVING AND GETTING THE SOLUTION
    # ************************************************************************************************************************************************************************************************************************************
    modelMinPenalty.update()
    modelMinPenalty.optimize()
    try:
        modelMinPenalty.printAttr('X')
    except:
        print('Something went wrong')


def fSolveWithPuLP():
    v01PlanePreceedsPlane = dict()
    modelPulp = LpProblem("Landing", LpMinimize)
    indexPlanePreceedsPlane = list()
    for (iPlane, iPlane2) in list(pMinSeparation.keys()):
        if iPlane == iPlane2: continue
        indexPlanePreceedsPlane.append((iPlane, iPlane2))
    print('Indices for v0PlanePreceedPlane:', indexPlanePreceedsPlane)
    v01PlanePreceedsPlane = LpVariable.dicts('PlanePreceedsPlan', indexPlanePreceedsPlane, lowBound=0, upBound=0,
                                             cat=LpBinary)

    # Arrival time and penalty variables
    vArrivalTime = dict()
    vEarliness = dict()
    vLateness = dict()

    vArrivalTime = LpVariable.dicts("Arrival", sPlanes, lowBound=0, upBound=None, cat=LpContinuous)
    vEarliness = LpVariable.dicts("Arrival", sPlanes, lowBound=0, upBound=None, cat=LpContinuous)
    vLateness = LpVariable.dicts("Arrival", sPlanes, lowBound=0, upBound=None, cat=LpContinuous)

    # CONSTRAINTS

    # Time window constraints
    for iPlane in sPlanes:
        modelPulp += vArrivalTime[iPlane] <= pLatestArrival[iPlane]
    for iPlane in sPlanes:
        modelPulp += vArrivalTime[iPlane] >= pEarliestArrival[iPlane]

    # ************************************************************************************************************************************************************************************************************************************
    # OBJECTIVE FUNCTION
    # ************************************************************************************************************************************************************************************************************************************
    modelPulp += 0
    # ************************************************************************************************************************************************************************************************************************************
    # SOLVING
    # ************************************************************************************************************************************************************************************************************************************
    modelPulp.solve()


sPlanes = list()

# Defining input parameters
pEarliestArrival = dict()
pLatestArrival = dict()
pTargetTime = dict()
pMinSeparation = dict()
pEarlinessPenality = dict()
pLatenessPenality = dict()



