from __future__ import annotations
from typing import List

from .layer import Layer

class FeedForwardNeuralNetwork:
    def __init__(self, totalLayers: int) -> None:
        self.totalLayers = totalLayers
        self.layers: List[Layer] = []
    
    def add_layer(
            self, 
            activation_function: str, 
            totalNeurons: int, 
            weight_dim: List[int], 
            weight: List[float]
        ):
        self.layers.append(
                Layer(
                    activation_function,
                    totalNeurons,
                    weight_dim,
                    weight
                )
            )
