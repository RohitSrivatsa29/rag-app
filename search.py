import json
from typing import List, Dict, Any
from database import Database
from embedding import EmbeddingManager
from thefuzz import process, fuzz

class RAGSearch:
    def __init__(self, db: Database, embedding_manager: EmbeddingManager):
        self.db = db
        self.embedding_manager = embedding_manager
        self.known_names = []
        self._load_known_names()
        self.last_entity = None  # {id, name}
        
    def _load_known_names(self):
        """Load all names from database for fuzzy matching"""
        records = self.db.get_all_records()
        self.known_names = []
        for record in records:
            try:
                metadata = json.loads(record['metadata'])
                # Personalities
                if 'name' in metadata:
                    self.known_names.append((metadata['name'], record['id']))
                # Concepts (Titles)
                if 'title' in metadata:
                     self.known_names.append((metadata['title'], record['id']))
            except:
                continue

    def expand_query(self, query: str) -> str:
        """Expand shortcuts to full words"""
        shortcuts = {
            "info": "information",
            "def": "definition",
            "desc": "description",
            "intro": "introduction"
        }
        words = query.split()
        expanded_words = [shortcuts.get(w.lower(), w) for w in words]
        return " ".join(expanded_words)
                
    def retrieve_relevant_documents(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Retrieve top-k relevant documents for a query with fuzzy matching and context"""
        
        # Expand shortcuts
        query = self.expand_query(query)
        
        query_lower = query.lower()
        pronouns = ["he", "she", "it", "they", "him", "her", "this"]
        has_pronoun = any(f" {p} " in f" {query_lower} " for p in pronouns) or \
                      any(query_lower.startswith(f"{p} ") for p in pronouns)
        
        forced_id = None
        
        # 1. Context Handling
        if has_pronoun and self.last_entity:
            print(f"DEBUG: Pronoun detected. Using context: {self.last_entity['name']}")
            forced_id = self.last_entity['id']
            
        # 2. Fuzzy Name Matching
        names_only = [n[0] for n in self.known_names]
        fuzzy_match_id = None
        
        if names_only:
            match_name, score = process.extractOne(query, names_only, scorer=fuzz.token_set_ratio)
            
            if score > 80:
                print(f"Fuzzy match found: {match_name} ({score}%)")
                for name, rid in self.known_names:
                    if name == match_name:
                        fuzzy_match_id = rid
                        break
        
        if fuzzy_match_id:
            forced_id = fuzzy_match_id
            
        # 3. Vector Search
        search_query = query
        if has_pronoun and self.last_entity and not fuzzy_match_id:
             search_query = f"{query} {self.last_entity['name']}"
             
        results = self.embedding_manager.search(search_query, k=top_k)
        
        # Combine results
        final_results = []
        seen_ids = set()
        
        if forced_id:
            final_results.append((forced_id, 2.0)) # Artificial high score
            seen_ids.add(forced_id)
            
        for rid, s in results:
            if rid not in seen_ids:
                final_results.append((rid, s))
                seen_ids.add(rid)
        
        final_results = final_results[:top_k]
        
        documents = []
        for record_id, score in final_results:
            record = self.db.get_record_by_id(record_id)
            if record:
                try:
                    original_data = json.loads(record['metadata'])
                except:
                    original_data = {}
                
                documents.append({
                    'id': record_id,
                    'content': record['content'],
                    'score': score,
                    'metadata': original_data
                })
                
        if documents:
            top_doc = documents[0]
            md = top_doc['metadata']
            files_name = md.get('name') or md.get('title')
            if files_name:
                self.last_entity = {
                    'id': top_doc['id'],
                    'name': files_name
                }
                print(f"DEBUG: Updated context to {files_name}")
        
        return documents
    
    def generate_answer(self, query: str, documents: List[Dict[str, Any]]) -> str:
        """Generate answer from retrieved documents with intent detection"""
        if not documents:
            return "I couldn't find any relevant information to answer your question. Please try rephrasing or ask something else."
        
        top_doc = documents[0]
        metadata = top_doc['metadata']
        query_lower = query.lower()

        # 1. Comprehensive Intent ("Everything", "Full Info")
        comprehensive_keywords = ["everything", "full info", "tell me about", "details", "all about", "who is"]
        # Basic check: if starts with "tell me about" or contains "everything"
        is_comprehensive = any(k in query_lower for k in comprehensive_keywords)
        
        # If specific questions like "who is X and what did he do", that implies comprehensive too.
        
        if is_comprehensive:
             # Gather available fields
             parts = []
             
             # Summary
             summary = metadata.get('summary') or metadata.get('explanation') or metadata.get('description')
             if summary: parts.append(summary)
             
             # Education
             if 'education' in metadata:
                 parts.append(f"Education: {metadata['education']}")
                 
             # Career
             if 'career' in metadata:
                 parts.append(f"Career: {metadata['career']}")
                 
             # Contribution
             if 'contribution' in metadata:
                 parts.append(f"Contribution: {metadata['contribution']}")
                 
             # Role
             if 'role' in metadata:
                 parts.append(f"Role: {metadata['role']} at {metadata.get('company', '')}")
                 
             return "\n\n".join(parts)

        # 2. Concept/Definition (Java/Python) -> Direct text, NO TITLE
        if 'explanation' in metadata:
             return metadata['explanation']
        if 'description' in metadata:
             return metadata['description']
             
        # 3. Specific Intent for Personalities
        name = metadata.get('name', 'This entity')
        
        # Education
        education_keywords = ["stud", "educat", "college", "university", "degree", "school", "graduat"]
        if any(k in query_lower for k in education_keywords):
            education = metadata.get('education')
            if education:
                return f"{name} studied at {education}."
                
        # Career
        career_keywords = ["work", "career", "join", "position", "compan", "history"]
        if any(k in query_lower for k in career_keywords):
            career = metadata.get('career')
            if career:
                return f"{career}"
                
        # Role
        role_keywords = ["role", "job", "title", "ceo", "founder", "position", "do"]
        if any(k in query_lower for k in role_keywords):
            role = metadata.get('role')
            company = metadata.get('company')
            if role:
                return f"{name} is the {role} of {company}."

        # Contribution
        contrib_keywords = ["known for", "did", "contribution", "invent", "create", "make", "built"]
        if any(k in query_lower for k in contrib_keywords):
            contribution = metadata.get('contribution')
            if contribution:
                 return f"{name} is known for: {contribution}."
        
        # Fallback to general summary fields
        fallback = metadata.get('summary') or metadata.get('explanation') or metadata.get('description') or metadata.get('content')
        if not fallback:
             return "I found some information but couldn't extract a clear summary."
             
        return fallback

    def answer_question(self, question: str) -> Dict[str, Any]:
        """Complete RAG pipeline: retrieve and generate answer"""
        # Retrieve relevant documents
        documents = self.retrieve_relevant_documents(question, top_k=5)
        
        # Generate answer
        answer = self.generate_answer(question, documents)
        
        return {
            'answer': answer,
            'sources': [
                {
                    'id': doc['id'],
                    'score': doc['score'],
                    'metadata': doc['metadata']
                }
                for doc in documents[:3]
            ]
        }
