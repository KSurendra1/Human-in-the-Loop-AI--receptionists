import json
import os
import uuid
import datetime
import time

class LocalDatabase:
    def __init__(self):
        self.db_dir = "local_db"
        self.help_requests_file = os.path.join(self.db_dir, "help_requests.json")
        self.knowledge_base_file = os.path.join(self.db_dir, "knowledge_base.json")
        self._init_db()
    
    def _init_db(self):
        # Create directory if it doesn't exist
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)
        
        # Initialize help requests file
        if not os.path.exists(self.help_requests_file):
            with open(self.help_requests_file, 'w') as f:
                json.dump({}, f)
        
        # Initialize knowledge base file
        if not os.path.exists(self.knowledge_base_file):
            with open(self.knowledge_base_file, 'w') as f:
                json.dump({}, f)
    
    def _read_help_requests(self):
        with open(self.help_requests_file, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    
    def _write_help_requests(self, data):
        with open(self.help_requests_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _read_knowledge_base(self):
        with open(self.knowledge_base_file, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    
    def _write_knowledge_base(self, data):
        with open(self.knowledge_base_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def create_help_request(self, query, status='pending'):
        """Create a new help request"""
        request_id = str(uuid.uuid4())
        timestamp = datetime.datetime.now().isoformat()
        
        help_requests = self._read_help_requests()
        help_requests[request_id] = {
            'id': request_id,
            'query': query,
            'status': status,
            'timestamp': timestamp,
            'customer_id': f"customer_{uuid.uuid4().hex[:8]}"
        }
        
        self._write_help_requests(help_requests)
        print(f"Created help request {request_id} for query: {query}")
        return request_id
    
    def get_all_help_requests(self):
        """Get all help requests"""
        return self._read_help_requests()
    
    def get_help_request_by_id(self, request_id):
        """Get a specific help request by ID"""
        help_requests = self._read_help_requests()
        return help_requests.get(request_id)
    
    def resolve_help_request(self, request_id, answer):
        """Mark a help request as resolved with supervisor's answer"""
        timestamp = datetime.datetime.now().isoformat()
        
        help_requests = self._read_help_requests()
        if request_id in help_requests:
            help_requests[request_id].update({
                'status': 'resolved',
                'supervisor_answer': answer,
                'resolved_at': timestamp
            })
            self._write_help_requests(help_requests)
            
            # Update knowledge base
            request = help_requests[request_id]
            self.add_to_knowledge_base(request['query'], answer)
            return True
        return False
    
    def mark_request_as_unresolved(self, request_id, reason='timeout'):
        """Mark a help request as unresolved"""
        timestamp = datetime.datetime.now().isoformat()
        
        help_requests = self._read_help_requests()
        if request_id in help_requests:
            help_requests[request_id].update({
                'status': 'unresolved',
                'reason': reason,
                'updated_at': timestamp
            })
            self._write_help_requests(help_requests)
            return True
        return False
    
    def add_to_knowledge_base(self, query, answer):
        """Add a new entry to the knowledge base"""
        entry_id = str(uuid.uuid4())
        timestamp = datetime.datetime.now().isoformat()
        
        knowledge_base = self._read_knowledge_base()
        knowledge_base[entry_id] = {
            'id': entry_id,
            'query': query,
            'answer': answer,
            'created_at': timestamp,
            'times_accessed': 0
        }
        
        self._write_knowledge_base(knowledge_base)
        return entry_id
    
    def get_knowledge_base(self):
        """Get the entire knowledge base"""
        return self._read_knowledge_base()
    
    def search_knowledge_base(self, query):
        """Search the knowledge base for matching entries"""
        knowledge = self._read_knowledge_base()
        results = []
        
        query_terms = query.lower().split()
        for entry_id, entry in knowledge.items():
            entry_text = (entry['query'] + ' ' + entry['answer']).lower()
            
            # Check if any term in the query appears in the entry
            if any(term in entry_text for term in query_terms):
                results.append(entry)
                
                # Update access count
                entry['times_accessed'] = entry.get('times_accessed', 0) + 1
                
        # Save the updated access counts
        if results:
            self._write_knowledge_base(knowledge)
            
        return results

# Create global instance
db = LocalDatabase()

# Export functions that match the Firebase API interface
create_help_request = db.create_help_request
get_all_help_requests = db.get_all_help_requests
get_help_request_by_id = db.get_help_request_by_id
resolve_help_request = db.resolve_help_request
mark_request_as_unresolved = db.mark_request_as_unresolved
add_to_knowledge_base = db.add_to_knowledge_base
get_knowledge_base = db.get_knowledge_base
search_knowledge_base = db.search_knowledge_base
