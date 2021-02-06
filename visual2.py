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
from bokeh.models import HoverTool
import os
from datetime import datetime 

temp = pd.read_csv('summary-monthly.csv')
data = temp.values.tolist()

data.sort(key = lambda date: datetime.strptime(date[0], '%m/%Y'))

df = pd.DataFrame(data, columns = ["Month", 'Total', 'SVM', "NB", "SVM Percent", "NB Percent", "Positive", "Negative", "Neutral", "Rate"])
print(df['SVM'])
df['Month'] = pd.to_datetime(df['Month'])

total = sum(df["Total"])
plot = figure(plot_height = 600, plot_width = 600, toolbar_location = "below", x_axis_type="datetime", x_axis_label = "Year", y_axis_label = "Total")
plot.title.text = str(total) + " documents analyzed.\nClick on the legend key to hide other results."

plot.circle(df["Month"], df["SVM"], color = 'blue', size = 15, alpha = 0.4, legend_label = "Propaganda (SVM)")
plot.circle(df["Month"], df['NB'], color = 'purple', size = 15, alpha = 0.4, legend_label = "Propaganda (NB)")
plot.circle(df["Month"], df['Positive'], color = 'green', size = 15, alpha = 0.4, legend_label = "Positive Sentiment")
plot.circle(df["Month"], df['Negative'], color = 'red', size = 15, alpha = 0.4, legend_label = "Negative Sentiment")
plot.circle(df["Month"], df['Neutral'], color = 'orange', size = 15, alpha = 0.4, legend_label = "Neutral Sentiment")

plot.legend.location = "top_left"
plot.legend.click_policy = "hide"

show(plot)

curdoc().title = "Analysis Results"
curdoc().add_root(plot)