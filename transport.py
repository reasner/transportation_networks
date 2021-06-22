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
cd = os.path.join(os.path.expanduser("~"),r'Dropbox',r'projects',r'transport')
cd_dotdot = os.path.join(os.path.expanduser("~"),r'Dropbox',r'projects')
# LOAD COUNTY SHAPEFILE
shapefile_path = os.path.join(cd_dotdot,r'cfs_cz_shapefile_and_distances',r'fips',r'fips.shp')
county_map = gpd.read_file(shapefile_path)
#combine counties into a single shape
county_map['cont_us'] = 1
cont_us_map = county_map.dissolve(by='cont_us')

#BOUNDING BOX
land_path = os.path.join(cd,r'Longitude_Graticules_and_World_Countries_Boundaries-shp',r'99bfd9e7-bb42-4728-87b5-07f8c8ac631c2020328-1-1vef4ev.lu5nk.shp')
land_map = gpd.read_file(land_path)
#reproject/buffer
warnings.filterwarnings("ignore")
land_map = land_map.to_crs("EPSG:5070")
land_map['geometry'] = land_map['geometry'].buffer(5)
warnings.filterwarnings("default")
#create bounding box and load into a geodataframe
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

#NAVIGABLE WATERWAYS
water_path = os.path.join(cd,r'CNW_v3_NAD83',r'CNW_v3_NAD83.shp')
water_map = gpd.read_file(water_path)
warnings.filterwarnings("ignore")
water_map = water_map.to_crs("EPSG:5070")
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
plt.savefig(water_img_path,bbox_inches='tight',pad_inches=0,dpi=200)
plt.clf()

#HIGHWAYS
road_path = os.path.join(cd,r'pa_nhs',r'PA_NHS.shp')
road_map = gpd.read_file(road_path)
road_map = road_map[~(road_map['State_Code'] == 2) & ~(road_map['State_Code'] == 15)]
road_map  = road_map[road_map.geometry.is_valid]
interstate_map = road_map[(road_map['F_SYSTEM'] == 1)]
highway_map = road_map[(road_map['F_SYSTEM'] == 2)]
other_road_map = road_map[(road_map['F_SYSTEM'] == 3)]
warnings.filterwarnings("ignore")
interstate_map = interstate_map.to_crs("EPSG:5070")
highway_map = highway_map.to_crs("EPSG:5070")
other_road_map = other_road_map.to_crs("EPSG:5070")
warnings.filterwarnings("default")
interstate_map = gpd.clip(interstate_map,bounding_box)
highway_map = gpd.clip(highway_map,bounding_box)
other_road_map = gpd.clip(other_road_map,bounding_box)
#interstate picture
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1])
ax.axis('off')
bounding_box.plot(ax=ax,facecolor="white",linewidth=0,edgecolor='none',antialiased=False)
interstate_map.plot(ax=ax,facecolor="none",linewidth=0.1,edgecolor='black',antialiased=False)
ax.margins(0)
ax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
interstate_img_path = os.path.join(cd,r'interstate_map.png')
plt.savefig(interstate_img_path,bbox_inches='tight',pad_inches=0,dpi=200)
plt.clf()
#highway picture
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1])
ax.axis('off')
bounding_box.plot(ax=ax,facecolor="white",linewidth=0,edgecolor='none',antialiased=False)
highway_map.plot(ax=ax,facecolor="none",linewidth=0.1,edgecolor='black',antialiased=False)
ax.margins(0)
ax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
highway_img_path = os.path.join(cd,r'highway_map.png')
plt.savefig(highway_img_path,bbox_inches='tight',pad_inches=0,dpi=200)
plt.clf()
#other road picture
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1])
ax.axis('off')
bounding_box.plot(ax=ax,facecolor="white",linewidth=0,edgecolor='none',antialiased=False)
other_road_map.plot(ax=ax,facecolor="none",linewidth=0.1,edgecolor='black',antialiased=False)
ax.margins(0)
ax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
other_road_img_path = os.path.join(cd,r'other_road_map.png')
plt.savefig(other_road_img_path,bbox_inches='tight',pad_inches=0,dpi=200)
plt.clf()

