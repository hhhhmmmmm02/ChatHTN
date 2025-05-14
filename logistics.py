### compilation order: <domain>Definitions, pyhop, openAINewVersion, <domain>


"""  ChatHTN: author Hector Munoz-Avila
    This code is built on top of pyhop and therefore it is released under  the Apache License, Version 2.0 

"""  

import pyhop
from logisticsDefinitions import *

state1 = pyhop.State('state1')
state1.at = {
                'package1':'location1',
                'truck1':'location2',
                'truck2':'location3',
                'airport1':'city1',
                'plane1':'airport2',
                'location1': 'city1',
                'location2': 'city1',
                'location3': 'city2',
                'airport2': 'city2'
            }


state1.cities = {'city1', 'city2'}
state1.airports =  {'airport1', 'airport2'}
state1.airplanes = {'plane1'}  ##
state1.trucks = {'truck1','truck2'}
state1.packages = {'package1'}
state1.postOffices = {'location1', 'location2','location3'}




pyhop.declare_axioms(same_city,isPackage,isAirport,isTruck,isPost,isLocation,isAirplane)
print("")
pyhop.print_axioms()
# operators

## for implementing symbolic: check if every argument is a variable. Maintain a single table: see above


pyhop.declare_operators(load_truck, unload_truck, drive_truck, load_plane, unload_plane, fly_plane, doNothing, verify_truckTransport, verify_airplaneTransport, verify_transferPackage)
print('')
pyhop.print_operators()


pyhop.declare_methods('truckTransport',   truckTransportMethod1,  truckTransportMethod2, truckTransportMethod3) ## YES: (0) YES: (2) YES: (5,2)  0methods: YES (5,2); 
pyhop.declare_methods('airplaneTransport',  airplaneTransportMethod1, airplaneTransportMethod2, airplaneTransportMethod3) # YES: (0) YES: (1) YES: (1) 0methods: YES: (1)
pyhop.declare_methods('transferPackage', transferPackageMethod1, transferPackageMethod2) # YES: (0) YES: (1,1,1,1,1) 0methods: YES: (1,1,1,1)
#Unsolvale problem: remove all occurings of 'plane1' in the state #### NO:(4)



print('')
pyhop.print_methods()

### defining tasks

pyhop.declare_tasks(airplaneTransport,transferPackage,truckTransport)

print('')
pyhop.print_tasks()

### going to declare tasks as (Preconditions,effects)
###
### truckTransport(package, src, dest)
### preconditions: isPackage(package), isLocation(src), isLocation(dest), at(package,src)
### preconditions: at(package,dest)
### airplaneTransport(plane, src, dest)
### preconditions: isPackage(package), isPlane(plane), isAirport(src), isAirport(dest), at(package,src)
### preconditions: at(package,dest)





print("""
********************************************************************************
Call pyhop.pyhop(state1,state.task1) with different verbosity levels
********************************************************************************
""")

# print("- If verbose=0 (the default), Pyhop returns the solution but prints nothing.\n")
# pyhop.pyhop(state1,state1.task,verbose=0))

#print('- If verbose=1, Pyhop prints the problem and solution, and returns the solution:')
#pyhop.pyhop(state1,state1.task,verbose=1)



print('- If verbose=2, Pyhop also prints a note at each recursive call:')
print('- added flag to skip input commands: skipHALT if True it will  skip input comands' ) ## this is the first argument below
solution = pyhop.pyhop(True, state1,[('transferPackage','package1','location1','location3')],verbose=2)

print(solution)

# print('- If verbose=3, Pyhop also prints the intermediate states:')
# pyhop.pyhop(state1,state1.task,verbose=3)

