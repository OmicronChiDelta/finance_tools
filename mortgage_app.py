#https://stackoverflow.com/questions/41926478/python-bokeh-send-additional-parameters-to-widget-event-handler
#https://stackoverflow.com/questions/65300681/clarification-on-bokehs-callback


import sys
if "E:\\finance_tools" not in sys.path:
    sys.path.append("E:\\finance_tools")
from utils import calc_min_payment, calc_balance

from bokeh.models import Slider, ColumnDataSource, MultiLine, Plot
from bokeh.layouts import column, row
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
slide_over = Slider(start=0,     end=500,      value=0,      step=1,    title="Fixed monthly overpayment")

#Compute graphic from defaults
m = calc_min_payment(slide_p.value, slide_r.value, slide_term.value)
month_ids = [i for i in range(12*slide_term.value)]
frac_years = [i/12 for i in month_ids]
t_min = [calc_balance(slide_p.value, slide_r.value, j, m+slide_over.value) for j in month_ids]
c = ["red" if i/12 < slide_fix.value else "lightsalmon" for i in range(len(frac_years) -1)]

#Insert data into CDS
source = ColumnDataSource(data={'xs':[[frac_years[i], frac_years[i+1]] for i, _ in enumerate(frac_years) if i < len(frac_years)-1], 
                                'ys':[[t_min[i], t_min[i+1]] for i, _ in enumerate(t_min) if i < len(t_min)-1], 
                                'line_color':c}) 
 
#Configure plot
trajectory = p.multi_line(xs="xs", ys="ys", line_color="line_color", line_width=5, source=source)

ds = trajectory.data_source

#%%Callback to recalculate repayment trajectory
def callback(attr, old, new):
        
    m = calc_min_payment(slide_p.value, slide_r.value, slide_term.value)
    
    month_ids = [i for i in range(12*slide_term.value)]
    frac_years = [i/12 for i in month_ids]
    
    #Minimal payment
    t_min = [calc_balance(slide_p.value, slide_r.value, j, m+slide_over.value) for j in month_ids]
    c = ["red" if i/12 < slide_fix.value else "lightsalmon" for i in range(len(frac_years) -1)]

    
    #Populate dictionary behind CDS with new data
    new_data = {'xs':[[frac_years[i], frac_years[i+1]] for i, _ in enumerate(frac_years) if i < len(frac_years)-1],
	            'ys':[[t_min[i], t_min[i+1]] for i, _ in enumerate(t_min) if i < len(t_min)-1],
	            "line_color":c}

    ds.data = new_data

#%% Configure final plot
slide_r.on_change('value', callback)
slide_term.on_change('value', callback)
slide_fix.on_change('value', callback)
slide_p.on_change('value', callback)
slide_over.on_change('value', callback)

# put sliders and plot in a layout and add to the document
curdoc().add_root(row(p, column(slide_r, slide_term, slide_fix, slide_p, slide_over)))