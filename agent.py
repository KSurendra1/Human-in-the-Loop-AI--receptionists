# agent.py
import os
import json
import asyncio
import uuid
from local_db import create_help_request, get_help_request_by_id

# Sample salon information to provide to the AI
SALON_INFO = {
    "name": "Elegant Style Salon",
    "business_hours": "Monday to Saturday, 9:00 AM to 7:00 PM",
    "services": {
        "haircut": {"men": "$25", "women": "$35", "children": "$20"},
        "coloring": {"basic": "$60", "highlights": "$100", "balayage": "$150"},
        "styling": {"blowout": "$30", "updo": "$45", "special event": "$75"},
        "treatments": {"deep conditioning": "$20", "keratin": "$150"}
    },
    "location": "123 Beauty Lane, Fashion City",
    "phone": "(555) 123-4567",
    "website": "www.elegantstylesalon.com",
    "booking_policy": "Appointments recommended, walk-ins welcome based on availability"
}

class SalonAgent:
    def __init__(self):
        self.salon_info = SALON_INFO
        
    async def handle_call(self):
        """Simulate handling a call from a customer"""
        print("Call received from customer")
        return "Call connected"
        
    async def process_query(self, query):
        """Process a query from the customer"""
        # Check if we have the answer in our knowledge
        if self._can_answer(query):
            return self._get_answer(query)
        else:
            # Create a help request for the supervisor
            request_id = create_help_request(query, "pending")
            print(f"Creating help request: {request_id} for query: {query}")
            
            # Simulate texting the supervisor
            self._notify_supervisor(query, request_id)
            
            return {
                "response": "Let me check with my supervisor and get back to you.",
                "request_id": request_id,
                "knows_answer": False
            }
    
    def _notify_supervisor(self, query, request_id):
        """Simulate texting the supervisor"""
        print(f"\n[SUPERVISOR NOTIFICATION] New help request {request_id}")
        print(f"Question: {query}")
        print(f"Please respond at: http://localhost:5000/requests\n")
    
    def _can_answer(self, query):
        """Determine if the agent can answer the query based on salon information"""
        # Simple keyword matching for demonstration
        query = query.lower()
        if "hour" in query or "open" in query:
            return True
        elif "service" in query or "price" in query or "cost" in query:
            return True
        elif "location" in query or "address" in query:
            return True
        elif "phone" in query or "number" in query or "contact" in query:
            return True
        elif "book" in query or "appointment" in query or "schedule" in query:
            return True
        return False
    
    def _get_answer(self, query):
        """Get the answer for a query we can handle"""
        query = query.lower()
        if "hour" in query or "open" in query:
            answer = f"Our salon is open {self.salon_info['business_hours']}"
        elif "service" in query or "price" in query or "cost" in query:
            answer = f"Here are our services and prices: {json.dumps(self.salon_info['services'], indent=2)}"
        elif "location" in query or "address" in query:
            answer = f"We are located at {self.salon_info['location']}"
        elif "phone" in query or "number" in query or "contact" in query:
            answer = f"You can reach us at {self.salon_info['phone']}"
        elif "book" in query or "appointment" in query or "schedule" in query:
            answer = f"Our booking policy: {self.salon_info['booking_policy']}"
        else:
            answer = "I don't have that information available right now."
        
        return {
            "response": answer,
            "knows_answer": True
        }
        
    async def follow_up_with_customer(self, request_id):
        """Follow up with customer after supervisor provides answer"""
        request = get_help_request_by_id(request_id)
        if request and request.get('status') == 'resolved':
            answer = request.get('supervisor_answer', 'No answer provided')
            # Simulate texting the customer
            print(f"\n[CUSTOMER NOTIFICATION] Follow-up for request {request_id}")
            print(f"Answer: {answer}\n")
            return True
        return False
