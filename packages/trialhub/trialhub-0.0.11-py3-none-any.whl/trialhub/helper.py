import itertools
import json
import pkg_resources

# A helper function to break an iterable into chunks of size batch_size.
def chunks(iterable, batch_size=100):        
    it = iter(iterable)
    chunk = tuple(itertools.islice(it, batch_size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it, batch_size))


from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

def get_secret(secret_name):
    credential = DefaultAzureCredential(additionally_allowed_tenants=['*'])
    secret_client = SecretClient(vault_url="https://trialhub-helpers.vault.azure.net/", credential=credential)
    secret = secret_client.get_secret(secret_name)
    return secret.value

def get_pubmed_types():
    config = json.loads(pkg_resources.resource_string(__name__, "config.json"))
    return config["pubmed"]["relevant_publication_types"]