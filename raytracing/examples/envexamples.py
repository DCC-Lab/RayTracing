import sys
import os
import matplotlib.pyplot as plt

""" This file is needed so the examples in the `examples` directory can be run direclty from there with 
the current version of the module """

# Append module root directory to sys.path
sys.path.insert(0,
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

# Some decent parameters for plots
# See https://matplotlib.org/api/font_manager_api.html#matplotlib.font_manager.FontProperties.set_size
params = {'legend.fontsize': 'x-large',
          'figure.figsize': (10, 7),
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large',
         'font.family':'helvetica'}
plt.rcParams.update(params)

