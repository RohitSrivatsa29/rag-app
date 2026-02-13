from database import Database
from embedding import EmbeddingManager
from search import RAGSearch
import json

def debug_search():
    print("Initializing components...")
    db = Database("knowledge.db")
    db.connect()
    
    embedding_manager = EmbeddingManager()
    if not embedding_manager.load_index():
        print("ERROR: Could not load index!")
        return

    rag = RAGSearch(db, embedding_manager)
    
    # Test queries
    queries = [
        "Who created Python?",
        "What is a variable?",
        "Sundar Pichai"
    ]
    
    for query in queries:
        print(f"\n{'='*50}")
        print(f"Query: {query}")
        print(f"{'='*50}")
        
        # 1. Check retrieval directly
        print("1. Retrieving documents...")
        results = rag.retrieve_relevant_documents(query, top_k=3)
        
        for i, doc in enumerate(results):
            print(f"\nResult {i+1}:")
            print(f"  Score: {doc['score']:.4f}")
            print(f"  ID: {doc['id']}")
            
            # Print metadata snippet to verify content
            try:
                meta = doc['metadata']
                title = meta.get('title') or meta.get('name') or "No Title"
                print(f"  Title: {title}")
                print(f"  Content Preview: {doc['content'][:100]}...")
            except:
                print("  Metadata fetch failed")

        # 2. Check generated answer
        print("\n2. Generated Answer:")
        answer = rag.answer_question(query)
        print(answer['answer'])

if __name__ == "__main__":
    debug_search()
