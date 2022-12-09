from kafka import KafkaProducer                                                                                         
from random import randint                                                                                              
from time import sleep                                                                                                  
import sys                                                                                                              
import pickle
import pandas as pd
import json
import time

BROKER = 'localhost:9092'                                                                                               
TOPIC = 'nyc'                                                                                                      
                                                                                                                       
try:                                                                                                                    
    p = KafkaProducer(bootstrap_servers=BROKER, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
except Exception as e:                                                                                                  
    print(f"ERROR --> {e}")                                                                                             
    sys.exit(1)     

csv_path = "small_temp.csv"
df_test = pd.read_csv(csv_path, sep = ',')  
data = df_test.to_numpy()

for lines in data[1:]:
    if len(lines)==0:
        break
    #Sleeps for 10 seconds
    print(lines)
    p.send(TOPIC, lines.tolist())
    time.sleep(10)