#RAILROADS
rail_path = os.path.join(cd,r'Railroads-shp',r'Railroads.shp')
rail_map = gpd.read_file(rail_path)
rail_map = rail_map[~(rail_map['stfips'] == '02')]
main_rail_map = rail_map[(rail_map['net'] == 'M')]
other_rail_map = rail_map[~(rail_map['net'] == 'M')]
warnings.filterwarnings("ignore")
main_rail_map = main_rail_map.to_crs("EPSG:5070")
other_rail_map = other_rail_map.to_crs("EPSG:5070")
warnings.filterwarnings("default")
main_rail_map = gpd.clip(main_rail_map,bounding_box)
other_rail_map = gpd.clip(other_rail_map,bounding_box)
#main rail
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1])
ax.axis('off')
bounding_box.plot(ax=ax,facecolor="white",linewidth=0,edgecolor='none',antialiased=False)
main_rail_map.plot(ax=ax,facecolor="none",linewidth=0.1,edgecolor='black',antialiased=False)
ax.margins(0)
ax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
main_rail_img_path = os.path.join(cd,r'main_rail_map.png')
plt.savefig(main_rail_img_path,bbox_inches='tight',pad_inches=0,dpi=200)
plt.clf()
#other rail
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1])
ax.axis('off')
bounding_box.plot(ax=ax,facecolor="white",linewidth=0,edgecolor='none',antialiased=False)
other_rail_map.plot(ax=ax,facecolor="none",linewidth=0.1,edgecolor='black',antialiased=False)
ax.margins(0)
ax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
other_rail_img_path = os.path.join(cd,r'other_rail_map.png')
plt.savefig(other_rail_img_path,bbox_inches='tight',pad_inches=0,dpi=200)
plt.clf()

#LOCATIONS
if not os.path.exists(os.path.join(cd,r'pairs')):
    os.makedirs(os.path.join(cd,r'pairs'))
#Commuting Zones (CZ)
cz_map_path = os.path.join(cd_dotdot,r'cfs_cz_shapefile_and_distances',r'cz00',r'cz00.shp')
cz_map = gpd.read_file(cz_map_path)
cz_codes = cz_map['cz_area'].tolist()
cz_centroids_df = cz_map[['geometry']].copy()
warnings.filterwarnings("ignore")
cz_centroids_df.geometry = cz_centroids_df.centroid
cz_lon = cz_centroids_df.centroid.x.tolist()
cz_lat = cz_centroids_df.centroid.y.tolist()
cz_loc = pd.DataFrame(
    {'cz_code': cz_codes,
     'cz_lon': cz_lon,
     'cz_lat': cz_lat
    })
cz_loc_out_path = os.path.join(cd,r'cz_loc.csv')
cz_loc.to_csv(cz_loc_out_path,index=False)
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
cz_out_path = os.path.join(cd,r'pairs',r'cz_pair.csv')
cz_out_df.to_csv(cz_out_path,index=False)
#map of locations
fig, ax = plt.subplots(1, figsize=(8.5,6.5))
ax.axis('off')
cz_centroids_df.plot(ax=ax,marker=',',color='red',markersize=1,antialiased=False)
bounding_box.plot(ax=ax,facecolor="none",linewidth=0.1,edgecolor='white',antialiased=False)
cz_cent_img_path = os.path.join(cd,r'cz_cent_map.png')
plt.savefig(cz_cent_img_path,bbox_inches='tight',pad_inches=0,dpi=200)
plt.clf()
#Commodity Flow Survery (CFS) Areas
cfs_map_path = os.path.join(cd_dotdot,r'cfs_cz_shapefile_and_distances',r'cfs07',r'cfs07.shp')
cfs_map = gpd.read_file(cfs_map_path)
cfs_map = cfs_map.sort_values(by='cfs_area')
unique_codes_ordered = cfs_map['cfs_area']
unique_codes_ordered.to_csv('unique_codes_ordered.csv',index=False)
cfs_codes = cfs_map['cfs_area'].tolist()
cfs_centroids_df = cfs_map[['geometry']].copy()
warnings.filterwarnings("ignore")
cfs_centroids_df.geometry = cfs_centroids_df.centroid
cfs_lon = cfs_centroids_df.centroid.x.tolist()
cfs_lat = cfs_centroids_df.centroid.y.tolist()
cfs_loc = pd.DataFrame(
    {'cfs_code': cfs_codes,
     'cfs_lon': cfs_lon,
     'cfs_lat': cfs_lat
    })
