import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
from dotenv import load_dotenv
import json
import uuid
import datetime

# Load environment variables
load_dotenv()

# Get Firebase credentials path with fallback
firebase_cred_path = os.getenv('FIREBASE_CREDENTIAL_PATH')
if not firebase_cred_path or not os.path.exists(firebase_cred_path):
    # Provide a default path or prompt user
    print("Firebase credentials file not found!")
    print("Please enter the path to your Firebase credentials JSON file:")
    firebase_cred_path = input("> ").strip()
    
    # Check if the provided path exists
    if not os.path.exists(firebase_cred_path):
        raise FileNotFoundError(f"Firebase credentials file not found at {firebase_cred_path}")

# Get Firebase database URL with fallback
firebase_db_url = os.getenv('FIREBASE_DATABASE_URL')
if not firebase_db_url:
    # Provide a default URL or prompt user
    print("Firebase database URL not found in environment variables!")
    print("Please enter your Firebase database URL:")
    firebase_db_url = input("> ").strip()

# Initialize Firebase
cred = credentials.Certificate(firebase_cred_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': firebase_db_url
})

# Rest of your database.py code...

def create_help_request(query, status='pending'):
    """Create a new help request in the database"""
    request_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().isoformat()
    
    ref = db.reference("/help_requests")
    ref.child(request_id).set({
        'id': request_id,
        'query': query,
        'status': status,
        'timestamp': timestamp,
        'customer_id': f"customer_{uuid.uuid4().hex[:8]}"  # Simulated customer ID
    })
    
    return request_id

def get_all_help_requests():
    """Get all help requests from the database"""
    ref = db.reference("/help_requests")
    return ref.get() or {}

def get_help_request_by_id(request_id):
    """Get a specific help request by ID"""
    ref = db.reference(f"/help_requests/{request_id}")
    return ref.get()

def update_help_request(request_id, data):
    """Update a help request with new data"""
    ref = db.reference(f"/help_requests/{request_id}")
    ref.update(data)
    return True

def resolve_help_request(request_id, answer):
    """Mark a help request as resolved with supervisor's answer"""
    timestamp = datetime.datetime.now().isoformat()
    
    ref = db.reference(f"/help_requests/{request_id}")
    ref.update({
        'status': 'resolved',
        'supervisor_answer': answer,
        'resolved_at': timestamp
    })
    
    # Update knowledge base with the new information
    request = get_help_request_by_id(request_id)
    if request:
        add_to_knowledge_base(request['query'], answer)
    
    return True

def mark_request_as_unresolved(request_id, reason='timeout'):
    """Mark a help request as unresolved"""
    timestamp = datetime.datetime.now().isoformat()
    
    ref = db.reference(f"/help_requests/{request_id}")
    ref.update({
        'status': 'unresolved',
        'reason': reason,
        'updated_at': timestamp
    })
    
    return True

def add_to_knowledge_base(query, answer):
    """Add a new entry to the knowledge base"""
    entry_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().isoformat()
    
    ref = db.reference("/knowledge_base")
    ref.child(entry_id).set({
        'id': entry_id,
        'query': query,
        'answer': answer,
        'created_at': timestamp,
        'times_accessed': 0
    })
    
    return entry_id

def get_knowledge_base():
    """Get the entire knowledge base"""
    ref = db.reference("/knowledge_base")
    return ref.get() or {}

def search_knowledge_base(query):
    """Search the knowledge base for matching entries"""
    # Simple search implementation - in real world, use more sophisticated search methods
    knowledge = get_knowledge_base()
    results = []
    
    query_terms = query.lower().split()
    for entry_id, entry in knowledge.items():
        entry_text = (entry['query'] + ' ' + entry['answer']).lower()
        
        # Check if any term in the query appears in the entry
        if any(term in entry_text for term in query_terms):
            results.append(entry)
            
            # Update access count
            ref = db.reference(f"/knowledge_base/{entry_id}")
            ref.update({
                'times_accessed': entry.get('times_accessed', 0) + 1
            })
    
    return results

# Initialize empty database if it doesn't exist
def init_database():
    ref = db.reference("/")
    data = ref.get()
    if not data:
        ref.set({
            'help_requests': {},
            'knowledge_base': {}
        })

# Call init_database on import
init_database()
