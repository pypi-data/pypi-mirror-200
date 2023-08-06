from PyGraphing.legend_alone import Legend, NormalItem, Icon, Rect
from PySVG import Text, Font

f = Font('Arial', 12, '700')
t = Text()
t.font = f
t.fill = (0, 0, 0)
t.fill_opacity = 1

svg = Legend(t)
svg.size = 140, 700
svg.y0 = 85
svg.background.fill = (15, 15, 200)
svg.background.fill_opacity = 0


def icon(color):
    rect = Rect('10%', '10%', '80%', '80%')
    rect.fill = color
    rect.fill_opacity = 1

    return Icon(rect, 15, 15)


def item(name, color):
    text = t.copy()
    text.text = name

    i = NormalItem(icon(color), text)
    i.middle = 10
    i.angle = -60

    i.w = 80
    i.h = 100

    i.xc = 50
    i.yc = 50

    return i


biotage = item('Biotage SLE - DE', (9, 151, 214))
phenomenex_de = item('Phenomenex SLE - DE', (7, 216, 121))
phenomenex_synth = item('Phenomenex SLE - Synth.', (89, 246, 246))
thermo = item('Thermo SLE - Synth.', (121, 21, 142))
validated = item('Validated Method', (218, 7, 158))

svg.items = [biotage, phenomenex_de, phenomenex_synth, thermo, validated]

with open('test.svg', 'w') as file:
    file.write(svg.construct())
