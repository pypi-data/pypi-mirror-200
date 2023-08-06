import psycopg2

from data_job_crawler.config.definitions import JOB_MARKET_DB_PWD, JOB_MARKET_DB_USER


class OldJobsCrawlerPipeline:
    def __init__(self):
        self.connection = None
        self.cur = None

    def open_spider(self, spider):
        hostname = 'localhost'
        username = JOB_MARKET_DB_USER
        password = JOB_MARKET_DB_PWD
        database = 'job_market'
        self.connection = psycopg2.connect(
            host=hostname, user=username, password=password,
            dbname=database)
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        for field in item.fields:
            item.setdefault(field, 'NULL')
        try:
            print('\n'*2, item, '\n'*2)
            self.cur.execute(
                "SELECT id, url FROM processed_jobs WHERE url ~ %s;",
                (item['old_url'][0]))
            self.cur.execute(
                "SELECT id, url FROM processed_jobs WHERE url ~ %s;",
                (item['old_url'][0]))
            self.connection.commit()
        except:
            self.connection.rollback()
            raise
        return item


class JobsCrawlerPipeline:

    def __init__(self):
        self.connection = None
        self.cur = None

    def open_spider(self, spider):
        hostname = 'localhost'
        username = JOB_MARKET_DB_USER
        password = JOB_MARKET_DB_PWD
        database = 'job_market'
        self.connection = psycopg2.connect(
            host=hostname, user=username, password=password,
            dbname=database)
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        for field in item.fields:
            item.setdefault(field, 'NULL')
        try:
            self.cur.execute(
                "INSERT INTO raw_jobs(url, title, company, location, type, industry, text, remote, created_at) "
                "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                "ON CONFLICT (url) DO UPDATE "
                "SET title=EXCLUDED.title, location=EXCLUDED.location;",
                (item['url'][0], item['title'][0], item['company'][0], item['location'][0], item['type'][0],
                 item['industry'][0], item['text'][0], item['remote'][0], item['created_at'][0]))
            self.connection.commit()
        except:
            self.connection.rollback()
            raise
        return item
