import pandas as pd
import os
import statsmodels.api as sm
from scipy.stats import zscore
import numpy as np

main_folder=os.getcwd()
Parcellations_dir=os.path.join(main_folder, '3_output', '3.1_parcellations/')
outpath=os.path.join(main_folder, '3_output', '3.4_cooks_distance')

CBF_file_names = [ # names of CBF files
    'O-LIFE-UE', # O-LIFE-UE regression
    'O-LIFE-IA', # O-LIFE-IA regression
    'O-LIFE-CD', # O-LIFE-CD regression
    'O-LIFE-IA-covars', # O-LIFE-IA regression with covariates
    'O-LIFE-CD-covars', # O-LIFE-CD regression with covariates
]

atlas_names = [ # names of receptor atlas files
    'GABAa5_Ro15_10hc_lukow', #GABAa5
    'GABAbz_flumazenil_norgaard2021', #GABAbz
    'mGluRR5_abp688_smart2019', # mGluR5
    'NMDA_ge179_galovic2021' # NMDA
]

# Get labels for some of the schaefer_2018 atlas (I couldn't find the Xiao labels anywhere, so the last 22 labels are empty)
labels_df = pd.read_csv(os.path.join('1_data', 'Parcellation_atlas', 'Schaefer2018_100Parcels_7Networks_Xiao_2019_SubCorSeg_resampled_asl.csv'), usecols=['id', 'label', 'hemisphere'])

# Assign all receptor density values to one dataframe
atlas_paths = [os.path.join(Parcellations_dir, (atlas_names[a])+'.txt') for a in range(len(atlas_names))]
receptor_pracellations = pd.DataFrame(columns=atlas_names)
for atlas in range(len(atlas_paths)):
    receptor_pracellations[atlas_names[atlas]] = pd.read_csv(atlas_paths[atlas], header=None)

# Assign all CBF values to one dataframe
CBF_parcellated_paths = [os.path.join(Parcellations_dir, (CBF_file_names[a])+'.txt') for a in range(len(CBF_file_names))]
CBF_pracellations = pd.DataFrame(columns=CBF_file_names)
for CBF_map in range(len(CBF_parcellated_paths)):
    CBF_pracellations[CBF_file_names[CBF_map]] = pd.read_csv(CBF_parcellated_paths[CBF_map], header=None)

CBF_pracellations_z = zscore(CBF_pracellations)

schaefer = os.path.join(main_folder, '1_data', 'Parcellation_atlas/', 'Schaefer2018_100Parcels_7Networks_Xiao_2019_SubCorSeg_resampled_asl.nii')

# Empty dataframe to assign results into
cooks_distance_df = pd.DataFrame()

# Compute the correlations and assign to the above df
for column_no in range(len(CBF_pracellations_z.columns)):
    
    y = CBF_pracellations_z[CBF_file_names[column_no]]

    # Linear regression model
    model = sm.OLS(endog=y, exog=receptor_pracellations).fit()

    # Calculate Cook's distance
    influence = model.get_influence()
    cooks_distance = influence.cooks_distance[0]
    cooks_distance_df[CBF_file_names[column_no]] = cooks_distance


# Save all rersults into one csv file
cooks_distance_df.to_csv(path_or_buf=outpath+"/all_cooks_distance_results.csv", sep=",")

# Sort cook distance values for each CBF comparison and save in separate files
for CBF_comparison in range(len(CBF_file_names)):
    print(f"\nSorted results for {CBF_file_names[CBF_comparison]}:")
    # extract a singe column of the cooks_distance_df dataframe to sort
    single_col_cooks = cooks_distance_df[CBF_file_names[CBF_comparison]]

    # extract indices of cooks_distance_df sorted from largest to smallest (only first 20 values)
    sorted_cooks_idx = single_col_cooks.argsort()[::-1]

    # sort the values
    values_sorted = single_col_cooks[sorted_cooks_idx]

    # get the labels of brain regions for the rergions (i.e. reorder the indices)
    label_idx_sorted = labels_df['id'][sorted_cooks_idx]
    labels_sorted = labels_df['label'][sorted_cooks_idx]

    # Join into one df
    cooks_sorted_df = pd.concat([label_idx_sorted, values_sorted, labels_sorted], ignore_index=True, axis=1)
    cooks_sorted_df.columns=['id', 'values', 'labels']

    print(cooks_sorted_df)
    cooks_sorted_df.to_csv(path_or_buf=os.path.join(outpath,CBF_file_names[CBF_comparison]+'_cook_sorted.csv'), index=False)
    