import os

from dotenv import load_dotenv
from google.cloud import storage
from weaviate.embedded import EmbeddedOptions
import weaviate
from QAChat.Common.init_db import clear_db
from get_tokens import get_tokens_path

load_dotenv(get_tokens_path())
bucket_name = "qabot_db_data"
blob_folder = "weaviate"
weaviate_client = weaviate.Client(embedded_options=EmbeddedOptions())



def upload_database():
    """Uploads a file to the bucket."""

    result = weaviate_client.backup.create(
        backup_id='weaviate',
        backend='gcs',
        include_classes=['Embeddings', 'LoadedChannels', 'LastModified', 'BlackList'],
        wait_for_completion=True,
    )
    print(result)


def download_database():
    """Downloads a blob from the bucket."""
    clear_db(weaviate_client)
    result = weaviate_client.backup.restore(
        backup_id="weaviate",
        backend="gcs",
        wait_for_completion=True,
    )

    print(result)


def main():
    download_database()


if __name__ == "__main__":
    main()
