from __future__ import annotations

class Synapse:
    def __init__(
            self, 
            neuron_from: Neuron, 
            neuron_to: Neuron, 
            weight: float = 0,
            synapse_name: str = ""
        ) -> None:
        self.name : str = synapse_name
        self.weight : float = weight
        self.neuron_from : Neuron = neuron_from
        self.neuron_to : Neuron = neuron_to
