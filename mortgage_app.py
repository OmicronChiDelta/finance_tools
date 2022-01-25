# myapp.py
#hello

import sys
if "E:\\mortgage" not in sys.path:
    sys.path.append("E:\\mortgage")
from utils import calc_min_payment, calc_balance

from bokeh.models import Slider
from bokeh.layouts import column
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc

#Plot area and styling
p = figure(x_range=(0, 100), y_range=(0, 100), toolbar_location=None)

#Variables
slide_r    = Slider(start=1,      end=7,      value=1.04,   step=0.01, title="Interest rate")
slide_term = Slider(start=10,     end=40,     value=30,     step=1, title="Mortgage term")
slide_fix  = Slider(start=0,      end=10,     value=5,      step=1, title="Fixed-term length")
slide_p    = Slider(start=100000, end=500000, value=208499, step=1, title="Principal")

i = 0

ds = r.data_source

# create a callback that adds a number in a random location
def callback():
    global i

    # BEST PRACTICE --- update .data in one step with a new dict
    new_data = dict()
    new_data['x'] = ds.data['x'] + [random()*70 + 15]
    new_data['y'] = ds.data['y'] + [random()*70 + 15]
    new_data['text_color'] = ds.data['text_color'] + [RdYlBu3[i%3]]
    new_data['text'] = ds.data['text'] + [str(i)]
    ds.data = new_data

    i = i + 1

slide_r.on_change(callback)
slide_term.on_change(callback)
slide_fix.on_change(callback)
slide_p.on_change(callback)

# put sliders and plot in a layout and add to the document
curdoc().add_root(column(p, slide_r, slide_term, slide_fix, slide_p))