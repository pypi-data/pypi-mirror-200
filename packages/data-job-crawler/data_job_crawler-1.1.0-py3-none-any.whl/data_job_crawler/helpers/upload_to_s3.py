import boto3
from datetime import datetime
from data_job_crawler.config.definitions import BUCKET

today = datetime.now().strftime('%d-%m-%y')
s3 = boto3.resource('s3')

s3.Bucket(BUCKET).upload_file(f"/Users/donor/PycharmProjects/data-job-crawler/data_job_crawler/crawler/spiders/data"
                              f"/wttj_links_{today}.txt", f"wttj_links_{today}.txt")
