import numpy as np

shape_s = np.array(
    [[[0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0],
      [0, 0, 1, 1, 0],
      [0, 1, 1, 0, 0],
      [0, 0, 0, 0, 0]],
     [[0, 0, 0, 0, 0],
      [0, 0, 1, 0, 0],
      [0, 0, 1, 1, 0],
      [0, 0, 0, 1, 0],
      [0, 0, 0, 0, 0]]], dtype=np.int32)

shape_z = np.array(
    [[[0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0],
      [0, 1, 1, 0, 0],
      [0, 0, 1, 1, 0],
      [0, 0, 0, 0, 0]],
     [[0, 0, 0, 0, 0],
      [0, 0, 1, 0, 0],
      [0, 1, 1, 0, 0],
      [0, 1, 0, 0, 0],
      [0, 0, 0, 0, 0]]], dtype=np.int32)

shape_i = np.array(
    [[[0, 0, 1, 0, 0],
      [0, 0, 1, 0, 0],
      [0, 0, 1, 0, 0],
      [0, 0, 1, 0, 0],
      [0, 0, 0, 0, 0]],
     [[0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0],
      [1, 1, 1, 1, 0],
      [0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0]]], dtype=np.int32)

shape_o = np.array(
    [[[0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0],
      [0, 1, 1, 0, 0],
      [0, 1, 1, 0, 0],
      [0, 0, 0, 0, 0]]], dtype=np.int32)

shape_j = np.array(
    [[[0, 0, 0, 0, 0],
      [0, 1, 0, 0, 0],
      [0, 1, 1, 1, 0],
      [0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0]],
     [[0, 0, 0, 0, 0],
      [0, 0, 1, 1, 0],
      [0, 0, 1, 0, 0],
      [0, 0, 1, 0, 0],
      [0, 0, 0, 0, 0]],
     [[0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0],
      [0, 1, 1, 1, 0],
      [0, 0, 0, 1, 0],
      [0, 0, 0, 0, 0]],
     [[0, 0, 0, 0, 0],
      [0, 0, 1, 0, 0],
      [0, 0, 1, 0, 0],
      [0, 1, 1, 0, 0],
      [0, 0, 0, 0, 0]]], dtype=np.int32)

shape_l = np.array(
    [[[0, 0, 0, 0, 0],
      [0, 0, 0, 1, 0],
      [0, 1, 1, 1, 0],
      [0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0]],
     [[0, 0, 0, 0, 0],
      [0, 0, 1, 0, 0],
      [0, 0, 1, 0, 0],
      [0, 0, 1, 1, 0],
      [0, 0, 0, 0, 0]],
     [[0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0],
      [0, 1, 1, 1, 0],
      [0, 1, 0, 0, 0],
      [0, 0, 0, 0, 0]],
     [[0, 0, 0, 0, 0],
      [0, 1, 1, 0, 0],
      [0, 0, 1, 0, 0],
      [0, 0, 1, 0, 0],
      [0, 0, 0, 0, 0]]], dtype=np.int32)

shape_t = np.array(
    [[[0, 0, 0, 0, 0],
      [0, 0, 1, 0, 0],
      [0, 1, 1, 1, 0],
      [0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0]],
     [[0, 0, 0, 0, 0],
      [0, 0, 1, 0, 0],
      [0, 0, 1, 1, 0],
      [0, 0, 1, 0, 0],
      [0, 0, 0, 0, 0]],
     [[0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0],
      [0, 1, 1, 1, 0],
      [0, 0, 1, 0, 0],
      [0, 0, 0, 0, 0]],
     [[0, 0, 0, 0, 0],
      [0, 0, 1, 0, 0],
      [0, 1, 1, 0, 0],
      [0, 0, 1, 0, 0],
      [0, 0, 0, 0, 0]]], dtype=np.int32)

shapes = np.array([shape_s, shape_z, shape_i, shape_o, shape_j, shape_l, shape_t], dtype=object)
shapes_color = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


class Shape:
    def __init__(self):
        # x is close to center: int [5, 7)
        self.x = np.random.randint(5, 7)
        # y is on top
        self.y = 0
        self.rotation = 0

        seed = np.random.randint(0, shapes.shape[0] + 1)

        self.shape = shapes[seed]
        self.color = shapes_color[seed]

    def get_shape(self):
        # returns current shape
        return self.shape[self.rotation].copy()

    def get_rotated(self):
        # returns rotated shape but does not rotate it
        rotation = self.rotation + 1
        if rotation == self.shape.shape[3]:
            rotation = 0
        return self.shape[rotation].copy()

    def rotate(self):
        # rotates the shape
        self.rotation += 1
        if self.rotation == self.shape.shape[3]:
            self.rotation = 0
