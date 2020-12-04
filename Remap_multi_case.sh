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
export FOLDER_S9=S9.6_x192_y192_e70m_011220-163621
export FOLDER_S4=S4.8_x192_y192_e70m_011220-163631
export FOLDER_S2=S2.4_x192_y192_e70m_011220-163641
export FOLDER_S1=S1.2_x192_y192_e70m_011220-163651
export FOLDER_S0=S0.6_x192_y192_e70m_011220-163710

# Define the remap folder.
export FOLDER_REMAP=$WORKDIR/REMAP
if [ ! -d $FOLDER_REMAP ]
then
        mkdir $FOLDER_REMAP
fi
cd $FOLDER_REMAP
export TARGET_GRID_DESCRIPTION=$FOLDER_REMAP/grid_description_x192_y192_e70m
export WEIGHTS_FILE=$FOLDER_REMAP/weights_torus_x192_y192_e70m.nc


# Loops of the difference cases.
for FOLDER_IN in $FOLDER_S0 $FOLDER_S1 $FOLDER_S2 $FOLDER_S4 $FOLDER_9
do
	echo "Processing of $FOLDER_IN"		# MARK THE process
        case ${FOLDER_IN:1:1} in
                0)
                        STR0=River_like_S0.6_wso5_river16
                        ;;
                1)
                        STR0=River_like_S1.2_wso5_river8
                        ;;
                2)
                        STR0=River_like_S2.4_wso5_river4
                        ;;
                4)
                        STR0=River_like_S4.8_wso5_river2
                        ;;
                9)
                        STR0=River_like_S9.6_wso5_river1
                        ;;
                *)
        esac

	# Define the file path.
        export FILE_INSTA=$WORKDIR/$FOLDER_IN/${STR0}_24h_insta_DOM01_ML_0001.nc
        export FILE_RAD=$WORKDIR/$FOLDER_IN/${STR0}_24h_rad_DOM01_ML_0001.nc
	export FILE_LAND=$WORKDIR/$FOLDER_IN/${STR0}_24h_land_DOM01_ML_0001.nc
	export FILE_PROF=$WORKDIR/$FOLDER_IN/${STR0}_24h_profile.nc
	export FILE_TSERIES=$WORKDIR/$FOLDER_IN/${STR0}_24h_tseries.nc
 
	export FILE_INSTA_REMAP=$FOLDER_REMAP/Remap_${STR0}_24h_insta_DOM01_ML_0001.nc
	export FILE_RAD_REMAP=$FOLDER_REMAP/Remap_${STR0}_24h_rad_DOM01_ML_0001.nc
	export FILE_LAND_REMAP=$FOLDER_REMAP/Remap_${STR0}_24h_LAND_DOM01_ML_0001.nc

	# create the weight file if it does not exist
	if [ ! -f "$WEIGHTS_FILE" ];then
		echo "Creating $WEIGHTS_FILE"
		cdo gendis,$TARGET_GRID_DESCRIPTION $FILE_INSTA $WEIGHTS_FILE
		echo "Created $WEIGHTS_FILE" 
	fi
		
	# remap
	cdo remap,$TARGET_GRID_DESCRIPTION,$WEIGHTS_FILE $FILE_INSTA $FILE_INSTA_REMAP
	cdo remap,$TARGET_GRID_DESCRIPTION,$WEIGHTS_FILE $FILE_LAND $FILE_LAND_REMAP
	cdo remap,$TARGET_GRID_DESCRIPTION,$WEIGHTS_FILE $FILE_RAD $FILE_RAD_REMAP
	
	# copy the prof and tseries
	cp $FILE_PROF .
	cp $FILE_TSERIES .
done

