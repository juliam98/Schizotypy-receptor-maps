import pandas as pd
import os

main_folder=os.getcwd()
PET_dir=os.path.join(main_folder, '1_data', 'PET_maps/')
outpath=os.path.join(main_folder, '3_output', '3.1_parcellations/')

atlas_names = [ # names of receptor atlas files
    'D1_sch23390_kaller2017', #D1
    'D2_fallypride_jaworska2020', # D2
    'DAT_fpcit_dukart2018', #DAT
    'FDOPA_fluorodopa_hc12_gomez', #FDOPA
    'GABAa5_Ro15_10hc_lukow', #GABAa5
    'GABAbz_flumazenil_norgaard2021', #GABAbz
    'mGluRR5_abp688_smart2019', # mGluR5
    'NMDA_ge179_galovic2021' # NMDA
]

import numpy as np
from neuromaps.parcellate import Parcellater

# scale = 'scale100'

schaefer = os.path.join(main_folder, '1_data', 'Parcellation_atlas/', 'Schaefer2018_100Parcels_7Networks_Xiao_2019_SubCorSeg_resampled_asl.nii')

parcellated = {}
parcellater = Parcellater(parcellation=schaefer, space='MNI152', resampling_target='parcellation')

for PET_atlas in atlas_names:
    atlas_file = os.path.join(PET_dir, PET_atlas+'.nii.gz')
    parcellated[PET_atlas] = parcellater.fit_transform(data=atlas_file, space='MNI152', ignore_background_data=True)
    np.savetxt(outpath+PET_atlas+'.txt', np.transpose(parcellated[PET_atlas]))
    
print('Done!')