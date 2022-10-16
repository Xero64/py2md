#%%
# Import Dependencies
from IPython.display import display_markdown
from pysectprop.extruded import OmegaSection

#%%
# Create Section
omsect = OmegaSection(20.0, 1.6, 20.0, 1.6, 10.0, 1.6, rf=0.0, rl=0.0)

#%%
# Display Section Properties
display_markdown(omsect)

#%%
# Plot Section
ax = omsect.plot()
