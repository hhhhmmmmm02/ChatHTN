### compilation order: <domain>Definitions, pyhop, openAINewVersion, <domain>

"""  ChatHTN: author Hector Munoz-Avila
    This code is built on top of pyhop and therefore it is released under the  Apache License, Version 2.0 

"""  

import pyhop
from houseHoldRobotDefinitions import *

# ## how to make it symbolic. WHY I NEED THIS? because we want to pass operators to ChatGPT. But actually not 
# ## needed as I can pass the text of the python operators
# ## state maintains a list with all values as a dictionary:
# ## auxiliary functions below are needed
# ## always check if vatiable is defined in value table
# ## state.value:
# state1.value = {
#                 'package1':'location1',
#                 'airport1':'city1'
#                 ###...
#             }
# ## state.isType for every state variable: sop no need for the isPackage(pck) function
# state1.isType ={
#                 'package1':'package',
#                 'airprot1':'airport'
#                 ##...
#              }

# # state.types: list all types
# state1.Types = {'package',
#                 'airport'
#                 ##....
#                 }


# # state variables

state1 = pyhop.State('state1')
state1.at = {
                'robot':'livingRoom',
                'bedRoom':'dirtyANDmessy',
                'livingRoom':'cleanANDmessy',
                'kitchen':'dirtyANDorganized'
            }

state1.robots = {'robot'}
state1.rooms =  {'bedRoom','livingRoom'}
state1.kitchens = {'kitchen'}
state1.objects = {'dinner'}
state1.houses = {'house'}



### this list must be replicated in HouseHoldRobotDefinitions >> translateAxiomsToText(axioms,skipHALT)
pyhop.declare_axioms(isRobot,isRoom,isKitchen,isLocation,isMeal,isHouse,aDirtyLocation,aRobot,houseIsClean,aRobotAtLoc,isDirtyLocation,aMessyLocation,isMessyLocation,isOrganizedLocation,houseIsOrganized,houseIsTakenCare)
print("")
pyhop.print_axioms()


# operators


### this list must be replicated in HouseHoldRobotDefinitions >> translateOperatorsToText(operators,skipHALT)
pyhop.declare_operators(move, sweep, pick_up, drop, organize,doNothing,verify_sweepTask,verify_cleanHouse,verify_organizeHouse,verify_organizeTask, verify_takeCareHouse)
print('')
pyhop.print_operators()


pyhop.declare_methods('cleanHouse', cleanHouseM1, cleanHouseM2) #### YES YES 0methods: YES
pyhop.declare_methods('organizeHouse', organizeHouseM1, organizeHouseM2)  #### YES YES 0methods: YES
pyhop.declare_methods('sweepTask', sweepTaskM1,sweepTaskM2) #### YES YES 0methods: YES
pyhop.declare_methods('organizeTask', organizeTaskM1,organizeTaskM2) #### YES YES 0methods: YES
pyhop.declare_methods('takeCareHouse', takeCareHouseM1) #### NO 0methods: NO

## No solution: remove all occurings of 'robot' in the state ##### NO


print('')
pyhop.print_methods()

### defining tasks

pyhop.declare_tasks(cleanHouse,sweepTask,organizeHouse,organizeTask,takeCareHouse)

print('')
pyhop.print_tasks()







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
print('- added flag to skip input commands: skipHALT if True it will  skip input comands' )
pyhop.pyhop(True, state1,[('takeCareHouse','house')],verbose=2)

# print('- If verbose=3, Pyhop also prints the intermediate states:')
# pyhop.pyhop(state1,state1.task,verbose=3)

