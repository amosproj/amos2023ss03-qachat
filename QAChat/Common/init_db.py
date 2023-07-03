# SPDX-FileCopyrightText: 2023 Felix Nützel
def init_db(weaviate_client):
    global client
    client = weaviate_client
    if not weaviate_client.schema.exists("Embeddings"):
        weaviate_client.schema.create_class(
            {
                "class": "Embeddings",
                "properties": [
                    {"name": "type_id", "dataType": ["string"]},
                    {"name": "type", "dataType": ["string"]},
                    {"name": "last_changed", "dataType": ["string"]},
                    {"name": "text", "dataType": ["string"]},
                ],
            }
        )
    if not weaviate_client.schema.exists("LastModified"):
        weaviate_client.schema.create_class(
            {
                "class": "LastModified",
                "properties": [
                    {"name": "type", "dataType": ["string"]},
                    {"name": "last_update", "dataType": ["string"]},
                ],
            }
        )

    if not weaviate_client.schema.exists("BlackList"):
        weaviate_client.schema.create_class(
            {
                "class": "BlackList",
                "properties": [
                    {"name": "identifier", "dataType": ["string"]},
                    {"name": "note", "dataType": ["string"]},
                ],
            }
        )

    if not weaviate_client.schema.exists("LoadedChannels"):
        weaviate_client.schema.create_class(
            {
                "class": "LoadedChannels",
                "properties": [
                    {"name": "channel_id", "dataType": ["string"]},
                    {"name": "channel_name", "dataType": ["string"]},
                ],
            }
        )


def clear_db(weaviate_client):
    return weaviate_client.schema.delete_all()


def add_entry_to_black_list(weaviate_client, identifier, note=None):
    return weaviate_client.data_object.create(
        {"identifier": identifier, "note": note}, "BlackList"
    )
