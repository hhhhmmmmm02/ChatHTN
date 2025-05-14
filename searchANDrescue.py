### compilation order: <domain>Definitions, pyhop, openAINewVersion, <domain>


"""  ChatHTN: author Hector Munoz-Avila
    This code is built on top of pyhop and therefore it is released under the  Apache License, Version 2.0 

"""  

import pyhop
from searchANDrescueDefinitions import *

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
                'drone':'base',
                'john':'forest',
                'maria':'hill1'
            }
state1.drone={'drone'}##
state1.safeZone ={'hospital'}
state1.location ={'hospital','base','forest','mobil','hill1'}
state1.scanned ={'hospital':'yes',
                 'base':'yes',
                 'forest':'no',
                 'mobil':'yes',
                 'hill1':'yes'}
state1.weather ={'hospital':'clear',
                 'base':'clear',
                 'forest':'clear',
                 'mobil':'clear',
                 'hill1':'clear'}
state1.person={'john','maria'}
state1.region={'region'}



### this list must be replicated in <domain>Definitions >> translateAxiomsToText(axioms,skipHALT)
pyhop.declare_axioms(isLocation,isSafeZone,isDrone,isPerson,isRescuedSurvivor,needsRescueSurvivor,aDrone,aSafeZone,aDroneAtLoc,anUnscannedArea,isRegion,allAreasScanned,aSurvivorAt,noSurvivorsAt,isScanned,isUnScanned,allPeopleRescued)
print("")
pyhop.print_axioms()


# operators


### this list must be replicated in <domain>Definitions >> translateOperatorsToText(operators,skipHALT)
pyhop.declare_operators(fly,scanArea,pickUpSurvivor,dropSurvivor,doNothing,verify_rescueSurvivor,verify_searchANDrescue,verify_checkSurvivors,verify_scanAreaTask)
print('')
pyhop.print_operators()

pyhop.declare_methods('rescueSurvivor',   rescueSurvivorM1, rescueSurvivorM2) #rescueSurvivorM1:  YES:(2); , rescueSurvivorM2: YES:(1); 0methods: YES:(2)
pyhop.declare_methods('checkSurvivors',   checkSurvivorsM1,   checkSurvivorsM2) # checkSurvivorsM1:  YES:(0) checkSurvivorsM2:YES(1) 0methods: YES(1)
pyhop.declare_methods('scanAreaTask',  scanAreaTaskM1,scanAreaTaskM2,scanAreaTaskM3) # scanAreaTaskM1: YES (0) scanAreaTaskM2:  YES (0) scanAreaTaskM3: YES (1); 0methods: YES(1)
pyhop.declare_methods('searchANDrescue',searchANDrescueM1,searchANDrescueM2,searchANDrescueM3) #searchANDrescueM1: YES:(1); searchANDrescueM2: YES (0); searchANDrescueM3:YES  (1); 0methods: YES(1,1)



## No solution: make 'forest':'storm' ##### NO (4)


print('')
pyhop.print_methods()

### defining compound tasks

pyhop.declare_tasks(rescueSurvivor,searchANDrescue,checkSurvivors,scanAreaTask)

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
pyhop.pyhop(True, state1, [('searchANDrescue', 'region')],verbose=2)

# print('- If verbose=3, Pyhop also prints the intermediate states:')
# pyhop.pyhop(state1,state1.task,verbose=3)

