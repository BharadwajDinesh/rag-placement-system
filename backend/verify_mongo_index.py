"""
Verify MongoDB Atlas vector index is created and working
"""

from pymongo import MongoClient
from app.config import get_settings
import sys

def verify_mongo_setup():
    print("=" * 60)
    print("MongoDB Atlas Vector Index Verification")
    print("=" * 60)
    
    try:
        # Load settings
        print("\n1. Loading configuration...")
        settings = get_settings()
        print(f"   [OK] Database: {settings.MONGODB_DB_NAME}")
        print(f"   [OK] Collection: {settings.MONGODB_COLLECTION}")
        
        # Connect to MongoDB
        print("\n2. Connecting to MongoDB Atlas...")
        client = MongoClient(settings.MONGODB_URI, serverSelectionTimeoutMS=5000)
        
        # Test connection
        client.admin.command('ping')
        print("   [OK] Connected successfully!")
        
        # Get database and collection
        db = client[settings.MONGODB_DB_NAME]
        collection = db[settings.MONGODB_COLLECTION]
        
        # Check collection exists and count documents
        print("\n3. Checking collection...")
        doc_count = collection.count_documents({})
        print(f"   [OK] Collection exists")
        print(f"   [INFO] Documents in collection: {doc_count}")
        
        if doc_count == 0:
            print("   [WARNING] No documents found. Upload PDFs to populate.")
        
        # List all indexes
        print("\n4. Checking indexes...")
        indexes = list(collection.list_indexes())
        
        print(f"   [INFO] Found {len(indexes)} index(es):")
        for idx in indexes:
            print(f"      - {idx['name']}")
        
        # Check for vector index (Atlas Search indexes are separate)
        print("\n5. Checking for vector search index...")
        print("   [INFO] Vector search indexes must be checked in Atlas UI")
        print("   [INFO] Go to: Atlas UI → Cluster → Search Indexes tab")
        print("   [INFO] Look for: 'vector_index' with status 'Active'")
        
        # Sample document check
        if doc_count > 0:
            print("\n6. Checking document structure...")
            sample_doc = collection.find_one()
            
            has_text = 'text' in sample_doc
            has_embedding = 'embedding' in sample_doc
            
            print(f"   [{'OK' if has_text else 'MISSING'}] 'text' field: {has_text}")
            print(f"   [{'OK' if has_embedding else 'MISSING'}] 'embedding' field: {has_embedding}")
            
            if has_embedding:
                embedding_len = len(sample_doc['embedding'])
                print(f"   [INFO] Embedding dimensions: {embedding_len}")
                if embedding_len != 384:
                    print(f"   [WARNING] Expected 384 dimensions, got {embedding_len}")
        
        print("\n" + "=" * 60)
        print("[SUCCESS] MongoDB connection verified!")
        print("=" * 60)
        
        if doc_count == 0:
            print("\nNext steps:")
            print("1. Create vector index in Atlas UI (see mongodb_vector_index_setup.md)")
            print("2. Upload and process PDF documents")
        else:
            print("\nNext steps:")
            print("1. Verify vector index exists in Atlas UI")
            print("2. Test vector search queries")
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {e}")
        print("\nPossible issues:")
        print("1. MongoDB URI incorrect")
        print("2. Network/firewall blocking connection")
        print("3. Database credentials invalid")
        return False

if __name__ == "__main__":
    success = verify_mongo_setup()
    sys.exit(0 if success else 1)
