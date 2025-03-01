
"""  ChatHTN: author Hector Munoz-Avila
    This code is released under the  Apache License, Version 2.0 

"""  

### compilation order: <domain>Definitions, pyhop, openAI, <domain>

### In the function translateOperatorsToText below, need to copy-paste the operators list as defined
###     in the <domain> module when declaring the opererators: pyhop.declare_operators(...)
### In the function translateAxiomsToText below, need to to copy-paste the axioms list as defined
###    in the <domain> module when declaring the axioms: pyhop.declare_axioms(...)



### Axioms


## check if 2 locations are in same city


def same_city(state, location_a, location_b):
    city_a = state.at[location_a]
    city_b = state.at[location_b]
    if city_a == city_b:
        return True
    else:
        return False

### check if item is a package

def isPackage(state, p):
    if p in state.packages:
        return True
    return False

# check whether a location is an airport

def isAirport(state, a):
    if a in state.airports:
        return True
    return False

def isTruck(state, t):
    if t in state.trucks:
        return True
    return False


def isPost(state, p):
    if p in state.postOffices:
        return True
    return False

def isLocation(state, l):
    if isPost(state,l) or isAirport(state,l):
        return True
    return False

# check whether an object is an airplane

def isAirplane(state, plane):
    if plane in state.airplanes:
        return True
    return False

##### Operators


def drive_truck(state, truck, location_a, location_b):
    if not isTruck(state,truck) or not isLocation(state,location_a) or not isLocation(state,location_b):
        return False
    if state.at[truck] == location_a and same_city(state, location_a, location_b):
        state.at[truck] = location_b
        return state
    else:
        return False 

def load_truck(state, package, truck, loc):
    if not isPackage(state,package) or not isTruck(state,truck) or not isLocation(state, loc):
        return False
    if state.at[package] == loc and state.at[truck] == loc:
        state.at[package] = truck
        return state
    else:
        return False


def unload_truck(state, package, truck, loc):
    if not isPackage(state,package) or not isTruck(state,truck) or not isLocation(state, loc):
        return False
    if state.at[package] == truck and state.at[truck] == loc:
        state.at[package] = loc
        return state
    else:
        return False


# move a plane from airport_a to airport_b
def fly_plane(state, plane, airport_a, airport_b):
    if not isAirplane(state,plane) or not isAirport(state, airport_a) or not isAirport(state, airport_b):
        return False
    if state.at[plane] == airport_a:
        state.at[plane] = airport_b
        return state
    else:
        return False


def load_plane(state, package, plane, airport):
    if not isPackage(state,package) or not isAirplane(state,plane) or not isAirport(state, airport):
        return False
    if state.at[package] == airport and state.at[plane] == airport:
        state.at[package] = plane
        return state
    else:
        return False


def unload_plane(state, package, plane, airport):
    if not isPackage(state,package) or not isAirplane(state,plane) or not isAirport(state, airport):
        return False
    if state.at[package] == plane and state.at[plane] == airport:
        state.at[package] = airport
        return state
    else:
        return False

def doNothing(state,dummy):
    print("doNothing operator")
    return state

#### task verifier operators


def verify_truckTransport(state, package, src, dest):
    if not isPackage(state,package) or not isLocation(state,src) or not isLocation(state,dest):
            return False
    if state.at[package] == dest:
        return state
    else:
        return False


def verify_airplaneTransport(state, package, src, dest):
    if not isPackage(state,package) or not isAirport(state,src) or not isAirport(state,dest):
        return False
    if state.at[package] == dest:
        return state
    else:
        return False



def verify_transferPackage(state, package, src, dest):
    if not isPackage(state,package) or not isLocation(state,src) or not isLocation(state,dest):
        return False
    if state.at[package] == dest:
        return state
    else:
        return False

##########################

### Auxiliary functions needed for methods. 

# return truck in location

def truckAtLocation(state, loc):
    for t in state.trucks:
        if state.at[t] == loc:
            return t
    return None
    
# return plane in location

def planeAtLocation(state, loc):
    for a in state.airplanes:
        if state.at[a] == loc:
            return a
    return None
    
## return truck in location of a city
    
def truckAtCity(state, loc):
    city = state.at[loc]
    for t in state.trucks:
        if (city == state.at[state.at[t]]):
            return t
    return None

## return plane 
    
def aPlane(state, loc):
    for a in state.airplanes:
        return a
    return None
    
## return airport in city 
    
def anAirport(state, city):
    try: ## any plane
        airport = next(a for a in state.airports if state.at[a] == city)
        return airport
    except:
        return None



# methods

def truckTransportMethod1(state, package, src, dest):
    # Preconditions: package and truck at src, both in the same city
    if not isPackage(state,package) or not isLocation(state,src) or not isLocation(state,dest):
        return False
    if src == dest:
        return [
            ('doNothing','dummy')
        ]
    return False

def truckTransportMethod2(state, package, src, dest):
    # Preconditions: package and truck at src, both in the same city
    if not isPackage(state,package) or not isLocation(state,src) or not isLocation(state,dest):
        return False
    if state.at[package] == src and same_city(state,src,dest) and truckAtLocation(state,src):
        truck = truckAtLocation(state,src)
        return [
            ('load_truck', package, truck, src),
            ('drive_truck', truck, src, dest),
            ('unload_truck', package, truck, dest)
        ]
    return False

