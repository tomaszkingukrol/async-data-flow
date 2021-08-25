from abc import ABC, abstractmethod


class DataFlowExecutor(ABC):
    @abstractmethod
    def run(self, pipe: tuple, **kwargs):
        pass


class DataFlowInspector(ABC):
    @abstractmethod
    def check_pipe_args(self, pipe: tuple) -> set:
        pass