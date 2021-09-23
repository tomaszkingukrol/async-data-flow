from abc import ABC, abstractmethod


class DataFlowExecutor(ABC):
    @abstractmethod
    def run(self, pipe: tuple, **kwargs):
        ''' Executor in DataFlow must implement run method
        '''


class DataFlowInspector(ABC):
    @abstractmethod
    def check_dataflow_args(self, pipe: tuple):
        ''' Inspector in DataFlow must implement check_dataflow_args method
        '''