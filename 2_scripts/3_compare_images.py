from neuromaps import stats
import os
import time
import itertools
import numpy as np
import pandas as pd

main_folder=os.getcwd()
Parcellations_dir=os.path.join(main_folder, '3_output', '3.1_parcellations/')
PET_dir=os.path.join(main_folder, '1_data', 'PET_maps/')
nullpath=os.path.join(main_folder, '3_output', '3.2_nulls')
outpath=os.path.join(main_folder, '3_output', '3.3_correlations')

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
# full receptor atlas paths
atlas_paths = [os.path.join(Parcellations_dir, (atlas_names[a])+'.txt') for a in range(len(atlas_names))]

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

# full CBF null files paths
CBF_null_paths = [os.path.join(nullpath, 'nulls_'+(CBF_file_names[a])+'_122.npy') for a in range(len(CBF_file_names))]
CBF_parcellated_paths = [os.path.join(Parcellations_dir, (CBF_file_names[a])+'.txt') for a in range(len(CBF_file_names))]

# load nulls
nulls_CBF_threshold_1_no_covariates = np.load(CBF_null_paths[1])

# load data
CBF_parcellated_no_covariates=np.loadtxt(CBF_parcellated_paths[0])
CBF_parcellated_age_sex_coffee_cigs=np.loadtxt(CBF_parcellated_paths[1])

# Empty dataframe to assign results into
idx_pairs = list(itertools.product(CBF_file_names, atlas_names))
index = pd.MultiIndex.from_tuples(idx_pairs, names=["CBF_map", "atlas"])
results = pd.DataFrame(columns=['corr','pval','sign?'], index=index)

# Compute the correlations and assign to the above df
for CBF_idx in range(len(CBF_parcellated_paths)):
    print(f'Calculating correlations of {CBF_file_names[CBF_idx]} with each atlas...')
    CBF_data=np.loadtxt(CBF_parcellated_paths[CBF_idx]) # Load parcellated CBF maps data
    nulls=np.load(CBF_null_paths[CBF_idx]) # Load the nulls
    # Iterate through each atlas
    for atlas_idx in range(len(atlas_names)):
        atlas_data = np.loadtxt(atlas_paths[atlas_idx]) # load parcellated receptor atlas values
        # CALCULATE CORRELATIONS
        corr, pval = stats.compare_images(CBF_data, atlas_data, metric='spearmanr', nulls=nulls)
        # ADD RESULTS TO THE DF
        results['corr'].at[CBF_file_names[CBF_idx], atlas_names[atlas_idx]] = round(corr,4)
        results['pval'].at[CBF_file_names[CBF_idx], atlas_names[atlas_idx]] = round(pval,4)
        # CHECK IF P VALUES ARE SIGNIFICANT
        if pval<=0.05:
            results['sign?'].at[CBF_file_names[CBF_idx], atlas_names[atlas_idx]] = 'Y'
        else:
            results['sign?'].at[CBF_file_names[CBF_idx], atlas_names[atlas_idx]] = 'N'
    # A nice output for a premium user experience xxx        
    print(f'Finished calculating correlations for {CBF_file_names[CBF_idx]}')
    time.sleep(0.1)

results.to_csv(os.path.join(outpath,'all_correlations.csv'),index=True, sep=',')
print('Done')