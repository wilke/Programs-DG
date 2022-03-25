
import numpy as np
import plotly.express as px




fig = px.line(x=['03-23', '03-30', '04-13'], y=[[0.018, 0.174, 0], [0.512, 0.53, 0], [0.453, 0.262, 0], [0, 0, 0.957], [0.0176406, 0.147057, 0], [0.499921, 0.555018, 0], [0.4682737, 0.285328, 0], [0, 0, 0.944534]], title="sample figure")
print(fig)
fig.show()
