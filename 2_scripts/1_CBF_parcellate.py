import pandas as pd
import os

main_folder=os.getcwd()
CBF_dir=os.path.join(main_folder, '1_data', 'CBF_files/')
outpath=os.path.join(main_folder, '3_output', '3.1_parcellations/')

CBF_file_names = [ # names of CBF files
    'CBF_no_cov', # no covariates
    'CBF_cov_age_gender', # 2 covariates: age, sex
    'CBF_cov_age_gender_caffeine_nicotine', # all 4 covariates: age, sex, coffee, cigarettes
    'O-LIFE-UE', # O-LIFE-UE regression
    'O-LIFE-IA', # O-LIFE-IA regression
    'O-LIFE-CD', # O-LIFE-CD regression
    'O-LIFE-UE-covars', # O-LIFE-UE regression with covariates
    'O-LIFE-IA-covars', # O-LIFE-IA regression with covariates
    'O-LIFE-CD-covars', # O-LIFE-CD regression with covariates
]

import numpy as np
from neuromaps.parcellate import Parcellater

# scale = 'scale100'

schaefer = os.path.join(main_folder, '1_data', 'Parcellation_atlas/', 'Schaefer2018_100Parcels_7Networks_Xiao_2019_SubCorSeg_resampled_asl.nii')

parcellated = {}
parcellater = Parcellater(parcellation=schaefer, space='MNI152', resampling_target='parcellation')
for CBF_map in CBF_file_names:
    CBF_path = os.path.join(CBF_dir, CBF_map+'.nii')
    parcellated[CBF_map] = parcellater.fit_transform(data=CBF_path, space='MNI152', ignore_background_data=True)
    parcellater.fit()
    np.savetxt(os.path.join(outpath,CBF_map+'.txt'), np.transpose(parcellated[CBF_map]))
    
print('Done!')