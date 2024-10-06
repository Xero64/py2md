#%%
# Import Dependencies
from math import radians, sin

from IPython.display import display_markdown
from matplotlib.pyplot import figure

from py2md.classes import MDFigure

#%%
# Create Plot
th = [float(i) for i in range(361)]
thrad = [radians(thi) for thi in th]
y = [sin(thi) for thi in thrad]

fig = figure()
ax = fig.gca()
ax.grid(True)
_ = ax.plot(th, y)

#%%
# Create Object and Display
test = MDFigure(fig)
display_markdown(test)
