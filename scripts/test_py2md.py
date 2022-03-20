#%%
# [markdown]
# # Some Markdown
# **Bold Text**
# ~~Strike-through~~
# | Column 1 | Column 2 | Column 3 |
# | -------- | -------- | -------- |
# | Value 1  | Value 2  | Value 3  |

#%%
# Import Dependencies
from IPython.display import display
from matplotlib.pyplot import figure
from py2md.classes import MDTable

#%%
# Create Table
table = MDTable()
table.add_column('y', '.2f')
table.add_column('z', '.2f')
print(table.columns[0].length)
print(table.columns[1].length)
table.add_row([15.0, 1000.0])
print(table.columns[0].length)
print(table.columns[1].length)

display(table)

#%%
# [markdown]
# # Latex Equations
# $$
# \begin{bmatrix}
# 2.0 & 5.0 \\
# 4.4 & 5.2
# \end{bmatrix}
# $$
# $$
# E = m.c^2
# $$

#%%
# Simple Plots

fig = figure(figsize=(12, 8))
ax = fig.gca()
ax.plot([1.0, 2.0, 3.0], [5.0, 3.0, 4.0], label='Plot')
ax.grid(True)
l = ax.legend()
