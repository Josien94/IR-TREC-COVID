# IR-TREC-COVID

This project includes creating a search engine related to the TREC-COVID challenge. In particular, a _BM25F_ algorithm is used, where the field-specific length normalisation _b_ is alterated.

The data that is used for this research - originated from the COVID-19 Open Research Dataset (CORD-19) - is retrieved from [Amazon AWS](https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/historical_releases.html). TheTREC-COVID challenge of 2020 had several rounds. We used the latest (5th) round to collect the most up to date dataset. This round uses the release of July 16th 2020 of the CORD-19 dataset. It consists of parsed biomedical literature articles, where each paragraphshould be annotated with a section (e.g. "Introduction", "Methods").

The test set for the TREC-COVID challenge - provided by NIST - is retrieved from the [main website](https://ir.nist.gov/covidSubmit/data.html). Here, also the used topic set for the TREC-COVID challenge is included. Furthermore, NIST provides a [standard tool](https://github.com/usnistgov/trec_eval) for evaluation of the TREC results, which compares the submitted results against the test results.

The main steps of the project are:

1. Get Data
2. Index Data
3. Search data
4. Evaluate results.

To execute the first 3 steps, execute **IR-TREC-COVD.sh**.

Then, follow the [instructions](<(https://github.com/usnistgov/trec_eval)>) fir installing _trec_eval_.
To evalaute the results, please execute the following steps:

1. Make three folders in the root folder of _trec_eval_ called "inputF1", "inputF2", "inputF3"
2. Place the output files of the first three steps in the corresponding folder (i.e. "outputF1 -> inputF1")
3. Make three folders in the root folder of _trec_eval_ called "outputF1", "outputF2", "ouputF3"
4. Run **executeTREC.sh**
5. The output results are placed in the output Folders
6. Run **src/plots.py** in the root folder of _trec_eval_ to generate plots
