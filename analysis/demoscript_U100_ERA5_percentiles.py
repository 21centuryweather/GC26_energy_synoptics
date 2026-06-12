import sys
import os
import xarray as xr
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import matplotlib.colors as colors
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from calendar import monthrange, month_name

# Bounds for Australia (degrees lon/lat) #
lon_min, lon_max = 110, 160 
lat_min, lat_max = -45, -5

# Input data paths #
u_winds_directory = "/g/data/rt52/era5/single-levels/reanalysis/100u/" # 100-meter u-winds #
v_winds_directory = "/g/data/rt52/era5/single-levels/reanalysis/100v/" # 100-meter v-winds #

# Climatology date settings #
year_start, year_end = 1996, 2025 # Needs 18 GB of memory instead of the regular 9 GB on GADI. #
month_select = 1 # 1-based (1 = Jan., 2 = Feb., etc...) #

# Loops through years, months; slices and aggregates wind data #
for clim_year in range(year_start, year_end+1):
    print(clim_year)
    last_day = monthrange(clim_year, month_select)[1]
    path_daterange = (f"{clim_year}{month_select:02d}01-"
                      f"{clim_year}{month_select:02d}{last_day:02d}.nc")

    # Paths for u/v winds #
    u_file_path = (f"{u_winds_directory}{clim_year}/100u_era5_oper_sfc_{path_daterange}")
    v_file_path = (f"{v_winds_directory}{clim_year}/100v_era5_oper_sfc_{path_daterange}")

    # Opening u-winds #
    ds_era5_a = xr.open_dataset(u_file_path)
    ds_u100 = ds_era5_a["u100"]    
    ds_u100_subset = ds_u100.sel(
        longitude=slice(lon_min-.5, lon_max+.5), # Trimming so we don't work with the entire global domain #
        latitude=slice(lat_max+.5, lat_min-.5) 
    )

    # Opening v-winds #
    ds_era5_b = xr.open_dataset(v_file_path)
    ds_v100 = ds_era5_b["v100"]    
    ds_v100_subset = ds_v100.sel(
        longitude=slice(lon_min-.5, lon_max+.5), # Trimming so we don't work with the entire global domain #
        latitude=slice(lat_max+.5, lat_min-.5)
    )

    # Calculating 100-m wind magnitude #
    ds_wind = np.sqrt((ds_u100_subset**2)+(ds_v100_subset**2))

    # Stacking the arrays together to construct one large array (there are more memory-efficient ways to do this) #
    if clim_year == year_start:
        ds_wind_aggregate = ds_wind
    if clim_year > year_start:
        ds_wind_aggregate = np.concatenate((ds_wind_aggregate, ds_wind),axis=0)

# Calculating quantiles #
wind_25_percentile = np.percentile(ds_wind_aggregate, 25, axis=0)
wind_10_percentile = np.percentile(ds_wind_aggregate, 10, axis=0)
wind_5_percentile = np.percentile(ds_wind_aggregate, 5, axis=0)

# Getting Lats/Lons from last file opened #
lon_1d = ds_v100_subset["longitude"]
lat_1d = ds_v100_subset["latitude"]

# Making lat/lons into 2d grids #
lon2d, lat2d = np.meshgrid(lon_1d, lat_1d)

# Plotting #
# 25th-Percentile Map #
fig_25percentile = plt.figure(figsize=(10, 6))

# Map configuration #
ax1 = plt.axes(projection=ccrs.PlateCarree(central_longitude=134))
ax1.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())

# Add map features #
ax1.coastlines()
ax1.add_feature(cfeature.BORDERS, linestyle=':')
ax1.add_feature(cfeature.LAND, alpha=0.3)
ax1.add_feature(cfeature.OCEAN, alpha=0.2)

# Add title #
ax1.set_title(f"25th-Percentile 100-m Wind Speed (m/s), {month_name[month_select]}, {year_start}-{year_end}")

cf1 = ax1.contourf(  
    lon2d,
    lat2d,
    wind_25_percentile,
    cmap="PuRd",
    transform=ccrs.PlateCarree(),
    transform_first = True
)

cbar = plt.colorbar(cf1, location='right')
cbar.set_label("100-m Wind Speed (m/s)")

# 10th-Percentile Map #
fig_10percentile = plt.figure(figsize=(10, 6))

# Map configuration #
ax2 = plt.axes(projection=ccrs.PlateCarree(central_longitude=134))
ax2.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())

# Add map features #
ax2.coastlines()
ax2.add_feature(cfeature.BORDERS, linestyle=':')
ax2.add_feature(cfeature.LAND, alpha=0.3)
ax2.add_feature(cfeature.OCEAN, alpha=0.2)

# Add title #
ax2.set_title(f"10th-Percentile 100-m Wind Speed (m/s), {month_name[month_select]}, {year_start}-{year_end}")

cf2 = ax2.contourf(  
    lon2d,
    lat2d,
    wind_10_percentile,
    cmap="PuRd",
    transform=ccrs.PlateCarree(),
    transform_first = True
)

cbar2 = plt.colorbar(cf2, location='right')
cbar2.set_label("100-m Wind Speed (m/s)")

# 5th-Percentile Map #
fig_5percentile = plt.figure(figsize=(10, 6))

# Map configuration #
ax3 = plt.axes(projection=ccrs.PlateCarree(central_longitude=134))
ax3.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())

# Add map features #
ax3.coastlines()
ax3.add_feature(cfeature.BORDERS, linestyle=':')
ax3.add_feature(cfeature.LAND, alpha=0.3)
ax3.add_feature(cfeature.OCEAN, alpha=0.2)

# Add title #
ax3.set_title(f"5th-Percentile 100-m Wind Speed (m/s), {month_name[month_select]}, {year_start}-{year_end}")

cf3 = ax3.contourf(  
    lon2d,
    lat2d,
    wind_5_percentile,
    cmap="PuRd",
    transform=ccrs.PlateCarree(),
    transform_first = True
)

cbar3 = plt.colorbar(cf3, location='right')
cbar3.set_label("100-m Wind Speed (m/s)")
