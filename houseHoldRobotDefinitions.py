"""  ChatHTN: author Hector Munoz-Avila
    This code is  released under the  Apache License, Version 2.0 

"""  


### compilation order: <domain>Definitions, pyhop, openAI, <domain>

### In the function translateOperatorsToText below, need to copy-paste the operators list as defined
###     in the <domain> module when declaring the opererators: pyhop.declare_operators(...)
### In the function translateAxiomsToText below, need to to copy-paste the axioms list as defined
###     in the <domain> module when declaring the axioms: pyhop.declare_axioms(...)



### Axioms

def isRobot(state, r):
    if r in state.robots:
        return True
    else:
        return False

def isRoom(state, r):
    if r in state.rooms:
        return True
    else:
        return False

def isKitchen(state, k):
    if k in state.kitchens:
        return True
    else:
        return False

def isLocation(state, l):
    if isRoom(state,l) or isKitchen(state,l):  
        return True
    else:
        return False

def isMeal(state, m):
    if m in state.meals: 
        return True
    else:
        return False

def isObject(state, o):
    if isMeal(state,o): 
        return True
    else:
        return False

def isHouse(state, h):
    if h in state.houses: 
        return True
    else:
        return False


##### Operators

# move(robot, location1, location2)
# Preconditions:
# at(robot, location1)
# location1 ≠ location2
# Effects:
# ¬at(robot, location1)
# at(robot, location2)

def move(state, robot, location1, location2):
    if not isRobot(state,robot) or not isLocation(state,location1) or not isLocation(state,location2):
        return False
    if state.at[robot] == location1 and location1 != location2:
        state.at[robot] = location2
        return state
    else:
        return False

# sweep(robot, room)
# Preconditions:
# at(robot, room)
# clean(room, dirty)
# Effects:
# ¬clean(room, dirty)
# clean(room, clean)

def sweep(state, robot, location):
    if not isRobot(state,robot) or not isLocation(state,location):
        return False
    if state.at[robot] == location and state.at[location] == 'dirtyANDmessy':   
        state.at[location] = 'cleanANDmessy'  
        return state
    if state.at[robot] == location and state.at[location] == 'dirtyANDorganized':   
        state.at[location] = 'cleanANDorganized'  
        return state
    return False


# pick_up(robot, object, location)
# Preconditions:
# at(robot, location)
# ¬has(robot, object)
# Effects:
# has(robot, object)

def pick_up(state, robot, object, location):
    if not isRobot(state,robot) or not isObject(state,object) or not isLocation(location):
        return False
    if state.at[robot] == location and state.at[object] != robot:  
        state.at[object] = robot  
        return state
    return False


# drop(robot, object, location)
# Preconditions:
# at(robot, location)
# has(robot, object)
# Effects:
# ¬has(robot, object)

def drop(state, robot, object, location):
    if not isRobot(state,robot) or not isObject(state,object) or not isLocation(location):
        return False
    if state.at[robot] == location and state.at[object] == robot:  
        state.at[object] = location  
        return state
    return False


# organize(robot, room)
# Preconditions:
# at(robot, room)
# organized(room, messy)
# Effects:
# ¬organized(room, messy)
# organized(room, organized)

def organize(state,robot, loc):
    if not isRobot(state,robot) or not isLocation(state,loc):
        return False
    if state.at[robot] == loc and state.at[loc] == 'dirtyANDmessy':  
        state.at[loc] = 'dirtyANDorganized' 
        return state 
    if state.at[robot] == loc and state.at[loc] == 'cleanANDmessy':  
        state.at[loc] = 'cleanANDorganized' 
        return state
    return False 

def doNothing(state,house):
    return state

#### task verifier operators


def verify_cleanHouse(state, house):
    if not isHouse(state,house):
        return False
    if houseIsClean(state,house):
        return state
    else:
        return False
    
def verify_organizeHouse(state, house):
    if not isHouse(state,house):
        return False
    if houseIsOrganized(state,house):
        return state
    else:
        return False
    
def verify_sweepTask(state, loc):
    if not isLocation(state,loc):
        return False
    if isCleanLocation(state,loc):
        return state
    else:
        return False

def verify_organizeTask(state, loc):
    if not isLocation(state,loc):
        return False
    if isOrganizedLocation(state,loc):
        return state
    else:
        return False
    
def verify_takeCareHouse(state, house):
    if not isHouse(state,house):
        return False
    if houseIsOrganized(state,house) and houseIsClean(state,house):
        return state
    else:
        return False


