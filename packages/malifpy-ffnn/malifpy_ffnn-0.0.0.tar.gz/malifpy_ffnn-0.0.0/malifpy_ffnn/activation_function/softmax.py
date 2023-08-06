from __future__ import annotations
from .activation_function import ActivationFunction

class SoftMax(ActivationFunction):
    def __init__(self) -> None:
        self.sum_of_weighted_sum: float

    def setup(self, **kwargs) -> SoftMax:
        self.sum_of_weighted_sum = kwargs["sum_of_weighted_sum"]
        return self

    def __call__(self, weighted_input):
        return weighted_input / self.sum_of_weighted_sum

