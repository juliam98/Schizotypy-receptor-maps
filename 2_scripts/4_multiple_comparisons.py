from statsmodels.stats.multitest import multipletests
import pandas as pd
import os

main_folder=os.getcwd()
corr_dir=os.path.join(main_folder, '3_results', '3.3_correlations')

CBF_file_names = [ # names of CBF files
    'CBF_no_cov', # no covariates
    # 'CBF_cov_age_gender', # 2 covariates: age, sex
    # 'CBF_cov_age_gender_caffeine_nicotine', # all 4 covariates: age, sex, coffee, cigarettes
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

# Join all results into one dataframe
all_pvals = pd.DataFrame(pd.read_csv(os.path.join(corr_dir, CBF_file_names[map] +'_correlations.csv'), index_col='Atlas')['pval'] for map in range(len(CBF_file_names)))
all_pvals.index = CBF_file_names

# reshape the dataframe so all p_values are in one column, this is required for the statsmodels package to do bonferroni correction
all_pvals = pd.melt(all_pvals, ignore_index=False, var_name='CBF map', value_name='p_val')

# BONFERRONI CORRECTION
all_pvals['p_reject'], all_pvals['pvals_corrected'], dontneedthis, alphacBonf = multipletests(pvals=all_pvals['p_val'], method='holm', alpha=0.05)

# Pivot the p-values dataframe back to previous shape in preparation for data visualisation
bool_pvals = all_pvals.pivot(columns='CBF map', values='p_reject')
# the order of column and rows was changes in the process, so re-index the dataframe
bool_pvals = bool_pvals.reindex((CBF_file_names), axis='rows')
bool_pvals = bool_pvals.reindex((atlas_names), axis='columns')

bool_pvals.to_csv(corr_dir+'/all_p_values_bonferroni.csv',index_label='atlas')