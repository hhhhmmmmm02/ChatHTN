"""  ChatHTN: author Hector Munoz-Avila
    This code is  released under the  Apache License, Version 2.0 

"""  

### compilation order: <domain>Definitions, pyhop, openAI, <domain>

### In the function translateOperatorsToText below, need to copy-paste the operators list as defined
###     in the <domain> module when declaring the opererators: pyhop.declare_operators(...)
### In the function translateAxiomsToText below, need to to copy-paste the axioms list as defined
###     in the <domain> module when declaring the axioms: pyhop.declare_axioms(...)



### Axioms

def isLocation(state, l):
    if l in state.location:
        return True
    else:
        return False
    
def isSafeZone(state, s):
    if s in state.safeZone:
        return True
    else:
        return False

def isDrone(state, d):
    if d in state.drone:
        return True
    else:
        return False
    
def isPerson(state, p):
    if p in state.person:
        return True
    else:
        return False

    


def isRescuedSurvivor(state, survivor):
    if not isPerson(state,survivor):
        return False
    locationSurvivor = state.at[survivor]
    if isSafeZone(state,locationSurvivor):
        return True
    else:
        return False

def needsRescueSurvivor(state, survivor):
    if not isRescuedSurvivor(state, survivor):
        return True
    else:
        return False  



###  Operators

def fly(state, drone, location1, location2):
    if not isDrone(state,drone) or not isLocation(state,location1) or not isLocation(state,location2):
        return False
    if state.at[drone] == location1 and (state.weather[location2] == 'clear'):
        state.at[drone] = location2
        return state
    else:
        return False
    
def scanArea(state, drone, location):
    if not isDrone(state,drone) or not isLocation(state,location):
        return False
    if state.at[drone] == location:
        state.scanned[location] = 'yes'
        return state
    else:
        return False
    

def pickUpSurvivor(state, drone, survivor, location):
    if not isDrone(state,drone) or not isPerson(state,survivor) or not isLocation(state,location):
        return False
    if state.at[drone] == location and state.at[survivor] == location:
        state.at[survivor] = drone
        return state
    else:
        return False
    

def dropSurvivor(state, drone, survivor, location):
    if not isDrone(state,drone) or not isPerson(state,survivor) or not isLocation(state,location):
        return False
    if state.at[drone] == location and state.at[survivor] == drone and isSafeZone(state,location):
        state.at[survivor] = location
        return state
    else:
        return False
   
def doNothing(state,dummy):
    return state

#### task verifier operators


def verify_rescueSurvivor(state, survivor,location):
    if not isPerson(state,survivor) or not isLocation(state,location):
        return False
    if isRescuedSurvivor(state, survivor):
        return state
    else:
        return False
  

def verify_searchANDrescue(state,region):
    if  isRegion(state,region) and allPeopleRescued(state,region):
        return state
    else:
        return False

def verify_checkSurvivors(state, loc):
   if isLocation(state,loc) and noSurvivorsAt(state,loc):
            return state
   else:
            return False


def verify_scanAreaTask(state, loc):
    if isLocation(state,loc) and isScanned(state,loc):
        return state
    else:
        return False
    
##########################

### Auxiliary functions needed for methods. 

# return truck in location

    
def aDrone(state):
    for d in state.drone:
        return d
    return None

def aSafeZone(state):
    for s in state.safeZone:
        return s
    return None

def aSurvivorAt(state,loc):
    for p in state.person:
        if state.at[p] == loc:
            return p
    return None

def noSurvivorsAt(state,loc):
    if not aSurvivorAt(state,loc):
        return True
    else:
        return False


def aDroneAtLoc(state,loc):
    for d in state.drone:
        if state.at[d] == loc:
            return d
    return None


def anUnscannedArea(state,region):
    for l in state.location:
        if state.scanned[l] == 'no':
            return l
    return None

def anUnrescuedPerson(state,region):
    for p in state.person:
        loc = state.at[p]
        if not loc in state.safeZone:
            return p
    return None


def isScanned(state,loc):
    if state.scanned[loc] == 'yes':
            return True
    return False

def isUnScanned(state,loc):
    if state.scanned[loc] == 'no':
            return True
    return False


def allAreasScanned(state,region):
    if anUnscannedArea(state,region):
        return False
    else:
        return True
    
def allPeopleRescued(state,region):
    for p in state.person:
        location = state.at[p]
        if not location in state.safeZone:
            return False
    return True


def isRegion(state,r):
    if r in state.region:
        return True
    return False

   
# methods


def rescueSurvivorM1(state, survivor,location):
    if not isPerson(state,survivor) or not isLocation(state,location):
        return False
    
    if state.weather[location] == 'clear' and state.at[survivor] == location and not isRescuedSurvivor(state, survivor):
        if aDroneAtLoc(state,location):
            drone = aDroneAtLoc(state,location)
            safeZone = aSafeZone(state)
            if safeZone and drone:
                return [('pickUpSurvivor',drone,survivor,location),
                        ('fly', drone, location, safeZone),
                        ('dropSurvivor', drone, survivor,safeZone)]
    return False  

def rescueSurvivorM2(state, survivor,location):
    if not isPerson(state,survivor) or not isLocation(state,location):
        return False
    if state.weather[location] == 'clear' and state.at[survivor] == location:
        drone = aDrone(state)
        droneLocation = state.at[drone]
        safeZone = aSafeZone(state)
        if safeZone and drone and safeZone != location:
            return [('fly', drone, droneLocation, location),
                    ('rescueSurvivor', survivor, location)]
    return False
 
        

