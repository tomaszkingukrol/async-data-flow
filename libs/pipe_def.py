from abc import ABC, abstractmethod


class PipeExecutor(ABC):
    @abstractmethod
    def run(self, pipe: tuple, **kwargs):
        pass


class PipeInspector(ABC):
    @abstractmethod
    def check_pipe_args(self, pipe: tuple) -> set:
        pass