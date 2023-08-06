from PySVG.Draw import Generic_Path
from PySVG import Section


class OneWay(Section):
    def __init__(self, parent, x: list, y: list, r: list):
        super().__init__(0, 0)
        self.plot = parent
        self.line = Generic_Path()
        self.width = 0.8

        self.exes = x
        self.whys = y
        self.err = [y[i] + r[i] for i in range(len(y))]

    def _process(self):
        w = self.plot.cart2pixel_x([self.width])[0]
        x = self.plot.cart2pixel_x(self.exes)
        y = self.plot.cart2pixel_y(self.whys)
        r = self.plot.cart2pixel_y(self.err)

        bars = []

        for i in range(len(x)):
            bar = [('M', x[i] - w / 2, r[i]),
                   ('L', x[i] + w / 2, r[i]),
                   ('M', x[i], y[i]),
                   ('L', x[i], r[i])]
            bars += bar

        self.line.points = bars
        self.add_child(self.line)

    def construct(self):
        self._process()
        return super().construct()


class TwoWay(Section):
    def __init__(self, parent, x: list, y: list, r: list):
        super().__init__(0, 0)
        self.plot = parent
        self.line = Generic_Path()
        self.width = 0.8

        self.exes = x
        self.whys = y
        self.err = r

    def _process(self):
        w = self.plot.cart2pixel_x([self.width])[0]
        x = self.plot.cart2pixel_x(self.exes)
        y = self.plot.cart2pixel_y(self.whys)
        r1 = self.plot.cart2pixel_y([self.whys[i] + self.err[i] for i in range(len(y))])
        r2 = self.plot.cart2pixel_y([self.whys[i] - self.err[i] for i in range(len(y))])

        bars = []

        for i in range(len(x)):
            bar = [('M', x[i] - w / 2, r1[i]),
                   ('L', x[i] + w / 2, r1[i]),
                   ('M', x[i] - w / 2, r2[i]),
                   ('L', x[i] + w / 2, r2[i]),
                   ('M', x[i], r1[i]),
                   ('L', x[i], r2[i])]
            bars += bar

        self.line.points = bars
        self.add_child(self.line)

    def construct(self):
        self._process()
        return super().construct()


class Individual(Generic_Path):
    def __init__(self, parent, x, y, r):
        super().__init__()
        self.plot = parent
        self.width = 0.8

        self.exes = x
        self.whys = y
        self.err = y + r

    def _process(self):
        w = self.plot.cart2pixel_x([self.width])[0]
        x = self.plot.cart2pixel_x([self.exes])[0]
        y = self.plot.cart2pixel_y([self.whys])[0]
        r = self.plot.cart2pixel_y([self.err])[0]

        self.points = [('M', x - w, r), ('L', x + w, r), ('M', x, y), ('L', x, r)]

    def construct(self):
        self._process()
        return super().construct()
