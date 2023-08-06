from manim import *
from manim_ml.neural_network.layers.feed_forward import FeedForwardLayer
from manim_ml.neural_network.neural_network import NeuralNetwork

import manim_ml

print(manim_ml.config.color_scheme)

class NeuralNetworkScene(Scene):
    def construct(self):
        layers = [FeedForwardLayer(3), FeedForwardLayer(5), FeedForwardLayer(3)]
        nn = NeuralNetwork(layers)
        self.add(nn)
        nn.move_to(ORIGIN)
        nn.scale(2)
        forward_propagation_animation = nn.make_forward_pass_animation(
            run_time=5, passing_flash=True
        )
        self.play(forward_propagation_animation)