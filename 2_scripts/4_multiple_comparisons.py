from statsmodels.stats.multitest import multipletests
import pandas as pd
import os

main_folder=os.getcwd()
corr_dir=os.path.join(main_folder, '3_output', '3.3_correlations')

# Separate comparisons into primary research question, secondary research questions, and both repeated but with covariates
Q_1st = ('CBF_no_cov')
Q_2nd = [
    'O-LIFE-UE', # O-LIFE-UE regression
    'O-LIFE-IA', # O-LIFE-IA regression
    'O-LIFE-CD' # O-LIFE-CD regression
]
Q_1st_covars = [
    'CBF_cov_age_gender', # 2 covariates: age, sex
    'CBF_cov_age_gender_caffeine_nicotine' # all 4 covariates: age, sex, coffee, cigarettes
]
Q_2nd_covars = [
    'O-LIFE-UE-covars', # O-LIFE-UE regression with covariates
    'O-LIFE-IA-covars', # O-LIFE-IA regression with covariates
    'O-LIFE-CD-covars' # O-LIFE-CD regression with covariates
]

# Read the file with all correlation and p values
correlations = pd.read_csv(os.path.join(corr_dir, "all_correlations.csv"), index_col=(0,1))
correlations['pvals_corrected'] = None # empty column where corrected p_values will be assigned
correlations['p_reject'] = None # empty column where corrected p_values will be assigned

# get sections of the full df that correspond to each of the comparisons
corr_1st = correlations['pval'].loc[Q_1st]
corr_2nd = correlations['pval'].loc[Q_2nd]
corr_1st_covar = correlations['pval'].loc[Q_1st_covars]
corr_2nd_covar = correlations['pval'].loc[Q_2nd_covars]

# multiple comparisons correction
correlations.loc[Q_1st, 'p_reject'], correlations.loc[Q_1st, 'pvals_corrected'], dontneedthis, dontneedthat = multipletests(pvals=corr_1st, method='holm', alpha=0.05)
correlations.loc[Q_2nd, 'p_reject'], correlations.loc[Q_2nd, 'pvals_corrected'], dontneedthis, dontneedthat = multipletests(pvals=corr_2nd, method='holm', alpha=0.05)
correlations.loc[Q_1st_covars, 'p_reject'], correlations.loc[Q_1st_covars, 'pvals_corrected'], dontneedthis, dontneedthat = multipletests(pvals=corr_1st_covar, method='fdr_bh', alpha=0.05)
correlations.loc[Q_2nd_covars, 'p_reject'], correlations.loc[Q_2nd_covars, 'pvals_corrected'], dontneedthis, dontneedthat = multipletests(pvals=corr_2nd_covar, method='holm', alpha=0.05)

# save to csv file
correlations.to_csv(corr_dir+'/all_correlations_p_adj.csv',index=True, sep=',')