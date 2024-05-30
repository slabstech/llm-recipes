import prance
from typing import List
from mistral_common.tokens.tokenizers.mistral import MistralTokenizer
from mistral_common.protocol.instruct.request import ChatCompletionRequest
from mistral_common.protocol.instruct.tool_calls import Function, Tool
import ollama
from mistral_common.protocol.instruct.messages import UserMessage
import json
import requests
import functools

def load_openapi_spec(file_path):
    parser = prance.ResolvingParser(file_path, backend='openapi-spec-validator')
    spec = parser.specification
    return spec

def generate_tools(objs)-> List[Tool]:
    params = ['operationId', 'description',  'parameters']
    spec = load_openapi_spec('openapi.json')
    user_tools = []
    for obj in objs:
        resource, field = obj
        path = '/' + resource + '/{' + field + '}'
        function_name=spec['paths'][path]['get'][params[0]]
        function_description=spec['paths'][path]['get'][params[1]]
        function_parameters=spec['paths'][path]['get'][params[2]]
        func_parameters = {
        "type": "object",
        "properties": {
            function_parameters[0]['name']: {
                "type": function_parameters[0]['schema']['type'],
                "description": function_parameters[0]['description']
            }
        },
        "required": [function_parameters[0]['name']]
    }
        user_function= Function(name = function_name, description = function_description, parameters = func_parameters, )
        user_tool = Tool(function = user_function)
        user_tools.append(user_tool)
    return user_tools

def get_user_messages(queries: List[str]) -> List[UserMessage]:
    user_messages=[]
    for query in queries:
        user_message = UserMessage(content=query)
        user_messages.append(user_message)
    return user_messages

def process_results(tool_calls, messages):
    index = 0 
    for tool_call in tool_calls:
        function_name = tool_call["name"]
        function_params = (tool_call["arguments"]) 
        print(messages[index].content)
        function_result = names_to_functions[function_name](**function_params)
        print(function_result)
        index = index + 1


def getPetById(petId: int) -> str:
    try:
        method = 'GET'
        headers=None
        data=None
        url =  'https://petstore3.swagger.io/api/v3/pet/' + str(petId)
        response = requests.request(method, url, headers=headers, data=data)
        # Raise an exception if the response was unsuccessful
        response.raise_for_status()
        #response = make_api_call('GET', url + str(petId))
        if response.ok :
            json_response = response.json()
            if petId == json_response['id']:
                return json_response
        return json.dumps({'error': 'Pet id not found.'})
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return json.dumps({'error': 'Pet id not found.'})
        else:
            return json.dumps({'error': 'Error with API.'})

def getUserByName(username: str) -> str:
    try:
        url = 'https://petstore3.swagger.io/api/v3/user/' + username
        response = requests.get(url)
        # Raise an exception if the response was unsuccessful
        response.raise_for_status()
        if response.ok :
            json_response = response.json()
            if username == json_response['username']:
                return json_response
        return json.dumps({'error': 'Username id not found.'})
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return json.dumps({'error': 'Username not found.'})
        else:
            return json.dumps({'error': 'Error with API.'})

names_to_functions = {
  'getPetById': functools.partial(getPetById, petId=''),
  'getUserByName': functools.partial(getUserByName, username='')  
}


def execute_generator():
    queries = ["What's the status of my Pet 1?", "Find information of user user1?" ,  "What's the status of my Store Order 3?"]
    return_objs = [['pet','petId'], ['user', 'username'], ['store/order','orderId']]

    user_messages=get_user_messages(queries)
    user_tools = generate_tools(return_objs)

    tokenizer = MistralTokenizer.v3()
    completion_request = ChatCompletionRequest(tools=user_tools, messages=user_messages,)
    tokenized = tokenizer.encode_chat_completion(completion_request)
    tokens, text = tokenized.tokens, tokenized.text
    print(text)
    result = ollama.generate(model='mistral:7b', prompt=text, raw=True,stream=False)
    print(result['response'])
    tool_call = result['response'].split("\n\n")
    function_call = tool_call[0].replace("[TOOL_CALLS] ","")
    function_c = json.loads(function_call)
    function_name = function_c[0]["name"]
    function_params = (function_c[0]["arguments"]) 
    print("\nfunction_name: ", function_name, "\nfunction_params: ", function_params)

    tool_calls = json.loads(result[0])
    tool_calls
    
    process_results(tool_calls, user_messages)