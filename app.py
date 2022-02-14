#https://stackoverflow.com/questions/41926478/python-bokeh-send-additional-parameters-to-widget-event-handler
#https://stackoverflow.com/questions/65300681/clarification-on-bokehs-callback

from bokeh.models import Slider, ColumnDataSource, MultiLine, Plot
from bokeh.layouts import column, row
from bokeh.plotting import figure, curdoc
from bokeh.models import NumeralTickFormatter

#PREP FOR DOCKER FILE - use path manager instead
# import sys
# if "E:\\finance_tools" not in sys.path:
#     sys.path.append("E:\\finance_tools")
from utils_maths import calc_min_payment, calc_balance
from utils_graphics import make_trajectory



#%%
#Variables
max_term = 40
max_p = 400000
primary_a = "red"
primary_b = "dodgerblue"



#%% Graphics
p = figure(x_range=(0, max_term), y_range=(0, max_p), toolbar_location=None, x_axis_label='Time / years', y_axis_label='Balance / £')
p.yaxis.formatter=NumeralTickFormatter(format="00")
p.yaxis.ticker.desired_num_ticks = 40
p.yaxis.minor_tick_line_color = None  #turn off y-axis minor ticks

q = figure(x_range=["A", "B"], y_range=(0, 2000), toolbar_location=None, plot_width=300, plot_height=350, x_axis_label='Deal', y_axis_label='Monthly repayment / £')
q.yaxis.ticker.desired_num_ticks = 20
q.yaxis.minor_tick_line_color = None  #turn off y-axis minor ticks

slide_r_a    = Slider(start=1,      end=7,        value=1.04,   step=0.01, title="Interest rate")
slide_term_a = Slider(start=10,     end=max_term, value=30,     step=1,    title="Mortgage term")
slide_fix_a  = Slider(start=0,      end=10,       value=5,      step=1,    title="Fixed-term length")
slide_p_a    = Slider(start=100000, end=max_p,    value=208499, step=1,    title="Principal")
slide_over_a = Slider(start=0,      end=1000,     value=0,      step=1,    title="Fixed monthly overpayment")

slide_r_b    = Slider(start=1,      end=7,        value=1.04,   step=0.01, title="Interest rate")
slide_term_b = Slider(start=10,     end=max_term, value=30,     step=1,    title="Mortgage term")
slide_fix_b  = Slider(start=0,      end=10,       value=5,      step=1,    title="Fixed-term length")
slide_p_b    = Slider(start=100000, end=max_p,    value=208499, step=1,    title="Principal")
slide_over_b = Slider(start=0,      end=1000,     value=300,    step=1,    title="Fixed monthly overpayment")

#Insert data into CDS
source_a = ColumnDataSource(data=make_trajectory(slide_p_a, slide_r_a, slide_term_a, slide_over_a, slide_fix_a, primary_a)[0])
source_b = ColumnDataSource(data=make_trajectory(slide_p_b, slide_r_b, slide_term_b, slide_over_b, slide_fix_b, primary_b)[0])
source_ra = ColumnDataSource(data=make_trajectory(slide_p_a, slide_r_a, slide_term_a, slide_over_a, slide_fix_a, primary_a)[1])
source_ra.data.update({"xs":["A"]})
source_rb = ColumnDataSource(data=make_trajectory(slide_p_b, slide_r_b, slide_term_b, slide_over_b, slide_fix_b, primary_b)[1])
source_rb.data.update({"xs":["B"]})

#Configure plots
trajectory_a = p.multi_line(xs="xs", ys="ys", line_color="line_color", line_width=5, source=source_a)
trajectory_b = p.multi_line(xs="xs", ys="ys", line_color="line_color", line_width=5, source=source_b)
rep_a_min = q.vbar(x="xs", top="ymin_top", bottom="ymin_bot", width=0.5, source=source_ra, fill_color=primary_a)
rep_a_over = q.vbar(x="xs", top="yover_top", bottom="yover_bot", width=0.5, source=source_ra, fill_color=primary_a, hatch_pattern="@")
rep_b_min = q.vbar(x="xs", top="ymin_top", bottom="ymin_bot", width=0.5, source=source_rb, fill_color=primary_b)
rep_b_over = q.vbar(x="xs", top="yover_top", bottom="yover_bot", width=0.5, source=source_rb, fill_color=primary_b, hatch_pattern="@")



#%% Configure functionality and positioning
def callback_a(attr, old, new):
    traj_update = make_trajectory(slide_p_a, slide_r_a, slide_term_a, slide_over_a, slide_fix_a, primary_a)
    trajectory_a.data_source.data = traj_update[0]
    
    rep_a_min.data_source.data = traj_update[1]
    rep_a_over.data_source.data = traj_update[1]
    
    rep_a_min.data_source.data.update({"xs":["A"]})
    rep_a_over.data_source.data.update({"xs":["A"]})

    
def callback_b(attr, old, new):
    traj_update = make_trajectory(slide_p_b, slide_r_b, slide_term_b, slide_over_b, slide_fix_b, primary_b)
    trajectory_b.data_source.data = traj_update[0]

    rep_b_min.data_source.data = traj_update[1]
    rep_b_over.data_source.data = traj_update[1]
    
    rep_b_min.data_source.data.update({"xs":["B"]})
    rep_b_over.data_source.data.update({"xs":["B"]})

slide_r_a.on_change('value',    callback_a)
slide_term_a.on_change('value', callback_a)
slide_fix_a.on_change('value',  callback_a)
slide_p_a.on_change('value',    callback_a)
slide_over_a.on_change('value', callback_a)

slide_r_b.on_change('value',    callback_b)
slide_term_b.on_change('value', callback_b)
slide_fix_b.on_change('value',  callback_b)
slide_p_b.on_change('value',    callback_b)
slide_over_b.on_change('value', callback_b)

# put sliders and plot in a layout and add to the document
curdoc().add_root(row(p, column(slide_r_a, slide_term_a, slide_fix_a, slide_p_a, slide_over_a, q), column(slide_r_b, slide_term_b, slide_fix_b, slide_p_b, slide_over_b)))