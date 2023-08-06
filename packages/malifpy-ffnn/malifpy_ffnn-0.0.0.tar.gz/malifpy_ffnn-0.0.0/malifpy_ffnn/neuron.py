from __future__ import annotations
from typing import List, Union

from .synapse import Synapse
from .layer import Layer


class Neuron:
    def __init__(self) -> None:
        self.name : str = ""
        self.output : Union[float, None] = None
        self.weighted_sum: Union[float, None] = None
        self.synapse_in  : List[Synapse] = []
        self.synapse_out : List[Synapse] = []
        self.layer : Layer

    def get_output(self) -> float:
        if self.output == None:
            self.output = self.layer.get_activation_function()(self.get_weighted_sum())
        return self.output

    def get_weighted_sum(self) -> float:
        if self.weighted_sum == None:
            self.weighted_sum = 0
            for synapse in self.synapse_in:
                self.weighted_sum += synapse.neuron_from.get_output() * synapse.weight
        return self.weighted_sum

    def connect_from(self, neuron_arg: Neuron) -> None:
        """
        Menghubungkan Neuron argumen **KE** Neuron ini.
        """
        new_synapse : Synapse = Synapse(neuron_arg, self)
        self.add_synapse_in(new_synapse)
        neuron_arg.add_synapse_out(new_synapse)

    def add_synapse_in(self, s: Synapse) -> None:
        """
        Memasukkan Synapse ke synapse_in
        """
        self.synapse_in.append(s)

    def connect_to(self, neuron_arg: Neuron) -> None:
        """
        Menghubungkan Neuron ini ke **KE** Neuron argumen.
        """
        new_synapse : Synapse = Synapse(neuron_arg, self)
        self.add_synapse_in(new_synapse)
        neuron_arg.add_synapse_out(new_synapse)

    def add_synapse_out(self, s: Synapse) -> None:
        """
        Memasukkan Synapse ke synapse_out
        """
        self.synapse_out.append(s)
