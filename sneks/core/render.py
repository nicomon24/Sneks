'''
    Rendering object of multigridworld. Receives a map from gridworld and
    transform it into a visible image (applies colors and zoom)
'''

import gym
import numpy as np

class Renderer:

    def __init__(self, size, zoom_factor=1, object_colors={}):
        self.COLORS = {
            # Void
            0: (0,0,0),
            # Player
            100: (0, 255, 0),
            101: (0, 0, 255),
            102: (0, 255, 0),
            # Food
            1: (255, 0, 0)
        }
        for key, value in object_colors.items():
            self.COLORS[key] = value
        self.zoom_factor = zoom_factor
        self.size = size
        self.height = size[0]
        self.width = size[1]
        self.viewer = None

    def _get_image(self, state):
        # Transform to RGB image with 3 channels
        color_lu = np.vectorize(lambda x: self.COLORS[x], otypes=[np.uint8, np.uint8, np.uint8])
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

    def _render(self, state, mode='human', close=False):
        if close:
            if self.viewer is not None:
                self.viewer.close()
                self.viewer = None
            return
        img = self._get_image(state)
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
