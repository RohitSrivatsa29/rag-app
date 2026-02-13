from database import Database
from embedding import EmbeddingManager
from search import RAGSearch

def simple_debug():
    db = Database("knowledge.db")
    db.connect()
    embedding_manager = EmbeddingManager()
    embedding_manager.load_index()
    rag = RAGSearch(db, embedding_manager) 
    
    query = "Who created Python?"
    print(f"Query: {query}")
    
    print(f"Query: {query}")
    
    # Check answer generation directly
    answer = rag.answer_question(query)
    print("\nGenerated Answer:")
    print(answer['answer'])

if __name__ == "__main__":
    simple_debug()
