from azure.storage.blob import BlobServiceClient, ContainerClient
from azure.core.exceptions import ResourceNotFoundError
from .helper import get_secret

class AzureStorage:
    def __init__(self):
        azure_storage_connection_string = get_secret("azure-storage-connection-string")

        self.blob_service_client = BlobServiceClient.from_connection_string(
            azure_storage_connection_string
        )

    def create_container(self, container_name):
        container_client = self.blob_service_client.get_container_client(container_name)
        container_client.create_container()

    def delete_container(self, container_name):
        container_client = self.blob_service_client.get_container_client(container_name)
        container_client.delete_container()

    def list_containers(self):
        containers = self.blob_service_client.list_containers()
        return [container.name for container in containers]

    def update_container_metadata(self, container_name, metadata):
        container_client = self.blob_service_client.get_container_client(container_name)
        container_properties = container_client.get_container_properties()
        container_properties.metadata.update(metadata)
        container_client.set_container_metadata(container_properties.metadata)

    def read_container_metadata(self, container_name):
        container_client = self.blob_service_client.get_container_client(container_name)
        container_properties = container_client.get_container_properties()
        return container_properties.metadata

    def list_blobs(self, container_name):
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_list = container_client.list_blobs()
        return [blob.name for blob in blob_list]

    def upload_blob(self, container_name, blob_name, data, overwrite=False):
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(data, overwrite=overwrite)

    def download_blob(self, container_name, blob_name):
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        try:
            blob_data = blob_client.download_blob()
            return blob_data.content_as_text()
        except ResourceNotFoundError:
            return None
    
    def download_raw_blob(self, container_name, blob_name):
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        try:
            blob_data = blob_client.download_blob()
            return blob_data
        except ResourceNotFoundError:
            return None

    def delete_blob(self, container_name, blob_name):
        container_client = self.blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.delete_blob()