##########################

### Auxiliary functions needed for methods. 

# return truck in location

def aDirtyLocation(state):
    for r in state.rooms:
        if state.at[r] == 'dirtyANDmessy' or state.at[r] == 'dirtyANDorganized':
            return r
    for k in state.kitchens:
        if state.at[k] == 'dirtyANDmessy' or state.at[k] == 'dirtyANDorganized':
            return k
    return None

def aMessyLocation(state):
    for r in state.rooms:
        if state.at[r] == 'dirtyANDmessy' or state.at[r] == 'cleanANDmessy':
            return r
    for k in state.kitchens:
        if state.at[k] == 'dirtyANDmessy' or state.at[k] == 'cleanANDmessy':
            return k
    return None

def isDirtyLocation(state,loc):
    if state.at[loc] == 'dirtyANDmessy' or state.at[loc] == 'dirtyANDorganized':
        return True
    else:
        return False
    
def isMessyLocation(state,loc):
    if state.at[loc] == 'dirtyANDmessy' or state.at[loc] == 'cleanANDmessy':
        return True
    else:
        return False
    
def isCleanLocation(state,loc):
    if state.at[loc] == 'cleanANDmessy' or state.at[loc] == 'cleanANDorganized':
        return True
    else:
        return False
    
def isOrganizedLocation(state,loc):
    if state.at[loc] == 'cleanANDorganized' or state.at[loc] == 'dirtyANDorganized':
        return True
    else:
        return False

def aRobot(state):
    for r in state.robots:
        return r
    return None

def aRobotAtLoc(state,loc):
    for r in state.robots:
        if state.at[r] == loc:
            return r
    return None

def houseIsClean(state,house):
    if not isHouse(state,house):
        return False
    if not aDirtyLocation(state):
        return True
    else:
        return False

def houseIsOrganized(state,house):
    if not isHouse(state,house):
        return False
    if not aMessyLocation(state):
        return True
    else:
        return False
    

def houseIsTakenCare(state,house):
    if not isHouse(state,house):
        return False
    if houseIsOrganized(state,house) and houseIsClean(state,house):
        return True
    else:
        return False

# methods


def organizeTaskM1(state, loc):
    if not isLocation(state,loc) or not isMessyLocation(state,loc):
        return False
    
    robot = aRobotAtLoc(state,loc)
    if not robot:
        return False
    else:
        return [('organize',robot,loc)]
    

def organizeTaskM2(state, loc):
    if not isLocation(state,loc) or not isMessyLocation(state,loc):
        return False
    
    robot = aRobot(state)
    if not robot:
         return False
    else:
        robLoc = state.at[robot]
        if robLoc != loc:
            return [
                ('move',robot,robLoc,loc),
                ('organize',robot,loc)]
    return False

#  clean_house()
# Method: clean_house_by_room()
# Preconditions:

# There exists at least one room such that clean(room, dirty).
# Decomposition:
# For each room where clean(room, dirty):

# move(robot, current_location, room)
# sweep(robot, room)

def sweepTaskM1(state, loc):
    if not isLocation(state,loc) or not isDirtyLocation(state,loc):
        return False
    
    robot = aRobotAtLoc(state,loc)
    if not robot:
        return False
    else:
        return [('sweep',robot,loc)]
    

def sweepTaskM2(state, loc):
    if not isLocation(state,loc) or not isDirtyLocation(state,loc):
        return False
    
    robot = aRobot(state)
    if not robot:
         return False
    else:
        robLoc = state.at[robot]
        if robLoc != loc:
            return [
                ('move',robot,robLoc,loc),
                ('sweep',robot,loc)]
    return False
    
   


def cleanHouseM1(state,house):
    if not isHouse(state,house):
        return False
    if houseIsClean(state,house):
        return [('doNothing','house')]
    else:
        return False


def cleanHouseM2(state,house):
    if not isHouse(state,house):
        return False
    if aDirtyLocation(state):
        dirtyLocation = aDirtyLocation(state)
        return [
            ('sweepTask',dirtyLocation),
            ('cleanHouse', house)]
    else:
        return False


def organizeHouseM1(state,house):
    if not isHouse(state,house):
        return False
    if houseIsOrganized(state,house):
        return [('doNothing','house')]
    else:
        return False


def organizeHouseM2(state,house):
    if not isHouse(state,house):
        return False
    if aMessyLocation(state):
        messyLocation = aMessyLocation(state)
        return [
            ('organizeTask',messyLocation),
            ('organizeHouse', house)]
    else:
        return False

