from manim import *

from PIL import Image
import numpy as np

class NeuralNetworkScene(ThreeDScene):
    """Test Scene for the Neural Network"""

    def construct(self):
        # Make the Layer object
        image = Image.open("../assets/mnist/digit.jpeg")
        numpy_image = np.asarray(image)

        square = Square().shift([0.0, 2.5, 0.0])
        self.add(square)

        image_mobject = ImageMobject(
            numpy_image, 
            image_mode="RGB"
        ).scale(10)

        self.add(image_mobject)
        self.play(
            self.camera._frame_center.animate.shift(
                np.array([3.0, 0.0, 0])
            )
        )