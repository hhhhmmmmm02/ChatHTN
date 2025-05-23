

from __future__ import print_function
import copy,sys, pprint

queriesChatGPT= 0

### compilation order: <domain>Definitions, pyhop, openAINewVersion, <domain>
### comment/uncomment in Line 116 (approx.), depending on domain

"""  ChatHTN: author Hector Munoz-Avila
    This code is built on top of pyhop and therefore it is released under the  Apache License, Version 2.0 

"""  

"""  
Pyhop, version 1.2.2 -- a simple SHOP-like planner written in Python.
Author: Dana S. Nau, 2013.05.31

Copyright 2013 Dana S. Nau - http://www.cs.umd.edu/~nau

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

Pyhop should work correctly in both Python 2.7 and Python 3.2.
For examples of how to use it, see the example files that come with Pyhop.

Pyhop provides the following classes and functions:

- foo = State('foo') tells Pyhop to create an empty state object named 'foo'.
  To put variables and values into it, you should do assignments such as
  foo.var1 = val1

- bar = Goal('bar') tells Pyhop to create an empty goal object named 'bar'.
  To put variables and values into it, you should do assignments such as
  bar.var1 = val1

- print_state(foo) will print the variables and values in the state foo.

- print_goal(foo) will print the variables and values in the goal foo.

- declare_operators(o1, o2, ..., ok) tells Pyhop that o1, o2, ..., ok
  are all of the planning operators; this supersedes any previous call
  to declare_operators.

- print_operators() will print out the list of available operators.

- declare_methods('foo', m1, m2, ..., mk) tells Pyhop that m1, m2, ..., mk
  are all of the methods for tasks having 'foo' as their taskname; this
  supersedes any previous call to declare_methods('foo', ...).

- print_methods() will print out a list of all declared methods.

- pyhop(state1,tasklist) tells Pyhop to find a plan for accomplishing tasklist
  (a list of tasks), starting from an initial state state1, using whatever
  methods and operators you declared previously.

- In the above call to pyhop, you can add an optional 3rd argument called
  'verbose' that tells pyhop how much debugging printout it should provide:
- if verbose = 0 (the default), pyhop returns the solution but prints nothing;
- if verbose = 1, it prints the initial parameters and the answer;
- if verbose = 2, it also prints a message on each recursive call;
- if verbose = 3, it also prints info about what it's computing.
"""

# Pyhop's planning algorithm is very similar to the one in SHOP and JSHOP
# (see http://www.cs.umd.edu/projects/shop). Like SHOP and JSHOP, Pyhop uses
# HTN methods to decompose tasks into smaller and smaller subtasks, until it
# finds tasks that correspond directly to actions. But Pyhop differs from
# SHOP and JSHOP in several ways that should make it easier to use Pyhop
# as part of other programs:
#
# (1) In Pyhop, one writes methods and operators as ordinary Python functions
#     (rather than using a special-purpose language, as in SHOP and JSHOP).
#
# (2) Instead of representing states as collections of logical assertions,
#     Pyhop uses state-variable representation: a state is a Python object
#     that contains variable bindings. For example, to define a state in
#     which box b is located in room r1, you might write something like this:
#     s = State()
#     s.loc['b'] = 'r1'
#
# (3) You also can define goals as Python objects. For example, to specify
#     that a goal of having box b in room r2, you might write this:
#     g = Goal()
#     g.loc['b'] = 'r2'
#     Like most HTN planners, Pyhop will ignore g unless you explicitly
#     tell it what to do with g. You can do that by referring to g in
#     your methods and operators, and passing g to them as an argument.
#     In the same fashion, you could tell Pyhop to achieve any one of
#     several different goals, or to achieve them in some desired sequence.
#
# (4) Unlike SHOP and JSHOP, Pyhop doesn't include a Horn-clause inference
#     engine for evaluating preconditions of operators and methods. So far,
#     I've seen no need for it; I've found it easier to write precondition
#     evaluations directly in Python. But I could consider adding such a
#     feature if someone convinces me that it's really necessary.
#
# Accompanying this file are several files that give examples of how to use
# Pyhop. To run them, launch python and type "import blocks_world_examples"
# or "import simple_travel_example".



import copy
import inspect

##### Unselect one of the following depending on the domain
from logisticsDefinitions import *
###from houseHoldRobotDefinitions import *
###from searchANDrescueDefinitions import *



############################################################

