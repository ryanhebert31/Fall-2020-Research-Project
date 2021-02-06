#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 15:33:28 2020

@author: ryanhebert
"""

import pandas as pd
import numpy as np
from bokeh.plotting import save, show, figure
from bokeh.io import curdoc
import os


df = pd.read_csv('summary-yearly.csv')
years = df['Date']

total = sum(df["Total"])
plot = figure(plot_height = 600, plot_width = 600, toolbar_location = "below", x_axis_label = "Year", y_axis_label = "Total")
plot.title.text = str(total) + " documents analyzed.\nClick on the legend key to hide other results"

plot.circle(years, df['SVM'], color = 'blue', size = 15, alpha = 0.4, legend_label = "Propaganda (SVM)")
plot.circle(years, df['NB'], color = 'purple', size = 15, alpha = 0.4, legend_label = "Propaganda (NB)")
plot.circle(years, df['Positive'], color = 'green', size = 15, alpha = 0.4, legend_label = "Positive Sentiment")
plot.circle(years, df['Negative'], color = 'red', size = 15, alpha = 0.4, legend_label = "Negative Sentiment")
plot.circle(years, df['Neutral'], color = 'orange', size = 15, alpha = 0.4, legend_label = "Neutral Sentiment")

plot.legend.location = "top_left"
plot.legend.click_policy = "hide"

show(plot)

curdoc().title = "Analysis Results"
curdoc().add_root(plot)
    