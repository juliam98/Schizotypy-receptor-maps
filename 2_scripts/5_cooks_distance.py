import pandas as pd
import os
import statsmodels.api as sm
from scipy.stats import zscore
import itertools
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
labels_df = pd.read_csv(os.path.join('1_data', 'Parcellation_atlas', 'Schaefer2018_100Parcels_7Networks_Xiao_2019_SubCorSeg_resampled_asl.csv'), usecols=['label', 'hemisphere'])
print(labels_df)

# Assign all receptor density values to one dataframe
atlas_paths = [os.path.join(Parcellations_dir, (atlas_names[a])+'.txt') for a in range(len(atlas_names))]
receptor_pracellations = pd.DataFrame(columns=atlas_names)
for atlas in range(len(atlas_paths)):
    receptor_pracellations[atlas_names[atlas]] = pd.read_csv(atlas_paths[atlas])

# Assign all CBF values to one dataframe
CBF_parcellated_paths = [os.path.join(Parcellations_dir, (CBF_file_names[a])+'.txt') for a in range(len(CBF_file_names))]
CBF_pracellations = pd.DataFrame(columns=CBF_file_names)
for CBF_map in range(len(CBF_parcellated_paths)):
    CBF_pracellations[CBF_file_names[CBF_map]] = pd.read_csv(CBF_parcellated_paths[CBF_map])

CBF_pracellations_z = zscore(CBF_pracellations)

schaefer = os.path.join(main_folder, '1_data', 'Parcellation_atlas/', 'Schaefer2018_100Parcels_7Networks_Xiao_2019_SubCorSeg_resampled_asl.nii')

# print(CBF_pracellations)

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

    # Save Cook's distance as a column in the DataFrame
    cooks_distance_df[column_no] = cooks_distance

    # Sort the samples by Cook's distance and extract the sample indices in order
    sorted_indices = np.argsort(cooks_distance)[::-1]

    # Create labels for each sample using its name, yeo_7, and hemisphere
    sample_labels = [f"{row.label} {row.hemisphere}" for _, row in labels_df.iterrows()]

    # Print the top 20 most important samples
    print(f"\nTop 20 most important samples column {CBF_file_names[column_no]}:")
    for i in sorted_indices[:19]:
        print(f"{sample_labels[i]}: {cooks_distance[i]:.4f}")

    # Save the top 20 most important samples to a CSV file
    top_samples = [sample_labels[i] for i in sorted_indices[:19]]
    top_cooks = [cooks_distance[i] for i in sorted_indices[:19]]
    top_df = pd.DataFrame({'Sample': top_samples, "Cook's Distance": top_cooks})
    top_df.to_csv(os.path.join(outpath,CBF_file_names[column_no]+'.csv'), index=False)
