from datetime import datetime
import ast
import boto3

from data_job_crawler.config.definitions import BUCKET


def extract_links_from_s3(website):
    today = datetime.now().strftime('%d-%m-%y')
    key = f'{website}_links_{today}.txt'
    s3 = boto3.resource('s3')
    obj = s3.Object(BUCKET, key)
    links = obj.get()['Body'].read().decode('utf-8')
    return ast.literal_eval(links)


def extract_links_from_file(filepath):
    with open(filepath, 'r') as f:
        lines = [line.rstrip('\n') for line in f]
    return lines[:10]
