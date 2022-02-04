# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 10:47:01 2022

@author: Alex White
"""
#PREP FOR DOCKER FILE - use path manager instead
# import sys
# if "E:\\finance_tools" not in sys.path:
#     sys.path.append("E:\\finance_tools")
from utils_maths import calc_min_payment, calc_balance

from matplotlib.colors import rgb2hex, to_rgba



def make_trajectory(p_slider, r_slider, term_slider, over_slider, fix_slider, traj_colour):

	"""
	Create/update data structure powering each repayment visual using current state from each slider
	"""

	#Timebase
	month_ids = [i for i in range(12*term_slider.value)]
	frac_years = [i/12 for i in month_ids]
	
	repay_min = calc_min_payment(p_slider.value, r_slider.value, term_slider.value)
	
	#Trajectory @ min. monthly repayment
	traj_min = [calc_balance(p_slider.value, r_slider.value, j, repay_min+over_slider.value) for j in month_ids]
	
	#Indicate where fixed term ends
	fade = rgb2hex(to_rgba(traj_colour, alpha=0.1), keep_alpha=True)
	c = [traj_colour if i/12 < fix_slider.value else fade for i in range(len(frac_years) -1)]
	
    #"list of lists" format
	data_dict = {'xs':[[frac_years[i], frac_years[i+1]] for i, _ in enumerate(frac_years) if i < len(frac_years)-1],
	             'ys':[[traj_min[i], traj_min[i+1]] for i, _ in enumerate(traj_min) if i < len(traj_min)-1],
	             "line_color":c}
	
	return data_dict



if __name__ == "__main__":
	pass