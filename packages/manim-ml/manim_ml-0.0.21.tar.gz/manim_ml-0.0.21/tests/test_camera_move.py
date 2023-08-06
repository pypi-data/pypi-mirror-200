from manim import *
from manim_ml.neural_network.layers.convolutional_2d import Convolutional2DLayer
from manim_ml.neural_network.layers.feed_forward import FeedForwardLayer
from manim_ml.neural_network.layers.image import ImageLayer
from manim_ml.neural_network.neural_network import NeuralNetwork
from PIL import Image
from manim_ml.utils.mobjects.image import GrayscaleImageMobject
import numpy as np

# Make the specific scene
config.pixel_height = 1200
config.pixel_width = 1900
config.frame_height = 6.0
config.frame_width = 6.0

class CustomCamera(ThreeDCamera):

    def __init__(
        self,
        frame=None,
        fixed_dimension=0,
        default_frame_stroke_color=WHITE,
        default_frame_stroke_width=0,
        **kwargs,
    ):
        """
        Frame is a Mobject, (should almost certainly be a rectangle)
        determining which region of space the camera displays
        """
        self.fixed_dimension = fixed_dimension
        self.default_frame_stroke_color = default_frame_stroke_color
        self.default_frame_stroke_width = default_frame_stroke_width
        if frame is None:
            frame = ScreenRectangle(height=config["frame_height"])
            frame.set_stroke(
                self.default_frame_stroke_color,
                self.default_frame_stroke_width,
            )
        self.frame = frame
        super().__init__(**kwargs)

    # TODO, make these work for a rotated frame
    @property
    def frame_height(self):
        """Returns the height of the frame.

        Returns
        -------
        float
            The height of the frame.
        """
        return self.frame.height

    @property
    def frame_width(self):
        """Returns the width of the frame

        Returns
        -------
        float
            The width of the frame.
        """
        return self.frame.width

    @property
    def frame_center(self):
        """Returns the centerpoint of the frame in cartesian coordinates.

        Returns
        -------
        np.array
            The cartesian coordinates of the center of the frame.
        """
        return self.frame.get_center()

    @frame_height.setter
    def frame_height(self, frame_height: float):
        """Sets the height of the frame in MUnits.

        Parameters
        ----------
        frame_height
            The new frame_height.
        """
        self.frame.stretch_to_fit_height(frame_height)

    @frame_width.setter
    def frame_width(self, frame_width: float):
        """Sets the width of the frame in MUnits.

        Parameters
        ----------
        frame_width
            The new frame_width.
        """
        self.frame.stretch_to_fit_width(frame_width)

    @frame_center.setter
    def frame_center(self, frame_center: np.ndarray | list | tuple | Mobject):
        """Sets the centerpoint of the frame.

        Parameters
        ----------
        frame_center
            The point to which the frame must be moved.
            If is of type mobject, the frame will be moved to
            the center of that mobject.
        """
        self.frame.move_to(frame_center)

    def capture_mobjects(self, mobjects, **kwargs):
        # self.reset_frame_center()
        # self.realign_frame_shape()
        super().capture_mobjects(mobjects, **kwargs)


    # Since the frame can be moving around, the cairo
    # context used for updating should be regenerated
    # at each frame.  So no caching.
    def get_cached_cairo_context(self, pixel_array):
        """
        Since the frame can be moving around, the cairo
        context used for updating should be regenerated
        at each frame.  So no caching.
        """
        return None


    def cache_cairo_context(self, pixel_array, ctx):
        """
        Since the frame can be moving around, the cairo
        context used for updating should be regenerated
        at each frame.  So no caching.
        """
        pass

    def get_mobjects_indicating_movement(self):
        """
        Returns all mobjects whose movement implies that the camera
        should think of all other mobjects on the screen as moving

        Returns
        -------
        list
        """
        return [self.frame]

    def auto_zoom(
        self,
        mobjects: list[Mobject],
        margin: float = 0,
        only_mobjects_in_frame: bool = False,
        animate: bool = True,
    ):
        """Zooms on to a given array of mobjects (or a singular mobject)
        and automatically resizes to frame all the mobjects.

        .. NOTE::

            This method only works when 2D-objects in the XY-plane are considered, it
            will not work correctly when the camera has been rotated.

        Parameters
        ----------
        mobjects
            The mobject or array of mobjects that the camera will focus on.

        margin
            The width of the margin that is added to the frame (optional, 0 by default).

        only_mobjects_in_frame
            If set to ``True``, only allows focusing on mobjects that are already in frame.

        animate
            If set to ``False``, applies the changes instead of returning the corresponding animation

        Returns
        -------
        Union[_AnimationBuilder, ScreenRectangle]
            _AnimationBuilder that zooms the camera view to a given list of mobjects
            or ScreenRectangle with position and size updated to zoomed position.

        """
        scene_critical_x_left = None
        scene_critical_x_right = None
        scene_critical_y_up = None
        scene_critical_y_down = None

        for m in mobjects:
            if (m == self.frame) or (
                only_mobjects_in_frame and not self.is_in_frame(m)
            ):
                # detected camera frame, should not be used to calculate final position of camera
                continue

            # initialize scene critical points with first mobjects critical points
            if scene_critical_x_left is None:
                scene_critical_x_left = m.get_critical_point(LEFT)[0]
                scene_critical_x_right = m.get_critical_point(RIGHT)[0]
                scene_critical_y_up = m.get_critical_point(UP)[1]
                scene_critical_y_down = m.get_critical_point(DOWN)[1]

            else:
                if m.get_critical_point(LEFT)[0] < scene_critical_x_left:
                    scene_critical_x_left = m.get_critical_point(LEFT)[0]

                if m.get_critical_point(RIGHT)[0] > scene_critical_x_right:
                    scene_critical_x_right = m.get_critical_point(RIGHT)[0]

                if m.get_critical_point(UP)[1] > scene_critical_y_up:
                    scene_critical_y_up = m.get_critical_point(UP)[1]

                if m.get_critical_point(DOWN)[1] < scene_critical_y_down:
                    scene_critical_y_down = m.get_critical_point(DOWN)[1]

        # calculate center x and y
        x = (scene_critical_x_left + scene_critical_x_right) / 2
        y = (scene_critical_y_up + scene_critical_y_down) / 2

        # calculate proposed width and height of zoomed scene
        new_width = abs(scene_critical_x_left - scene_critical_x_right)
        new_height = abs(scene_critical_y_up - scene_critical_y_down)

        m_target = self.frame.animate if animate else self.frame
        # zoom to fit all mobjects along the side that has the largest size
        if new_width / self.frame.width > new_height / self.frame.height:
            return m_target.set_x(x).set_y(y).set(width=new_width + margin)
        else:
            return m_target.set_x(x).set_y(y).set(height=new_height + margin)

