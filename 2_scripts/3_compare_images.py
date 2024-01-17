from neuromaps import stats
import os
import time
import numpy as np
import pandas as pd

main_folder='/Users/juliamarcinkowska/Desktop/MSc_THESIS/DataAnalysis/emorisk_2/'
Parcellations_dir=os.path.join(main_folder, '3_results', '3.1_parcellations/')
PET_dir=os.path.join(main_folder, '1_data', 'PET_maps/')
nullpath=os.path.join(main_folder, '3_results', '3.2_nulls')
outpath=os.path.join(main_folder, '3_results', '3.3_correlations')

atlas_names = [ # names of receptor atlas files
    'D1_sch23390_kaller2017', #D1
    'D2_fallypride_jaworska2020', # D2
    'DAT_fpcit_dukart2018', #DAT
    'GABAa5_Ro15_10hc_lukow', #GABAa5
    'GABAbz_flumazenil_norgaard2021', #GABAbz
    'mGluRR5_abp688_smart2019', # mGluR5
    'NMDA_ge179_galovic2021', # NMDA
    'SV2A_ucbj_finnema2016' # SV2A
]
# full receptor atlas paths
atlas_paths = [os.path.join(Parcellations_dir, (atlas_names[a])+'.txt') for a in range(len(atlas_names))]

CBF_file_names = [ # names of CBF files
    'CBF_no_cov', # no covariates
    'CBF_cov_age_gender', # 2 covariates: age, sex
    'CBF_cov_age_gender_caffeine_nicotine', # all 4 covariates: age, sex, coffee, cigarettes
    'O-LIFE-UE', # O-LIFE-UE regression
    'O-LIFE-IA', # O-LIFE-IA regression
    'O-LIFE-CD' # O-LIFE-CD regression
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
results = pd.DataFrame(columns=['corr','pval','sign?'], index=atlas_names)

for CBF_map in CBF_parcellated_paths:
    CBF_index = CBF_parcellated_paths.index(CBF_map) # get current number of iteration 
    print(f'Calculating correlations of {CBF_file_names[CBF_index]} with each atlas...')
    CBF_data=np.loadtxt(CBF_map)
    nulls=np.load(CBF_null_paths[CBF_index])
    for parcellated_atlas in atlas_paths:
        # DATA
        iteration = atlas_paths.index(parcellated_atlas) # get current number of ieration 
        map_name = atlas_names[iteration] # get the filename from atlas_names list using iteration as index
        atlas = np.loadtxt(parcellated_atlas) # load parcellated receptor atlas values
        # CALCULATE CORRELATIONS
        corr, pval = stats.compare_images(CBF_data, atlas, metric='spearmanr', nulls=nulls)
        # ADD RESULTS TO THE DF
        results.at[map_name, 'corr'] = round(corr,4)
        results.at[map_name, 'pval'] = round(pval,4)
        # CHECK IF P VALUES ARE SIGNIFICANT
        if pval<=0.05:
            results.at[map_name, 'sign?'] = 'Y'
        else:
            results.at[map_name, 'sign?'] = 'N'
    print(results)
    results.to_csv(os.path.join(outpath, CBF_file_names[CBF_index]+'_correlations.csv'),index_label='Atlas')
    file = open(main_folder+'4_figures/README.md', "a")
    file.write("\n\n")
    file.write(CBF_file_names[CBF_index])
    file.write("\n")
    results.to_markdown(file, mode='at', **{'tablefmt':"github"})
    file.close()
    time.sleep(0.1)
