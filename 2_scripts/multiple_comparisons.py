from statsmodels.stats.multitest import multipletests
import pandas as pd
import os

main_folder='/Users/juliamarcinkowska/Desktop/MSc_THESIS/DataAnalysis/emorisk_2/'
corr_dir=os.path.join(main_folder, '3_results', '3.3_correlations')

CBF_file_names = [ # names of CBF files
    'CBF_no_cov', # no covariates
    'CBF_cov_age_gender', # 2 covariates: age, sex
    'CBF_cov_age_gender_caffeine_nicotine', # all 4 covariates: age, sex, coffee, cigarettes
    'O-LIFE-UE-con_0001', # O-LIFE-UE regression
    'O-LIFE-IA-con_0001', # O-LIFE-IA regression
    'O-LIFE-CD-con_0001' # O-LIFE-CD regression
]

# full CBF files paths
corr_paths= [os.path.join(corr_dir, (CBF_file_names[a])+'_correlations.csv') for a in range(len(CBF_file_names))]

all_pvals = pd.DataFrame()
all_corrs = pd.DataFrame()

for map in range(len(CBF_file_names)):
    all_pvals[CBF_file_names[map]] = pd.read_csv(corr_paths[map])['pval']
    all_corrs[CBF_file_names[map]] = pd.read_csv(corr_paths[map])['corr']

pvals_1d = all_pvals.to_numpy().flatten('F')

a = multipletests(pvals=pvals_1d, method='bonferroni', alpha=0.05)

print(a)