from input_data import*
from pyomo.environ import*

# Input data
inputOption = 0 # 0 csv, 1 xlsx
info_path =[ "..\input_data\\",
 "..\input_data\input_landing_scheduling.xlsx"]
sFlights, pEarliestArrival, pLatestArrival, pTargetTime, pEarlinessPenalty, pTardinessPenalty, pMinSeparation = \
read_input_data(inputOption, info_path[inputOption])


# Creating the model
m = AbstractModel()

# Sets
m.sFlights = Set()
m.sFlight1Flight2 = Set(dimen=2)

# Paramters
m.pLatestArrival = Param(m.sFlights, mutable=True)
m.pEarliestArrival = Param(m.sFlights, mutable=True)
m.pTargetTime = Param(m.sFlights, mutable=True)
m.pTardinessPenalty = Param(m.sFlights, mutable=True)
m.pEarlinessPenalty = Param(m.sFlights, mutable=True)
m.pMinSeparation = Param(m.sFlight1Flight2, mutable=True)
m.pBigM = Param(mutable=True)

# Variables
m.vArrival = Var(m.sFlights, within=NonNegativeReals)
m.vEarliness = Var(m.sFlights, within=NonNegativeReals)
m.vTardiness = Var(m.sFlights, within=NonNegativeReals)
m.v01FlightPreceedsFlight = Var(m.sFlight1Flight2, within=Binary)
m.vTotalPenalty = Var(within=NonNegativeReals)

def fcEarliestArrival (model, f):
    return model.vArrival[f] >= model.pEarliestArrival[f]

def fcLatestArrival (model, f):
    return model.vArrival[f] <= model.pLatestArrival[f]

def fcPrecedenceExists (model, f, f2):
    return model.v01FlightPreceedsFlight[f, f2] + model.v01FlightPreceedsFlight[f2, f] == 1

def fcMinSeparation (model, f, f2):
    return model.vArrival[f2] >= model.vArrival[f] + model.pMinSeparation[f,f2] \
        - model.pBigM*model.v01FlightPreceedsFlight[f, f2]

def fcEarliness (model, f):
    return model.vEarliness[f] >= model.pTargetTime[f] - model.vArrival[f]

def fcTardiness (model, f):
    return model.vTardiness[f] >= model.vArrival[f] - model.pTargetTime[f]

def fcTotalPenalty (model):
    return model.vTotalPenalty == sum(model.vEarliness[f]*model.pEarlinessPenalty[f] +
               model.vTardiness[f]*model.pTardinessPenalty[f] for f in model.sFlights)

def fobj_expression(model):
    return model.vTotalPenalty


sFlight1Flight2 = [(f, f2) for f in sFlights for f2 in sFlights if f != f2]
pBigM = 1000

input_data = {None:{
    'sFlights': {None: sFlights},
    'sFlight1Flight2':{None: sFlight1Flight2},
    'pMinSeparation': pMinSeparation,
    'pTargetTime': pTargetTime,
    'pEarliestArrival': pEarliestArrival,
    'pLatestArrival': pLatestArrival,
    'pTardinessPenalty' : pTardinessPenalty,
    'pEarlinessPenalty' : pEarlinessPenalty,
    'pBigM': {None: pBigM}
}}

# Defining model
m.cEarliestArrival = Constraint(m.sFlights, rule=fcEarliestArrival)
m.cLatestArrival = Constraint(m.sFlights, rule=fcLatestArrival)
m.cTotalPenalty = Constraint(rule=fcTotalPenalty) # THIS CONSTRAINTS CAUSES AN ERROR. review
m.cPrecedenceExists = Constraint(m.sFlight1Flight2, rule=fcPrecedenceExists)
m.cMinSeparation = Constraint(m.sFlight1Flight2, rule=fcMinSeparation)
m.cEarliness = Constraint(m.sFlights, rule=fcEarliness)
m.cTardiness = Constraint(m.sFlights, rule=fcTardiness)

#Obj. function
m.fObj = Objective(rule=fobj_expression, sense=minimize)

# Creating model instance
instance = m.create_instance(input_data)

# Solving the model
opt = SolverFactory('gurobi')
results = opt.solve(instance)
print(results)
print(instance.vTotalPenalty.value)