from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json
from config import API_KEY
from template import ruleset

#cloud configuration files to connect to astra vector database
cloud_config={
    "secure_connect_bundle":"secure-connect-ai-db.zip"
}

#loads json file required to database configuration
with open("ai_db-token.json") as ai_db:
    secrets = json.load(ai_db)

CLIENT_ID = secrets["clientId"]
CLIENT_SECRET = secrets["secret"]

auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config,auth_provider=auth_provider)
session = cluster.connect()

row = session.execute("select release_version from system.local").one()

if row:
    print(row[0])
else: 
    print("An error occured")
