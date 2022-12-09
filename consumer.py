from kafka import KafkaConsumer
from json import loads
import ast
import pickle
import numpy as np
from process_inputs import missing, add_new_cols, write_csv
import pandas as pd
import json
import sys
import ast
from pyspark import SparkContext                                                                                        
from pyspark.sql import SparkSession                                                                                    
from pyspark.streaming import StreamingContext                                                                          
from pyspark.streaming.kafka import KafkaUtils


consumer = KafkaConsumer(
    'tweets',
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group')

mm = pickle.load(open("models/model.sav", 'rb'))

# sc = SparkContext(appName="Something")                                                                                     
# ssc = StreamingContext(sc, 5)                                                                                                                                                                                                              
ss = SparkSession.builder.appName("Something").config("spark.sql.warehouse.dir", "/user/hve/warehouse").config("hive.metastore.uris", "thrift://localhost:9083").enableHiveSupport().getOrCreate()                                                                                                  
ss.sparkContext.setLogLevel('WARN')                                                                                     


for message in consumer:
    # Get the message
    message = message.value.decode('utf8').replace("\n", '')

    # Preprocess the data
    X_test, org = write_csv(message)
    
    # Predict the data
    prediction = mm.predict(X_test.fillna(0))

    # Store the data
    data = [org + [str(prediction[0])]]
    print(data)
    df = ss.createDataFrame(data, schema=['Id', 'MSSubClass', 'MSZoning', 'LotFrontage', 'LotArea', 'Street', 'Alley', 'LotShape', 'LandContour', 'Utilities', 'LotConfig', 'LandSlope', 'Neighborhood', 'Condition1', 'Condition2', 'BldgType', 'HouseStyle', 'OverallQual', 'OverallCond', 'YearBuilt', 'YearRemodAdd', 'RoofStyle', 'RoofMatl', 'Exterior1st', 'Exterior2nd', 'MasVnrType', 'MasVnrArea', 'ExterQual', 'ExterCond', 'Foundation', 'BsmtQual', 'BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinSF1', 'BsmtFinType2', 'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF', 'Heating', 'HeatingQC', 'CentralAir', 'Electrical', '1stFlrSF', '2ndFlrSF', 'LowQualFinSF', 'GrLivArea', 'BsmtFullBath', 'BsmtHalfBath', 'FullBath', 'HalfBath', 'BedroomAbvGr', 'KitchenAbvGr', 'KitchenQual', 'TotRmsAbvGrd', 'Functional', 'Fireplaces', 'FireplaceQu', 'GarageType', 'GarageYrBlt', 'GarageFinish', 'GarageCars', 'GarageArea', 'GarageQual', 'GarageCond', 'PavedDrive', 'WoodDeckSF', 'OpenPorchSF', 'EnclosedPorch', '3SsnPorch', 'ScreenPorch', 'PoolArea', 'PoolQC', 'Fence', 'MiscFeature', 'MiscVal', 'MoSold', 'YrSold', 'SaleType', 'SaleCondition', 'pred'])
    df.write.saveAsTable(name='default.tweets', format='hive', mode='append')
    