def askChatGPT(state,task1,nonprimitiveTasks, skipHALT):

    from openAINewVersion import askChatWhichOperators, chat_with_gpt, translateToText, translateAtomsToText, translateStateToText

    if not skipHALT: 
        input("asking chatGPT  ENTER")
        input("ENTER AGAIN")

    if task1[0] in nonprimitiveTasks:
        taskName = nonprimitiveTasks[task1[0]]
    else:
        return []
    taskPrecsEffs = taskName(state,*task1[1:],True) ## if valid arguments, return task, its preconditions and its effects
    if taskPrecsEffs is None:
        return []
    taskText = translateToText(task1)
    precsText = translateAtomsToText(taskPrecsEffs[1])
    effectsText = translateAtomsToText(taskPrecsEffs[2])
    stateText = translateStateToText(state)
    operatorsText = translateOperatorsToText(operators,skipHALT)
    axiomsText = translateAxiomsToText(axioms, skipHALT)

    
    print("")
    print("Asking chatGPT for a task breakdown of task: ", taskText, " preconditions: ", precsText," effects: ",  
          effectsText) ###, " state: ", stateText, "operators: ", operatorsText, "axioms: ", axiomsText)
    print("wait for ChatGPT's response")
    response = chat_with_gpt(taskText, precsText, effectsText, stateText, operatorsText, axiomsText)
    
    
    print("Here is ChatGPT response: ",response)
    if not skipHALT: input("ENTER")



    # othertasksText = ""
    # i = 0
    # taskNames = []
    # for npTask in nonprimitiveTasks:
    #     if npTask != task1[0]:
    #         taskNames.append(npTask)
    #         taskPrecsEff = eval(npTask)(state,*task1[1:],False) ## returns generic task, preconditions and effects
    #         othertasksText += " Task "+ str(i)+": "+ translateAtomsToText(taskPrecsEff[0]) + "; preconditions: " + translateAtomsToText(taskPrecsEff[1]) + "; effects: " + translateAtomsToText(taskPrecsEff[2])
    #         i += 1

    print("Asking ChatGPT to map the task breakdown to the operators")
    print("wait for ChatGPT's response")


    newResponse = askChatWhichOperators(response, taskText, precsText, effectsText, stateText, operatorsText, axiomsText)
    print("Here is ChatGPT new Response: "+newResponse)

    if not skipHALT: input(" ENTER")

    from openAINewVersion import newExtractOperators

    ### This was the code when newResponse was verbose:
    #tasksReturnedText = extract_named_predicates(newResponse,taskNames)
    #generatedSubTasks = predicates_to_sexpr_list(tasksReturnedText)
    #generatedSubTasksFinal = remove_duplicate_predicates(generatedSubTasks)

    generatedSubTasksFinal = newExtractOperators(newResponse)
    
    print("Here are the subtasks generated by ChatGPT: ")
    print(generatedSubTasksFinal)
    print("")


    return generatedSubTasksFinal

def generateVerifyTask(task1):
    verify_task = copy.copy(task1)
    verify_task = list(verify_task)
    nameTask_task1 = f"{'verify_'}{verify_task[0]}"
    verify_task = verify_task[1:]
    verify_task.insert(0, nameTask_task1)
    verify_task = tuple(verify_task)
    return verify_task

def alreadyVisited(t,at_t,theStack):
    ### the correct way to check for loop if stack = [(task,state),(task,state),...]
    ### if (task1,state) is in stack then there is an infinite loop!
 
    for (task,at_task) in theStack:
        if not task[0].startswith("verify"):
            if task == t and at_task == at_t:
                print("state and task: ", t, "already visited")
                return True
    ####print("not visited")
    return False
  
############################################################
# States and goals

class State():
    """A state is just a collection of variable bindings."""
    def __init__(self,name):
        self.__name__ = name

class Goal():
    """A goal is just a collection of variable bindings."""
    def __init__(self,name):
        self.__name__ = name


### print_state and print_goal are identical except for the name

def print_state(state,indent=4):
    """Print each variable in state, indented by indent spaces."""
    if state != False:
        for (name,val) in vars(state).items():
            if name != '__name__':
                for x in range(indent): sys.stdout.write(' ')
                sys.stdout.write(state.__name__ + '.' + name)
                print(' =', val)
    else: print('False')

