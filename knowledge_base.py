from database import add_to_knowledge_base, get_knowledge_base, search_knowledge_base

class KnowledgeBaseManager:
    def __init__(self):
        pass
        
    def learn_answer(self, query, answer):
        """Add a new entry to the knowledge base"""
        return add_to_knowledge_base(query, answer)
    
    def get_all_entries(self):
        """Get all knowledge base entries"""
        return get_knowledge_base()
    
    def search(self, query):
        """Search the knowledge base for relevant entries"""
        return search_knowledge_base(query)
    
    def check_knowledge(self, query):
        """Check if the knowledge base has info about a query"""
        results = search_knowledge_base(query)
        if results:
            return True, results[0]['answer']
        return False, None
