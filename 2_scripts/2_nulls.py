from timeit import default_timer as timer
import os
from inquirer import List, prompt
import numpy as np
from neuromaps.nulls import burt2020

CBF_file_names = [ # names of CBF files
    'CBF_no_cov', # no covariates
    'CBF_cov_age_gender', # 2 covariates: age, sex
    'CBF_cov_age_gender_caffeine_nicotine', # all 4 covariates: age, sex, coffee, cigarettes
    'O-LIFE-UE', # O-LIFE-UE regression
    'O-LIFE-IA', # O-LIFE-IA regression
    'O-LIFE-CD' # O-LIFE-CD regression
]

# Nulls take about 20 minutes to generate, so instead of looping through all 6 files at once, the next line 
# will ask the user for input on which nulls to generate on this run of the code

which_CBF_nulls = [List('CBF_choice',
                        message="Which nulls would you like to generate?",
                        choices=CBF_file_names)]
answers = prompt(which_CBF_nulls) # prompt the user to select one of the CBF maps

CBF_null = answers['CBF_choice'] # save the answer here as the name of the file chosen

start = timer()
print(f"Generating nulls for {CBF_null}. Please wait...")

# File paths
main_folder='/Users/juliamarcinkowska/Desktop/MSc_THESIS/DataAnalysis/emorisk_2/'
CBF_dir=os.path.join(main_folder, '3_results', '3.1_parcellations/')
outpath=os.path.join(main_folder, '3_results', '3.2_nulls/')

# Null settings
scale = '122'
seed = 1212

# Parcellation atlas
schaefer = main_folder+'1_data/Parcellation_atlas/Schaefer2018_100Parcels_7Networks_Xiao_2019_SubCorSeg_resampled_asl.nii'

# Load the parcellated CBF map from txt file
CBF_parcellated_map = np.loadtxt(fname=os.path.join(CBF_dir,CBF_null+'.txt'))

# Generate nulls with brainsmash burt2020
nulls = burt2020(data=CBF_parcellated_map, atlas='MNI152', density='2mm',
                       n_perm=5000, seed=seed, parcellation=schaefer)

np.save(outpath+'nulls_'+CBF_null+'_'+scale+'.npy', nulls)

end = timer()
runtime=round(end-start, 2)

if runtime>60:
    runtime=round(runtime/60,0)
    unit='min'
else:
    unit='s'

print(f"Finished generating nulls. Runtime: {runtime} {unit}")