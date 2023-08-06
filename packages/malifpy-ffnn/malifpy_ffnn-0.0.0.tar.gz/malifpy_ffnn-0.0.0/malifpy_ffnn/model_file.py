import re
from typing import Union

from .feed_forward_neural_network import FeedForwardNeuralNetwork

class FFNNModelFile:
    def __init__(self, model_file: str):
        self.model_file: str = model_file
        self.model: Union[None, FeedForwardNeuralNetwork] = None

        # Regexes
        self.re_totalLayers = r"totalLayers (\d+)"
        self.re_layer = r"(\s{4})\[\n([\s\w]+)\n(\1)\]"

    def load_file(self):
        # Load from self.model_file
        with open(self.model_file, "r") as model_file:
            model_txt: str = model_file.read()
            totalLayersNum = re.findall(self.re_totalLayers, model_txt)[0];
            print(totalLayersNum)
            layers = re.finditer(self.re_layer, model_txt)
            for idx, layer in enumerate(layers):
                print(f"Layer {idx}")
                print(layer[2])

if __name__ == "__main__":
    mf = FFNNModelFile("test/s1.txt")
    mf.load_file()
