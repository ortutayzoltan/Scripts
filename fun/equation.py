#!/usr/bin/python3

import numpy as np
x = np.array([1,2,3])
y = np.array([10,20,30])
deg = 3

#p(x) = p[0] * x**deg + ... + p[deg]
print([round(x,2) for x in np.polyfit(x, y, deg)])