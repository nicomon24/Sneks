'''
    Rendering object of Sneks. Receives a map from gridworld and
    transform it into a visible image (applies colors and zoom)
'''

import gym
import numpy as np

class SnekColor:

    def __init__(self, body_color, head_color):
        self.body_color = body_color
        self.head_color = head_color

'''
    This class translates the world state with block ids into an RGB image, with
    a selected zoom factor. This can be used to return an RGB observation or
    to render the world.
'''
class RGBifier:

    def __init__(self, size, zoom_factor=1, players_colors = {}):
        # Setting default colors
        self.pcolors = {
            0: SnekColor((0, 204, 0), (0, 77, 0)),
            1: SnekColor((0, 0, 204), (0, 0, 77)),
        }
        self.zoom_factor = zoom_factor
        self.size = size
        self.height = size[0]
        self.width = size[1]

    def get_color(self, state):
        # Void => BLACK
        if state == 0:
            return (0,0,0)
        # Wall => WHITE
        elif state == 255:
            return (255, 255, 255)
        # Food => RED
        elif state == 64:
            return (255, 0, 0)
        else:
            # Get player ID
            pid = (state - 100) // 2
            is_head = (state - 100) % 2
            # Checking that default color exists
            if pid not in self.pcolors.keys():
                pid = 0
            # Assign color (default or given)
            if is_head == 0:
                return self.pcolors[pid].body_color
            else:
                return self.pcolors[pid].head_color

    def get_image(self, state):
        # Transform to RGB image with 3 channels
        color_lu = np.vectorize(lambda x: self.get_color(x), otypes=[np.uint8, np.uint8, np.uint8])
        _img = np.array(color_lu(state))
        # Zoom every channel
        _img_zoomed = np.zeros((3, self.height * self.zoom_factor, self.width * self.zoom_factor), dtype=np.uint8)
        for c in range(3):
            for i in range(_img.shape[1]):
                for j in range(_img.shape[2]):
                        _img_zoomed[c, i*self.zoom_factor:i*self.zoom_factor+self.zoom_factor,
                                    j*self.zoom_factor:j*self.zoom_factor+self.zoom_factor] = np.full((self.zoom_factor, self.zoom_factor), _img[c,i,j])
        # Transpose to get channels as last
        _img_zoomed = np.transpose(_img_zoomed, [1,2,0])
        return _img_zoomed

'''
    This class specifically handles the renderer for the environment.
'''
class Renderer:

    def __init__(self, size, zoom_factor=1, players_colors={}):
        self.rgb = RGBifier(size, zoom_factor, players_colors)
        self.viewer = None

    def _render(self, state, mode='human', close=False):
        if close:
            if self.viewer is not None:
                self.viewer.close()
                self.viewer = None
            return
        img = self.rgb.get_image(state)
        if mode == 'rgb_array':
            return img
        elif mode == 'human':
            from gym.envs.classic_control import rendering
            if self.viewer is None:
                self.viewer = rendering.SimpleImageViewer()
            self.viewer.imshow(img)
            return self.viewer.isopen

    def close(self):
        if self.viewer is not None:
            self.viewer.close()
            self.viewer = None
