
class DataFlowException(Exception):
    '''Basic exception for asyncdataflow module.
    '''
    error_msg = 'DataFlow exception occured.'

    def __init__(self, *args):
        self.message = self.error_msg.format(*args)
        super().__init__(self.message)


class DataFlowError(DataFlowException):
    '''Basic exception for asyncdataflow process. 
    '''

class DataFlowRunItemError(DataFlowError):
    '''Basic exception for any errors when DataFlow is running.
    '''

class DataFlowMergeResultError(DataFlowRunItemError):
    '''Raised when returned dictionaries cannot be merged.
    '''
    error_msg = 'Conflict with merge {0} to {1}.'


class DataFlowFunctionResultError(DataFlowRunItemError):
    '''Raised when function return other value that dictionary.
    '''
    error_msg = 'Function {0} must return dictionary'


class DataFlowDefinitionError(DataFlowError):
    '''Basic exception for any errors during DataFlow definition.
    '''

class DataFlowFunctionArgsError(DataFlowDefinitionError):
    '''Raised when function has another arguments that POSITIONAL_OR_KEYWORD arguments.
    '''
    error_msg = 'Argument {1} in function {0} must be POSITIONAL_OR_KEYWORD argument.'


class DataFlowNotCallableError(DataFlowDefinitionError):
    '''Raised when DataFlow contain not callable objects.
    '''
    error_msg = '{0} is not a callable object. DataFlow can contain only callable objects.'


class DataFlowNotTupleError(DataFlowDefinitionError):
    '''Raised when DataFlow is defined not as tuple.
    '''
    error_msg = '{0} is not a tuple. DataFlow must be defined as tuple'


class DataFlowEmptyError(DataFlowDefinitionError):
    '''Raised when DataFlow or sub-DataFlow is empty - tuple or nested tuple defined DataFlow cannot be empty.
    '''
    error_msg = 'DataFlow or sub DataFlow cannot be empty.'


class ArgsMapperError(DataFlowException):
    '''Basic exception for any errors returned by amapper (argument mapper).
    '''

class ArgsMapperInputKeyError(ArgsMapperError):
    '''Raised when mapping defined in input argument do not correspond to initial function arguments.
    '''
    error_msg = 'Key {2} is not passed as arguments {1} to {0}.'


class ArgsMapperOutputKeyError(ArgsMapperError):
    '''Raised when mapping defined in output argument do not correspond to returned from function dictionary. 
    '''
    error_msg = 'Key {2} is not in returned dictionary {1} from {0}.'


class ArgsMapperArgsError(ArgsMapperError):
    '''Raised when passed arguments to functions do not corespond to origin arguments.
    '''
    error_msg = 'Wrong arguments {1} passed to {0}.'


class DispatchError(DataFlowException):
    '''Raised when dispatched function didn't be registered
    '''
    error_msg = 'Dispatched function {0} not exists'

