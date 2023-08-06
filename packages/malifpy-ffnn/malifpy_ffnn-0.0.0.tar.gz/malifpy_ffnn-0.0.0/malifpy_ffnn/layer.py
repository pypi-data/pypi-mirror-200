from typing import Callable
from .activation_function import SoftMax


class Layer:
    def get_activation_function(self) -> Callable[[float], float]:
        func : Callable[[float], float] = SoftMax().setup(sum_of_weighted_sum = 1)
        return func
