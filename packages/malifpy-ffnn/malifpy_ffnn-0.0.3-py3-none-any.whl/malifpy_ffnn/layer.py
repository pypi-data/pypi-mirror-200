from __future__ import annotations
from typing import Callable, List
import malifpy_ffnn.activation_function as act_fun


class Layer:
    def __init__(
            self, 
            activation_function: str,
            totalNeurons: int,
            weight_dim: List[int],
            weight: List[float]
            ) -> None:
        self.neurons: List[Neuron] = []
        self.activation_function = activation_function
        self.total_neurons = totalNeurons
        self.weight_dim = weight_dim
        self.weight = weight

    def get_activation_function(self) -> Callable[..., float]:
        def act_func(f):
            return act_fun.softMax(f, self.get_sum_of_weighted_sum())
        return act_func

    def get_sum_of_weighted_sum(self):
        sum_ = 0
        for neuron in self.neurons:
            sum_ += neuron.get_weighted_sum()
        return sum_
