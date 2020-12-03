"""
--------------------------
File Name:  insta_visualization_v01
Author: zhang (FZJ/IBG3)
Contact: leojayak@gmail.com
Date: 22.11.20

Description: To visualize the output from ICON-LEM (torus).
            The output data has already been remap through cdo.
--------------------------
"""

# -----------------------
# Packages
# -----------------------
import os
import matplotlib.pyplot as plt
import numpy as np
import netCDF4 as nc
import geocat.ncomp


def calculate_turbulent(ds):
    """
    :param ds: Input arrays of the wind (e.g. v3d, w3d, u3d).
    :return: Wind turbulence.
    """
    # make a copy of the input array.
    ds_turbulent = ds.copy()
    ds_turbulent[:] = np.nan

    # Loops to calculate every time step.
    wind_mean = np.mean(ds, 0)  # average along time [height_layer, lat, lon]
    for count_i in np.arange(0, ds.shape[0]):
        ds_turbulent[count_i, :, :, :] = ds[count_i, :, :, :] - wind_mean

    # Return the wind turbulent array [time, height_layer, lat, lon]
    return ds_turbulent


# -----------------
# Parameters.
# ------------------
g = 9.8  # [m/s-2]
cp = 1004.64    # heat capacity

# ---------------------------------
# Work Direction and file path.
# ---------------------------------
#work_dir = r'/home/zhang/practise/remap_torus'  # Work directory.
work_dir = r'/p/scratch/cslts/zhang23/JUWELS_RiverLike/post_processing_python/REMAP'
os.chdir(work_dir)

folder_output = 'visualization_output'  # folder for the output figures.
if not os.path.exists(folder_output):
    os.mkdir(folder_output)

#file_insta = "remap_river_insta.nc"  # insta
#file_land = "remap_river_land.nc"  # land
#file_rad = "remap_river_rad.nc"  # rad
#file_prof = "nh_cbl_river_like_x70y70_wso055_06h_profile.nc"  # profile
#file_tseries = "nh_cbl_river_like_x70y70_wso055_06h_tseries.nc"  # time-series.

file_insta = "Remap_River_like_S9.6_wso5_river1_24h_insta_DOM01_ML_0001.nc"
file_land = "Remap_River_like_S9.6_wso5_river1_24h_LAND_DOM01_ML_0001.nc"
file_rad = "Remap_River_like_S9.6_wso5_river1_24h_rad_DOM01_ML_0001.nc"
file_prof = "River_like_S9.6_wso5_river1_24h_profile.nc"
file_tseries = "River_like_S9.6_wso5_river1_24h_tseries.nc"



# ------------------------------
# Open and read data.
# ------------------------------
nc_insta = nc.Dataset(file_insta, "r")
nc_land = nc.Dataset(file_land, "r")
nc_rad = nc.Dataset(file_rad, "r")
nc_prof = nc.Dataset(file_prof, "r")
nc_tseries = nc.Dataset(file_tseries, "r")

z_ifc = nc_insta["z_ifc"][:, 1, 1]  # geometric_height_at_half_level_center, (65: 3200 to 0 by 50 m).
z_mc = nc_insta["z_mc"][:, 1, 1]  # geometric_height_at_full_level_center, (64: 3175 to 25 by 50 m).

lat = nc_insta["lat"][:].astype(float)  # Longitudes.
lon = nc_insta["lon"][:].astype(float)  # Latitudes.

v3d = nc_insta["v"][:]  # wind velocity at horizontal v [time, z_ifc, lat, lon]
w3d = nc_insta["w"][:]  # wind velocity at vertical w [time, z_ifc, lat, lon]
u3d = nc_insta["u"][:]  # wind velocity at horizontal u [time, z_ifc, lat, lat]

# ------------------------------------------
# Calculate the phase-correlated wind speed.
# -------------------------------------------
v3d_avg_x = np.mean(v3d, 3)
w3d_avg_x = np.mean(w3d, 3)  # Average along y (mean of lon)

v3d_avg_x_t = np.mean(v3d_avg_x, 0)  # Mean of time.  (z_ifc, lat)
w3d_avg_x_t = np.mean(w3d_avg_x, 0)

# Interpolates a regular grid to a rectilinear one using bi-linear interpolation.
w3d_avg_x_t_linint2 = geocat.ncomp.linint2(w3d_avg_x_t, icycx=False, xo=lat, yo=z_mc, xi=lat, yi=z_ifc)

v_prof_avg_x_t = np.mean(v3d_avg_x_t, 1)  # Profile average (65,)
w_prof_avg_x_t = np.mean(w3d_avg_x_t_linint2, 1)  # Profile average (64,)

v_phase = v3d_avg_x_t.copy()
w_phase = w3d_avg_x_t_linint2.copy()
for idx_y in np.arange(0, len(lat)):
    v_phase[:, idx_y] = v3d_avg_x_t[:, idx_y] - v_prof_avg_x_t
    w_phase[:, idx_y] = w3d_avg_x_t_linint2[:, idx_y] - w_prof_avg_x_t