def print_goal(goal,indent=4):
    """Print each variable in goal, indented by indent spaces."""
    if goal != False:
        for (name,val) in vars(goal).items():
            if name != '__name__':
                for x in range(indent): sys.stdout.write(' ')
                sys.stdout.write(goal.__name__ + '.' + name)
                print(' =', val)
    else: print('False')

############################################################
# Helper functions that may be useful in domain models

def forall(seq,cond):
    """True if cond(x) holds for all x in seq, otherwise False."""
    for x in seq:
        if not cond(x): return False
    return True

def find_if(cond,seq):
    """
    Return the first x in seq such that cond(x) holds, if there is one.
    Otherwise return None.
    """
    for x in seq:
        if cond(x): return x
    return None

############################################################
# Commands to tell Pyhop what the operators and methods are

operators = {}
methods = {}
nonprimitiveTasks = {}
axioms = {}

def declare_axioms(*a_list):
    """
    Call this after defining the operators, to tell Pyhop what they are.
    a_list must be a list of functions, not strings.
    """
    axioms.update({a.__name__:a for a in a_list})
    return axioms

def declare_tasks(*t_list):
    """
    Call this after defining the operators, to tell Pyhop what they are.
    t_list must be a list of functions, not strings.
    """
    nonprimitiveTasks.update({t.__name__:t for t in t_list})
    return nonprimitiveTasks


def declare_operators(*op_list):
    """
    Call this after defining the operators, to tell Pyhop what they are.
    op_list must be a list of functions, not strings.
    """
    operators.update({op.__name__:op for op in op_list})
    return operators

def declare_methods(task_name,*method_list):
    """
    Call this once for each task, to tell Pyhop what the methods are.
    task_name must be a string.
    method_list must be a list of functions, not strings.
    """
    methods.update({task_name:list(method_list)})
    return methods[task_name]

############################################################
# Commands to find out what the operators and methods are

def print_operators(olist=operators):
    """Print out the names of the operators"""
    print('OPERATORS:', ', '.join(olist))

def print_methods(mlist=methods):
    """Print out a table of what the methods are for each task"""
    print('{:<14}{}'.format('TASK:','METHODS:'))
    for task in mlist:
        print('{:<14}'.format(task) + ', '.join([f.__name__ for f in mlist[task]]))

def print_tasks(tlist=nonprimitiveTasks):
    """Print out the names of the tasks"""
    print('TASKS:', ', '.join(tlist))

def print_axioms(alist=axioms):
    """Print out the names of the tasks"""
    print('AXIOMS:', ', '.join(alist))

############################################################
# The actual planner

def pyhop(skipHALT,state,tasks,verbose):
    """
    Try to find a plan that accomplishes tasks in state.
    If successful, return the plan. Otherwise return False.
    """
    if verbose>0: print('** pyhop, verbose={}: **\n   state = {}\n   tasks = {}'.format(verbose, state.__name__, tasks))
    ### first  parameter is added to check for directAncesctors: works like a stack but its flushout as soon
    ### as a non verifier operator is executed

    ### the correct way to check for loop if stack = [(task,state),(task,state),...]
    ### if (task1,state) is in stack then there is an infinite loop!
    ### the first parameter is the stack

    ### print('- added counter for number of queriesChatGPT' ) ## this is a global variable to count even when seek_plan backtracks
    global queriesChatGPT 

    result = seek_plan([],skipHALT,state,tasks,[],0,verbose)
    if verbose>0: 
        print('** RESULT =',result,'\n')
        print("queriesChatGPT: ",queriesChatGPT)
    return result

