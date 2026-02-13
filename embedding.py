import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Tuple
import pickle
import os

class EmbeddingManager:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize embedding model"""
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        self.index = None
        self.id_mapping = []  # Maps index position to record id
        
    def create_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for texts"""
        print(f"Generating embeddings for {len(texts)} texts...")
        embeddings = self.model.encode(texts, show_progress_bar=True)
        return embeddings
    
    def build_index(self, embeddings: np.ndarray, record_ids: List[str]):
        """Build FAISS index from embeddings"""
        print(f"Building FAISS index with {len(embeddings)} vectors...")
        
        # Normalize embeddings for cosine similarity
        embeddings = embeddings.astype('float32')
        faiss.normalize_L2(embeddings)
        
        # Create FAISS index
        self.index = faiss.IndexFlatIP(self.dimension)  # Inner Product for cosine similarity
        self.index.add(embeddings)
        
        # Store id mapping
        self.id_mapping = record_ids
        
        print(f"FAISS index built successfully with {self.index.ntotal} vectors")
    
    def search(self, query: str, k: int = 5) -> List[Tuple[str, float]]:
        """Search for similar documents"""
        if self.index is None:
            raise ValueError("Index not built yet")
        
        # Generate query embedding
        query_embedding = self.model.encode([query]).astype('float32')
        faiss.normalize_L2(query_embedding)
        
        # Search in index
        distances, indices = self.index.search(query_embedding, k)
        
        # Return results with record ids and similarity scores
        results = []
        for idx, score in zip(indices[0], distances[0]):
            if idx < len(self.id_mapping):
                results.append((self.id_mapping[idx], float(score)))
        
        return results
    
    def save_index(self, index_path: str = "faiss_index.bin", mapping_path: str = "id_mapping.pkl"):
        """Save FAISS index and id mapping to disk"""
        if self.index is None:
            raise ValueError("No index to save")
        
        faiss.write_index(self.index, index_path)
        with open(mapping_path, 'wb') as f:
            pickle.dump(self.id_mapping, f)
        
        print(f"Index saved to {index_path}")
    
    def load_index(self, index_path: str = "faiss_index.bin", mapping_path: str = "id_mapping.pkl"):
        """Load FAISS index and id mapping from disk"""
        if os.path.exists(index_path) and os.path.exists(mapping_path):
            self.index = faiss.read_index(index_path)
            with open(mapping_path, 'rb') as f:
                self.id_mapping = pickle.load(f)
            print(f"Index loaded from {index_path} with {self.index.ntotal} vectors")
            return True
        return False
