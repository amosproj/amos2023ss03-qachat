import os

from dotenv import load_dotenv
from google.cloud import storage
from weaviate.embedded import DEFAULT_PERSISTENCE_DATA_PATH

from get_tokens import get_tokens_path
import shutil

load_dotenv(get_tokens_path())
bucket_name = "qabot_db_data"
blob_folder = "weaviate"


def upload_database():
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    # The path to your file to upload
    source_file_folder = DEFAULT_PERSISTENCE_DATA_PATH

    blobs = bucket.list_blobs(prefix=blob_folder)
    # Delete blobs
    for blob in blobs:
        blob.delete()

    for root, dirs, files in os.walk(source_file_folder):
        for file in files:
            local_file = os.path.join(root, file)
            destination_blob_name = blob_folder + local_file[len(source_file_folder):]
            print(f"{local_file} to {destination_blob_name}")
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(local_file)


def download_database():
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    destination_file_folder = DEFAULT_PERSISTENCE_DATA_PATH

    if os.path.exists(destination_file_folder):
        # Remove the folder
        shutil.rmtree(destination_file_folder)

    blobs = bucket.list_blobs(prefix=blob_folder)
    for blob in blobs:
        filename = blob.name

        source_file_name = (
                destination_file_folder + "/" + "/".join(str(filename).split("/")[1:])
        )
        directory = os.path.dirname(source_file_name)
        if not os.path.isdir(directory):
            os.makedirs(directory)

        blob.download_to_filename(source_file_name)


def main():
    download_database()


if __name__ == "__main__":
    main()
