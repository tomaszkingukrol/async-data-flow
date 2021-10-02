from abc import ABC, abstractmethod


class DataFlowExecutor(ABC):
    @abstractmethod
    def run(self, pipe: tuple, **kwargs):
        ''' DataFlow Executor Class must implement run method
        '''


class DataFlowInspector(ABC):
    @abstractmethod
    def check_dataflow_args(self, pipe: tuple):
        ''' DataFlow Inspector class must implement check_dataflow_args method
        '''