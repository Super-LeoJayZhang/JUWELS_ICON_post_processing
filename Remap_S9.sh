########################################################
# Lijie Zhang (FZJ-IBG3) 01-Dec-2020
# Run the post processing (visualization of ICON output
# with the River-like soil moisture heterogeneity input
#########################################################

# --------------
# load modules on juwels
# -------------
module load GCC/9.3.0
module load ParaStationMPI/5.4.7-1
module load CDO/1.9.8

echo "Start"

#########################################
# Remap the icon output
##########################################

# ----------------------
# Define the work path
# ----------------------
export WORKDIR=/p/scratch/cslts/zhang23/JUWELS_RiverLike
export FOLDER_S9=$WORKDIR/S9.6_x192_y192_e70m_011220-163621
export FOLDER_REMAP=$WORKDIR/post_processing_python/REMAP
if [ ! -d $FOLDER_REMAP ]
then
	mkdir $FOLDER_REMAP
fi


export FILE_INSTA=$FOLDER_S9/River_like_S9.6_wso5_river1_24h_insta_DOM01_ML_0001.nc
export FILE_RAD=$FOLDER_S9/River_like_S9.6_wso5_river1_24h_rad_DOM01_ML_0001.nc
export FILE_LAND=$FOLDER_S9/River_like_S9.6_wso5_river1_24h_land_DOM01_ML_0001.nc
export FILE_PROF=$FOLDER_S9/River_like_S9.6_wso5_river1_24h_profile.nc
export FILE_TSERIES=$FOLDER_S9/River_like_S9.6_wso5_river1_24h_tseries.nc

export TARGET_GRID_DESCRIPTION=$WORKDIR/post_processing_python/grid_description_x192_y192_e70m
export WEIGHTS_FILE=$FOLDER_REMAP/weights_torus_x192_y192_e70m.nc

export FILE_INSTA_REMAP=$FOLDER_REMAP/Remap_River_like_S9.6_wso5_river1_24h_insta_DOM01_ML_0001.nc
export FILE_RAD_REMAP=$FOLDER_REMAP/Remap_River_like_S9.6_wso5_river1_24h_rad_DOM01_ML_0001.nc
export FILE_LAND_REMAP=$FOLDER_REMAP/Remap_River_like_S9.6_wso5_river1_24h_LAND_DOM01_ML_0001.nc


cd $FOLDER_REMAP

# Create the weight file for x192_y192_e70m.
cdo gendis,$TARGET_GRID_DESCRIPTION $FILE_INSTA $WEIGHTS_FILE

# Remap
cdo remap,$TARGET_GRID_DESCRIPTION,$WEIGHTS_FILE $FILE_INSTA $FILE_INSTA_REMAP
cdo remap,$TARGET_GRID_DESCRIPTION,$WEIGHTS_FILE $FILE_LAND $FILE_LAND_REMAP
cdo remap,$TARGET_GRID_DESCRIPTION,$WEIGHTS_FILE $FILE_RAD $FILE_RAD_REMAP

cp $FILE_PROF .
cp $FILE_TSERIES .

echo "Finished remapping!"
