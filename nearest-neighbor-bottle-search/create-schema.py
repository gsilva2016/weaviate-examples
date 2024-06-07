import os
import weaviate

WEAVIATE_URL = os.getenv('WEAVIATE_URL')
if not WEAVIATE_URL:
    WEAVIATE_URL = 'http://localhost:8080'

print(WEAVIATE_URL, flush=True)

client = weaviate.Client(WEAVIATE_URL)

# creating the Dog class with the following properties: breed, image, and filepath

schema = {
    "classes": [
        {
            "class": "Bottle",
            "description": "Images of different bottles",
            "moduleConfig": {
                "img2vec-neural": {
                    "imageFields": [
                        "image"
                    ]
                }
            },
            "vectorIndexType": "hnsw", 
            "vectorizer": "img2vec-neural", # the img2vec-neural Weaviate module
            "properties": [
                {
                    "name": "brand",
                    "dataType": ["string"],
                    "description": "name of bottle brand",
                },
                {
                    "name": "image",
                    "dataType": ["blob"],
                    "description": "image",
                },
                {
                    "name": "filepath",
                    "dataType":["string"],
                    "description": "filepath of the images",
                }
            ]
        }
    ]
}

# adding the schema 
client.schema.create(schema)

print("The schema has been defined.")
