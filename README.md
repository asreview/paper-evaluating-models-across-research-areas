# Active learning for screening prioritization in systematic reviews - a simulation study
This repository provides supplementary material on the paper _Active learning for screening prioritization in systematic reviews - a simulation study_.

- Authors: Gerbrich Ferdinands, Raoul Schram, Jonathan de Bruin, Ayoub Bagheri, Daniel Oberski, Lars Tummers, Rens van de Schoot
- Maintainer: Gerbrich Ferdinands
- Date: 30-07-2020
- Version 1.0.0
- Data collection and simulation period: January - May 2020
- Manuscript submitted on 10-08-2020.

This repository contains scripts and data required to reproduce the results: the systematic review datasets and their preprocessing scripts, scripts for the simulations, scripts for the processing and analysis of the results of the simulations, and scripts for producing the figures and tables.

# Content
This archive is organized as such that it follows the steps needed to reproduce the study that was carried out:

1. `datasets` -  collection and preprocessing of six systematic review datasets, production of Table 1.
2. `simulation_study` - simulating seven active learning models on the systematic review datasets.
3. `results` - the simulation study output was processed and analyzed to arrive at the results discussed in the manuscript (Figure 1 and 2, Table 2, 3, and 4).

Please follow the order above if you want to reproduce this study. Every subdirectory contains its own `readme` that will guide you through the process of that particular step.

This repository contains one additional folder called `other`, containing the ethical approval form by the FETC, and the grant approval by SURFsara.

### Disclaimer
Simulating a systematic review produces files that are very large in size. The total amount of storage needed for all the raw output files is over 900 GB. GitHub does not allow for repositories of this size, therefore the raw datafiles of the simulation are stored on the Open Science Framework instead. Due to a bug in OSF, the files had to be distributed over 2 projects, https://osf.io/7mr2g/ and https://osf.io/ag2xp/.

# Requirements
All computations were run on macOS Catalina 10.15.2. The steps in this repository assume you have R (3.6.1) and RStudio (1.2.5042) installed. Moreover, Python version 3.7 or higher is required. If you don't have python you can follow [this installation guide](https://asreview.nl/#!/quick-start). Any further requirements are discussed in the `simulation_study` readme.

# Privacy
Only openly available data was used in this study. The study has been approved by the Ethics Committee of the Faculty of Social and Behavioural Sciences of Utrecht University, filed as an amendment under study 20-104. The approval document can be found in the `other` directory of this repository.

# Permission and access
This research archive is openly published on GitHub, https://github.com/asreview/paper-evaluating-models-across-research-areas under MIT license. Therefore it is 'Open Access' and thus available for anyone. This repository will remain online for at least 10 years.

# Contact
This repository is maintained by Gerbrich Ferdinands. For any further questions, please e-mail me at `g.ferdinands@uu.nl`.
