from statsmodels.stats.multitest import multipletests
import pandas as pd
import os
import itertools

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

correlations = pd.read_csv(os.path.join(corr_dir, "all_correlations.csv"), index_col=(0,1))
correlations['pvals_corrected'] = None

corr_1st = correlations['pval'].loc[Q_1st]
corr_2nd = correlations['pval'].loc[Q_2nd]
corr_1st_covar = correlations['pval'].loc[Q_1st_covars]
corr_2nd_covar = correlations['pval'].loc[Q_2nd_covars]

a, correlations.loc[Q_1st, 'pvals_corrected'], dontneedthis, dontneedthat = multipletests(pvals=corr_1st, method='sidak', alpha=0.05)
a, correlations.loc[Q_2nd, 'pvals_corrected'], dontneedthis, dontneedthat = multipletests(pvals=corr_2nd, method='sidak', alpha=0.05)
a, correlations.loc[Q_1st_covars, 'pvals_corrected'], dontneedthis, dontneedthat = multipletests(pvals=corr_1st_covar, method='sidak', alpha=0.05)
a, correlations.loc[Q_2nd_covars, 'pvals_corrected'], dontneedthis, dontneedthat = multipletests(pvals=corr_2nd_covar, method='sidak', alpha=0.05)

correlations.to_csv(corr_dir+'/all_correlations_p_adj.csv',index=True, sep=',')
