from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

uri = "mongodb+srv://NIGHTFURY:d5RX6H9wSFuMMTkJ@ragcluster.rcxx58o.mongodb.net/?appName=RAGcluster"

client = MongoClient(uri)

try:
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ping')
    print("Connection to MongoDB server was successful.")
    # 3. Verify the Database and Collection exist
    db = client["placement_rag"]
    collection = db["documents"]
    
    # 4. Check for your Vector Index
    indexes = list(collection.list_search_indexes())
    found = any(idx['name'] == 'vector_index' for idx in indexes)
    
    if found:
        print("✅ 'vector_index' is visible and ready for your RAG app.")
    else:
        print("⚠️ Connected, but 'vector_index' was not found in 'placement_rag.documents'.")
        print("Double-check your collection name in Atlas!")
except ConnectionFailure:
    print("❌ Connection failed. Check your IP Access List in Atlas.")
finally:
    client.close()