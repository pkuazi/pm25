from IPython.core.pylabtools import figsize
import numpy as np
from matplotlib import pyplot as plt
figsize(12.5, 4)
plt.rcParams['savefig.dpi']=300
plt.rcParams['figure.dpi']=300
colors = ['#348ABD','#A60628']
prior = [1/21., 20/21.]
posterior = [0.87, 1-0.87]

plt.bar([0,.7],prior,alpha=0.7,width=0.25,color=colors[0],label="prior distribution", lw='3', edgecolor="#348ABD")
plt.bar([0+0.25, .7+0.25], posterior, alpha = 0.7, width=0.25,color=colors[1],label="posterior distribution",lw='3',edgecolor="#A60628")

plt.xticks([0.2,0.95],["libararian", "farmer"])
plt.title("prior and posterior probabilities of Steve's occupation")
plt.ylabel("Probability")
plt.legend(loc = "upper left")

plt.show()