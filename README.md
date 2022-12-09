# New York Violation location predictor
This project is about training a model on big data and predicting Violation location using [New York parking violations](https://www.kaggle.com/new-york-city/nyc-parking-tickets) data for the year 2013-2014 using pyspark

## Introduction
Given New York parking Violations data, the main objective is to build a machine learning model and be able to predict real time as the data is streamed.
1. For building ML model on the big data, Pyspark was used. Random forest and XGBoost were used to predict Violation locations. Lot of preprocessing was done, more information can be obtained from `Quarantined Cops_Final Project.pdf`. Overall XGboost achieved 99.4% accuracy and Random forest achieved 95% accuracy on the test dataset
2. Using Kafka and google pubsub, data from google cloud storage was streamed to kafka server using google pubsub. With the help of sparkstreaming in dataproc, streamed data was predicted with a latency of 4.8secs for batch of 3 data sent every 30secs

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Libraries needed

```
xgboost
pandas
pickle
sklearn
```

## Information about files
##final

New terminal:

```

hdfs namenode -format
start-dfs.sh
hadoop fs -put small_temp.csv /user/input/small_temp.csv
```

New terminal:

```
python Train_dataproc.py
```

2. New terminal:

```
python producer.py
```
3. New terminal:

```
python Real_time.py
```

