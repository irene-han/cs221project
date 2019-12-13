# A Biomarker Panel for Depression: An AI Approach
## Code:

#### For our baseline experiment, we ran the following commands:
python3 logistic.py

python3 k-means.py

#### For our p-progress experiment, we ran the following python commands:
python3 extract.py //note 1

python3 gbm.py

#### For our final experiments on broad depression, we ran the following python commands:
python3 process.py //note 2

python3 gbm.py

#### For our final experiments on probable depression, we ran the following python commands:
python3 probable_depression.py //note 3

python3 gbm.py //note 4



## Note:
1 This program takes raw data from the UK BioBank and outputs normalized data to the text file: “data_biomarkers_normalized”. This output file does not contain interaction terms.

2 This program takes raw data from the UK BioBank and outputs pre-processed data to the text file: “data_biomarkers_normalized_by_age_v2”. This output file does contain interaction terms.
This program is equivalent to process.py, but uses “probable depression” labels instead of “broad depression labels”

3 This program runs our gbm and DBSCAN algorithms.

## Data:
Our data came from the UK BioBank, a private database. We made up a fake database of 10 participants for “data_biomarkers_normalized” and ““data_biomarkers_normalized_by_age_v2” using the following command:
python3 generate_fake_data.py

All fake data files contain the prefix: “fake_”