cfs_loc_out_path = os.path.join(cd,r'cfs_loc.csv')
cfs_loc.to_csv(cfs_loc_out_path,index=False)
warnings.filterwarnings("default")
cfs_areas = list(zip(cfs_lon,cfs_lat))
cfs_distances = []
for ind1,cfs1 in enumerate(cfs_areas):
    for ind2,cfs2 in enumerate(cfs_areas):
        orig_cfs_code = cfs_codes[ind1]
        dest_cfs_code = cfs_codes[ind2]
        local_list = [cfs1,cfs2,orig_cfs_code,dest_cfs_code]
        cfs_distances.append(local_list)
orig_cfs_lon = []
orig_cfs_lat = []
dest_cfs_lon = []
dest_cfs_lat = []
dist_cfs = []
orig_cfs_code = []
dest_cfs_code = []
for entry in cfs_distances:
    orig_cfs_lon.append(entry[0][0])
    orig_cfs_lat.append(entry[0][1])
    dest_cfs_lon.append(entry[1][0])
    dest_cfs_lat.append(entry[1][1])
    orig_cfs_code.append(entry[2])
    dest_cfs_code.append(entry[3])
cfs_out = {'orig_lon':orig_cfs_lon,'orig_lat':orig_cfs_lat,'dest_lon':dest_cfs_lon,'dest_lat':dest_cfs_lat,'orig_code':orig_cfs_code,'dest_code':dest_cfs_code}  
cfs_out_df = pd.DataFrame(cfs_out)
cfs_out_path = os.path.join(cd,r'pairs',r'cfs_pair.csv')
cfs_out_df.to_csv(cfs_out_path,index=False)
#map of locations
fig, ax = plt.subplots(1, figsize=(8.5,6.5))
ax.axis('off')
cfs_centroids_df.plot(ax=ax,marker=',',color='red',markersize=1,antialiased=False)
bounding_box.plot(ax=ax,facecolor="none",linewidth=0.1,edgecolor='white',antialiased=False)
cfs_cent_img_path = os.path.join(cd,r'cfs_cent_map.png')
plt.savefig(cfs_cent_img_path,bbox_inches='tight',pad_inches=0,dpi=200)
plt.clf()
#Counties (cty) 
cty_codes = county_map['fips'].tolist()
cty_centroids_df = county_map[['geometry']].copy()
warnings.filterwarnings("ignore")
cty_centroids_df.geometry = cty_centroids_df.centroid
cty_lon = cty_centroids_df.centroid.x.tolist()
cty_lat = cty_centroids_df.centroid.y.tolist()
cty_loc = pd.DataFrame(
    {'cty_code': cty_codes,
     'cty_lon': cty_lon,
     'cty_lat': cty_lat
    })
cty_loc_out_path = os.path.join(cd,r'cty_loc.csv')
cty_loc.to_csv(cty_loc_out_path,index=False)
warnings.filterwarnings("default")
cty_areas = list(zip(cty_lon,cty_lat))
cty_distances = []
for ind1,cty1 in enumerate(cty_areas):
    for ind2,cty2 in enumerate(cty_areas):
        orig_cty_code = cty_codes[ind1]
        dest_cty_code = cty_codes[ind2]
        local_list = [cty1,cty2,orig_cty_code,dest_cty_code]
        cty_distances.append(local_list)
