from prefect_azure import AzureBlobStorageCredentials
from dotenv import load_dotenv
import os

load_dotenv('.env')

absc = AzureBlobStorageCredentials(
    connection_string=os.getenv("AZURE_STORAGE_CONNECTION_STRING")
)

absc.save('eventflows', overwrite=True)