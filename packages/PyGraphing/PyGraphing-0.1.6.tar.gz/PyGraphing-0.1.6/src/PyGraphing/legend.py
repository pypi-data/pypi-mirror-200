from PySVG.SVG import SVG, Section
from PySVG.Draw import Rect
from PySVG import Text
from .icon import Icon


class Item(Section):
    def __init__(self, icon: Icon = None, name: Text = None):
        super().__init__(0, 0)

        self.w = 0
        self.h = icon.h + 5

        self.left = 0
        self.right = 0
        self.middle = 0

        self.icon = icon

        self.text = name

        self.background = Rect(0, 0, self.w, self.h)
        self.background.active = False

    def fit_width(self):
        text_width = self.text.font.getTextWidth(self.text.text)
        self.w = self.icon.w + self.left + self.middle + self.right + text_width
        return self.w

    def construct(self):
        if self.background.active:
            self.background.w = self.w
            self.background.h = self.h
            self.add_child(self.background)

        if self.icon is not None:
            if self.icon.active:
                self.add_child(self.icon)

        if self.text is not None:
            if self.text.active:
                self.add_child(self.text)

        return super().construct()


class NormalItem(Item):
    def __init__(self, icon: Icon, text: Text):
        super().__init__(icon, text)

    def _set(self):
        self.icon.x = self.left
        self.icon.y = self.h / 2 - self.icon.h / 2

        self.text.x = self.left + self.middle + self.icon.w
        self.text.y = self.h / 2

        self.text.baseline = 'central'
        self.text.anchor = 'start'

    def construct(self):
        self._set()

        return super().construct()


class Legend(SVG):
    def __init__(self, text: Text):
        super().__init__(0, 0)
        self.text = text
        self.distance = 5

        self.x = 0
        self.y = 0

        self.items = []

        self.background = Rect()
        self.background.active = False

    def add_item(self, name: str, shape: Icon):
        text = self.text.copy()
        text.text = name

        self.items.append(NormalItem(shape, text))

    def xywh(self, x, y, w, h):
        self.x = x
        self.y = y
        self.size = (w, h)

    def construct(self):
        if self.x == 0 and self.y == 0:
            return super().construct()

        svg = super().construct()

        return f'<g transform="translate({self.x} {self.y})>\n   {svg}\n</g>'


class VLegend(Legend):
    def __init__(self, text: Text):
        super().__init__(text)

        self.y0 = 0

    def _set(self):
        w, h = self.size
        y = self.y0
        for item in self.items:
            item.x = 0
            item.y = y
            item.w = w

            y += item.h + self.distance

            self.add_child(item)

    def construct(self):
        self.add_child(self.background)
        self._set()

        return super().construct()


class HLegend(Legend):
    def justify(self):
        w, _ = self.size
        widths = [item.fit_width() for item in self.items]
        self.distance = (w - sum(widths)) / (len(widths) - 1)

    def _set(self):
        w, h = self.size
        x = 0

        for item in self.items:
            item.x = x
            item.y = h / 2
            item.fit_width()

            x += item.w + self.distance

            self.add_child(item, 'child')

    def construct(self):
        self.add_child(self.background)
        self._set()

        return super().construct()