class NeuralNetworkScene(ThreeDScene):
    """Test Scene for the Neural Network"""

    def __init__(self):
        super().__init__()# camera_class=CustomCamera)

    def make_camera_follow_forward_pass(self, neural_network, buffer=1.0):
        per_layer_animations = neural_network.make_forward_pass_animation(
            per_layer_animations=True
        )
        all_layers = neural_network.all_layers
        # Compute the width and height of the frame
        """
        max_width = 0
        max_height = 0
        for layer_index in range(1, len(all_layers) - 1):
            prev_layer = all_layers[layer_index - 1]
            current_layer = all_layers[layer_index]
            next_layer = all_layers[layer_index + 1]
            group = Group(prev_layer, current_layer, next_layer)

            max_width = max(max_width, group.width)
            max_height = max(max_height, group.height)

        frame_width = max_width * (1 + buffer)
        frame_height = max_height * (1 + buffer)
        """
        animations = []
        # Start off zoomed into first section
        print(all_layers[0])
        """
        animations.append(
            FadeIn(
                Dot(
                    all_layers[0].get_center()
                )
            )
        )
        """
        animations.append(
            Group(*self.mobjects).animate.shift(
                ORIGIN - all_layers[0].get_center(),
            ),
        )
        print(all_layers[0].get_center())
        """
        zoom_animation = AnimationGroup(
            self.camera.auto_zoom(
                [
                    all_layers[0],
                ],
                margin=buffer,
            ).build(),
            run_time=5.0,
        )
        """
        #animations.append(zoom_animation)
        forward_pass_animation = per_layer_animations[all_layers[0]]
        print(per_layer_animations)
        animations.append(
            forward_pass_animation
        )
        # Go through each animation
        for layer_index in range(1, len(all_layers) - 1):
            prev_layer = all_layers[layer_index - 1]
            current_layer = all_layers[layer_index]
            next_layer = all_layers[layer_index + 1]
            # Get the current layer animation
            layer_animation = per_layer_animations[prev_layer]
            # Zoom in on a group
            """
            zoom_animation = AnimationGroup(
                self.camera.auto_zoom(
                    [
                        prev_layer, 
                        current_layer,
                        next_layer
                    ],
                    margin=buffer,
                ).build(),
                run_time=5.0,
            )
            """
            animations.append(
                Group(*self.mobjects).animate.shift(
                    ORIGIN - current_layer.get_center(),
                    run_time=5.0
                )
            )
            # animations.append(zoom_animation)
            # Now add the actual layer animation
            animations.append(layer_animation)
        return Succession(
            *animations,
            lag_ratio=1.0
        )


    def construct(self):
        # Make the Layer object
        image = Image.open("../assets/mnist/digit.jpeg")
        numpy_image = np.asarray(image)
        layer_dict = {
            "image1": ImageLayer(numpy_image, height=1.5),
            "conv1": Convolutional2DLayer(1, 7, filter_spacing=0.32),
            "conv2": Convolutional2DLayer(3, 5, 3, filter_spacing=0.32),
            "conv3": Convolutional2DLayer(5, 3, 3, filter_spacing=0.18),
            "feed1": FeedForwardLayer(3),
            "feed2": FeedForwardLayer(3),
        }
        nn = NeuralNetwork(
            layer_dict,
            layer_spacing=0.25,
            debug_mode=True
        )
        # Make Animation
        self.add(nn)
        # self.play(Create(nn))
        self.add(Dot(nn.all_layers[0].get_center(), z_index=20))
        # self.camera.frame_center = nn.all_layers[0].get_center()
        # print(self.camera.frame.get_center())
        """
        self.play(
            self.camera.frame.animate.move_to(
                nn.all_layers[0].get_center()
            )
        )
        """
        # print(self.mobjects)
        # self.play(Group(*self.mobjects).animate.shift(RIGHT))
        # print(self.camera._frame_center.get_center())
        image_mobject = ImageMobject(
            numpy_image, 
            image_mode="RGB"
        )
        self.add(image_mobject)
        self.play(
            self.camera._frame_center.animate.shift(
                np.array([0.2, 0.0, 0])
            )
        )
        """
        self.camera.frame_center = np.array([-0.5, 0, 0])
        """
        """
        self.begin_ambient_camera_rotation(rate=0.2, about="phi")
        self.wait(5)
        self.stop_ambient_camera_rotation()
        """
        """
        self.move_camera(
            frame_center=np.array([-3, 0, 0])
        )
        self.play(
            nn.make_forward_pass_animation(),
            run_time=10
        )
        self.play(
            self.make_camera_follow_forward_pass(nn),
            run_time=10
        )
        """
