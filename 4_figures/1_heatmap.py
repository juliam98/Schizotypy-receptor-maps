import pandas as pd
import os
import numpy as np

main_folder=os.getcwd()
corr_dir=os.path.join(main_folder, '3_output', '3.3_correlations')

CBF_files1 = [ # names of CBF files
    'CBF_no_cov', # no covariates
    'O-LIFE-UE', # O-LIFE-UE regression
    'O-LIFE-IA', # O-LIFE-IA regression
    'O-LIFE-CD' # O-LIFE-CD regression
]

CBF_files2 = [ # names of CBF files
    'CBF_cov_age_gender', # 2 covariates: age, sex
    'CBF_cov_age_gender_caffeine_nicotine', # all 4 covariates: age, sex, coffee, cigarettes
    'O-LIFE-UE-covars', # O-LIFE-UE regression with covariates
    'O-LIFE-IA-covars', # O-LIFE-IA regression with covariates
    'O-LIFE-CD-covars' # O-LIFE-CD regression with covariates
]

atlas_names = [ # names of receptor atlas files
    # 'D1_sch23390_kaller2017', #D1
    # 'D2_fallypride_jaworska2020', # D2
    # 'DAT_fpcit_dukart2018', #DAT
    'FDOPA_fluorodopa_hc12_gomez', #FDOPA
    'GABAa5_Ro15_10hc_lukow', #GABAa5
    'GABAbz_flumazenil_norgaard2021', #GABAbz
    'mGluRR5_abp688_smart2019', # mGluR5
    'NMDA_ge179_galovic2021' # NMDA
]

# Import all correlation values
all_data = pd.read_csv(os.path.join(corr_dir, 'all_correlations_p_adj.csv'), index_col=(0,1))

# Separate into no covariates, and covariates comparisons, as they will be plotted separately
df_comparison1 = all_data.loc[CBF_files1]
df_comparison2 = all_data.loc[CBF_files2]

# Reshape the df: just boolean values indicating if correlation is statistically significant
bool_signf1 = df_comparison1['p_reject'].unstack(1)
bool_signf1 = bool_signf1.mask(bool_signf1, '*') # replace True with asterisk to indicate significant values
bool_signf1 = bool_signf1.replace(False, ' ')

bool_signf2 = df_comparison2['p_reject'].unstack(1)
bool_signf2 = bool_signf2.mask(bool_signf2, '*') # replace True with asterisk to indicate significant values
bool_signf2 = bool_signf2.replace(False, ' ')

# Reshape the df: just correlation values 
corr1 = round(df_comparison1['corr'].unstack(1),2)
corr2 = round(df_comparison2['corr'].unstack(1),2)

# DATA VISUALISATION
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.font_manager import FontProperties

rc('text')
font = FontProperties()
font.set_size('x-large')

# Transparent background for figures
plt.rcParams.update({
    "savefig.facecolor": (1.0, 1.0, 1.0, 0.0), 
})

# Labels for the heatmap- y axis
CBF_labels1 = [ # names of CBF files
    'HS>LS', # no covariates
    'O-LIFE-UE', # O-LIFE-UE regression
    'O-LIFE-IA', # O-LIFE-IA regression
    'O-LIFE-CD' # O-LIFE-CD regression
]
CBF_labels2 = [
    'HS>LS \n(2 cov)',
    'HS>LS \n(4 cov)',
    'O-LIFE-UE\ncov', # O-LIFE-UE regression with covariates
    'O-LIFE-IA\ncov', # O-LIFE-IA regression with covariates
    'O-LIFE-CD\ncov' # O-LIFE-CD regression with covariates
]
receptor_labels = (lambda atlas_names: [(x.split("_")[0]) for x in atlas_names])(atlas_names) # extract receptor names to label the heatmap

# create dataframe of zeros to use for annotating the heatmap without affecting the colour
map_zeroes1 = pd.DataFrame(np.zeros((len(CBF_files1), len(atlas_names))))
map_zeroes2 = pd.DataFrame(np.zeros((len(CBF_files2), len(atlas_names))))
# Define figure size
plt.figure(figsize=(10,6))
# Define the colour palette
cmap=sns.color_palette("RdBu", as_cmap=True)

# HEATMAP 1
# First heatmap1 is the transparent/ no-colour heatmap containing just the annotations of correlation coefficients
heatmap_values1 = sns.heatmap(map_zeroes1, cmap=None, annot_kws={'va':'top','fontsize':'x-large'}, annot=corr1, square=False, cbar=False)

# The second heatmap1 is the main one, colour based on strength of correlations, while annotations are based on p_values (* if significant after Bonferroni)
heatmap_main1 = sns.heatmap(corr1, cmap=cmap, center=0, annot_kws={'va':'bottom', 'fontsize':'large'}, annot=bool_signf1, fmt='', square=False, vmin=-0.7, vmax=0.7)

# Set labels/title
heatmap_main1.set(xlabel="", ylabel="")
heatmap_main1.set_title(label="Heatmap of spearman's correlations",fontproperties=font)
heatmap_main1.set_xticklabels(labels=receptor_labels,fontproperties=font)
heatmap_main1.set_yticklabels(labels=CBF_labels1,fontproperties=font)
# Rotate labels on x axis by 45 degrees
plt.xticks(rotation=45, ha="right")
plt.yticks(rotation=0, ha="right")
# Fit all labels within the figure
plt.tight_layout()
# plt.show()
plt.savefig(main_folder+'/4_figures/heatmap_main_comparisons.png', dpi=350)

# clear all figure properties from memory before plotting the second heatmap
plt.figure().clear()
plt.close()
plt.cla()
plt.clf()

# HEATMAP 2
# First heatmap2 is the transparent/ no-colour heatmap containing just the annotations of correlation coefficients
heatmap_values2 = sns.heatmap(map_zeroes2, cmap=None, annot_kws={'va':'top','fontsize':'x-large'}, annot=corr2, square=False, cbar=False)

# The second heatmap2 is the main one, colour based on strength of correlations, while annotations are based on p_values (* if significant after Bonferroni)
heatmap_main2 = sns.heatmap(corr2, cmap=cmap, center=0, annot_kws={'va':'bottom', 'fontsize':'large'}, annot=bool_signf2, fmt='', square=False, vmin=-0.7, vmax=0.7)

# Set labels/title
heatmap_main2.set(xlabel="", ylabel="")
heatmap_main2.set_title(label="Heatmap of spearman's correlations",fontproperties=font)
heatmap_main2.set_xticklabels(labels=receptor_labels,fontproperties=font)
heatmap_main2.set_yticklabels(labels=CBF_labels2,fontproperties=font)
# Rotate labels on x axis by 45 degrees
plt.xticks(rotation=45, ha="right")
# Fit all labels within the figure
plt.tight_layout()
# plt.show()
plt.savefig(main_folder+'/4_figures/heatmap_covariates_comparisons.png', dpi=350)