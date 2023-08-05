import pymongo
import json
from .helper import get_secret
import pkg_resources

class MongoDB:
    def __init__(self):
         # load the connection string from a config file
        config = json.loads(pkg_resources.resource_string(__name__, "config.json"))
        
        connection_string = get_secret("mongodb-connection-string")
        db_name = config["mongodb"]["db_name"]
        
        client = pymongo.MongoClient(connection_string, serverSelectionTimeoutMS=5000)
        try:
            print(client.server_info())
        except Exception:
            print("Unable to connect to the server.")

        self.db = client[db_name]
        