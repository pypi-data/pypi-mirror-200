from Bio import Entrez
import json
import pkg_resources

class PubMedEntrez:
    def __init__(self):
        # load the connection string from a config file
        config = json.loads(pkg_resources.resource_string(__name__, "config.json"))

        self.email = config["pubmed"]["email"]

    # http://biopython.org/DIST/docs/tutorial/Tutorial.html#sec146
    def search(self, query, max_results=100, skip_results=0):
        Entrez.email = self.email
        handle = Entrez.esearch(db='pubmed',
                                retstart=skip_results,
                                sort='relevance',
                                retmax=max_results,
                                retmode='xml',
                                term=query)
        results = Entrez.read(handle)
        return results
    
    # http://biopython.org/DIST/docs/tutorial/Tutorial.html#sec%3Aefetch
    def fetch_details(self, id_list):
        ids = ','.join(id_list)
        Entrez.email = self.email
        handle = Entrez.efetch(db='pubmed',
                                retmode='xml',
                                id=ids)
        results = Entrez.read(handle)
        return results
    
    # http://biopython.org/DIST/docs/tutorial/Tutorial.html#sec147
    def post_ids(self, id_list):
        ids = ','.join(id_list)
        Entrez.email = self.email
        handle = Entrez.epost(db='pubmed',
                                id=ids)
        search_results = Entrez.read(handle)
        webenv = search_results["WebEnv"]
        query_key = search_results["QueryKey"]

        results = { "WebEnv": webenv, "QueryKey": query_key }
        return results
    
    # http://biopython.org/DIST/docs/tutorial/Tutorial.html#sec%3Aentrez-webenv
    def fetch_details_by_webenv(self, webenv, query_key, max_results=100, skip_results=0):
        Entrez.email = self.email
        handle = Entrez.efetch(db='pubmed',
                                retstart=skip_results,
                                retmax=max_results,
                                retmode='xml',
                                webenv=webenv,
                                query_key=query_key)
        results = Entrez.read(handle)
        return results
    
        # http://biopython.org/DIST/docs/tutorial/Tutorial.html#sec%3Aentrez-webenv
        # batch_size = 50
        # print("Count: " + str(itemsCount))
        # out_handle = open("pubmed.temp", "w")
        # for start in range(0, itemsCount, batch_size):
        #     end = min(itemsCount, start + batch_size)
        #     print("Going to download record %i to %i" % (start + 1, end))
        #     fetch_handle = Entrez.efetch(
        #         db="pubmed",
        #         retmode="xml",
        #         retstart=start,
        #         retmax=batch_size,
        #         webenv=webenv,
        #         query_key=query_key)
        #     data =  Entrez.read(fetch_handle)
        #     print(json.dumps(data))
        #     fetch_handle.close()
        #     out_handle.write(json.dumps(data))
        # out_handle.close()
        
        # return out_handle