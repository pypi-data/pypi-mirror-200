from __future__ import annotations
from typing import Union

import malifpy_ffnn.feed_forward_neural_network as ffnn

class FFNNModelFile:
    def __init__(self, model_file: str) -> None:
        self.model_file: str = model_file
        self.load_file()

    def load_file(self) -> FFNNModelFile:
        # Load from self.model_file
        with open(self.model_file, "r") as model_file:
            model_txt: str = model_file.read()
            model_split = model_txt.split("\n\n")
            self.ffnn = ffnn.FeedForwardNeuralNetwork(int(model_split[0]))
            for line in model_split[1:]:
                arg_arr = line.splitlines()
                act_func = arg_arr[0]
                totalNeurons = int(arg_arr[1])
                weight_dim = [int(dim) for dim in arg_arr[2].split()]
                weight = [float(w) for w in arg_arr[2].split()]
                self.ffnn.add_layer(
                        act_func,
                        totalNeurons,
                        weight_dim,
                        weight
                    )
        return self

    def get_ffnn(self) -> ffnn.FeedForwardNeuralNetwork:
        return self.ffnn

if __name__ == "__main__":
    mf = FFNNModelFile("test/s2.txt")
    mf.load_file()
    for layer in mf.get_ffnn().layers:
        print(layer.activation_function)
        print(layer.total_neurons)
        print(layer.weight)
