_DATAFLOW_FUNCTION_ARGS_ERROR = 'Argument {1} in function {0} must be POSITIONAL_OR_KEYWORD argument.'
_DATAFLOW_NOT_CALLABLE_ERROR = '{0} is not a callable object. DataFlow can contain only callable objects.'
_DATAFLOW_NOT_TUPLE_ERROR = '{0} is not a tuple. DataFlow must be defined as tuple'
_DATAFLOW_EMPTY_ERROR = 'DataFlow or sub DataFlow cannot be empty.'
_DATAFLOW_MERGE_ERROR = 'Conflict with merge {0} to {1}.'

_ARGS_MAPPER_INPUT_KEY_ERROR = 'Key {2} is not passed as arguments {1} to {0}.'
_ARGS_MAPPER_OUTPUT_KEY_ERROR = 'Key {2} is not in returned dictionary {1} from {0}.'
_ARGS_MAPPER_ARGS_ERROR = 'Wrong arguments {1} passed to {0}.'

_DISPATCH_ERROR = 'Dispatched function {1} not exists'


class DataFlowException(Exception):
    '''Basic exception for asyncdataflow module.
    '''
    def __init__(self, *args, error_string: str):
        self.message = error_string.format(*args)
        super(__class__, self).__init__(self.message)


class DataFlowError(DataFlowException):
    '''Basic exception for asyncdataflow process. 
    '''
    def __init__(self, *args, error_string: str):
        super(__class__, self).__init__(*args, error_string=error_string)


class DataFlowRunItemError(DataFlowError):
    '''Basic exception for any errors when DataFlow is running.
    '''
    def __init__(self, *args, error_string: str):
        super(__class__, self).__init__(*args, error_string=error_string)      


class DataFlowMergeResultError(DataFlowRunItemError):
    '''Raised when returned dictionary from function shoudn't be merged with returned dictionary by other functions.
    '''
    def __init__(self, *args):
        super(__class__, self).__init__(*args, error_string=_DATAFLOW_MERGE_ERROR) 


class DataFlowDefinitionError(DataFlowError):
    '''Basic exception for any errors when DataFlow is defined.
    '''
    def __init__(self, *args, error_string: str):
        super(__class__, self).__init__(*args, error_string=error_string)      


class DataFlowFunctionArgsError(DataFlowDefinitionError):
    '''Raised when function used in DataFlow has another arguments that POSITIONAL_OR_KEYWORD arguments.
    '''
    def __init__(self, *args):
        super(__class__, self).__init__(*args, error_string=_DATAFLOW_FUNCTION_ARGS_ERROR)      


class DataFlowNotCallableError(DataFlowDefinitionError):
    '''Raised when DataFlow contain not callable objects.
    '''
    def __init__(self, *args):
        super(__class__, self).__init__(*args, error_string=_DATAFLOW_NOT_CALLABLE_ERROR) 


class DataFlowNotTupleError(DataFlowDefinitionError):
    '''Raised when DataFlow is defined as other that tuple collection.
    '''
    def __init__(self, *args):
        super(__class__, self).__init__(*args, error_string=_DATAFLOW_NOT_TUPLE_ERROR) 


class DataFlowEmptyError(DataFlowDefinitionError):
    '''Raised when DataFlow or sub-DataFlow is empty - tuple or nested tuple defined DataFlow is empty.
    '''
    def __init__(self, *args):
        super(__class__, self).__init__(*args, error_string=_DATAFLOW_EMPTY_ERROR) 


class ArgsMapperError(DataFlowException):
    '''Basic exception for any errors returned by args_mapper.
    '''
    def __init__(self, *args, error_string: str):
        super(__class__, self).__init__(*args, error_string=error_string)


class ArgsMapperInputKeyError(ArgsMapperError):
    '''Raised when mapping defined in input argument do not correspond to initial function arguments.
    '''
    def __init__(self, *args):
        super(__class__, self).__init__(*args, error_string=_ARGS_MAPPER_INPUT_KEY_ERROR)


class ArgsMapperOutputKeyError(ArgsMapperError):
    '''Raised when mapping defined in output argument do not correspond to returned from function dictionary. 
    '''
    def __init__(self, *args):
        super(__class__, self).__init__(*args, error_string=_ARGS_MAPPER_OUTPUT_KEY_ERROR)


class ArgsMapperArgsError(ArgsMapperError):
    '''Raised when passed arguments to functions do not fit to origin arguments.
    '''
    def __init__(self, *args):
        super(__class__, self).__init__(*args, error_string=_ARGS_MAPPER_ARGS_ERROR)


class DispatchError(DataFlowException):
    '''Raised when dispatched function didn't be registered
    '''
    def __init__(self, *args):
        super(__class__, self).__init__(*args, error_string=_ARGS_MAPPER_INPUT_KEY_ERROR)