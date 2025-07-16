from app.database import client
from pprint import pprint

def inspect_db():
    db = client["savorsync_db"]
    print("Collections in 'savorsync_db':")
    for collection_name in db.list_collection_names():
        print(f"\nCollection: {collection_name}")
        collection = db[collection_name]
        documents = list(collection.find())
        if not documents:
            print("  (No documents)")
        for doc in documents:
            pprint(doc)

if __name__ == "__main__":
    inspect_db() 