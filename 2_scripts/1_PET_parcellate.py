# '    ____                         _  _         _          ____   _____  _____          _    _                        
# '   |  _ \  __ _  _ __  ___  ___ | || |  __ _ | |_  ___  |  _ \ | ____||_   _|   __ _ | |_ | |  __ _  ___   ___  ___ 
# '   | |_) |/ _` || '__|/ __|/ _ \| || | / _` || __|/ _ \ | |_) ||  _|    | |    / _` || __|| | / _` |/ __| / _ \/ __|
# '   |  __/| (_| || |  | (__|  __/| || || (_| || |_|  __/ |  __/ | |___   | |   | (_| || |_ | || (_| |\__ \|  __/\__ \
# '   |_|    \__,_||_|   \___|\___||_||_| \__,_| \__|\___| |_|    |_____|  |_|    \__,_| \__||_| \__,_||___/ \___||___/
# '                                                                                                                                                                         

import pandas as pd
import os

main_folder='/Users/juliamarcinkowska/Desktop/MSc_THESIS/DataAnalysis/emorisk_2/'
PET_dir=os.path.join(main_folder, '1_data', 'PET_maps/')
outpath=os.path.join(main_folder, '3_results', '3.1_parcellations/')

atlas_names = [
    'D1_sch23390_kaller2017', #D1
    'D2_fallypride_jaworska2020', # D2
    'DAT_fpcit_dukart2018', #DAT
    'GABAa5_Ro15_10hc_lukow', #GABAa5
    'GABAbz_flumazenil_norgaard2021', #GABAbz
    'mGluRR5_abp688_smart2019', # mGluR5
    'NMDA_ge179_galovic2021', # NMDA
    'SV2A_ucbj_finnema2016' # SV2A
]

import numpy as np
from neuromaps.parcellate import Parcellater

# scale = 'scale100'

schaefer = main_folder+'1_data/Parcellation_atlas/Schaefer2018_100Parcels_7Networks_Xiao_2019_SubCorSeg_resampled_asl.nii'

parcellated = {}
parcellater = Parcellater(schaefer, 'MNI152')

for PET_atlas in atlas_names:
    atlas_file = os.path.join(PET_dir, PET_atlas+'.nii.gz')
    parcellated[PET_atlas] = parcellater.fit_transform(atlas_file, 'MNI152', True)
    np.savetxt(outpath+PET_atlas+'.txt', np.transpose(parcellated[PET_atlas]))
    
print('Done!')