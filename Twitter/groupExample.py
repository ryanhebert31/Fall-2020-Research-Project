#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 14:35:58 2020

@author: ryanhebert
"""

import re

str1="link:www.cnn.com"
str2="link:www.abcdefg.edu"


comp = re.compile(r"link\:www\.(\w{1,3})(\w{1,10})\.(\w{3})")

result = comp.search(str1)

if result is not None:
    print(result.group(1))
    print(result.group(2))
    
result = comp.search(str2)

if result is not None:
    print(result.group(1))
    print(result.group(2))    