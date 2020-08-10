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

# function that reads results for all 15 runs at once (all.json files)
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

# function for extracting all separate runs (results_x.json files)
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

## Load results for 15 separate trials

``` r
# read all 15 trials separately
runs <- lapply(models, FUN = read_trials)

# all in one dataframe
runs <- do.call("rbind", runs)

# convert loss (ttd) to percentage 
runs$loss <- runs$loss*100

# save results file 
saveRDS(runs, "output/runs.RDS")
```

Compute standarad deviation from the 15 separate trials.

``` r
# compute standard deviation 
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

# save results file 
saveRDS(results, "output/results.RDS")
```

Create table for manuscript (all means over 15 runs)

| model        | wss.95\_nudging | rrf.10\_nudging | loss\_nudging | wss.95\_ptsd | rrf.10\_ptsd | loss\_ptsd | wss.95\_software | rrf.10\_software | loss\_software | wss.95\_ace | rrf.10\_ace | loss\_ace | wss.95\_virus | rrf.10\_virus | loss\_virus | wss.95\_wilson | rrf.10\_wilson | loss\_wilson |
| :----------- | --------------: | --------------: | ------------: | -----------: | -----------: | ---------: | ---------------: | ---------------: | -------------: | ----------: | ----------: | --------: | ------------: | ------------: | ----------: | -------------: | -------------: | -----------: |
| NB + TF-IDF  |            71.7 |            65.3 |           9.3 |         91.7 |         99.6 |        1.7 |             92.3 |             98.2 |            1.4 |        82.9 |        90.5 |       4.9 |          71.2 |          73.9 |         8.2 |           83.4 |           87.3 |          3.9 |
| LR + D2V     |            71.6 |            67.5 |           8.8 |         90.1 |         98.6 |        1.9 |             91.7 |             99.0 |            1.4 |        77.4 |        81.7 |       5.4 |          70.4 |          70.6 |         8.3 |           84.0 |           90.6 |          4.7 |
| LR + TF-IDF  |            66.9 |            62.1 |           9.5 |         91.7 |         99.8 |        1.7 |             92.0 |             99.0 |            1.4 |        81.1 |        88.5 |       5.9 |          70.3 |          73.7 |         8.3 |           80.5 |           89.1 |          4.3 |
| RF + D2V     |            66.3 |            62.6 |          10.3 |         88.2 |         97.1 |        3.0 |             91.0 |             99.2 |            1.6 |        68.6 |        80.8 |       7.2 |          67.2 |          67.3 |         9.2 |           77.9 |           75.5 |          7.2 |
| RF + TF-IDF  |            64.9 |            53.6 |          11.7 |         84.5 |         94.8 |        3.3 |             90.5 |             99.0 |            2.0 |        71.3 |        82.3 |       6.8 |          63.9 |          62.1 |        10.5 |           81.6 |           86.7 |          5.6 |
| SVM + D2V    |            70.9 |            67.3 |           8.8 |         90.6 |         97.8 |        2.1 |             92.0 |             99.3 |            1.4 |        78.3 |        84.2 |       6.1 |          70.7 |          73.6 |         8.4 |           82.7 |           91.5 |          4.5 |
| SVM + TF-IDF |            66.2 |            60.2 |          10.1 |         91.0 |         98.6 |        2.1 |             92.0 |             99.0 |            1.9 |        75.8 |        86.2 |       7.1 |          69.7 |          73.4 |         8.5 |           79.9 |           90.6 |          4.0 |

Create table for manuscript

``` r
nicetab <- function(results, statistic){
  test <- results %>% select(model, dataset, all_of(statistic))
  sdname <- paste0("sd", statistic)

  test <- left_join(test, sdruns[,c("model", "dataset", sdname)], by = c("model", "dataset"))
  
  test[,statistic] <- sprintf("%.1f", round(test[,statistic],1)) 
  test[,sdname] <-  sprintf("%.2f", round(test[,sdname],2)) 
  test$tab <- with(test, paste0(test[,statistic], " (", test[,sdname], ")"))
  
  tab <- test %>%
      select(model, dataset, tab) %>%
      pivot_wider(names_from = dataset, values_from = c("tab"))
  
  tab <- tab %>%
    select(model, nudging, ptsd, software, ace, virus, wilson)
  names(tab) <- c("", "Nudging", "PTSD", "Software", "ACE", "Virus", "Wilson")
  return(tab)
}
```

# ATD table

``` r
tabatd <- nicetab(results, "loss") 
tabatd <- tabatd[c(7, 1, 5, 3, 6, 4, 2),]
# add range rows 
mad <- results %>% group_by(dataset) %>% summarise(median = sprintf("%.1f", round(median(loss), 1)), mad = sprintf("%.2f", round(mad(loss), 2)))

mad <- with(mad, paste0(median, " (", mad, ")"))

tabatd <- rbind(tabatd, (c("median (MAD)", mad[c(2:4, 1, 5,6)])))

saveRDS(tabatd, file = "tables/tab2_atd.RDS")

# print(xtable(tabatd, align = c("r", "r", rep("c", 6))), 
#       include.rownames=FALSE, comment = FALSE, booktabs = TRUE, hline.after = c(0,7))
```

# <WSS@95> table

