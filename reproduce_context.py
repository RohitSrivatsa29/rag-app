from database import Database
from embedding import EmbeddingManager
from search import RAGSearch

def reproduce_context():
    print("Initializing Search Engine...")
    db = Database("knowledge_v2.db")
    db.connect()
    
    embedding_manager = EmbeddingManager()
    embedding_manager.load_index()
    
    rag = RAGSearch(db, embedding_manager)
    
    # 1. Establish Context
    print("\n1. Asking: 'Who is Sundar Pichai?'")
    res1 = rag.answer_question("Who is Sundar Pichai")
    print(f"Context should now be set to Sundar Pichai.")
    
    with open("debug_l3_clean.txt", "w", encoding="utf-8") as f:
        f.write("=== QUERY 1 ===\n")
        f.write(f"Answer: {res1['answer']}\n")
        if res1.get('sources'):
             f.write(f"Source: {res1['sources'][0]['metadata']}\n")
        f.write(f"Last Entity: {rag.last_entity}\n")
        f.write("===============\n")

    if not rag.last_entity:
        with open("debug_l3_clean.txt", "a", encoding="utf-8") as f:
             f.write("❌ DEBUG FAILURE: Context was NOT set after first question.\n")
        import sys; sys.exit(1)
    
    if not rag.last_entity:
        print("❌ DEBUG FAILURE: Context was NOT set after first question.")
        import sys; sys.exit(1)
    
    # 2. Test Context
    
    # 2. Test Context
    print("\n2. Asking: 'his education'")
    res2 = rag.answer_question("his education")
    ans2 = res2['answer']
    
    with open("debug_l3_clean.txt", "a", encoding="utf-8") as f:
        f.write("\n=== QUERY 2 ===\n")
        f.write(f"Answer: {ans2}\n")
        if res2.get('sources'):
            f.write(f"Top Source: {res2['sources'][0]['metadata'].get('name')}\n")
            for i, src in enumerate(res2['sources']):
                f.write(f"   Src {i}: {src['metadata']}\n")
        f.write("-" * 20 + "\n")
    
    print("Debug info written to debug_l3_clean.txt")

    # Sundar Pichai studied at IIT Kharagpur, Stanford, Wharton.
    # Andrew Ng studied at CMU, MIT, Berkeley.
    
    if "Stanford" in ans2 or "Wharton" in ans2 or "Kharagpur" in ans2:
        print("✅ SUCCESS: Context was used (Found Sundar's education).")
    elif "Andrew Ng" in ans2 or "Berkeley" in ans2:
        print("❌ FAILURE: Context ignored (Found Andrew Ng).")
    else:
        print("❓ UNKNOWN: Could not determine entity from answer.")

if __name__ == "__main__":
    reproduce_context()
