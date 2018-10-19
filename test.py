import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

x = np.random.random(10)
y = np.random.random(10)

slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)

plt.plot(x,y,'o',label='original data')
plt.plot(x, intercept+slope*x, 'r', label='fitted data')
plt.legend()
plt.show()