orig_cty_lon = []
orig_cty_lat = []
dest_cty_lon = []
dest_cty_lat = []
dist_cty = []
orig_cty_code = []
dest_cty_code = []
for entry in cty_distances:
    orig_cty_lon.append(entry[0][0])
    orig_cty_lat.append(entry[0][1])
    dest_cty_lon.append(entry[1][0])
    dest_cty_lat.append(entry[1][1])
    orig_cty_code.append(entry[2])
    dest_cty_code.append(entry[3])
cty_out = {'orig_lon':orig_cty_lon,'orig_lat':orig_cty_lat,'dest_lon':dest_cty_lon,'dest_lat':dest_cty_lat,'orig_code':orig_cty_code,'dest_code':dest_cty_code}  
cty_out_df = pd.DataFrame(cty_out)
cty_out_path = os.path.join(cd,r'pairs',r'cty_pair.csv')
cty_out_df.to_csv(cty_out_path,index=False)
#map of locations
fig, ax = plt.subplots(1, figsize=(8.5,6.5))
ax.axis('off')
cty_centroids_df.plot(ax=ax,marker=',',color='red',markersize=1,antialiased=False)
bounding_box.plot(ax=ax,facecolor="none",linewidth=0.1,edgecolor='white',antialiased=False)
cty_cent_img_path = os.path.join(cd,r'cty_cent_map.png')
plt.savefig(cty_cent_img_path,bbox_inches='tight',pad_inches=0,dpi=200)
plt.clf()

#PRETTY NETWORK MAPS
#road and water
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1])
ax.axis('off')
bounding_box.plot(ax=ax,facecolor="blue",linewidth=0,edgecolor='none')
us_land_map.plot(ax=ax,facecolor="white",linewidth=0.1,edgecolor='none')
other_road_map.plot(ax=ax,facecolor="none",linewidth=0.1,edgecolor='0.8')
highway_map.plot(ax=ax,facecolor="none",linewidth=0.1,edgecolor='0.4')
interstate_map.plot(ax=ax,facecolor="none",linewidth=0.25,edgecolor='0')
water_map.plot(ax=ax,facecolor="none",linewidth=0.5,edgecolor='blue')
pretty_road_img_path = os.path.join(cd,r'road_network.png')
#pretty_road_img_path = os.path.join(cd,r'road_network.eps')
ax.margins(0)
ax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
plt.savefig(pretty_road_img_path,bbox_inches='tight',pad_inches=0,dpi=200)
#plt.savefig(pretty_road_img_path,bbox_inches='tight',format='eps',pad_inches=0,dpi=200)
plt.clf()

#rail and water
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1])
ax.axis('off')
bounding_box.plot(ax=ax,facecolor="blue",linewidth=0,edgecolor='none')
us_land_map.plot(ax=ax,facecolor="white",linewidth=0.1,edgecolor='none')
other_rail_map.plot(ax=ax,facecolor="none",linewidth=0.15,edgecolor='0.4')
main_rail_map.plot(ax=ax,facecolor="none",linewidth=0.25,edgecolor='0')
water_map.plot(ax=ax,facecolor="none",linewidth=0.5,edgecolor='blue')
ax.margins(0)
ax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
pretty_rail_img_path = os.path.join(cd,r'rail_network.png')
#pretty_rail_img_path = os.path.join(cd,r'rail_network.eps')
plt.savefig(pretty_rail_img_path,bbox_inches='tight',pad_inches=0,dpi=200)
#plt.savefig(pretty_rail_img_path,bbox_inches='tight',format='eps',pad_inches=0,dpi=200)
plt.clf()


