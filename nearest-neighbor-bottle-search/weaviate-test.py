import os
import weaviate


WEAVIATE_URL = os.getenv('WEAVIATE_URL')
if not WEAVIATE_URL:
    WEAVIATE_URL = 'http://127.0.0.1:8000'

client = weaviate.Client(WEAVIATE_URL)
schema = client.schema.get()
print(schema)