def seek_plan(theStack,skipHALT,state,tasks,plan,depth,verbose):
    """
    Workhorse for pyhop. state and tasks are as in pyhop.
    - plan is the current partial plan.
    - depth is the recursion depth, for use in debugging
    - verbose is whether to print debugging messages
    """
    global queriesChatGPT

    if verbose>1: print('depth {} tasks {}'.format(depth,tasks))
    if tasks == []:
        if verbose>2: print('depth {} returns plan {}'.format(depth,plan))
        return plan 
    task1 = tasks[0]
    if verbose>1: 
        print("next task:", task1)


    ### the correct way to check for loop if stack = [(task,state),(task,state),...]
    ### if (task1,state) is in stack then there is an infinite loop!
    
    if alreadyVisited(task1,state.at,theStack):
            print("Direct ancestor of itself: ", task1, " returning failure")
            if not skipHALT: input("halt")
            return False
    
    
    if task1[0] in operators:
        if task1[0].startswith("verify_"):
            if plan and plan[-1] == task1: ## repeated verify_ task; so skip it
                solution  = seek_plan(theStack,skipHALT,state,tasks[1:],plan,depth+1,verbose)
                if solution != False:
                    return solution 
                else:
                    return False
            
        if verbose>1: 
            print(" primitive")
            if not skipHALT: input("ENTER")
        if verbose>2: print('depth {} action {}'.format(depth,task1))
        operator = operators[task1[0]]

        # Check if the number of arguments matches
        sig = inspect.signature(operator)
        num_params = len(sig.parameters) - 1
        if len(task1[1:]) != num_params:
            print("error number of parameters Task1 name: ", task1[0],"< operator:", operator, "complete task: ", task1, " no plan can be generated")
            ##print(f"Error: {operator.__name__} takes {num_params} positional arguments but {len(*task1[1:])} were given")
            return False 
        
        ### need to check if arguments are tru objects 

        newstate = operator(copy.deepcopy(state),*task1[1:])
        if verbose>2:
            print('depth {} new state:'.format(depth))
            print_state(newstate)
        if newstate:
            ## keeping track of all (task,state) visited in a stack
            theStack.insert(0,(task1,state.at))
            solution  = seek_plan(theStack,skipHALT,newstate,tasks[1:],plan+[task1],depth+1,verbose)
            if solution != False:
                return solution 
            else:
                return False 
            
        if verbose>2: print('depth {} returns failure'.format(depth))
        return False

    if task1[0] in methods:
        if verbose>1: 
            print(" nonprimitive")
            if not skipHALT: input("ENTER")
        if verbose>2: print('depth {} method instance {}'.format(depth,task1))

        # Check if the number of arguments matches
        taskDefinition = nonprimitiveTasks[task1[0]]
        sig = inspect.signature(taskDefinition)
        num_params = len(sig.parameters) - 2 ## minus state and checkArguments
        if len(task1[1:]) != num_params:
            print(task1, " has incorrect number of arguments")
            return False 
        if not taskDefinition(state,*task1[1:],True): ### checks that arguments are true objects
            return False
        
        relevant = methods[task1[0]]
        for method in relevant:
            subtasks = method(state,*task1[1:])
            # Can't just say "if subtasks:", because that's wrong if subtasks == []
            if verbose>2:
                print('depth {} new tasks: {}'.format(depth,subtasks))
            if subtasks != False:
                verify_task = generateVerifyTask(task1)
                if tasks[-1] != verify_task:
                    subtasks.append(verify_task)
                theStack.insert(0,(task1,state.at))
                solution  = seek_plan(theStack,skipHALT,state,subtasks+tasks[1:],plan,depth+1,verbose)
                if solution != False:
                    return solution
    
    
    #### If it reaches this point:
    ###     task1[0] is compound and no methods are applicable
    ###     by adding the code below, will avoid backtrackigng to parent task
    ###     NEW code starts here


        taskDefinition = nonprimitiveTasks.get(task1[0],False)
        if taskDefinition == False: ###not a name of a task
            print(task1[0], " is not an existing task name or has incorrect number of arguments")
            return False
        sig = inspect.signature(taskDefinition)
        num_params = len(sig.parameters) - 2 ## minus state and checkArguments
        if len(task1[1:]) != num_params:
            print(task1, " has incorrect number of arguments")
            return False
        if not taskDefinition(state,*task1[1:],True): ### checks that arguments are true objects
            return False

        chatGPTtasks = askChatGPT(state,task1,nonprimitiveTasks,skipHALT)
        queriesChatGPT = queriesChatGPT + 1
        print("chatGPTtasks: ", chatGPTtasks, "queriesChatGPT:",queriesChatGPT)
        if  len(chatGPTtasks) > 0 and task1 != chatGPTtasks[0]:
            print("task1: ", task1)
            print("chatGPTtasks+tasks[1:]: ", chatGPTtasks+tasks[1:])
            theStack.insert(0,(task1,state.at))
            verify_task = generateVerifyTask(task1)
            if chatGPTtasks[-1] != verify_task:
                chatGPTtasks.append(verify_task)

            solution  = seek_plan( theStack,skipHALT,state,chatGPTtasks+tasks[1:],plan,depth+1,verbose)
            if solution == False:
                print("no solution from chatGPT fix")
            return solution 

        if verbose>2: print('depth {} returns failure'.format(depth))
        return False
        
    ### NEW code ends
    
   