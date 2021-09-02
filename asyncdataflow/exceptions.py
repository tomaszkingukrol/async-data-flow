_DATAFLOW_FUNCTION_ARGS_ERROR = 'Argument {} in function {} must be POSITIONAL_OR_KEYWORD argument.'


DATAFLOW_MERGE_ERROR = 'Merge result from {} error.'
DATAFLOW_DEFINITION_ERROR = '{} is not a callable object. DataFlow can contain only callable objects.'
DATAFLOW_EMPTY_ERROR = 'DataFlow or sub DataFlow cannot be empty.'
DATAFLOW_ARGS_ERROR = 'Function {} in DataFlow must use only POSITIONAL_OR_KEYWORD arguments.'

_ARGS_MAPPER_INPUT_KEY_ERROR = 'key {} is not passed as arguments {} to {}.'
_ARGS_MAPPER_OUTPUT_KEY_ERROR = 'key {} is not returned dictionary {} from {}.'
_ARGS_MAPPER_ARGS_ERROR = 'wrong arguments {} passed to {}.'


class DataFlowException(TypeError):
    '''
    '''
    def __init__(self, *args, error_string: str):
        self.message = error_string.format(*args)
        super(__class__, self).__init__(self.message)


class DataFlowError(DataFlowException):
    '''
    '''
    def __init__(self, *args, error_string: str):
        super(__class__, self).__init__(*args, error_string=error_string)


class DataFlowDefinitionError(DataFlowError):
    '''
    '''
    def __init__(self, *args, error_string: str):
        super(__class__, self).__init__(*args, error_string=error_string)      


class DataFlowFunctionArgsError(DataFlowDefinitionError):
    '''
    '''
    def __init__(self, *args, error_string: str):
        super(__class__, self).__init__(*args, error_string=_DATAFLOW_FUNCTION_ARGS_ERROR)      




class ArgsMapperError(DataFlowException):
    '''
    '''
    def __init__(self, *args, error_string: str):
        super(__class__, self).__init__(*args, error_string=error_string)


class ArgsMapperInputKeyError(ArgsMapperError):
    '''
    '''
    def __init__(self, *args):
        super(__class__, self).__init__(*args, error_string=_ARGS_MAPPER_INPUT_KEY_ERROR)


class ArgsMapperOutputKeyError(ArgsMapperError):
    '''
    '''
    def __init__(self, *args):
        super(__class__, self).__init__(*args, error_string=_ARGS_MAPPER_OUTPUT_KEY_ERROR)


class ArgsMapperArgsError(ArgsMapperError):
    '''
    '''
    def __init__(self, *args):
        super(__class__, self).__init__(*args, error_string=_ARGS_MAPPER_ARGS_ERROR)


