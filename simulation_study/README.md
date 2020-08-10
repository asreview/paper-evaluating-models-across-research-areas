Simulation study scripts
========================

This directory contains all steps taken in simulating active learning models on systematic review datasets.

# Content

This repository contains:

  - `simulation` documentation on how the models were simulated on the systematic review datasets.
  - `requirements.txt` software requirements for running simulations.

To reproduce the research, follow the steps in `simulation`. Documentation on how hyperparameters were optimized can be found in [this repository](https://github.com/asreview/paper-optimizing-hyperparameters).

# Models

We are simulating 7 models on 6 systematic review datasets. Each model is abbreviated to ease scripting:

| Model        | Abbreviation |
| :----------- | :----------- |
| NB + TF-IDF  | BCTD         |
| LR + D2V     | RCTD         |
| LR + TF-IDF  | SCTD         |
| RF + D2V     | LCTD         |
| RF + TF-IDF  | RCDD         |
| SVM + D2V    | SCDD         |
| SVM + TF-IDF | LCDD         |

The first letter denotes the classification strategy, NB, LR, RF, or
SVM. The second letter stands for C of certainty sampling. The third
letter denotes the feature extraction strategy, TF-IDF or D2V. The
fourth letter stands the balance strategy, D for DR.

# Requirements

This study requires having several packages installed, like ASReview
version 0.9.3 (van de Schoot et al. 2020). All these requirements are
listed in the `requirements.txt` file. Assuming you have Python 3.7 or
higher, you can run the following in your bash terminal to install all
requirements:

``` bash
pip install -r requirements.txt
```

This automatically installs asreview version 0.9.3 and several
dependencies. Moreover, a specific branch of the asreview simulation
extension should be installed. Run the following in your bash terminal:

``` bash
git clone https://github.com/GerbrichFerdinands/asreview-thesis-simulation.git
```

And then, within the newly created directory, the following:

``` bash
pip install .
```

# References

<div id="refs" class="references hanging-indent">

<div id="ref-ASReview2020">

Schoot, Rens van de, Jonathan de Bruin, Raoul Schram, Parisa Zahedi,
Bianca Kramer, Gerbrich Ferdinands, Albert Harkema, Qixiang Fang, and
Daniel Oberski. 2020. “ASReview: Active Learning for Systematic
Reviews,” April. <https://doi.org/10/ggssnj>.

</div>

</div>
