from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager
import os
import uvicorn

from database import Database
from data_loader import DataLoader
from embedding import EmbeddingManager
from search import RAGSearch

# Global variables for application state
db = None
embedding_manager = None
rag_search = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize application on startup"""
    global db, embedding_manager, rag_search
    
    print("="*50)
    print("Starting RAG Application")
    print("="*50)
    
    # Initialize database
    print("\n1. Initializing database...")
    db = Database("knowledge_v2.db")
    db.connect()
    db.create_table()
    
    # Check if database is empty
    record_count = db.count_records()
    print(f"   Database has {record_count} records")
    
    # Load data if database is empty
    if record_count == 0:
        print("\n2. Loading data from JSON files...")
        loader = DataLoader("data")
        loaded = loader.load_into_database(db)
        
        if loaded == 0:
            print("\n   WARNING: No data loaded!")
            print("   Place JSON files in the 'data' folder to enable search.")
            print("   Application will start but searches will return no results.")
    else:
        print("\n2. Using existing database")
    
    # Initialize embedding manager
    print("\n3. Initializing embedding model...")
    embedding_manager = EmbeddingManager()
    
    # Try to load existing index
    index_exists = embedding_manager.load_index("faiss_index_v2.bin", "id_mapping_v2.pkl")
    
    # Build index if doesn't exist or if new data was loaded
    if not index_exists or (record_count == 0 and db.count_records() > 0):
        print("\n4. Building FAISS index...")
        records = db.get_all_records()
        
        if records:
            texts = [r['content'] for r in records]
            ids = [r['id'] for r in records]
            
            embeddings = embedding_manager.create_embeddings(texts)
            embedding_manager.build_index(embeddings, ids)
            
            # Save index for future use
            embedding_manager.save_index("faiss_index_v2.bin", "id_mapping_v2.pkl")
        else:
            print("   No records to index")
    else:
        print("\n4. Using existing FAISS index")
    
    # Initialize RAG search
    print("\n5. Initializing RAG search...")
    rag_search = RAGSearch(db, embedding_manager)
    
    print("\n" + "="*50)
    print("RAG Application Ready!")
    print(f"Total records: {db.count_records()}")
    print("="*50 + "\n")
    
    yield
    
    # Cleanup on shutdown
    if db:
        db.close()

# Create FastAPI app
app = FastAPI(
    title="RAG Application",
    description="Retrieval-Augmented Generation Web Application",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str

# API Endpoints
@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """Answer a question using RAG"""
    if not rag_search:
        raise HTTPException(status_code=503, detail="Service not ready")
    
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    try:
        result = rag_search.answer_question(request.question.strip())
        return AnswerResponse(answer=result['answer'])
    except Exception as e:
        print(f"Error processing question: {e}")
        raise HTTPException(status_code=500, detail="Error processing question")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    record_count = db.count_records() if db else 0
    return {
        "status": "healthy",
        "records": record_count,
        "index_ready": embedding_manager.index is not None if embedding_manager else False
    }

# Serve frontend static files
frontend_path = "frontend/dist"
if os.path.exists(frontend_path):
    # Mount static files
    app.mount("/assets", StaticFiles(directory=f"{frontend_path}/assets"), name="assets")
    
    @app.get("/")
    async def serve_frontend():
        """Serve the React frontend"""
        return FileResponse(f"{frontend_path}/index.html")
    
    @app.get("/{full_path:path}")
    async def serve_frontend_routes(full_path: str):
        """Serve React app for all other routes"""
        file_path = f"{frontend_path}/{full_path}"
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(f"{frontend_path}/index.html")
else:
    @app.get("/")
    async def root():
        return {
            "message": "RAG API is running",
            "frontend": "not built - run: cd frontend && npm install && npm run build"
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
