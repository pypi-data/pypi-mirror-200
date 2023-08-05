import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


import pinecone
from tqdm import tqdm
from time import sleep
import json
from .helper import chunks, get_secret
import pkg_resources

class VectorDB:
    def __init__(self):
         # load the connection string from a config file
        config = json.loads(pkg_resources.resource_string(__name__, "config.json"))
        
        index_name = config["pinecone"]["index_name"]
        api_key = get_secret("pinecone-api-key")
        environment = config["pinecone"]["environment"]
        self.vector_size = config["pinecone"]["vector_size"]
               
        pinecone.init(
            api_key=api_key,
            environment=environment, 
            vector_size=self.vector_size, 
        )
       
        self.index = pinecone.Index(index_name)
        # view index stats
        print(self.index.describe_index_stats())

    

    def is_vector_indexed(self, id):
        vector1 = [float(0.1) for i in range(self.vector_size)]
        res = self.index.query(
            vector=vector1,
            filter={
                'id': id
            },
            top_k=1, 
            include_metadata=False
        )

        return len(res['matches']) == 1
    
    def upsert(self, ids, embeddings, metadata, namespace=None, batch_size=100):
        to_upsert = list(zip(ids, embeddings, metadata))
       
        for to_upsert_chunk in chunks(to_upsert, batch_size):
            self.index.upsert(
                vectors=to_upsert_chunk,
                namespace=namespace
            )
    
    def query(self, vector, filter=None, top_k=10, include_metadata=True, namespace=None):
        res = self.index.query(
            vector=vector,
            filter=filter,
            top_k=top_k, 
            include_metadata=include_metadata,
            namespace=namespace
        )
        return res
    