#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 15:33:28 2020

@author: ryanhebert
"""

import pandas as pd
import numpy as np
from bokeh.plotting import save, show, figure, output_file
from bokeh.server.server import Server


df = pd.read_csv('test31.csv')

gt = []
pd = []
fx = []

# print(df)

gt_i = np.where(df['source'] == "Global Times")

pd_i = np.where(df['source'] == "Peoples Daily")

fx_i = np.where(df['source'] == "Fox")


gt = df.loc[gt_i[0].tolist() , :]
pd = df.loc[gt_i[0].tolist() , :]
fx = df.loc[gt_i[0].tolist() , :]


multi_line_plot = figure(plot_height = 300, plot_width = 300, toolbar_location = "below")
# multi_line_plot.line(gt[], gt_tw_prop, color = 'red', line_width = 1)
multi_line_plot.line(gt['year'], gt['prop'], color = 'red', line_width = 3)

# multi_line_plot.line(pd_tw_years, pd_tw_prop, color = 'green', line_width = 1)
multi_line_plot.line(pd['year'], pd['prop'], color = 'green', line_width = 3)

# multi_line_plot.line(fx_tw_years, fx_tw_prop, color = 'blue', line_width = 1)
multi_line_plot.line(fx['year'], fx['prop'], color = 'blue', line_width = 3)

show(multi_line_plot) 
