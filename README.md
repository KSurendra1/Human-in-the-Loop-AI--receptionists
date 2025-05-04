# Frontdesk Engineering Test: Human-in-the-Loop-AI-receptionists

This project implements a human-in-the-loop system for AI agents. If the AI doesn't know the answer to a question, it escalates to a human supervisor, follows up with the customer, and updates its knowledge base.

## Project Overview

The system consists of several key components:
- AI Agent (`agent.py`): Handles initial customer interactions and queries
- Database Management (`database.py`, `local_db.py`): Manages data storage and retrieval
- Knowledge Base (`knowledge_base.py`): Stores and updates AI knowledge
- Web Application (`app.py`): Provides the interface for human supervisors
- Mock Database (`mock_database.py`): For testing and development purposes

## Setup Instructions

### Prerequisites
- Python 3.9 or later
- Firebase account (for database)
- LiveKit account (for AI agent)

### Installation

1. Clone this repository:
```bash
git clone [https://github.com/KSurendra1/Human-in-the-Loop-AI--receptionists]
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
- Create a `.env` file with your Firebase and LiveKit credentials
- Configure database settings in `database.py`

### Project Structure
- `templates/`: HTML templates for the web interface
- `static/`: Static assets (CSS, JavaScript, images)
- `local_db/`: Local database files
- `app.py`: Main application entry point
- `agent.py`: AI agent implementation
- `database.py`: Database management
- `knowledge_base.py`: Knowledge base management

## Usage

1. Start the application:
```bash
python app.py
```

2. Access the web interface at `http://localhost:5000`

3. The AI agent will handle customer queries and escalate to human supervisors when needed.

## Features
- AI-powered customer support
- Human supervisor escalation
- Knowledge base updates
- Real-time communication
- Local and cloud database support

## Contributing
Please follow the standard git workflow for contributing to this project.

## License
[Specify License]
