# Schizotypy-receptor-maps
## Aims
This repository contains code and data used in the analysis of ASL-MRI data from high and low schizotypy individuals. 

Six publically-available receptor density/ molecular atlases were used to correlate regional rCBF associated with [O-LIFE](https://pubmed.ncbi.nlm.nih.gov/16417985/) scores. The aim of this analysis is to investigate the contribution of those six receptors (and transporters/vesicles) on changes in neuronal activity associated with schizotypy traits.

## Data analysis process
### The receptor/ molecular maps used in the analysis are:
| Receptor | Reference    | Radiotracer                |
|----------|--------------|----------------------------|
| DAT      | dukart2018   | [<sup>123</sup>I]-FP-CIT   |
| D2       | jaworska2020 | [<sup>18</sup>F]fallypride |
| D1       | kaller2017   | [<sup>11</sup>C]-SCH 23390 |
| GABAa    | norgaard2021 | [<sup>11</sup>C]flumazenil |
| GABAa5   | lukow2022    | [<sup>11</sup>C]Ro15-4513  |
| mGluR5   | smart2019    | [<sup>11</sup>C]ABP688     |
| NMDA     | galovic2021  | [<sup>11</sup>C]GE-179     |

### Data analysis steps:
<br>
<img src="https://github.com/juliam98/Schizotypy-receptor-maps/assets/93785710/998a82ed-4003-4ec4-89f2-db0e44c5af3b"  width="800">
<br>

<br>The numbering of the steps below corresponds to numbers in the names of python files: <br>

1. Parcellate each CBF map using the Schaefer parcellation atlas. The resulting 122 values for each CBF map represent average regional blood flow values for each brain region of the Schaefer atlas. Similarily, parcellate each of the receptor/molecular maps.

2. Generate null distribution of each CBF map using the 
[neuromaps](https://netneurolab.github.io/neuromaps/)
toolbox. <br>
3. Correlate each parcellated CBF map with all parcellated receptor/molecular atlas using spearman's correlation and using the null models.
4. Correct for multiple comparisons.

## Results
View results [here](5_results#results_section).