def takeCareHouseM1(state,house):
    if not isHouse(state,house):
        return False
    else:
        return [
            ('organizeHouse',house),
            ('cleanHouse', house)]
   

# There exists at least one room such that organized(room, messy).
# Decomposition:
# For each room where organized(room, messy):

# move(robot, current_location, room)
# organize(robot, room)


#### Definition of Tasks - these are used for ChatGPT; not needed by Pyhop

def organizeTask(state, loc, checkArguments):
    if checkArguments: ## checking if the arguments are valid and returning the task, its preconditions and its effects
        if isLocation(state,loc):
            return [
                [('organizeTask', loc)],
                [('isMessyLocation', loc)],
                [('isOrganizedLocation', loc)]
            ]
    else: ## returning the task name and preconditions and effects with generic arguments for ChatGPT
        return [
                [('organizeTask', 'location')],
                [('isMessyLocation', 'location')],
                [('isOrganizedLocation', 'location')]
            ]


def sweepTask(state, loc, checkArguments):
    if checkArguments: ## checking if the arguments are valid and returning the task, its preconditions and its effects
        if isLocation(state,loc):
            return [
                [('sweepTask', loc)],
                [('isDirtyLocation', loc)],
                [('isCleanLocation', loc)]
            ]
    else: ## returning the task name and preconditions and effects with generic arguments for ChatGPT
        return [
                [('sweepTask', 'location')],
                [('isDirtyLocation', 'location')],
                [('isCleanLocation', 'location')]
            ]


def cleanHouse(state, house, checkArguments):
    if checkArguments: ## checking if the arguments are valid and returning the task, its preconditions and its effects
        if isHouse(state,house):
            return [
                [('cleanHouse', house)],
                [('isHouse', house)],
                [('houseIsClean', house)]
            ]
    else: ## returning the task name and preconditions and effects with generic arguments for ChatGPT
        return [
                [('cleanHouse', 'house')],
                [('isHouse', 'house')],
                [('houseIsClean', 'house')]
            ]

def organizeHouse(state, house, checkArguments):
    if checkArguments: ## checking if the arguments are valid and returning the task, its preconditions and its effects
        if isHouse(state,house):
            return [
                [('organizeHouse', house)],
                [('isHouse', house)],
                [('houseIsOrganized', house)]
            ]
    else: ## returning the task name and preconditions and effects with generic arguments for ChatGPT
        return [
                [('organizeHouse', 'house')],
                [('isHouse', 'house')],
                [('houseIsOrganized', 'house')]
            ]
    
def takeCareHouse(state, house, checkArguments):
    if checkArguments: ## checking if the arguments are valid and returning the task, its preconditions and its effects
        if isHouse(state,house):
            return [
                [('takeCareHouse', house)],
                [('isHouse', house)],
                [('houseIsTakenCare', house)]
            ]
    else: ## returning the task name and preconditions and effects with generic arguments for ChatGPT
        return [
                [('takeCareHouse', 'house')],
                [('isHouse', 'house')],
                [('houseIsOrganized', 'house'),('houseIsOrganized', house)]
            ]
    

########## The following are functions needed to generate the domain for ChatGPT
            
    
import inspect
    
def get_function_source(func_name,skipHALT):
   
    try:
        # Retrieve the source code of the given function
        source = inspect.getsource(func_name)
        return source
    except TypeError:
        print("func_name: ", func_name, " not a function")
        if not skipHALT: input("halt")
        return "Provided argument is not a function."
    except Exception as e:
        return f"An error occurred: {e}"


def translateOperatorsToText(operators,skipHALT):
    operators = (move, sweep, pick_up, drop, organize,doNothing,verify_cleanHouse, verify_organizeHouse, verify_sweepTask, verify_organizeTask, verify_takeCareHouse)
    textOperators = ""
    for oper in operators:
        textOperators += get_function_source(oper,skipHALT)
    return textOperators

def translateAxiomsToText(axioms,skipHALT):
    axioms = (isRobot,isRoom,isKitchen,isLocation,isMeal,isHouse,aDirtyLocation,aRobot,houseIsClean,aRobotAtLoc,isDirtyLocation,aMessyLocation,isMessyLocation,isOrganizedLocation,houseIsOrganized,houseIsTakenCare)
    textAxioms = ""
    for ax in axioms:
        textAxioms += get_function_source(ax, skipHALT)
    return textAxioms