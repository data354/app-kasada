import io
from azure.storage.blob import BlobServiceClient
from google.oauth2 import service_account
import os



# Configuration des autorisations Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
connect_str = "Your adls connexion strings"  # Remplacez par votre chaîne de connexion Azure
credential_path = os.getenv("CREDENTIALS_PATH")

def authenticate_google_drive():
# Replace 'FOLDER_NAME' with the name you want to give your new folder
#folder_name = 'Test Upload'
# setup google drive
    credentials = service_account.Credentials.from_service_account_file(
        'creds/credentials.json', scopes=['https://www.googleapis.com/auth/drive']
    )
    return credentials



def authenticate_azure_blob(connect_str):
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    return blob_service_client

def list_files_in_drive_folder(service, folder_id):
    # Ajout d'un filtre pour n'inclure que les fichiers dont le nom se termine par .xlsm
    query = f"'{folder_id}' in parents and mimeType != 'application/vnd.google-apps.folder' and name contains '.xlsm'"
    results = service.files().list(
        q=query,
        fields="files(id, name, mimeType)",
        pageSize=1000
    ).execute()
    return results.get('files', [])

def get_folder_name(service, folder_id):
    folder = service.files().get(fileId=folder_id, fields='name').execute()
    return folder.get('name', 'unknown_folder')

def download_file_from_drive(service, file_id):
    try:
        request = service.files().get_media(fileId=file_id)
        file_stream = io.BytesIO(request.execute())
        return file_stream
    except Exception as e:
        print(f"Erreur lors du téléchargement du fichier {file_id}: {e}")
        return None

def upload_file_to_azure_blob(blob_service_client, container_name, folder_name, file_name, file_stream):
    """
    Télécharge un fichier dans Azure Blob Storage, écrasant tout fichier existant avec le même nom.
    """
    if file_stream is not None:
        # Vérification et création du conteneur si nécessaire
        container_client = blob_service_client.get_container_client(container_name)
        if not container_client.exists():
            container_client.create_container()

        # Obtention du blob client et écrasement de l'ancien fichier
        blob_client = container_client.get_blob_client(f"{folder_name}/{file_name}")
        blob_client.upload_blob(file_stream, overwrite=True)
        
        print(f"Fichier {file_name} téléversé avec succès dans le dossier {folder_name} du conteneur {container_name}.")
        return True
    else:
        print(f"Le fichier {file_name} n'a pas été téléversé.")
        return False

def list_files_in_azure(blob_service_client, container_name, folder_name):
    container_client = blob_service_client.get_container_client(container_name)
    blob_list = container_client.list_blobs(name_starts_with=folder_name)
    azure_files = [blob.name.split('/')[-1] for blob in blob_list]  # Liste des noms de fichiers
    return azure_files

def delete_file_in_azure(blob_service_client, container_name, file_name):
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(file_name)
    blob_client.delete_blob()
    print(f"Fichier {file_name} supprimé du conteneur {container_name}.")
    