def truckTransportMethod3(state, package, src, dest):
    # Preconditions: package and truck at src, both in the same city
    if not isPackage(state,package) or not isLocation(state,src) or not isLocation(state,dest):
        return False
    if state.at[package] == src and same_city(state,src,dest) and not truckAtLocation(state,src):
        truck = truckAtCity(state,src)
        if truck is None:
            return False
        else:
            loc_truck = state.at[truck]
            return [
                ('drive_truck', truck, loc_truck, src),
                ('truckTransport', package, src, dest)
            ]
    return False


def airplaneTransportMethod1(state, package, src, dest):
    if not isPackage(state,package) or not isAirport(state,src) or not isAirport(state,dest):
        return False
    if state.at[package] == src and src == dest:
        return [
            ('doNothing','dummy')
        ]
    return False


def airplaneTransportMethod2(state, package, src, dest):
    if not isPackage(state,package) or not isAirport(state,src) or not isAirport(state,dest):
        return False
    if state.at[package] == src and isAirport(state,src) and isAirport(state,dest) and planeAtLocation(state,src):
        airplane = planeAtLocation(state,src)
        return [
            ('load_plane', package, airplane, src),
            ('fly_plane', airplane, src, dest),
            ('unload_plane', package, airplane, dest)
        ]
    return False


def airplaneTransportMethod3(state, package, src, dest):
    if not isPackage(state,package) or not isAirport(state,src) or not isAirport(state,dest):
        return False
    if state.at[package] == src and isAirport(state,src) and isAirport(state,dest) and not planeAtLocation(state,src) and aPlane(state,src):
        airplane = aPlane(state,src)
        loc_airplane = state.at[airplane]
        return [
            ('fly_plane', airplane, loc_airplane, src),
            ('airplaneTransport', package,src, dest)
        ]
    return False


def transferPackageMethod1(state, package, src, dest):
    if not isPackage(state,package) or not isLocation(state,src) or not isLocation(state,dest):
        return False
    if state.at[package] == src and same_city(state,src,dest):
        return [
            ('truckTransport', package, src,dest )
        ]
    return False

def transferPackageMethod2(state, package, src, dest):
    if not isPackage(state,package) or not isLocation(state,src) or not isLocation(state,dest):
        return False
    if state.at[package] == src and not(same_city(state,src,dest)):
        city_src = state.at[src]
        city_dest = state.at[dest]
        airport_src = anAirport(state,city_src)
        airport_dest = anAirport(state,city_dest)
        if airport_src is None or airport_dest is None:
            return False
        return [
            ('truckTransport', package, src, airport_src ),
            ('airplaneTransport', package, airport_src,airport_dest ),
            ('truckTransport', package, airport_dest, dest )
        ]
    return False



#### Definition of Tasks - these are used for ChatGPT; not needed by Pyhop

def truckTransport(state, package, src, dest, checkArguments):
    if checkArguments: ## checking if the arguments are valid and returning the task, its preconditions and its effects
        if not isPackage(state,package) or not isLocation(state,src) or not isLocation(state,dest):
            return None
        return [
            [('truckTransport', package, src, dest)],
            [('isPackage', package), ('isLocation',src), ('isLocation',dest), ('at',package,src), ('same_city',src,dest)],
            [('at', package,dest)]
        ]
    else: ## returning the task name and preconditions and effects with generic arguments for ChatGPT
        return [
                [('truckTransport', 'package', 'src', 'dest')],
                [('isPackage', 'package'), ('isLocation','src'), ('isLocation','dest'), ('at','package','src'), ('same_city','src','dest')],
                [('at', 'package','dest')]
            ]


def airplaneTransport(state, package, src, dest, checkArguments):
    if checkArguments: ## checking if the arguments are valid and returning the task, its preconditions and its effects
        if not isPackage(state,package) or not isAirport(state,src) or not isAirport(state,dest):
            return None
        return [
            [('airplaneTransport', package, src, dest)],
            [('isPackage', package), ('isAirport',src), ('isAirport',dest), ('at',package,src) ],
            [('at', package,dest)]
        ]
    else: ## returning the task name and preconditions and effects with generic arguments for ChatGPT
        return [
                [('airplaneTransport', 'package', 'src', 'dest')],
                [('isPackage', 'package'), ('isAirport','src'), ('isAirport','dest'), ('at','package','src')],
                [('at', 'package','dest')]
            ]


def transferPackage(state, package, src, dest, checkArguments):
    if checkArguments: ## checking if the arguments are valid and returning the task, its preconditions and its effects
        if not isPackage(state,package) or not isLocation(state,src) or not isLocation(state,dest):
            return None
        return [
            [('transferPackage', package, src, dest)],
            [('isPackage', package), ('isLocation',src), ('isLocation',dest), ('at',package,src)],
            [('at', package,dest)]
        ]
    else: ## returning the task name and preconditions and effects with generic arguments for ChatGPT
        return [
                [('transferPackage', 'package', 'src', 'dest')],
                [('isPackage', 'package'), ('isLocation','src'), ('isLocation','dest'), ('at','package','src')],
                [('at', 'package','dest')]
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
    operators = (load_truck, unload_truck, drive_truck, load_plane, unload_plane, fly_plane, doNothing, verify_truckTransport, verify_airplaneTransport, verify_transferPackage)
    textOperators = ""
    for oper in operators:
        textOperators += get_function_source(oper,skipHALT)
    return textOperators

def translateAxiomsToText(axioms,skipHALT):
    axioms = (same_city,isPackage,isAirport,isTruck,isPost,isLocation,isAirplane)
    textAxioms = ""
    for ax in axioms:
        textAxioms += get_function_source(ax, skipHALT)
    return textAxioms