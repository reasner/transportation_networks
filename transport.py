'''
This file creates maps of transportation networks in the United States.
'''

import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import warnings
from PIL import Image

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

#BOUNDING BOX
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
#bounding box to translate locations to pixels
bbox_bounds = bounding_box.bounds
bbox_bounds = bbox_bounds.T
bbox_out_path = os.path.join(cd,r'bbox_bounds.csv')
bbox_bounds.to_csv(bbox_out_path)

#WATER
water_path = os.path.join(cd,r'CNW_v3_NAD83',r'CNW_v3_NAD83.shp')
water_map = gpd.read_file(water_path)
warnings.filterwarnings("ignore")
water_map = water_map.to_crs("EPSG:4326")
warnings.filterwarnings("default")
water_map = gpd.clip(water_map,bounding_box)
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1])
ax.axis('off')
bounding_box.plot(ax=ax,facecolor="black",linewidth=0,edgecolor='none',antialiased=False)
us_land_map.plot(ax=ax,facecolor="white",linewidth=0.1,edgecolor='none',antialiased=False)
water_map.plot(ax=ax,facecolor="none",linewidth=0.1,edgecolor='black',antialiased=False)
ax.margins(0)
ax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
water_img_path = os.path.join(cd,r'water_map.png')
plt.savefig(water_img_path,bbox_inches='tight',pad_inches=0,dpi=100)

#ROAD
road_path = os.path.join(cd,r'tl_2016_us_primaryroads',r'tl_2016_us_primaryroads.shp')
road_map = gpd.read_file(road_path)
warnings.filterwarnings("ignore")
road_map = road_map.to_crs("EPSG:4326")
warnings.filterwarnings("default")
road_map = gpd.clip(road_map,bounding_box)
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1])
ax.axis('off')
bounding_box.plot(ax=ax,facecolor="white",linewidth=0,edgecolor='none',antialiased=False)
road_map.plot(ax=ax,facecolor="none",linewidth=0.1,edgecolor='black',antialiased=False)
ax.margins(0)
ax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
road_img_path = os.path.join(cd,r'road_map.png')
plt.savefig(road_img_path,bbox_inches='tight',pad_inches=0,dpi=100)

#RAIL
rail_path = os.path.join(cd,r'tl_2010_us_rails',r'tl_2010_us_rails.shp')
rail_map = gpd.read_file(rail_path)
warnings.filterwarnings("ignore")
rail_map = rail_map.to_crs("EPSG:4326")
warnings.filterwarnings("default")
rail_map = gpd.clip(rail_map,bounding_box)
rail_map = rail_map[rail_map['MTFCC'] == 'R1011']
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1])
ax.axis('off')
bounding_box.plot(ax=ax,facecolor="white",linewidth=0,edgecolor='none',antialiased=False)
rail_map.plot(ax=ax,facecolor="none",linewidth=0.1,edgecolor='black',antialiased=False)
ax.margins(0)
ax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
rail_img_path = os.path.join(cd,r'rail_map.png')
plt.savefig(rail_img_path,bbox_inches='tight',pad_inches=0,dpi=100)

#LOCATIONS
cz_crosswalk_path = os.path.join(cd,r'cz00_eqv_v1.xls')
cz_crosswalk_xls = pd.ExcelFile(cz_crosswalk_path,engine='xlrd')
cz_crosswalk_xls_sheet_names = cz_crosswalk_xls.sheet_names
cz_crosswalk = cz_crosswalk_xls.parse(cz_crosswalk_xls_sheet_names[0])
cz_crosswalk = cz_crosswalk[['FIPS','Commuting Zone ID, 2000']]
cz_crosswalk['FIPS'] = cz_crosswalk['FIPS'].apply(str)
cz_crosswalk['FIPS'] = cz_crosswalk['FIPS'].str.zfill(5)
cz_crosswalk['Commuting Zone ID, 2000'] = cz_crosswalk['Commuting Zone ID, 2000'].apply(str)
cz_crosswalk['Commuting Zone ID, 2000'] = cz_crosswalk['Commuting Zone ID, 2000'].str.zfill(3)
cz_crosswalk.columns = ['fips', 'cz_area']
##join county map and cfs crosswalk
cz_comb_df = pd.merge(county_map,cz_crosswalk,on='fips',how='inner')
cz_map = cz_comb_df.dissolve(by='cz_area')
cz_map.reset_index(inplace=True)
cz_map = cz_map[['cz_area','geometry']]
##cz
cz_codes = cz_map['cz_area'].tolist()
cz_centroids_df = cz_map[['geometry']].copy()
warnings.filterwarnings("ignore")
cz_centroids_df.geometry = cz_centroids_df.centroid
cz_lon = cz_centroids_df.centroid.x.tolist()
cz_lat = cz_centroids_df.centroid.y.tolist()
warnings.filterwarnings("default")
cz_areas = list(zip(cz_lon,cz_lat))
cz_distances = []
for ind1,cz1 in enumerate(cz_areas):
    for ind2,cz2 in enumerate(cz_areas):
        orig_cz_code = cz_codes[ind1]
        dest_cz_code = cz_codes[ind2]
        local_list = [cz1,cz2,orig_cz_code,dest_cz_code]
        cz_distances.append(local_list)
orig_cz_lon = []
orig_cz_lat = []
dest_cz_lon = []
dest_cz_lat = []
dist_cz = []
orig_cz_code = []
dest_cz_code = []
for entry in cz_distances:
    orig_cz_lon.append(entry[0][0])
    orig_cz_lat.append(entry[0][1])
    dest_cz_lon.append(entry[1][0])
    dest_cz_lat.append(entry[1][1])
    orig_cz_code.append(entry[2])
    dest_cz_code.append(entry[3])
cz_out = {'orig_lon':orig_cz_lon,'orig_lat':orig_cz_lat,'dest_lon':dest_cz_lon,'dest_lat':dest_cz_lat,'orig_code':orig_cz_code,'dest_code':dest_cz_code}  
cz_out_df = pd.DataFrame(cz_out)
cz_out_path = os.path.join(cd,r'cz_pair.csv')
cz_out_df.to_csv(cz_out_path,index=False)
#map of locations
fig, ax = plt.subplots(1, figsize=(8.5,6.5))
ax.axis('off')
cz_centroids_df.plot(ax=ax,marker=',',color='red',markersize=1,antialiased=False)
bounding_box.plot(ax=ax,facecolor="none",linewidth=0.1,edgecolor='white',antialiased=False)
cent_img_path = os.path.join(cd,r'cent_map.png')
plt.savefig(cent_img_path,bbox_inches='tight',dpi=100)
#adjust images
rail_image = Image.open(rail_img_path)
rail_width, rail_height = rail_image.size
rail_box = (0,1,rail_width,rail_height)
rail_region = rail_image.crop(rail_box)
rail_region.save(rail_img_path)

road_image = Image.open(road_img_path)
road_width, road_height = road_image.size
road_box = (0,2,road_width,road_height)
road_region = road_image.crop(road_box)
road_region.size
road_region.save(road_img_path)
