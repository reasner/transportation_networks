'''
This file creates maps of transportation networks in the United States.
'''

import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import warnings

# SETUP
cd = os.path.join(os.path.expanduser("~"),r'Documents',r'Projects',r'trans_dist')
