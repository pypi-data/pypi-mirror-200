from PySVG.Draw import Rect
from PySVG import Section
from ..plot import Plot


class Bar(Rect):
    def __init__(self, ancestor: Rect):
        super().__init__(0, 0, 0, 0)
        self.inherit(ancestor)

        self.index = 0
        self.group = 0
        self.value = 0
        self.name = ''


class Bars(Section):
    def __init__(self, parent: Plot, n_groups, n_bars):
        super().__init__(0, 0)
        self.bars = []
        self.plot = parent

        self.bar_ratio = 0.05
        self.group_ratio = 0.5

        self.n_groups = n_groups
        self.n_bars = n_bars

        self._bw = 0
        self._gw = 0
        self._bs = 0
        self._gs = 0

    def _bar_dict(self):
        d = {}
        for i in range(self.n_groups):
            for j in range(self.n_bars):
                b = [bar for bar in self.bars if bar.group == i and bar.index == j]
                if b:
                    d[(i, j)] = b[0]
                else:
                    d[(i, j)] = None

        return d

    def _dimensions(self):
        w = self.plot.xmax - self.plot.xmin

        total_group_width = w * (1 - self.group_ratio)
        group_width = total_group_width / self.n_groups
        group_space = w * self.group_ratio / (self.n_groups + 1)

        bar_width = group_width * (1 - self.bar_ratio) / self.n_bars
        bar_space = group_width * self.bar_ratio / (self.n_bars - 1)

        self._bw = bar_width
        self._bs = bar_space
        self._gw = group_width
        self._gs = group_space

        self._rects()

    def _rects(self):
        x = 0
        bars = self._bar_dict()
        for i in range(self.n_groups):
            x = i + 1 - self._gw / 2
            for j in range(self.n_bars):
                bar = bars[(i, j)]
                if bar:
                    self._set_xywh(bar, x)
                    self.add_child(bar)

                x += self._bw + self._bs
            x -= self._bs

    def _set_xywh(self, bar, x):
        exes = [x, x + self._bw]
        whys = [bar.value, 0]

        x = self.plot.cart2pixel_x(exes)
        w = abs(x[0] - x[1])
        y = self.plot.cart2pixel_y(whys)
        h = abs(y[0] - y[1])

        bar.x, bar.y, bar.w, bar.h = min(x), min(y), w, h

    def construct(self):
        self._dimensions()

        return super().construct()