# ----------------------------------------
# calculate convective velocity scale: w*.
# ----------------------------------------
tsfc = nc_land['t_g']  # Weighted Surface Temperature.
wth = nc_prof['wth']  # Resolved Potential Temperature Flux.
shfl_s = nc_land['shfl_s']  # Surface Sensible Head Flux
rho = nc_insta['rho'][:, -1, :, :]  # Air Density at the lowest layer.

shfl_s_avg = np.mean(np.mean(shfl_s, -1), -1)   # Domain-average.

pbl = z_mc[np.argmin(wth[24, :])]  # Let's assume the time 6h.

# convective velocity scale.
w_star = ((g / tsfc[24, :, :]) * pbl * (-shfl_s_avg[24] / (rho[24, :, :] * cp))) ** (1 / 3)
w_star = np.mean(np.array(w_star))

# --------------------
# visualization
# --------------------

result_w = np.flipud(w_phase / w_star)[0:32, :]
plt.contourf(result_w, cmap="bwr", levels=np.arange(-0.6, 0.61, 0.2))
#plt.colorbar()
cbar = plt.colorbar()
cbar.set_label('[m/s]', rotation=0, fontsize=14, y=1.07, labelpad=-40)

plt.xticks(ticks=[0, 48, 96, 144, 192], labels=[0, '', 0.5, '', 1])
plt.xlabel("x/\u03BB", fontsize=14)
plt.yticks(ticks=[0, 8, 16, 24, 31], labels=[0, 0.3, 0.6, 0.9, 1.2])
plt.ylabel("z/z_i", fontsize=14)
plt.savefig(os.path.join(folder_output, "w_phase.png"))
plt.close()


result_v = np.flipud(v_phase / w_star)[0:32, :]
plt.contourf(result_v, cmap="bwr", levels=np.arange(-2, 2.01, 0.2))
#plt.colorbar()
cbar = plt.colorbar()
cbar.set_label('[m/s]', rotation=0, fontsize=14, y=1.07, labelpad=-40)
plt.yticks(ticks=[0, 8, 16, 24, 31], labels=[0, 0.3, 0.6, 0.9, 1.2])
plt.xticks(ticks=[0, 48, 96, 144, 192], labels=[0, '', 0.5, '', 1])
plt.xlabel("x/\u03BB", fontsize=14)
plt.ylabel("z/z_i", fontsize=14)
plt.savefig(os.path.join(folder_output, "v_phase.png"))
plt.close()

# ---------------------
# Calculate the TKE (Turbulence Kinetic Energy).
# ---------------------
v_turbulent = calculate_turbulent(v3d)
u_turbulent = calculate_turbulent(u3d)
w_turbulent = calculate_turbulent(w3d)

# Calculate the turbulence kinetic energy (TKE).
tke = np.arange(v_turbulent.shape[0]).astype(float)
for count_i in np.arange(v_turbulent.shape[0]):
    tke[count_i] = np.mean((v_turbulent[count_i, :] ** 2 + u_turbulent[count_i, :] ** 2 + \
                           w_turbulent[count_i, 0:64, :, :] ** 2) * (1 / 2))

plt.plot(tke/(w_star ** 2))
plt.xticks(np.arange(0, 96.01, 8), labels=np.arange(0, 24.01, 2))
plt.xlabel("Time [h]", fontsize=16)
plt.ylabel("TKE/$w{*}^2$ [-]", fontsize=16)
plt.savefig(os.path.join(folder_output, "TKE.png"))
plt.close()

# ----------------------------------------------
# Visualization of the latent/sensible heat flux
# ----------------------------------------------

shfl_s = nc_land['shfl_s']  # Surface Sensible Heat Flux
lhfl_s = nc_land['lhfl_s']  # Surface Latent Heat Flux

shfl_s_avg = np.mean(shfl_s)                        # Domain-temporal average.
shfl_s_avg_t_y = np.mean(np.mean(shfl_s, 0), 1)     # y-axis and temporal average.

plt.plot(shfl_s_avg_t_y/shfl_s_avg)                 # Plot the shfl_s_avg_t_y / shfl_s_avg
plt.xticks(np.arange(0, 192.01, 48), labels=[0,'', 0.5, '', 1])
plt.xlabel("x/\u03BB", fontsize=12)
plt.yticks([0, 0.3, 0.6, 0.9, 1.2, 1.5], labels=[0, 0.3, 0.6, 0.9, 1.2, 1.5])
plt.ylabel("shfl_s/<shfl_s>", fontsize=12)
plt.savefig(os.path.join(folder_output, 'Sensible_heat_flux.png'))
plt.close()

lhfl_s_avg = np.mean(lhfl_s)
lhfl_s_avg_t_y = np.mean(np.mean(lhfl_s, 0), 1)

plt.plot(lhfl_s_avg_t_y/lhfl_s_avg)
plt.xticks(np.arange(0, 192.01, 48), labels=[0, '', 0.5, '', 1])
plt.xlabel("x/\u03BB", fontsize=12)
plt.yticks([0, 1, 2, 3], labels=[0, 1, 2, 3])
plt.ylabel("lhfl_s/<lhfl_s>", fontsize=12)
plt.savefig(os.path.join(folder_output, "latent_heat_flux.png"))
plt.close()
