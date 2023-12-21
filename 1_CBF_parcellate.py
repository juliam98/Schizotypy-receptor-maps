"""
Parcellate volumetric PET images
"""
import pandas as pd
import os

main_folder='/Users/juliamarcinkowska/Desktop/MSc_THESIS/DataAnalysis/emorisk_2/'
CBF_dir=os.path.join(main_folder, '1_data', 'CBF_files/')
outpath=os.path.join(main_folder, '3_results', '3.1_parcellations/')

CBF_files = [
    'CBF_threshold_1_no_covariates', # no covariates
    'CBF_threshold_1_age_sex_coffee_cigs', # all 4 covariates: age, sex, coffee, cigarettes
    'Difference_map'
]

import numpy as np
from neuromaps.parcellate import Parcellater

# scale = 'scale100'

schaefer = main_folder+'1_data/Parcellation_atlas/Schaefer2018_100Parcels_7Networks_Xiao_2019_SubCorSeg_resampled_asl.nii'

parcellated = {}
parcellater = Parcellater(schaefer, 'MNI152')
for CBF_map in CBF_files:
    CBF_path = os.path.join(CBF_dir, CBF_map+'.nii')
    parcellated[CBF_map] = parcellater.fit_transform(CBF_path, 'MNI152', True)
    np.savetxt(os.path.join(outpath,CBF_map+'.txt'), np.transpose(parcellated[CBF_map]))
    
print('Done!')