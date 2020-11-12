import boto3
import pandas as pd
from newspaper import application
import io

def get_boto_client():
    s3 = boto3.client(
        's3', 
        aws_access_key_id=application.config['AWSAccessKeyId'],
        aws_secret_access_key=application.config['AWSSecretKey'],
        region_name=application.config['AWSRegion']
    )
    return s3

def read_dataset():
    obj = get_boto_client().get_object(Bucket= 'datainnews' , Key = 'all.csv')
    df = pd.read_csv(io.BytesIO(obj['Body'].read()), encoding='utf8')
    return df