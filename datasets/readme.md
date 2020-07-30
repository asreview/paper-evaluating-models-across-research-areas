Preprocessing datasets
================

This notebook processes six systematic review datasets into datasets
suitable for simulating the screening process. The source code for this
notebook can be found in the `readme.Rmd` file.

  - **Wilson** - is on a review on effectiveness and safety of
    treatments of Wilson Disease, a rare genetic disorder of copper
    metabolism. Dataset: (Appenzeller-Herzog 2020). Paper:
    (Appenzeller‐Herzog et al. 2019).
  - **Ace** - contains publications on the efficacy of
    Angiotensin-converting enzyme (ACE) inhibitors, a drug treatment for
    heart disease Paper and dataset: (Cohen et al. 2006).
  - **Virus** - is from a systematic review on studies that performed
    viral Metagenomic Next-Generation Sequencing (mNGS) in farm animals
    (Kwok et al. 2020).
  - **Software** - from the software engineering field, contains
    publications on fault prediction in source code (Hall et al. 2012).
  - **Nudging** dataset - (Nagtegaal et al. 2019a) on nudging healthcare
    professionals (Nagtegaal et al. 2019b), stemming from the area of
  - **PTSD** - on studies applying latent trajectory analyses on
    posttraumatic stress after exposure to traumatic events (van de
    Schoot et al. 2017).

Data were preprocessed from their original source into a test dataset,
containing title and abstract of the publications obtained in the
initial search. Candidate studies with missing abstracts and duplicate
instances were removed from the data.

Every dataset has 2 versions: one for hyperparameter optimization
(`test_datasets`), and one for simulation (`sim_datasets`).

Every simulation dataset is a .csv file with the columns `title`,
`abstract`, `label_included`, the last one indicating whether a
publication was relevant or not. This is the label that is queried by
the active learning model when simulating a systematic review. The
reason for this sparse datasets (no keywords are included etc) is
twofold. 1) This is by PRISMA guidelines the only information that
should be used to identify relevant publications from a search and 2) I
wanted equal information for all datasets, and for some datasets this
was the only information that was available. For hyperparameter
optimization I used all information accessible to arrive at better
hyperparameters, with future projects in mind.

### Preprocessing datasets

For every datasets, 3 numbers are given: total number of publications,
abstract inclusions and final inclusions. For some datasets there are
discrepancies between how these numbers are reported in the publication
and how they actually are in the raw dataset. Therefore, these numbers
are given for how they are reported in the manuscript, how they are
found in the raw data, and how they are found in the test dataset,
e.g. after removing duplicates and missing abstracts. Moreover,
statistics on missingness and duplicates are given.

## Ace dataset

``` r
ace <- template

# information given in the paper -----------------------------------------------
ace["paper", ] <- c(2544, NA, round(2544*0.0160)) 

# raw --------------------------------------------------------------------------
# original paper not to linked directly. cannot be retrieved? 
# checked dataset online by cohen et al. 
#https://dmice.ohsu.edu/cohenaa/systematic-drug-class-review-data.html
ace["raw", ] <- c(2544, NA, 41)

# asreview dataset -------------------------------------------------------------
ace_asr <- read.csv("https://raw.github.com/asreview/systematic-review-datasets/master/datasets/Cohen_EBM/output/ACEInhibitors.csv",
                     header=T)
```

### Create test dataset

``` r
# replace empty abstracts by NA values. 
ace_asr[ace_asr$abstract == "", "abstract"] <- NA
# stats on missingness in this data
drops["ace",] <- ace_asr %>%
           summarise(n = length(abstract),
                    na = sum(is.na(abstract)),
                    na_rate = sum(is.na(abstract))/length(abstract)*100,
                    dup = sum(duplicated(abstract, incomparables = NA)),
                    dup_rate = sum(duplicated(abstract, incomparables = NA))/length(abstract)*100)

ace["asreview", ] <- c(nrow(ace_asr),
                       NA,
                       sum(ace_asr$label_included))

# drop missings and duplicates. 
ace_test <- ace_asr %>%
  drop_na(abstract) %>% # drop entries with missing abstracts
  distinct(abstract, .keep_all = TRUE) # remove entries with duplicate abstracts

# data on 
ace["test", ] <- c(nrow(ace_test),
                   NA,
                   sum(ace_test$label_included))
```

### Some statistics

