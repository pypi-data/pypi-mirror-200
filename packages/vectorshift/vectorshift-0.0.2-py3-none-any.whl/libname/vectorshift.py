import requests
import functools
import dill
import json

class Vectorshift():
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def transformation(self,
                       name: str,
                       inputs: dict,
                       outputs: dict,
                       description: str = 'No description',
                       type: str = 'Custom',
                       can_output: bool = True,
                       takes_context: bool = False,
                       override: bool = False):
        def transformation_decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                function_str = dill.source.getsource(func)
                function_str = function_str[function_str.find('\ndef ')+1:]
                transformation_params = {
                    'name': name,
                    'description': description,
                    'type': type,
                    'inputs': inputs,
                    'outputs': outputs,
                    'function': function_str,
                    'functionName': func.__name__,
                    'canOutput': can_output,
                    'takesContext': takes_context,
                    'override': override
                }
                requests.post('https://api.vector-shift.com/api/transformations/user/create',
                              data={'transformation': json.dumps(transformation_params), 'api_key': self.api_key})
                return func(*args, **kwargs)
            return wrapper
        return transformation_decorator

    def add_transformation(self,
                           func,
                           name: str,
                           inputs: dict,
                           outputs: dict,
                           description: str = 'No description',
                           type: str = 'Custom',
                           can_output: bool = True,
                           takes_context: bool = False,
                           override: bool = False):
        function_str = dill.source.getsource(func)
        function_str = function_str[function_str.find('\ndef ')+1:]
        transformation_params = {
            'name': name,
            'description': description,
            'type': type,
            'inputs': inputs,
            'outputs': outputs,
            'function': function_str,
            'functionName': func.__name__,
            'canOutput': can_output,
            'takesContext': takes_context,
            'override': override
        }
        return requests.post('https://api.vector-shift.com/api/transformations/user/create',
                             data={'transformation': json.dumps(transformation_params), 'api_key': self.api_key})
