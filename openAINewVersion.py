### compilation order: <domain>Definitions, pyhop, openAINewVersion, <domain>


"""  ChatHTN: author Hector Munoz-Avila
    This code is released under the  Apache License, Version 2.0 

"""  

from openai import OpenAI
openai = OpenAI(
    api_key = "YOUR KEY"
)

import re


### extracting the tasks from the API response

### OLD versiom
#def extract_predicates(api_response):
#    # Extract lines starting with 'Predicates: -'
#    predicates = re.findall(r'Predicates:\s*-\s*`(.*?)`', api_response)
#    return predicates'''

# (credit: ChatGPT)

def extract_named_predicates(api_response, names):
    # Build regex pattern to match predicates from the provided names
    pattern = re.compile(r'(`?(' + '|'.join(re.escape(name) for name in names) + r')\([^)]*\)`?)')
    matches = pattern.findall(api_response)
    predicates = [match[0].strip('`') for match in matches]
    return predicates

## extracts operators in pyhop form; removes the argument state (supposed to be first argument). (credit: ChatGPT)

def newExtractOperators(response: str):
    predicates = []
    for line in response.strip().split("\n"):
        line = line.strip()
        if line:
            func_name, args = line.split("(", 1)
            args = args.rstrip(")")
            args_list = [arg.strip().strip("'") for arg in args.split(",")]
            predicates.append((func_name,) + tuple(args_list[1:]))  # Remove 'state'
    return predicates

### converting the predicates into the pyhop task list format. (credit: ChatGPT)

def predicates_to_sexpr_list(predicates):
    sexpr_list = []
    for predicate in predicates:
        match = re.match(r'(\w+)\((.*?)\)', predicate)
        if match:
            name = match.group(1)
            args = [arg.strip() for arg in match.group(2).split(',')]
            sexpr_list.append((name, *args))
    return sexpr_list


### this is the version for the compact chatGPT return:

def parse_predicates(input_str):
    predicates = []
    for line in input_str.strip().split('\n'):
        if line:
            # Extract the predicate name and arguments
            name, args = line.split('(', 1)
            args = args.rstrip(')').split(', ')
            predicates.append((name, *args))
    return predicates


### New version (credit: ChatGPT):

def translateStateToText(state):
    predicates = []
    
    for attr_name, attr_value in vars(state).items():
        if isinstance(attr_value, set):  # For sets (single argument predicates)
            predicates.extend([f"{attr_name}('{item}')" for item in attr_value])
        elif isinstance(attr_value, dict):  # For dictionaries (two-argument predicates)
            predicates.extend([f"{attr_name}('{key}', '{value}')" for key, value in attr_value.items()])
    
    return ", ".join(predicates)




def translateToText(task1):
    text = task1[0]+"("
    for param in task1[1:]:
        text += param+", "
    text = text[:-2]
    text += ")"
    return(text)

def translateAtomsToText(list):
    text = ""
    for atom in list:
        text += translateToText(atom)+ ", "
    text = text[:-2]
    return text


def askChatWhichOperators(chatGPTtext, task, precs, effs, state, operatorsText, axiomsText):
    conversation=[
        {"role": "system", "content": "You are an AI planner specializing in HTN planning."},
        { "role":"user", 
        "content": 
        ". You generated the following response:"+chatGPTtext+ 
        "to my request to provide the Sub-Tasks Breakdown for the following task: " + task + 
        ". I also gave you the preconditions of the task: " + precs + " and the effects of the task: " + effs+
        ".and gave you the state: " +state + 
        "and gave you the domain  defined by the following operators (each defined as a  Python function):" + operatorsText+
        ". I also gave you the following python functions which are called to check some preconditions and to check some effects: " +axiomsText+
        ". As a follow-up, can you map  the subtasks you generated with the operators I provided, please? please list the operator names as predicates,"+
        " for the match you generate use only the predicate names of the operators and the arguments in your sub-task breakdown"+
        "Always respond with a compact, machine-readable format using predicate form. "+
        "Avoid explanations or extra text unless explicitly requested. "+
        "When generating your output, list only the predicates in the form: \n\n"+
        "predicate(arg1, arg2, ...)\n\n"+
        "where predicate is name of an operator I provided"+
        #"for predicate names use the  operator names exactly as written, including capitalization and formatting. "+
        " Separate predicates by newlines. Do not include explanations, headings, or descriptions."}
    ]

    response = openai.chat.completions.create(
        model= "gpt-4-turbo",
        messages = conversation,        
        max_tokens = 1000
    )
    return response.choices[0].message.content


    response = openai.chat.completions.create(
        model= "gpt-4-turbo",
        messages = conversation,        
        max_tokens = 1000
    )
    return response.choices[0].message.content

def chat_with_gpt(task, precs, effs, stateText,operatorsText, axiomsText):

    conversation=[
        {"role": "system", "content": "You are an AI planner specializing in HTN planning."},
        { "role":"user", 
        "content": "The domain is defined by the following operators (each defined as a  Python function):" + operatorsText +
        ". Some of the preconditions in the operators are defined by the following python functions: " +axiomsText+
        ". Provide the Sub-Tasks Breakdown for the following task: " + task  +
        ". Here are the preconditions of the task: " + precs +
          ". Here are the effects of the task: " + effs +
        ". Here is the current state: " +stateText }
    ]

# + "Always respond with a compact, machine-readable format using S-expressions. "+
#     "Avoid explanations or extra text unless explicitly requested. "+
#     "When generating a hierarchical plan, list only the predicates in the form: \n\n"+
#     "(predicate arg1 arg2 ...)\n\n"+
#     "Separate predicates by newlines. Do not include explanations, headings, or descriptions."

    response = openai.chat.completions.create(
        model= "gpt-4-turbo",
        messages = conversation,        
        max_tokens = 1000
    )
    return response.choices[0].message.content

""" goal = "Package picasso must be located in moma"
state = "package picasso is at Capitol. Capitol is a location in the city of Washington. There is an airport in Washington called Dallas. moma is located in New York city. There is an airport in New York called JFK."
response = chat_with_gpt(goal, state)
print("Chatbot: ",response) """