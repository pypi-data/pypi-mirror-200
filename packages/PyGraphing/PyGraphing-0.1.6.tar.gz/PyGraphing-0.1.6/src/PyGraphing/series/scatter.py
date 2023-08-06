from PySVG import Section, Image
from PySVG.Draw import Rect, Generic_Path
from .box import Box
from ..accessories.bezier import path_points


class Scatter(Section):
    def __init__(self, plot, shape, x: list, y: list):
        super().__init__(0, 0)
        self.plot = plot
        self.shape = shape
        self.exes = x
        self.whys = y

    def _process(self):
        x = self.plot.cart2pixel_x(self.exes)
        y = self.plot.cart2pixel_y(self.whys)

        for i in range(len(x)):
            icon = self.shape.copy()
            icon.x = x[i] - icon.w / 2
            icon.y = y[i] - icon.h / 2

            self.add_child(icon)

    def construct(self):
        self._process()
        return super().construct()


class ScatterBoxes(Scatter):
    def __init__(self, plot, shape, x: list, y: list, err: list):
        super().__init__(plot, shape, x, y)
        self.rect = Rect()
        self.err = err

        self.width = 0.8

    def _process(self):
        x = self.exes
        y = self.whys
        e = self.err
        w = self.width / 2

        for i in range(len(x)):
            box = Box(self.plot, (x[i] - w, y[i] - e[i]), (x[i] + w, y[i] + e[i]))
            box.inherit(self.rect)
            self.add_child(box)

        super()._process()

    def construct(self):
        return super().construct()


class ScatterBezier(Scatter):
    def __init__(self, plot, shape, x: list, y: list):
        super().__init__(plot, shape, x, y)
        self.line = Generic_Path()

    def _process(self):
        x = self.plot.cart2pixel_x(self.exes)
        y = self.plot.cart2pixel_y(self.whys)

        self.line.points = path_points(x, y)
        self.add_child(self.line)

        for i in range(len(x)):
            icon = self.shape.copy()
            icon.x = x[i] - icon.w / 2
            icon.y = y[i] - icon.h / 2

            self.add_child(icon)

    def construct(self):
        self._process()
        return super(Scatter, self).construct()


class ScatterImage(Scatter):
    """
    Must Be careful that the image is exactly the dimensions of the plot. Will address later.
    """

    def __init__(self, plot, path, shape, x: list, y: list):
        super().__init__(plot, shape, x, y)
        self.image = Image(0, 0, path)

    def _process(self):
        x = self.plot.cart2pixel_x(self.exes)
        y = self.plot.cart2pixel_y(self.whys)

        self.add_child(self.image)

        for i in range(len(x)):
            icon = self.shape.copy()
            icon.x = x[i] - icon.w / 2
            icon.y = y[i] - icon.h / 2

            self.add_child(icon)

    def construct(self):
        self._process()
        return super(Scatter, self).construct()
