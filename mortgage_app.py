#https://stackoverflow.com/questions/41926478/python-bokeh-send-additional-parameters-to-widget-event-handler
#https://stackoverflow.com/questions/65300681/clarification-on-bokehs-callback


import sys
if "E:\\finance_tools" not in sys.path:
    sys.path.append("E:\\finance_tools")
from utils import calc_min_payment, calc_balance

from bokeh.models import Slider, ColumnDataSource
from bokeh.layouts import column
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc



#%%
#Variables
max_term = 40
max_p = 500000

#Plot area and styling
p = figure(x_range=(0, max_term), y_range=(0, max_p), toolbar_location=None)

slide_r    = Slider(start=1,      end=7,        value=1.04,   step=0.01, title="Interest rate")
slide_term = Slider(start=10,     end=max_term, value=30,     step=1,    title="Mortgage term")
slide_fix  = Slider(start=0,      end=10,       value=5,      step=1,    title="Fixed-term length")
slide_p    = Slider(start=100000, end=max_p,    value=208499, step=1,    title="Principal")

#Compute graphic from defaults
m = calc_min_payment(slide_p.value, slide_r.value, slide_term.value)
month_ids = [i for i in range(12*slide_term.value)]
frac_years = [i/12 for i in month_ids]
t_min = [calc_balance(slide_p.value, slide_r.value, j, m) for j in month_ids]

#Insert data into CDS
source = ColumnDataSource(data={'x':frac_years, 'y':t_min}) 

#Configure plot
trajectory = p.line(x='x', y='y', line_width=2, source=source)
ds = trajectory.data_source



#%%Callback to recalculate repayment trajectory
def callback(attr, old, new):
        
    m = calc_min_payment(208499, new, 30)
    
    month_ids = [i for i in range(12*30)]
    frac_years = [i/12 for i in month_ids]
    
    #Minimal payment
    t_min = [calc_balance(208499, new, j, m) for j in month_ids]
    
    #Populate dictionary behind CDS with new data
    new_data = {'x':frac_years, 'y':t_min}
    ds.data = new_data



#%% Configure final plot
slide_r.on_change('value', callback)
#slide_term.on_change('value', callback)
#slide_fix.on_change('value', callback)
#slide_p.on_change('value', callback)

# put sliders and plot in a layout and add to the document
curdoc().add_root(column(p, slide_r, slide_term, slide_fix, slide_p))