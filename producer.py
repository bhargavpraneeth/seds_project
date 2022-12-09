#!/usr/bin/python3                                                                                                      
                                                                                                                        
from kafka import KafkaProducer                                                                                         
from random import randint                                                                                              
from time import sleep                                                                                                  
import sys                                                                                                              
import pickle
import pandas as pd
import json

BROKER = 'localhost:9092'                                                                                               
TOPIC = 'tweets'                                                                                                      
                                                                                                                       
try:                                                                                                                    
    p = KafkaProducer(bootstrap_servers=BROKER, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
except Exception as e:                                                                                                  
    print(f"ERROR --> {e}")                                                                                             
    sys.exit(1)     

csv_path = "models/test.csv"
df_test = pd.read_csv(csv_path, sep = ',')  

for item in df_test.to_numpy():
    item = item.tolist()
    print(item)
    p.send(TOPIC, json.dumps(item))                                                                      
    sleep(randint(1,4))