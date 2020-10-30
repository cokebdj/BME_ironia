import pandas as pd
import numpy as np
import json
import boto3

input_file_data = 's3:///sagemakerbmeironia/atenea_bme/data.csv'
input_file_names = 's3://sagemakerbmeironia/atenea_bme/names.csv'

data = pd.read_csv(input_file_data)
data['date_ws'] = data['date'].apply(lambda x:  x+ " 00:00:00")
data_pivot = pd.pivot_table(data, values='nav', index=['date_ws'], columns=['ironia_id'], aggfunc=np.sum)
data_pivot.to_csv('data.csv', sep=';')

names = pd.read_csv(input_file_names)
names['len'] = names['name'].apply(lambda x: len(x))
name_max = names.groupby(by='ironia_id')['len'].min().to_dict()
names['keep'] = names.apply(lambda row: row['len']==name_max[row['ironia_id']], axis=1)
dict_names = names.loc[names['keep']][['ironia_id', 'name']].set_index('name').to_dict()['ironia_id']

with open('names.json', 'w') as out_file:
    out = json.dumps(dict_names)
    out_file.write(out)
    
s3 = boto3.resource('s3')
s3.meta.client.upload_file('names.json', 'sagemakerbmeironia', 'sagemaker_input_data/names.json')
s3.meta.client.upload_file('data.csv', 'sagemakerbmeironia', 'sagemaker_input_data/data.csv')