import pandas as pd
import os

main_folder='/Users/juliamarcinkowska/Desktop/MSc_THESIS/DataAnalysis/emorisk_2/'
corr_dir=os.path.join(main_folder, '3_results', '3.3_correlations')

CBF_file_names = [ # names of CBF files
    'CBF_no_cov', # no covariates
    'CBF_cov_age_gender', # 2 covariates: age, sex
    'CBF_cov_age_gender_caffeine_nicotine', # all 4 covariates: age, sex, coffee, cigarettes
    'O-LIFE-UE', # O-LIFE-UE regression
    'O-LIFE-IA', # O-LIFE-IA regression
    'O-LIFE-CD' # O-LIFE-CD regression
]

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

# full CBF files paths
corr_paths= [os.path.join(corr_dir, (CBF_file_names[a])+'_correlations.csv') for a in range(len(CBF_file_names))]
# extract receptor names - split by'_'
receptor_names = [atlas_names[a].split('_')[0] for a in range(len(atlas_names))]
# Join all results into one dataframe- first create empty dataframe to store the output of the loop
all_corrs = pd.DataFrame(pd.read_csv(os.path.join(corr_dir, CBF_file_names[map] +'_correlations.csv'), index_col='Atlas')['corr'] for map in range(len(CBF_file_names)))
all_corrs.index = CBF_file_names

# get p_values from a csv file (corrected for multiple comparisons)
all_pvals = pd.read_csv(corr_dir+'/all_p_values_bonferroni.csv', index_col='atlas')
asterisk = all_pvals.mask(all_pvals, '*')
asterisk = asterisk.replace(False, ' ')
print(asterisk)
# asterisk = all_pvals.where(all_pvals is False, ' ')
# print(asterisk)

# DATA VISUALISATION
import seaborn as sns
import matplotlib.pyplot as plt

CBF_labels = [ # names of CBF files
    'CBF_no_cov', # no covariates
    'CBF_cov_2', # 2 covariates: age, sex
    'CBF_cov_4', # all 4 covariates: age, sex, coffee, cigarettes
    'O-LIFE-UE', # O-LIFE-UE regression
    'O-LIFE-IA', # O-LIFE-IA regression
    'O-LIFE-CD' # O-LIFE-CD regression
]

cmap=sns.color_palette("vlag", as_cmap=True)
heatmap = sns.heatmap(all_corrs, cmap=cmap, center=0, xticklabels=receptor_names, yticklabels=CBF_labels, annot=asterisk, fmt='', square=True)
heatmap.set(xlabel="", ylabel="", title="Heatmap of spearman's correlations")
plt.tight_layout()

# plt.show()
plt.savefig(main_folder+'4_figures/heatmap.png', dpi=350)