def searchANDrescueM1(state,region):
    if not isRegion(state,region):
        return False
    if allPeopleRescued(state,region):
        return [('doNothing','dummy')]
    else:
        return False


def searchANDrescueM2(state,region):
    if not isRegion(state,region):
        return False
    if anUnscannedArea(state,region):
        unScannedArea = anUnscannedArea(state,region)
        if state.weather[unScannedArea] == 'clear':
            return [
                ('scanAreaTask',unScannedArea),
                ('checkSurvivors', unScannedArea),
                ('searchANDrescue', region)]
    return False
    

def searchANDrescueM3(state,region):
    if not isRegion(state,region):
        return False
    if anUnrescuedPerson(state,region):
        person = anUnrescuedPerson(state,region)
        locationPerson = state.at[person]
        if state.weather[locationPerson] == 'clear':
            return [
                    ('rescueSurvivor', person, locationPerson),
                    ('searchANDrescue', region)
                    ]
    return False

def checkSurvivorsM1(state, loc):
    if not isLocation(state,loc):
        return False
    if state.scanned[loc] == 'yes' and not aSurvivorAt(state,loc):
        return [('doNothing', 'dummy')]
    else:
        return False
    
def checkSurvivorsM2(state, loc):
    if not isLocation(state,loc):
        return False
    if state.scanned[loc] == 'yes' and aSurvivorAt(state,loc):
        survivor = aSurvivorAt(state,loc)
        return [('rescueSurvivor', survivor, loc)]
    else:
        return False



def scanAreaTaskM1(state, loc):
    if isLocation(state,loc) and isScanned(state,loc):
        return [
            ('doNothing', 'dummy')
            ]
    else:
        return False
    
def scanAreaTaskM2(state, loc):
    if isLocation(state,loc) and isUnScanned(state,loc):
        drone = aDroneAtLoc(state,loc)
        if drone:
            return [
                ('scanArea', drone, loc)
                ]
    return False

  
def scanAreaTaskM3(state, loc):
    if isLocation(state,loc) and isUnScanned(state,loc):
        drone = aDrone(state)
        droneLocation = state.at[drone]
        if drone and loc != droneLocation and state.weather[loc] == 'clear':
            return [
                ('fly',drone,droneLocation,loc),
                ('scanArea', drone, loc)
                ]
    return False

#### Definition of Tasks - these are used for ChatGPT; not needed by Pyhop

def rescueSurvivor(state, survivor,location, checkArguments):
    if checkArguments: ## checking if the arguments are valid and returning the task, its preconditions and its effects
        if  isPerson(state,survivor) and isLocation(state,location):
            return [
                [('rescueSurvivor', survivor,location)],
                [('needsRescueSurvivor', survivor)],
                [('isRescuedSurvivor', survivor)]
                ]
        else: ## returning the task name and preconditions and effects with generic arguments for ChatGPT
            return  [
                [('rescueSurvivor', 'survivor','location')],
                [('needsRescueSurvivor', 'survivor')],
                [('isRescuedSurvivor', 'survivor')]
                ]
        
def searchANDrescue(state,region, checkArguments):
    if checkArguments: ## checking if the arguments are valid and returning the task, its preconditions and its effects
        if  isRegion(state,region):
            return [
                [('searchANDrescue', region)],
                [('isRegion', region)],
                [('allPeopleRescued', region)]
                ]
        else: ## returning the task name and preconditions and effects with generic arguments for ChatGPT
            return  [
                [('searchANDrescue', 'region')],
                [('isRegion', 'region')],
                [('allPeopleRescued', 'region')]
                ]
        
def checkSurvivors(state, loc, checkArguments):
    if checkArguments: ## checking if the arguments are valid and returning the task, its preconditions and its effects
        if isLocation(state,loc):
            return [
                [('checkSurvivors', loc)],
                [('isLocation', loc)],
                [('noSurvivorsAt', loc)]
                ]
        else: ## returning the task name and preconditions and effects with generic arguments for ChatGPT
            return  [
                [('checkSurvivors', 'loc')],
                [('isLocation', 'loc')],
                [('noSurvivorsAt', 'loc')]
                ]

def scanAreaTask(state, loc, checkArguments):
    if checkArguments: ## checking if the arguments are valid and returning the task, its preconditions and its effects
        if isLocation(state,loc):
            return [
                [('scanAreaTask', loc)],
                [('isUnScanned', loc)],
                [('isScanned', loc)]
                ]
        else: ## returning the task name and preconditions and effects with generic arguments for ChatGPT
            return  [
                [('scanAreaTask', 'location')],
                [('isUnScanned', 'location')],
                [('isScanned', 'location')]
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
    operators = (fly,scanArea,pickUpSurvivor,dropSurvivor,doNothing,verify_rescueSurvivor,verify_searchANDrescue,verify_checkSurvivors,verify_scanAreaTask)
    textOperators = ""
    for oper in operators:
        textOperators += get_function_source(oper,skipHALT)
    return textOperators

def translateAxiomsToText(axioms,skipHALT):
    axioms = (isLocation,isSafeZone,isDrone,isPerson,isRescuedSurvivor,needsRescueSurvivor,aDrone,aSafeZone,aDroneAtLoc,anUnscannedArea,isRegion,allAreasScanned,aSurvivorAt,noSurvivorsAt,isScanned,isUnScanned,allPeopleRescued)
    textAxioms = ""
    for ax in axioms:
        textAxioms += get_function_source(ax, skipHALT)
    return textAxioms