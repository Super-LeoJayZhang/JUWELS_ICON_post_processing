"""
--------------------------
File Name:  Plot_tkvh
Author: zhang (FZJ/IBG3)
Contact: leojayak@gmail.com
Date: 03.12.20

Description:
--------------------------
"""
import os
import matplotlib.pyplot as plt
import netCDF4 as nc
import numpy as np

# Change the work direction.
work_dir = r'/p/scratch/cslts/zhang23/JUWELS_RiverLike/post_processing_python/REMAP'
os.chdir(work_dir)
# File path
file_insta = "Remap_River_like_S9.6_wso5_river1_24h_insta_DOM01_ML_0001.nc"
file_land = "Remap_River_like_S9.6_wso5_river1_24h_LAND_DOM01_ML_0001.nc"
file_rad = "Remap_River_like_S9.6_wso5_river1_24h_rad_DOM01_ML_0001.nc"
file_prof = "River_like_S9.6_wso5_river1_24h_profile.nc"
file_tseries = "River_like_S9.6_wso5_river1_24h_tseries.nc"

# Open and read the data.
nc_insta = nc.Dataset(file_insta, "r")
tkvh = nc_insta['tkvh']
tkvh = np.mean(np.mean(np.mean(tkvh, -1), -1), -1)

# Draw the data.
plt.plot(tkvh)
plt.savefig('tkvh')
plt.close()


