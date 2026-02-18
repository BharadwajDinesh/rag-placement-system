# Creating MongoDB Atlas Vector Search Index

## ✅ Prerequisites Complete
- MongoDB connection: **Working**
- Documents in collection: **44**
- Embedding dimensions: **384**

## 🎯 Next Step: Create Vector Search Index

### Step-by-Step Instructions

#### 1. Go to MongoDB Atlas
Open: **https://cloud.mongodb.com/**

#### 2. Navigate to Your Cluster
- Select your project
- Click on your cluster: **RAGcluster**

#### 3. Go to Search Indexes
- Click on the **"Atlas Search"** tab (or "Search" in the top menu)
- Click **"Create Search Index"**

#### 4. Choose Index Type
- Select **"Atlas Vector Search"** (JSON Editor)
- Click **"Next"**

#### 5. Configure the Index

**Database and Collection:**
- Database: `placement_rag`
- Collection: `documents`

**Index Name:**
```
vector_index
```

**Index Definition (JSON):**
```json
{
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 384,
      "similarity": "cosine"
    }
  ]
}
```

#### 6. Create the Index
- Click **"Next"**
- Review the configuration
- Click **"Create Search Index"**

#### 7. Wait for Index to Build
- Status will show as "Building" initially
- Wait 1-2 minutes for it to become **"Active"**
- Refresh the page to check status

---

## 🧪 Test After Index Creation

Once the index status is "Active", run:

```powershell
cd "d:\M.Tech\My Projects\Agentic RAG\rag-placement-system\backend"
python test_retrieval.py
```

This will test semantic search with sample queries!

---

## 📸 Visual Guide

**What you're looking for:**

1. **Atlas Search Tab** → Create Search Index
2. **Index Type** → Atlas Vector Search (JSON Editor)
3. **Index Configuration:**
   - Name: `vector_index`
   - Database: `placement_rag`
   - Collection: `documents`
   - Field: `embedding`
   - Dimensions: `384`
   - Similarity: `cosine`

---

## ⚠️ Common Issues

**Issue: Can't find "Atlas Search" tab**
- Look for "Search" in the top navigation menu
- Or click on your cluster name → "Search Indexes" tab

**Issue: Index creation fails**
- Verify you have documents with `embedding` field (you do! ✅)
- Check that embedding dimensions are 384 (verified! ✅)

**Issue: Index stuck on "Building"**
- Wait 2-3 minutes
- Refresh the page
- For 44 documents, it should be quick

---

## 🎯 After Index is Active

Run these commands to test everything:

```powershell
# Test retrieval service
python test_retrieval.py

# Start the API server
uvicorn app.main:app --reload

# Test via browser
# Open: http://localhost:8000/docs
# Try the /api/query endpoint
```

Let me know once you've created the index and I'll help you test the retrieval system!
