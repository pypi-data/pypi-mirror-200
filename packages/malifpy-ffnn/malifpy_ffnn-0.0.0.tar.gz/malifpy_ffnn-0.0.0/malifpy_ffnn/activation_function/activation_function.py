from __future__ import annotations

from abc import ABC, abstractmethod


class ActivationFunction(ABC):
    @abstractmethod
    def setup(self, **kwargs) -> None:
        pass

    @abstractmethod
    def __call__(self, weighted_input):
        pass
