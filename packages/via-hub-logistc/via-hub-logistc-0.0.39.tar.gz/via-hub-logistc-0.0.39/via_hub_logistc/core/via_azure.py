from azure.storage.blob import BlobServiceClient

from robot.api.deco import keyword
from robot.api import Error

class blob():
    ###connect to blob service###
    @keyword(name="conect azure blob")
    def conect_azure_blob(self, host, account_name, account_key):
        try:
            str_conn = f'DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointsSuffix={host}'

            return  BlobServiceClient.from_connection_string(str_conn)
        except Exception as e:
            raise Error(e)


    ###List all directories in a container###
    @keyword(name="list all directories in container")
    def list_all_directories_in_container(self, connection, container_name, folder, format=True):
        try:

            client = connection.get_container_client(container_name)

            directories = []

            for file in client.walk_blobs(folder, delimiter='/'):
                if format == False:
                    directories.append(file.name)
                else:
                    directories.append(file.name[4:-1])

            return directories
        except Exception as e:
            raise Error(e)
    
    ### checks if the folder exists in the container ###
    @keyword(name="is exist directory in container")
    def is_exist_directory_in_container(self, connection, container_name, folder, directory):
        try:

            client = connection.get_container_client(container_name)

            for file in client.walk_blobs(folder, delimiter='/'):
                if directory.casefold() == str(file.name[4:-1]).casefold():
                    return file.name[4:-1]

            return None
        except Exception as e:
            raise Error(e)
