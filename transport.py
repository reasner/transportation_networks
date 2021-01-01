'''
This file creates maps of transportation networks in the United States.
'''

import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import warnings

# SETUP
cd = os.path.join(os.path.expanduser("~"),r'Documents',r'Projects',r'transport')

# LOAD COUNTY SHAPEFILE
shapefile_path = os.path.join(cd,r'gz_2010_us_050_00_500k',r'gz_2010_us_050_00_500k.shp')
county_map = gpd.read_file(shapefile_path)
county_map = county_map[(county_map['STATE'] != '02') & (county_map['STATE'] != '15') & (county_map['STATE'] != '72')]
county_map['fips'] = county_map['STATE'] + county_map['COUNTY']
warnings.filterwarnings("ignore")
county_map = county_map.to_crs("EPSG:4326")
county_map['geometry'] = county_map['geometry'].buffer(0.0001)
warnings.filterwarnings("default")
county_map['cont_us'] = 1
cont_us_map = county_map.dissolve(by='cont_us')

#load land old projection
land_path = os.path.join(cd,r'Longitude_Graticules_and_World_Countries_Boundaries-shp',r'99bfd9e7-bb42-4728-87b5-07f8c8ac631c2020328-1-1vef4ev.lu5nk.shp')
land_map = gpd.read_file(land_path)

#reproject/buffer
warnings.filterwarnings("ignore")
land_map = land_map.to_crs("EPSG:4326")
land_map['geometry'] = land_map['geometry'].buffer(0.0001)
warnings.filterwarnings("default")

#load create geodataframe from bounding box
bbox = cont_us_map.envelope
bounding_box = gpd.GeoDataFrame(gpd.GeoSeries(bbox), columns=['geometry'])

#combine
us_land_map = gpd.overlay(land_map,bounding_box,how='intersection')
us_land_map['all'] = 1
us_land_map = us_land_map.dissolve(by='all')

#plot
fig, ax = plt.subplots(1, figsize=(8,6))
ax.axis('off')
us_land_map.plot(ax=ax,facecolor="none",linewidth=0.1,edgecolor='gray',antialiased=False)
plt.show()

