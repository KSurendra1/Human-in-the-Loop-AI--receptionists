# app.py
from flask import Flask, render_template, request, jsonify, redirect, url_for
import asyncio
from local_db import (
    get_all_help_requests, get_help_request_by_id, resolve_help_request, 
    mark_request_as_unresolved, get_knowledge_base
)
from agent import SalonAgent
import datetime
import json

app = Flask(__name__)
agent = SalonAgent()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/requests')
def requests():
    """View all help requests"""
    help_requests = get_all_help_requests()
    # Convert to list and sort by timestamp
    help_requests_list = sorted(
        [req for req_id, req in help_requests.items()],
        key=lambda x: x.get('timestamp', ''),
        reverse=True
    )
    
    # Separate into pending and resolved/unresolved
    pending_requests = []
    resolved_requests = []
    
    for req in help_requests_list:
        if req['status'] == 'pending':
            pending_requests.append(req)
        else:
            resolved_requests.append(req)
    
    return render_template(
        'requests.html',
        pending_requests=pending_requests,
        resolved_requests=resolved_requests
    )

@app.route('/knowledge')
def knowledge():
    """View the knowledge base"""
    kb = get_knowledge_base()
    # Convert to list and sort by creation time
    kb_list = sorted(
        [entry for entry_id, entry in kb.items()],
        key=lambda x: x.get('created_at', ''),
        reverse=True
    )
    
    return render_template('knowledge.html', entries=kb_list)

@app.route('/api/resolve-request', methods=['POST'])
def api_resolve_request():
    """API endpoint to resolve a help request"""
    data = request.json
    request_id = data.get('request_id')
    answer = data.get('answer')
    
    if not request_id or not answer:
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
    
    # Resolve the request in the database
    resolve_help_request(request_id, answer)
    
    # Follow up with the customer
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(agent.follow_up_with_customer(request_id))
    
    return jsonify({'success': True})

@app.route('/api/mark-unresolved', methods=['POST'])
def api_mark_unresolved():
    """API endpoint to mark a request as unresolved"""
    data = request.json
    request_id = data.get('request_id')
    reason = data.get('reason', 'timeout')
    
    if not request_id:
        return jsonify({'success': False, 'error': 'Missing request ID'}), 400
    
    mark_request_as_unresolved(request_id, reason)
    return jsonify({'success': True})

@app.route('/api/simulate-call', methods=['POST'])
def api_simulate_call():
    """API endpoint to simulate a customer call"""
    data = request.json
    query = data.get('query')
    
    if not query:
        return jsonify({'success': False, 'error': 'Missing query'}), 400
    
    # Process the query
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(agent.process_query(query))
    
    return jsonify({'success': True, 'result': result})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
