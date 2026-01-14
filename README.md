# Todo AI Chatbot

An AI-powered task management application that allows users to manage their tasks through natural language conversations with an AI assistant.

## Features

- **Natural Language Processing**: Interact with your task list using everyday language
- **AI-Powered**: Powered by OpenAI's GPT models for understanding user requests
- **Full Task Management**: Create, read, update, delete, and complete tasks
- **Multi-User Support**: Secure authentication and user isolation
- **Conversation History**: Persistent chat sessions with context awareness
- **Real-Time Interaction**: Instant responses from the AI assistant

## Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: SQLModel with PostgreSQL (Neon) or SQLite
- **AI Service**: OpenAI API
- **Authentication**: JWT-based authentication

### Frontend
- **Framework**: Next.js with React
- **Styling**: Tailwind CSS
- **API Client**: Axios
- **State Management**: React Context API

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- Access to OpenAI API (for AI features)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy the environment file and configure your settings:
```bash
cp .env.example .env
```
Edit the `.env` file to add your OpenAI API key and database configuration.

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Copy the environment file:
```bash
cp .env.example .env.local
```

## Usage

### Running the Backend

1. Make sure you're in the `backend` directory
2. Run the server:
```bash
python app.py
```
The backend will start on `http://localhost:8000`

### Running the Frontend

1. Make sure you're in the `frontend` directory
2. Run the development server:
```bash
npm run dev
```
The frontend will start on `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create a new user account
- `POST /api/auth/login` - Authenticate user

### Task Management
- `GET /api/tasks` - Get all user tasks
- `POST /api/tasks` - Create a new task
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion

### Chat Interface
- `POST /api/chat` - Send a message to the AI assistant
- `GET /api/chat/conversations` - Get user's conversations
- `GET /api/chat/conversations/{id}/messages` - Get messages for a conversation

## Natural Language Commands

The AI chatbot understands various ways to interact with your tasks:

- **Creating tasks**: "Add a task to buy groceries", "Create a task to call mom tomorrow"
- **Listing tasks**: "Show me my tasks", "What do I need to do today?"
- **Completing tasks**: "Mark task 1 as complete", "I finished the report"
- **Deleting tasks**: "Delete the meeting task", "Remove the grocery task"
- **Updating tasks**: "Change the deadline of the project to Friday"

## Environment Variables

### Backend (.env)
- `OPENAI_API_KEY`: Your OpenAI API key
- `DATABASE_URL`: Database connection string (SQLite or PostgreSQL)
- `NEON_DATABASE_URL`: Neon PostgreSQL database URL (optional, overrides DATABASE_URL)
- `JWT_SECRET_KEY`: Secret key for JWT token generation
- `FRONTEND_ORIGIN`: Frontend URL for CORS configuration

### Frontend (.env.local)
- `NEXT_PUBLIC_API_BASE_URL`: Backend API URL (defaults to http://localhost:8000)

## Deployment

### Backend Deployment
The backend can be deployed to any platform that supports Python applications (Heroku, AWS, Google Cloud, etc.).

### Frontend Deployment
The frontend can be deployed to Vercel, Netlify, or any platform that supports Next.js applications.

## Development

### Running Tests
Backend tests can be run using pytest:
```bash
pytest
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.