# Schizotypy-receptor-maps
## Aims
This repository contains code and data used in the analysis of ASL-MRI data from high and low schizotypy individuals. 

Six publically-available receptor density/ molecular atlases were used to correlate regional rCBF associated with [O-LIFE](https://pubmed.ncbi.nlm.nih.gov/16417985/) scores. The aim of this analysis is to investigate the contribution of those six receptors (and transporters/vesicles) on changes in neuronal activity associated with schizotypy traits.

## Data analysis process
### The receptor/ molecular maps used in the analysis are:
- D1
- D2
- DAT
- GABAa5
- GABAbz
- mGlu5R
- NMDA
- SV2A

### Data analysis steps:
<br>
<img src="https://github.com/juliam98/Schizotypy-receptor-maps/assets/93785710/923a59d4-a504-453e-8784-31ec27dfba63"  width="800">
<br>

<br>The numbering of the steps below corresponds to numbers in the names of python files: <br>

1. Parcellate each CBF map using the Schaefer parcellation atlas. The resulting 122 values for each CBF map represent average regional blood flow values for each brain region of the Schaefer atlas. Similarily, parcellate each of the receptor/molecular maps.

2. Generate null distribution of each CBF map using the 
[neuromaps](https://netneurolab.github.io/neuromaps/)
toolbox. <br>
3. Correlate each parcellated CBF map with all parcellated receptor/molecular atlas using spearman's correlation and using the null models.
4. Correct for multiple comparisons.
