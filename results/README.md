Processing simulation output
================

This directory stores all files used to extract figures and statistics
from the simulation study output. The directory contains the following:

  - `extract_plots.ipynb`, a jupyter notebook producing recall curves
    from the simulation output (Figure 1 and 2 in the manuscript)
  - `extract_results.ipynb`, a jupyter notebook extracting `.json` files
    containing statistics from the `.h5` simulation output (WSS, RRF,
    ATD in table 2, 3, and 4 in the manuscript)
  - `one_seed`, containing all plots and `.json` statistics files
    produced by the two jupyter notebooks above. The plots are used in
    the manuscript, the data are further processed by this readme into
    tables before they are manuscript-ready.
  - `README.Rmd` containing R-code to transform the `.json` files into
    readable tables for the manuscript.
  - `output` contains the abovementioned tables, stored as `.RDS`
    files.  
  - the `datastats.RDS` is used in the analyses to compute adjusted ATD
    values (see code below)

# Requirements

Extracing data from the simulation output requires having several
packages installed, like ASReview version 0.9.3 (van de Schoot et al.
2020). All these requirements are listed in the `requirements.txt` file.
If you’ve already installed this file in the `simulation_study` step,
please skip this. If not, you can run the following in your terminal to
install all requirements:

``` bash
pip install -r ../simulation_study/requirements.txt
```

Additionally, to create the plots and statistics in the manuscript you
will need to install a specific branch of the asreview visualization
package. Run the following in your terminal:

``` bash
# clone visualization package from GitHub
git clone https://github.com/GerbrichFerdinands/asreview-thesis-visualization.git
```

And then, within the newly created directory, the following:

``` bash
# install visualization package 
pip install . 
```

# Reproduce data extraction

To reproduce the results, follow the steps below. If you do not want to
download the raw simulation output, start at step 3:

