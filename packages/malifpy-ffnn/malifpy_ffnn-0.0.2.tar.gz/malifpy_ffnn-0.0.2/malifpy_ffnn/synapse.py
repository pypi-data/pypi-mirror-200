from __future__ import annotations
import malifpy_ffnn.neuron

class Synapse:
    def __init__(
            self, 
            neuron_from: malifpy_ffnn.neuron.Neuron, 
            neuron_to: malifpy_ffnn.neuron.Neuron, 
            weight: float = 0,
            synapse_name: str = ""
        ) -> None:
        self.name : str = synapse_name
        self.weight : float = weight
        self.neuron_from : malifpy_ffnn.neuron.Neuron = neuron_from
        self.neuron_to : malifpy_ffnn.neuron.Neuron = neuron_to
