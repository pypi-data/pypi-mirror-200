from .pubmed_entrez import PubMedEntrez
from .azure_storage import AzureStorage
import json


class PubMedDownload:
    def __init__(self):
        self.pubmed_api = PubMedEntrez()
        self.azure_storage = AzureStorage()

    def download_to_azure(self, query, container_name, file_name, max_results=100, skip_results=0, batch_size = 50):
        blob = self.azure_storage.download_blob(container_name, file_name)
        
        if blob is None:
            blob_data = []
        else:
            blob_data = json.loads(blob.decode('utf-8'))
        
        search_results = self.pubmed_api.search(query, max_results, skip_results)
        id_list = search_results["IdList"]
        
        total_results = int(search_results["Count"])

        returned_results = len(id_list)
        print("Pubmed returned " + str(returned_results) + " results out of " + str(total_results) + " total results")

        # post the IDs to the server
        post_results = self.pubmed_api.post_ids(id_list)

        # Get the WebEnv and QueryKey
        webenv = post_results["WebEnv"]
        query_key = post_results["QueryKey"]

        for start in range(0, returned_results, batch_size):
            end = min(returned_results, start + batch_size)
            print("Going to download record %i to %i" % (start + 1, end))
            try:
                data = self.pubmed_api.fetch_details_by_webenv(webenv, query_key, batch_size, start)
                # print(data["PubmedArticle"])
                blob_data.extend(data["PubmedArticle"])
            except Exception as e:
                print("Error downloading records " + str(start + 1) + " to " + str(end))
                print(e)
                break

        # Upload the file to Azure Storage
        self.azure_storage.upload_blob(container_name, file_name, json.dumps(blob_data), True)

        print("Downloaded " + str(returned_results) + " records")
