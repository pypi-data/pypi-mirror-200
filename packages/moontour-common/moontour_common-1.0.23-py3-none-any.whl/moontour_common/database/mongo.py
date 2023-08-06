import os

import pymongo

host = os.getenv('MONGO_HOST', 'mongo')
mongo_client = pymongo.MongoClient(host).get_database('Moontour')
