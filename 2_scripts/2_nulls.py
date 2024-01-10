from timeit import default_timer as timer
import os
import time
import numpy as np
from neuromaps.nulls import burt2020

start = timer()
print("Generating nulls")

main_folder='/Users/juliamarcinkowska/Desktop/MSc_THESIS/DataAnalysis/emorisk_2/'
CBF_dir=os.path.join(main_folder, '3_results', '3.1_parcellations/')
outpath=os.path.join(main_folder, '3_results', '3.2_nulls/')

scale = '122'

schaefer = main_folder+'1_data/Parcellation_atlas/Schaefer2018_100Parcels_7Networks_Xiao_2019_SubCorSeg_resampled_asl.nii'

CBF_file_names = [ # names of CBF files
    'CBF_no_cov', # no covariates
    'CBF_cov_age_gender', # 2 covariates: age, sex
    'CBF_cov_age_gender_caffeine_nicotine', # all 4 covariates: age, sex, coffee, cigarettes
    'O-LIFE-UE-con_0001', # O-LIFE-UE regression
    'O-LIFE-IA-con_0001', # O-LIFE-IA regression
    'O-LIFE-CD-con_0001' # O-LIFE-CD regression
]

CBF_parcellated_map1 = np.loadtxt(fname=os.path.join(CBF_dir,CBF_file_names[0]+'.txt'))
CBF_parcellated_map2 = np.loadtxt(fname=os.path.join(CBF_dir,CBF_file_names[1]+'.txt'))

# # Generate nulls with brainsmash burt2020
nulls1 = burt2020(data=CBF_parcellated_map2, atlas='MNI152', density='2mm',
                       n_perm=5000, seed=1212, parcellation=schaefer)

np.save(outpath+'nulls_'+CBF_file_names[1]+'_'+scale+'.npy', nulls1)

end = timer()
runtime=round(end-start, 2)

if runtime>60:
    runtime=round(runtime/60,0)
    unit='min'
else:
    unit='s'

print(f"Finished generating nulls. Runtime: {runtime} {unit}")