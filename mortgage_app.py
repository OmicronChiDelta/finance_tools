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



#%%Callback to recalculate repayment trajectory
def callback(attr, old, new, p_slider, r_slider, term_slider, over_slider, fix_slider, ds):
        
    m = calc_min_payment(p_slider.value, r_slider.value, term_slider.value)
    
    month_ids = [i for i in range(12*term_slider.value)]
    frac_years = [i/12 for i in month_ids]
    
    #Minimal payment
    t_min = [calc_balance(p_slider.value, r_slider.value, j, m+over_slider.value) for j in month_ids]
    c = ["red" if i/12 < fix_slider.value else "lightsalmon" for i in range(len(frac_years) -1)]
    
    xs = [[frac_years[i], frac_years[i+1]] for i, _ in enumerate(frac_years) if i < len(frac_years)-1]
    ys = [[t_min[i], t_min[i+1]] for i, _ in enumerate(t_min) if i < len(t_min)-1]
    
    #Populate dictionary behind CDS with new data
    new_data = {'xs':xs, 'ys':ys, "line_color":c}
    
    ds.data = new_data



#%%
#Variables
max_term = 40
max_p = 500000

#Plot area and styling
p = figure(x_range=(0, max_term), y_range=(0, max_p), toolbar_location=None)

slide_r_a    = Slider(start=1,      end=7,        value=1.04,   step=0.01, title="Interest rate")
slide_term_a = Slider(start=10,     end=max_term, value=30,     step=1,    title="Mortgage term")
slide_fix_a  = Slider(start=0,      end=10,       value=5,      step=1,    title="Fixed-term length")
slide_p_a    = Slider(start=100000, end=max_p,    value=208499, step=1,    title="Principal")
slide_over_a = Slider(start=0,      end=500,      value=0,      step=1,    title="Fixed monthly overpayment")

slide_r_b    = Slider(start=1,      end=7,        value=2.5,    step=0.01, title="Interest rate")
slide_term_b = Slider(start=10,     end=max_term, value=30,     step=1,    title="Mortgage term")
slide_fix_b  = Slider(start=0,      end=10,       value=5,      step=1,    title="Fixed-term length")
slide_p_b    = Slider(start=100000, end=max_p,    value=208499, step=1,    title="Principal")
slide_over_b = Slider(start=0,      end=500,      value=0,      step=1,    title="Fixed monthly overpayment")

#Configure plots
source_a = ColumnDataSource() 
trajectory_a = p.multi_line(xs="xs", ys="ys", line_color="line_color", line_width=5, source=source_a)
ds_a = trajectory_a.data_source

source_b = ColumnDataSource() 
trajectory_b = p.multi_line(xs="xs", ys="ys", line_color="line_color", line_width=5, source=source_b)
ds_b = trajectory_b.data_source

callback(None, None, None, slide_p_a, slide_r_a, slide_term_a, slide_over_a, slide_fix_a, ds_a)
callback(None, None, None, slide_p_b, slide_r_b, slide_term_b, slide_over_b, slide_fix_b, ds_b)


#%% Configure final plot
slide_r_a.on_change('value', callback)
slide_term_a.on_change('value', callback)
slide_fix_a.on_change('value', callback)
slide_p_a.on_change('value', callback)
slide_over_a.on_change('value', callback)

slide_r_b.on_change('value', callback)
slide_term_b.on_change('value', callback)
slide_fix_b.on_change('value', callback)
slide_p_b.on_change('value', callback)
slide_over_b.on_change('value', callback)

# put sliders and plot in a layout and add to the document
curdoc().add_root(row(p, column(slide_r_a, slide_term_a, slide_fix_a, slide_p_a, slide_over_a), column(slide_r_b, slide_term_b, slide_fix_b, slide_p_b, slide_over_b)))