1.  Run all code in the `extract_plots.ipynb` notebook to create all
    plots. This requires having the raw simulation data, to be found on
    the OSF (<https://osf.io/7mr2g/> and <https://osf.io/ag2xp/>). Note
    that you will need to adjust the paths to where you’ve stored the
    simulation output on your local computer. Also, note that creating
    figures can take quite some time, depending on your computer. Mine
    took from 30 minutes to 5 hours per figure The final figures can be
    found in the `one_seed/plots` directory.
2.  Run all code in the `extract_results.ipynb` to extract the metrics
    WSS, RRF and ATD from the raw simulation data. Note that you will
    need to adjust the paths to where you’ve stored the simulation
    output on your local computer. Also, note that extracting all
    results will take quite some time, depending on your computer. Mine
    took 48 hours. The results are stored in the `one_seed/plots`
    directory.
3.  Follow the preprocessing steps in the `README.Rmd` files to create
    tables for in the manuscript, stored in the `output` directory.

## Define functions for reading simulation output

``` r
data <- readRDS("../simulation_study/R/00_datasets.RDS")
models <-c("BCTD", "LCDD", "LCTD", "RCDD", "RCTD", "SCDD", "SCTD")
names(models) <- c("NB + TF-IDF", "LR + D2V", "LR + TF-IDF", "RF + D2V", "RF + TF-IDF", "SVM + D2V", "SVM + TF-IDF" )

# function that reads results for all 15 runs
read_results <- function(m){
   files = list.files(paste0("one_seed/statistics/", m), pattern = "all.json", recursive = TRUE)
  # names of the files are the data
  names(files) <- str_split(files, "/", simplify = TRUE)[,1]
  # read data
  dat <- lapply(files, function(x) fromJSON(file = paste0("one_seed/statistics/", m, "/", x)))
  
  # extract wss, rrf, and loss
  dat <- map(dat, `[`, c("wss", "rrf", "loss"))

  # transorm into dataframe
  dat <- map_dfr(dat, ~ as.data.frame(.x), .id = "dataset")
  
  # add model name
  dat <- dat %>% 
    mutate(model = names(models[models == m]))

  return(dat)
}

# function for extracting all separate runs 
read_trials <- function(m){
   files <- list.files(paste0("one_seed/statistics/", m), pattern = "results_", recursive = TRUE, full.names=TRUE)
  # names of the files are the data
  names(files) <- str_split(files, "/", simplify = TRUE)[,4]
  
  # read data
  dat <- lapply(files, function(x) fromJSON(file = x))
  
  # extract wss, rrf, and loss
  dat <- map(dat, `[`, c("wss", "rrf", "loss"))

  # transorm into dataframe
  dat <- map_dfr(dat, ~ as.data.frame(.x), .id = "dataset")
  
  # add model name
  dat <- dat %>% 
    mutate(model = names(models[models == m]))

  return(dat)
}
```

The ATD values need to be adjusted for prior inclusions and exclusions
as the computation does not take into account that prior to the active
learning cycle, already 1 inclusion and 1 exclusion have been labelled
‘for free’.

``` r
# ATD needs to be adjusted for 1 prior inclusion and 1 prior exclusion! 
# compute adjusted ATD to make it equal to the area above the curve
datastats <- readRDS("datastats.RDS") %>%
  select(Dataset, candidates_test, incl_test) %>%
  # account for 1 prior exclusion and 1 prior inclusion
  mutate(n_1 = incl_test, n_excl = candidates_test-n_1, n_1_noprior = incl_test-1, candidates_noprior = candidates_test -1) %>%
  mutate(ratio = (n_1_noprior/n_1)/(candidates_noprior/candidates_test))

datastats$dataset <- c("ace", "nudging", "ptsd", "software", "virus", "wilson")
atdratio <- datastats %>%
  select(dataset, ratio)
```

## Load results for 15 separate trials

``` r
# read all 15 trials separately
runs <- lapply(models, FUN = read_trials)

# all in one dataframe
runs <- do.call("rbind", runs)

# convert loss (ttd) to percentage 
runs$loss <- runs$loss*100
# adjust loss to N_1 : N_1-1 (to the prior inclusions)
runs <- left_join(runs, atdratio, by = "dataset")
runs <- runs %>%
  mutate(loss = loss/ratio) %>%
  select(-ratio)

# save results file 
saveRDS(runs, "output/runs.RDS")
```

Compute standarad deviation from the 15 separate trials.

``` r
# compute standard deviation (bootstrapped)
sdruns <- 
  runs %>%
  select(dataset, model, wss.95, rrf.10, loss) %>% 
  group_by(model, dataset) %>%
  summarise(sdwss.95 = sd(wss.95),
            sdrrf.10 = sd(rrf.10),
            sdloss = sd(loss))

saveRDS(sdruns, "output/sdruns.RDS")
```

## Load results as means over all 15 trials

``` r
# extract results for all models
# list for models separately
results <- lapply(models, read_results)

# all in one dataframe
results <- do.call("rbind", results)

# convert loss (ttd) to percentage 
results$loss <- results$loss*100
# adjust loss to N_1 : N_1-1
results <- left_join(results, atdratio, by = "dataset")

results <- results %>%
  mutate(loss = loss/ratio) %>%
  select(-ratio)

# save results file 
saveRDS(results, "output/results.RDS")
```

Create table for manuscript (all means over 15 runs)

| model        | wss.95\_nudging | rrf.10\_nudging | loss\_nudging | wss.95\_ptsd | rrf.10\_ptsd | loss\_ptsd | wss.95\_software | rrf.10\_software | loss\_software | wss.95\_ace | rrf.10\_ace | loss\_ace | wss.95\_virus | rrf.10\_virus | loss\_virus | wss.95\_wilson | rrf.10\_wilson | loss\_wilson |
| :----------- | --------------: | --------------: | ------------: | -----------: | -----------: | ---------: | ---------------: | ---------------: | -------------: | ----------: | ----------: | --------: | ------------: | ------------: | ----------: | -------------: | -------------: | -----------: |
| NB + TF-IDF  |            71.7 |            65.3 |           9.4 |         91.7 |         99.6 |        1.8 |             92.3 |             98.2 |            1.5 |        82.9 |        90.5 |       5.0 |          71.2 |          73.9 |         8.2 |           83.4 |           87.3 |          4.1 |
| LR + D2V     |            71.6 |            67.5 |           8.9 |         90.1 |         98.6 |        1.9 |             91.7 |             99.0 |            1.4 |        77.4 |        81.7 |       5.6 |          70.4 |          70.6 |         8.4 |           84.0 |           90.6 |          4.9 |
| LR + TF-IDF  |            66.9 |            62.1 |           9.6 |         91.7 |         99.8 |        1.7 |             92.0 |             99.0 |            1.4 |        81.1 |        88.5 |       6.1 |          70.3 |          73.7 |         8.4 |           80.5 |           89.1 |          4.5 |
| RF + D2V     |            66.3 |            62.6 |          10.4 |         88.2 |         97.1 |        3.1 |             91.0 |             99.2 |            1.6 |        68.6 |        80.8 |       7.3 |          67.2 |          67.3 |         9.3 |           77.9 |           75.5 |          7.5 |
| RF + TF-IDF  |            64.9 |            53.6 |          11.8 |         84.5 |         94.8 |        3.4 |             90.5 |             99.0 |            2.0 |        71.3 |        82.3 |       7.0 |          63.9 |          62.1 |        10.6 |           81.6 |           86.7 |          5.9 |
| SVM + D2V    |            70.9 |            67.3 |           8.9 |         90.6 |         97.8 |        2.1 |             92.0 |             99.3 |            1.4 |        78.3 |        84.2 |       6.2 |          70.7 |          73.6 |         8.5 |           82.7 |           91.5 |          4.7 |
| SVM + TF-IDF |            66.2 |            60.2 |          10.2 |         91.0 |         98.6 |        2.1 |             92.0 |             99.0 |            1.9 |        75.8 |        86.2 |       7.3 |          69.7 |          73.4 |         8.5 |           79.9 |           90.6 |          4.2 |

# References

<div id="refs" class="references hanging-indent">

<div id="ref-ASReview2020">

Schoot, Rens van de, Jonathan de Bruin, Raoul Schram, Parisa Zahedi,
Bianca Kramer, Gerbrich Ferdinands, Albert Harkema, Qixiang Fang, and
Daniel Oberski. 2020. “ASReview: Active Learning for Systematic
Reviews,” April. <https://doi.org/10/ggssnj>.

</div>

</div>