On missingness (\# and %) and duplicates (\# and %):

|     |    n |  na | narate | dup | duprate |
| :-- | ---: | --: | -----: | --: | ------: |
| ace | 2544 | 309 |  12.15 |   0 |       0 |

On total number of publications, abstract inclusions (this information
was not available for this dataset) and final inclusions.

|          | search | ftext | incl |
| :------- | -----: | ----: | ---: |
| paper    |   2544 |    NA |   41 |
| raw      |   2544 |    NA |   41 |
| asreview |   2544 |    NA |   41 |
| test     |   2235 |    NA |   41 |

## Nudging dataset

``` r
# by Rosanna Nagtegaal
nudging <- template
nudging["paper", ] <- c(2006, 377, 100) 
```

``` r
# data is not public yet

# raw --------------------------------------------------------------------------
n_raw <- read.csv("raw/nagtegaal.csv")
#n_rr <- read.csv2("https://dataverse.harvard.edu/api/access/datafile/:persistentId?persistentId=doi:10.7910/DVN/WMGPGZ/HY6N2S",
                 # sep = ",")
#n_rr <- fread("https://dataverse.harvard.edu/api/access/datafile/:persistentId?persistentId=doi:10.7910/DVN/WMGPGZ/HY6N2S",
              #    sep = ",", encoding = "UTF-8")
# missing statistics
drops["nudging",] <- n_raw %>%
          summarise(n = length(abstract),
                    na = sum(is.na(abstract)),
                    na_rate = sum(is.na(abstract))/length(abstract)*100,
                    dup = sum(duplicated(abstract, incomparables = NA)),
                    dup_rate = sum(duplicated(abstract, incomparables = NA))/length(abstract)*100)
# asreview ---------------------------------------------------------------------

# remove missing abstracts 
nudging_test <- n_raw %>%
  drop_na(abstract) %>% # drop entries with missing abstracts
  filter(abstract != "", abstract != "NA") %>%
  distinct(abstract, .keep_all = TRUE) %>% # remove entries with duplicate abstracts
  mutate(id = X)

nudging["test", ] <- data_descr(nudging_test)
```

### Some statistics

On missingness (\# and %) and duplicates (\# and %):

|         |    n |  na |  narate | dup |   duprate |
| :------ | ---: | --: | ------: | --: | --------: |
| nudging | 2019 | 169 | 8.37048 |   3 | 0.1485884 |

On total number of publications, abstract inclusions (this information
was not available for this dataset) and final inclusions.

|          | search | ftext | incl |
| :------- | -----: | ----: | ---: |
| paper    |   2006 |   377 |  100 |
| raw      |      0 |     0 |    0 |
| asreview |      0 |     0 |    0 |
| test     |   1847 |   382 |  100 |

## PTSD dataset

``` r
ptsd <- template 
ptsd["paper", ] <- c(6185, 363, 38) # from flowchart 

# raw --------------------------------------------------------------------------
ptsd["raw", ] 
```

    ##     search ftext incl
    ## raw      0     0    0

``` r
# asreview ---------------------------------------------------------------------
ptsd_asr <- read.csv("https://raw.github.com/asreview/systematic-review-datasets/master/datasets/Van_de_Schoot_PTSD/output/PTSD_VandeSchoot_18.csv", 
                     header=T)

ptsd["asreview", ] <- data_descr(ptsd_asr)

# statistics on duplicates from asr data to test
drops["ptsd", ] <- ptsd_asr %>%
  summarise(n = length(abstract),
                    na = sum(is.na(abstract)),
                    narate = sum(is.na(abstract))/length(abstract)*100,
                    dup = sum(duplicated(abstract, incomparables = NA)),
                    duprate = sum(duplicated(abstract, incomparables = NA))/length(abstract)*100)
```

### Create test dataset

Now, remove duplicate entries and empty abstracts to arrive at test set.

``` r
ptsd_test <- ptsd_asr %>%
  drop_na(abstract) %>% # drop entries with missing abstracts
  filter(abstract != "", abstract != "NA") %>%
  distinct(abstract, .keep_all = TRUE)# remove entries with duplicate abstracts
```

There are 38 inclusions in this dataset, should be 34.

``` r
# get rid of 4 extra inclusions (see log book)
excl <- 
  ptsd_test %>%
  filter(included == 1, 
         str_detect(authors, "Sterling, M., Hendrikz, J., Kenardy, J.") |
         str_detect(authors, "Hou") |
         str_detect(authors, "Mason") |
         str_detect(authors, "Pérez")) %>%
  select(id)

indices <- ptsd_test$id %in% excl

# get rid of 4 papers
ptsd_test[indices, "included"] <- 0
```

``` r
# finalize dataset  
ptsd_test <- ptsd_test %>%
  select(id, authors, title, abstract, keywords, included, inclusion_code) # select relevant columns

ptsd["test", ] <- data_descr(ptsd_test)
```

### Some statistics

On missingness (\# and %) and duplicates (\# and %):

|      |    n | na | narate | dup |  duprate |
| :--- | ---: | -: | -----: | --: | -------: |
| ptsd | 5782 |  0 |      0 | 750 | 12.97129 |

On total number of publications, abstract inclusions (this information
was not available for this dataset) and final inclusions.

|          | search | ftext | incl |
| :------- | -----: | ----: | ---: |
| paper    |   6185 |   363 |   38 |
| raw      |      0 |     0 |    0 |
| asreview |   5782 |   356 |   38 |
| test     |   5031 |   328 |   38 |

## Software dataset

``` r
hall <- template

# paper ------------------------------------------------------------------------
hall["paper", ] <- c(8911, NA, 104)

# raw --------------------------------------------------------------------------
h_raw <- read.csv("https://zenodo.org/record/1162952/files/Hall.csv",
                  header=T)

hall["raw", ] <- c(length(h_raw$Document.Title),
                   NA,
                   sum(h_raw$label == "yes"))
                          
# asreview ---------------------------------------------------------------------
hall_asr <- read.csv("https://raw.githubusercontent.com/asreview/systematic-review-datasets/master/datasets/Four%20Software%20Engineer%20Data%20Sets/output/Software_Engineering_Hall.csv",
                     header=T)

hall["asreview", ] <- data_descr(hall_asr)
```

### Creating test dataset

``` r
hall_test <- hall_asr %>%
   drop_na(abstract) %>% # drop entries with missing abstracts
   filter(abstract != "") %>%
   distinct(abstract, .keep_all = TRUE) # remove entries with duplicate abstracts

hall_test <- hall_test %>% # add id
  mutate(id = 1:nrow(hall_test))
   
hall["test", ] <- data_descr(hall_test)
```

``` r
drops["software", ] <- 
  hall_asr %>%
  summarise(n = length(abstract),
                    na = sum(is.na(abstract)),
                    narate = sum(is.na(abstract))/length(abstract)*100,
                    dup = sum(duplicated(abstract, incomparables = NA)),
                    duprate = sum(duplicated(abstract, incomparables = NA))/length(abstract)*100)
```

### Some statistics

On missingness (\# and %) and duplicates (\# and %):

|    |  n | na | narate | dup | duprate |
| :- | -: | -: | -----: | --: | ------: |
| NA | NA | NA |     NA |  NA |      NA |

On total number of publications, abstract inclusions (this information
was not available for this dataset) and final inclusions.

|          | search | ftext | incl |
| :------- | -----: | ----: | ---: |
| paper    |   8911 |    NA |  104 |
| raw      |   8911 |    NA |  104 |
| asreview |   8911 |    NA |  104 |
| test     |   8896 |    NA |  104 |

## Virus dataset

``` r
virus <- template
virus["paper",] <- c(2481, 132, 120)
v_raw <- read.csv("raw/virus.csv")
v_raw$abstract[v_raw$abstract == ""] <- NA

virus["raw", ] <- data_descr(v_raw)

drops["virus", ] <- 
  v_raw %>%
  summarise(n = length(abstract),
                    na = sum(is.na(abstract)),
                    narate = sum(is.na(abstract))/length(abstract)*100,
                    dup = sum(duplicated(abstract, incomparables = NA)),
                    duprate = sum(duplicated(abstract, incomparables = NA))/length(abstract)*100)

v_test <- v_raw %>%
  drop_na(abstract) %>% # drop entries with missing abstracts
   filter(abstract != "") %>%
   distinct(abstract, .keep_all = TRUE)# remove entries with duplicate abstracts

virus["test",] <- data_descr(v_test)
```

### Some statistics

On missingness (\# and %) and duplicates (\# and %):

|       |    n |  na |   narate | dup |   duprate |
| :---- | ---: | --: | -------: | --: | --------: |
| virus | 2481 | 176 | 7.093914 |   1 | 0.0403063 |

On total number of publications, abstract inclusions (this information
was not available for this dataset) and final inclusions.

|          | search | ftext | incl |
| :------- | -----: | ----: | ---: |
| paper    |   2481 |   132 |  120 |
| raw      |   2481 |    NA |  120 |
| asreview |      0 |     0 |    0 |
| test     |   2304 |    NA |  114 |

## Wilson dataset

``` r
wilson <- template
# paper ------------------------------------------------------------------------
wilson["paper", ] <- c(3453, 174, 26)

# raw --------------------------------------------------------------------------
# w_ftext <- read.delim("../datasets/raw/DOKU_All FT-Screening_20200116_cap.txt")
# w_incl <- read.csv("../datasets/raw/DOKU_All Included_20200116_cap.csv")
# w_all <- read.csv("../datasets/raw/DOKU_All TiAb-Screening_20200116_cap.csv")
# wilson["raw", ] <- c(nrow(w_all), nrow(w_ftext), nrow(w_incl))
wilson["raw", ] <- c(3453, 174, 26) # looked it up

# asreview ---------------------------------------------------------------------
w_asr <- read.csv("https://raw.github.com/asreview/systematic-review-datasets/master/datasets/Appenzeller-Herzog_Wilson/output/output_csv_wilson.csv", header=T)

w_asr[w_asr$abstract == "", "abstract"] <- NA
drops["wilson", ] <- w_asr %>%
   summarise(n = length(abstract),
                    na = sum(is.na(abstract)),
                    narate = sum(is.na(abstract))/length(abstract)*100,
                    dup = sum(duplicated(abstract, incomparables = NA)),
                    duprate = sum(duplicated(abstract, incomparables = NA))/length(abstract)*100)
# add inclusion_code label 
w_asr$inclusion_code <- w_asr$label_abstract_screening + w_asr$label_included
w_asr$included <- w_asr$label_included
wilson["asreview", ] <- data_descr(w_asr)
```

``` r
# create test dataset
w_test <- w_asr %>%
  drop_na(abstract) %>% # drop entries with missing abstracts
  distinct(abstract, .keep_all = TRUE) # remove entries with duplicate abstracts

wilson["test",] <- data_descr(w_test)
```

### Some statistics

On missingness (\# and %) and duplicates (\# and %):

|        |    n |   na |  narate | dup |  duprate |
| :----- | ---: | ---: | ------: | --: | -------: |
| wilson | 3437 | 1090 | 31.7137 |  14 | 0.407332 |

On total number of publications, abstract inclusions (this information
was not available for this dataset) and final inclusions.

|          | search | ftext | incl |
| :------- | -----: | ----: | ---: |
| paper    |   3453 |   174 |   26 |
| raw      |   3453 |   174 |   26 |
| asreview |   3437 |   174 |   26 |
| test     |   2333 |   155 |   23 |

# Save descriptive statistics on all datasets

``` r
# put everything together in list. 
all <- list(Ace = ace,
            Nudging = nudging,
            PTSD = ptsd,
            Software = hall,
            Virus = virus,
            Wilson = wilson)

# save datafile, to serve as data for descriptive table in manuscript
saveRDS(all, file = "data_statistics/all.RDS")
saveRDS(drops, file = "data_statistics/drops.RDS")
```

# Statistics

All candidate papers, paper selected for full text screening, papers
included in final review and inclusion rate, for the test datasets.

|                  |      |         |      |          |       |        |
| :--------------- | :--- | :------ | :--- | :------- | :---- | :----- |
| Dataset          | Ace  | Nudging | PTSD | Software | Virus | Wilson |
| candidates\_test | 2235 | 1847    | 5031 | 8896     | 2304  | 2333   |
| fulltext\_test   | NA   | 382     | 328  | NA       | NA    | 155    |
| incl\_test       | 41   | 100     | 38   | 104      | 114   | 23     |
| inclrate\_test   | 1.83 | 5.41    | 0.76 | 1.17     | 4.95  | 0.99   |

Descriptives on missingness and duplicate abstracts in the raw datasets:

|          |    n |   NA | NA rate (%) | duplicates | duplicate rate (%) |
| :------- | ---: | ---: | ----------: | ---------: | -----------------: |
| ace      | 2544 |  309 |       12.15 |          0 |               0.00 |
| nudging  | 2019 |  169 |        8.37 |          3 |               0.15 |
| ptsd     | 5782 |    0 |        0.00 |        750 |              12.97 |
| software | 8911 |    0 |        0.00 |         15 |               0.17 |
| virus    | 2481 |  176 |        7.09 |          1 |               0.04 |
| wilson   | 3437 | 1090 |       31.71 |         14 |               0.41 |

# Write all test dataset files

``` r
# ace
write.csv(ace_test %>%  select(pubmedID, authors, title, abstract, keywords, label_included), "test_datasets/ace.csv", row.names = FALSE)

# nudging (no keywords available)
write.csv(nudging_test %>% select(id, title, abstract, included), "test_datasets/nudging.csv", row.names = FALSE)

# ptsd
write.csv(ptsd_test %>% select(id, authors, title, abstract, keywords, included), "test_datasets/ptsd.csv", row.names = FALSE)

# hall (no keywords available )
write.csv(hall_test, "test_datasets/software.csv", row.names = FALSE)

# virus 
write.csv(v_test %>% select(id, authors, title, abstract, keywords, included), "test_datasets/virus.csv", row.names = FALSE)

# wilson
write.csv(w_test %>% select(id, authors, title, abstract, keywords, included), "test_datasets/wilson.csv", row.names = FALSE)
```

# write test dataset files for simulation (removing keywords)

``` r
# ace
write.csv(ace_test %>%  select(pubmedID, title, abstract, label_included), "sim_datasets/ace.csv", row.names = FALSE)
# nudging (no keywords available)
write.csv(nudging_test %>% select(id, title, abstract, included), "sim_datasets/nudging.csv", row.names = FALSE)
# ptsd
write.csv(ptsd_test %>% select(id, title, abstract, included), "sim_datasets/ptsd.csv", row.names = FALSE)
# hall (no keywords available )
write.csv(hall_test, "sim_datasets/software.csv", row.names = FALSE)
# virus 
write.csv(v_test %>% select(id, title, abstract, included), "sim_datasets/virus.csv", row.names = FALSE)
# wilson
write.csv(w_test %>% select(id, title, abstract, included), "sim_datasets/wilson.csv", row.names = FALSE)
```

# References

<div id="refs" class="references hanging-indent">

<div id="ref-Appenzeller-Herzog2020">

Appenzeller-Herzog, Christian. 2020. “Data from Comparative
Effectiveness of Common Therapies for Wilson Disease: A Systematic
Review and Meta‐analysis of Controlled Studies.” Zenodo.
<https://doi.org/10.5281/zenodo.3625931>.

</div>

<div id="ref-Appenzeller-Herzog2019">

Appenzeller‐Herzog, Christian, Tim Mathes, Marlies L. S. Heeres, Karl
Heinz Weiss, Roderick H. J. Houwen, and Hannah Ewald. 2019. “Comparative
Effectiveness of Common Therapies for Wilson Disease: A Systematic
Review and Meta-Analysis of Controlled Studies.” *Liver Int.* 39 (11):
2136–52. <https://doi.org/10.1111/liv.14179>.

</div>

<div id="ref-Cohen2006">

Cohen, A. M., W. R. Hersh, K. Peterson, and Po-Yin Yen. 2006. “Reducing
Workload in Systematic Review Preparation Using Automated Citation
Classification.” *J Am Med Inform Assoc* 13 (2): 206–19.
<https://doi.org/10.1197/jamia.M1929>.

</div>

<div id="ref-Hall2012">

Hall, Tracy, Sarah Beecham, David Bowes, David Gray, and Steve Counsell.
2012. “A Systematic Literature Review on Fault Prediction Performance in
Software Engineering.” *IEEE Trans. Softw. Eng.* 38 (6): 1276–1304.
<https://doi.org/10.1109/TSE.2011.103>.

</div>

<div id="ref-Kwok2020">

Kwok, Kirsty T. T., David F. Nieuwenhuijse, My V. T. Phan, and Marion P.
G. Koopmans. 2020. “Virus Metagenomics in Farm Animals: A Systematic
Review.” *Viruses* 12 (1, 1): 107. <https://doi.org/10.3390/v12010107>.

</div>

<div id="ref-Nagtegaal2019a">

Nagtegaal, Rosanna, Lars Tummers, Mirko Noordegraaf, and Victor Bekkers.
2019a. “Nudging Healthcare Professionals Towards Evidence-Based
Medicine: A Systematic Scoping Review.” Harvard Dataverse.
<https://doi.org/10.7910/DVN/WMGPGZ>.

</div>

<div id="ref-Nagtegaal2019">

———. 2019b. “Nudging Healthcare Professionals Towards Evidence-Based
Medicine: A Systematic Scoping Review.” *J. Behav. Public Adm.* 2 (2).
<https://doi.org/doi.org/10.30636/jbpa.22.71>.

</div>

<div id="ref-vandeSchoot2017">

Schoot, Rens van de, Marit Sijbrandij, Sonja D. Winter, Sarah Depaoli,
and Jeroen K. Vermunt. 2017. “The GRoLTS-Checklist: Guidelines for
Reporting on Latent Trajectory Studies.” *Struct. Equ. Model.
Multidiscip. J.* 24 (3): 451–67. <https://doi.org/10/gdpcw9>.

</div>

</div>
