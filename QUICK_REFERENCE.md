# Quick Reference Guide

## 🚀 Quick Commands

### Local Development
```bash
# Setup (first time only)
pip install -r requirements.txt
cd frontend && npm install && npm run build && cd ..

# Run application
python app.py

# Visit
http://localhost:8000
```

### Testing
```bash
# Run tests
python test_app.py

# Check health
curl http://localhost:8000/health

# Test API
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Python?"}'
```

### Data Management
```bash
# Add new data
cp your-data.json data/

# Clear database and rebuild
rm knowledge.db faiss_index.bin id_mapping.pkl
python app.py  # Will rebuild on startup
```

### Frontend Development
```bash
cd frontend

# Dev mode (hot reload)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 📁 Key Files

| File | Purpose |
|------|---------|
| `app.py` | Main FastAPI application |
| `database.py` | SQLite operations |
| `embedding.py` | FAISS index and embeddings |
| `search.py` | RAG search logic |
| `data_loader.py` | Load JSON into database |
| `requirements.txt` | Python dependencies |
| `Procfile` | Render deployment config |
| `frontend/src/App.jsx` | React UI |

## 🔧 Configuration

### Change Embedding Model
Edit `embedding.py` line 9:
```python
def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
```

**Options:**
- `all-MiniLM-L6-v2` - Fast, 384 dim (default)
- `all-mpnet-base-v2` - Better quality, 768 dim
- `paraphrase-MiniLM-L3-v2` - Smaller, faster

### Adjust Retrieved Documents
Edit `search.py` line 17:
```python
def retrieve_relevant_documents(self, query: str, top_k: int = 3):
```

### Change UI Colors
Edit `frontend/src/App.jsx`:
- Background: `bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900`
- User message: `bg-blue-600`
- Assistant message: `bg-gray-800 border-gray-700`

## 📊 Data Format

### Supported JSON Structure
```json
[
  {
    "id": "unique_id",           // Required (or auto-generated)
    "title": "Title",            // Searchable
    "description": "Content",    // Searchable
    "category": "Category",      // Searchable
    "tags": ["tag1", "tag2"]     // Searchable
  }
]
```

### Searchable Fields (Auto-detected)
- title, name, question, query
- description, content, text, body, answer
- category, tags, keywords

Any field not listed is stored but not searched.

## 🌐 API Reference

### POST /ask
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Your question here"}'
```

**Response:**
```json
{
  "answer": "Based on the available information:\n\n1. **Title**\n   Description..."
}
```

### GET /health
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "records": 150,
  "index_ready": true
}
```

## 🐛 Common Issues

### Port 8000 already in use
```bash
# Find process
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
python app.py --port 8080
```

### Frontend not showing
```bash
# Rebuild frontend
cd frontend
npm run build
cd ..
python app.py
```

### No data loaded
```bash
# Check data files
ls -la data/

# Verify JSON syntax
python -m json.tool data/your-file.json

# Rebuild database
rm knowledge.db faiss_index.bin id_mapping.pkl
python app.py
```

## 📈 Performance Tips

### Faster Startup
- Use smaller embedding model
- Reduce dataset size
- Pre-build FAISS index (it's cached after first build)

### Better Results
- Use larger embedding model
- Increase `top_k` in search
- Add more contextual information to JSON

### Lower Memory
- Use `paraphrase-MiniLM-L3-v2` model
- Reduce dataset size
- Limit number of retrieved documents

## 🔒 Security Checklist

Before deploying to production:

- [ ] Add API authentication
- [ ] Implement rate limiting
- [ ] Restrict CORS origins
- [ ] Add input validation
- [ ] Set up logging
- [ ] Add error monitoring
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS (Render does this automatically)

## 📦 Deployment Checklist

Before deploying:

- [ ] JSON data files in `data/` folder
- [ ] Frontend built (`frontend/dist/` exists)
- [ ] All files committed to Git
- [ ] Tested locally (`python test_app.py`)
- [ ] `requirements.txt` up to date
- [ ] Procfile configured correctly

## 🔄 Update Workflow

### Update Data Only
```bash
# Modify data/*.json
rm knowledge.db faiss_index.bin id_mapping.pkl
git add data/
git commit -m "Update data"
git push
```

### Update Frontend Only
```bash
# Modify frontend/src/App.jsx
cd frontend && npm run build && cd ..
git add frontend/dist
git commit -m "Update UI"
git push
```

### Update Backend Only
```bash
# Modify Python files
git add *.py
git commit -m "Update backend"
git push
```

## 📞 Support

### Render Issues
- Logs: Render Dashboard → Your Service → Logs
- Docs: https://render.com/docs
- Community: https://community.render.com

### Application Issues
- Check `python test_app.py` output
- Review server logs for errors
- Verify data format is correct

### Performance Issues
- Check Render metrics in dashboard
- Consider upgrading to paid tier
- Optimize dataset size

## 🎯 Best Practices

1. **Data Quality**: Clean, well-structured JSON
2. **Testing**: Always test locally first
3. **Version Control**: Commit often, meaningful messages
4. **Documentation**: Update README for your use case
5. **Monitoring**: Check Render logs regularly
6. **Backups**: Keep local copy of data files
7. **Updates**: Pull latest changes before modifying

---

**Need more help?** See README.md or DEPLOYMENT.md for detailed guides.