``` r
tabwss95 <- nicetab(results, "wss.95") 
tabwss95 <- tabwss95[c(7, 1, 5, 3, 6, 4, 2),]
# add range rows 
mad <- results %>% group_by(dataset) %>% summarise(median = sprintf("%.1f", round(median(wss.95), 1)), 
                                                   mad = sprintf("%.2f", round(mad(wss.95), 2)))
# insert mad 
mad <- with(mad, paste0(median, " (", mad, ")"))

tabwss95 <- rbind(tabwss95, (c("median (MAD)", mad[c(2:4, 1, 5,6)])))
# insert N per dataset 
saveRDS(tabwss95, file = "tables/tab3_wss95.RDS")

print(xtable(tabwss95, align = c("r", "r", rep("c", 6))), 
      include.rownames=FALSE, comment = FALSE, booktabs = TRUE, hline.after = c(0,7))
```

    ## \begin{table}[ht]
    ## \centering
    ## \begin{tabular}{rcccccc}
    ##   & Nudging & PTSD & Software & ACE & Virus & Wilson \\ 
    ##   \midrule
    ## SVM + TF-IDF & 66.2 (2.90) & 91.0 (0.41) & 92.0 (0.10) & 75.8 (1.95) & 69.7 (0.81) & 79.9 (2.09) \\ 
    ##   NB + TF-IDF & 71.7 (1.37) & 91.7 (0.27) & 92.3 (0.08) & 82.9 (0.99) & 71.2 (0.62) & 83.4 (0.89) \\ 
    ##   RF + TF-IDF & 64.9 (2.50) & 84.5 (3.38) & 90.5 (0.34) & 71.3 (4.03) & 63.9 (3.54) & 81.6 (3.35) \\ 
    ##   LR + TF-IDF & 66.9 (4.01) & 91.7 (0.18) & 92.0 (0.10) & 81.1 (1.31) & 70.3 (0.65) & 80.5 (0.65) \\ 
    ##   SVM + D2V & 70.9 (1.68) & 90.6 (0.73) & 92.0 (0.21) & 78.3 (1.92) & 70.7 (1.76) & 82.7 (1.44) \\ 
    ##   RF + D2V & 66.3 (3.25) & 88.2 (3.23) & 91.0 (0.55) & 68.6 (7.11) & 67.2 (3.44) & 77.9 (3.43) \\ 
    ##   LR + D2V & 71.6 (1.66) & 90.1 (0.63) & 91.7 (0.13) & 77.4 (1.03) & 70.4 (1.34) & 84.0 (0.77) \\ 
    ##    \midrule
    ## median (MAD) & 66.9 (3.05) & 90.6 (1.53) & 92.0 (0.47) & 77.4 (5.51) & 70.3 (0.90) & 81.6 (2.48) \\ 
    ##   \end{tabular}
    ## \end{table}

``` r
  # kable(format = "latex") %>%
  # kableExtra()
```

# <RRF@10> table

``` r
tabrrf10 <- nicetab(results, "rrf.10") 

tabrrf10 <- tabrrf10[c(7, 1, 5, 3, 6, 4, 2),]
# add range rows 
mad <- results %>% group_by(dataset) %>% summarise(median = sprintf("%.1f", round(median(rrf.10), 1)), mad = sprintf("%.2f", round(mad(rrf.10), 2)))

mad <- with(mad, paste0(median, " (", mad, ")"))


tabrrf10 <- rbind(tabrrf10, (c("median (MAD)", mad[c(2:4, 1, 5,6)])))
saveRDS(tabrrf10, file = "tables/tab4_rrf10.RDS")

print(xtable(tabrrf10, align = c("r", "r", rep("c", 6))), 
      include.rownames=FALSE, comment = FALSE, booktabs = TRUE, hline.after = c(0,7))
```

    ## \begin{table}[ht]
    ## \centering
    ## \begin{tabular}{rcccccc}
    ##   & Nudging & PTSD & Software & ACE & Virus & Wilson \\ 
    ##   \midrule
    ## SVM + TF-IDF & 60.2 (3.12) & 98.6 (1.40) & 99.0 (0.00) & 86.2 (5.25) & 73.4 (1.62) & 90.6 (1.17) \\ 
    ##   NB + TF-IDF & 65.3 (2.61) & 99.6 (0.95) & 98.2 (0.34) & 90.5 (1.40) & 73.9 (1.70) & 87.3 (2.55) \\ 
    ##   RF + TF-IDF & 53.6 (2.71) & 94.8 (1.60) & 99.0 (0.00) & 82.3 (2.75) & 62.1 (3.19) & 86.7 (5.82) \\ 
    ##   LR + TF-IDF & 62.1 (2.59) & 99.8 (0.70) & 99.0 (0.00) & 88.5 (5.16) & 73.7 (1.48) & 89.1 (2.30) \\ 
    ##   SVM + D2V & 67.3 (3.00) & 97.8 (1.12) & 99.3 (0.44) & 84.2 (2.78) & 73.6 (2.54) & 91.5 (4.16) \\ 
    ##   RF + D2V & 62.6 (5.47) & 97.1 (1.90) & 99.2 (0.34) & 80.8 (5.72) & 67.3 (3.19) & 75.5 (14.35) \\ 
    ##   LR + D2V & 67.5 (2.59) & 98.6 (1.40) & 99.0 (0.00) & 81.7 (1.81) & 70.6 (2.21) & 90.6 (5.00) \\ 
    ##    \midrule
    ## median (MAD) & 62.6 (3.89) & 98.6 (1.60) & 99.0 (0.00) & 84.2 (3.71) & 73.4 (0.70) & 89.1 (2.70) \\ 
    ##   \end{tabular}
    ## \end{table}

# References

<div id="refs" class="references hanging-indent">

<div id="ref-ASReview2020">

Schoot, Rens van de, Jonathan de Bruin, Raoul Schram, Parisa Zahedi,
Bianca Kramer, Gerbrich Ferdinands, Albert Harkema, Qixiang Fang, and
Daniel Oberski. 2020. “ASReview: Active Learning for Systematic
Reviews,” April. <https://doi.org/10/ggssnj>.

</div>

</div>
