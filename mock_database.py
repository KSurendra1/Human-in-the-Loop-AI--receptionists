import json
import os
import uuid
import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# File paths for mock database
HELP_REQUESTS_FILE = "help_requests.json"
KNOWLEDGE_BASE_FILE = "knowledge_base.json"

# Initialize empty database files if they don't exist
def init_database():
    if not os.path.exists(HELP_REQUESTS_FILE):
        with open(HELP_REQUESTS_FILE, 'w') as f:
            json.dump({}, f)
    
    if not os.path.exists(KNOWLEDGE_BASE_FILE):
        with open(KNOWLEDGE_BASE_FILE, 'w') as f:
            json.dump({}, f)

# Helper functions to read and write data
def _read_help_requests():
    with open(HELP_REQUESTS_FILE, 'r') as f:
        return json.load(f)

def _write_help_requests(data):
    with open(HELP_REQUESTS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def _read_knowledge_base():
    with open(KNOWLEDGE_BASE_FILE, 'r') as f:
        return json.load(f)

def _write_knowledge_base(data):
    with open(KNOWLEDGE_BASE_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Database operation functions
def create_help_request(query, status='pending'):
    """Create a new help request in the database"""
    request_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().isoformat()
    
    help_requests = _read_help_requests()
    help_requests[request_id] = {
        'id': request_id,
        'query': query,
        'status': status,
        'timestamp': timestamp,
        'customer_id': f"customer_{uuid.uuid4().hex[:8]}"
    }
    
    _write_help_requests(help_requests)
    return request_id

def get_all_help_requests():
    """Get all help requests from the database"""
    return _read_help_requests()

def get_help_request_by_id(request_id):
    """Get a specific help request by ID"""
    help_requests = _read_help_requests()
    return help_requests.get(request_id)

def update_help_request(request_id, data):
    """Update a help request with new data"""
    help_requests = _read_help_requests()
    if request_id in help_requests:
        help_requests[request_id].update(data)
        _write_help_requests(help_requests)
        return True
    return False

def resolve_help_request(request_id, answer):
    """Mark a help request as resolved with supervisor's answer"""
    timestamp = datetime.datetime.now().isoformat()
    
    help_requests = _read_help_requests()
    if request_id in help_requests:
        help_requests[request_id].update({
            'status': 'resolved',
            'supervisor_answer': answer,
            'resolved_at': timestamp
        })
        _write_help_requests(help_requests)
        
        # Update knowledge base with the new information
        request = help_requests[request_id]
        add_to_knowledge_base(request['query'], answer)
        return True
    return False

def mark_request_as_unresolved(request_id, reason='timeout'):
    """Mark a help request as unresolved"""
    timestamp = datetime.datetime.now().isoformat()
    
    help_requests = _read_help_requests()
    if request_id in help_requests:
        help_requests[request_id].update({
            'status': 'unresolved',
            'reason': reason,
            'updated_at': timestamp
        })
        _write_help_requests(help_requests)
        return True
    return False

def add_to_knowledge_base(query, answer):
    """Add a new entry to the knowledge base"""
    entry_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().isoformat()
    
    knowledge_base = _read_knowledge_base()
    knowledge_base[entry_id] = {
        'id': entry_id,
        'query': query,
        'answer': answer,
        'created_at': timestamp,
        'times_accessed': 0
    }
    
    _write_knowledge_base(knowledge_base)
    return entry_id

def get_knowledge_base():
    """Get the entire knowledge base"""
    return _read_knowledge_base()

def search_knowledge_base(query):
    """Search the knowledge base for matching entries"""
    knowledge = _read_knowledge_base()
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
        _write_knowledge_base(knowledge)
        
    return results

# Initialize database on import
init_database()
