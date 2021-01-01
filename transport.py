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

#RAIL
rail_path = os.path.join(cd,r'tl_2010_us_rails',r'tl_2010_us_rails.shp')
rail_map = gpd.read_file(rail_path)
warnings.filterwarnings("ignore")
rail_map = rail_map.to_crs("EPSG:4326")
warnings.filterwarnings("default")
rail_map = gpd.clip(rail_map,bounding_box)
rail_map = rail_map[rail_map['MTFCC'] == 'R1011']
fig, ax = plt.subplots(1, figsize=(8,6))
ax.axis('off')
rail_map.plot(ax=ax,facecolor="none",linewidth=0.1,edgecolor='black',antialiased=False)
bounding_box.plot(ax=ax,facecolor="none",linewidth=0.1,edgecolor='white',antialiased=False)
rail_img_path = os.path.join(cd,r'rail_map.png')
plt.savefig(rail_img_path,bbox_inches='tight',dpi=100)

#ROAD
road_path = os.path.join(cd,r'tl_2016_us_primaryroads',r'tl_2016_us_primaryroads.shp')
road_map = gpd.read_file(road_path)
warnings.filterwarnings("ignore")
road_map = road_map.to_crs("EPSG:4326")
warnings.filterwarnings("default")
road_map = gpd.clip(road_map,bounding_box)
fig, ax = plt.subplots(1, figsize=(8,6))
ax.axis('off')
road_map.plot(ax=ax,facecolor="none",linewidth=0.1,edgecolor='black',antialiased=False)
bounding_box.plot(ax=ax,facecolor="none",linewidth=0.1,edgecolor='white',antialiased=False)
road_img_path = os.path.join(cd,r'road_map.png')
plt.savefig(road_img_path,bbox_inches='tight',dpi=100)

#WATER
water_path = os.path.join(cd,r'CNW_v3_NAD83',r'CNW_v3_NAD83.shp')
water_map = gpd.read_file(water_path)
warnings.filterwarnings("ignore")
water_map = water_map.to_crs("EPSG:4326")
warnings.filterwarnings("default")
water_map = gpd.clip(water_map,bounding_box)
fig, ax = plt.subplots(1, figsize=(8,6))
ax.axis('off')
bounding_box.plot(ax=ax,facecolor="black",linewidth=0.1,edgecolor='none',antialiased=False)
us_land_map.plot(ax=ax,facecolor="white",linewidth=0.1,edgecolor='none',antialiased=False)
water_map.plot(ax=ax,facecolor="none",linewidth=0.2,edgecolor='black',antialiased=False)
bounding_box.plot(ax=ax,facecolor="none",linewidth=0.1,edgecolor='white',antialiased=False)
water_img_path = os.path.join(cd,r'water_map.png')
plt.savefig(water_img_path,bbox_inches='tight',dpi=100)



