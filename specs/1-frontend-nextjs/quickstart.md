# Quickstart: Next.js Frontend for Todo App

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Access to the existing backend API (from Phase 1 CLI)

## Setup Instructions

### 1. Clone and Navigate
```bash
# Navigate to your project directory
cd /path/to/your/project
```

### 2. Create Frontend Directory
```bash
mkdir frontend
cd frontend
```

### 3. Initialize Next.js Project
```bash
npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
```

### 4. Install Additional Dependencies
```bash
npm install axios date-fns
npm install -D @types/node
```

### 5. Configure Environment Variables
Create a `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
# Adjust the URL to match your backend API endpoint
```

### 6. Project Structure
After setup, your frontend directory should look like:
```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   │   ├── TaskItem.tsx
│   │   ├── TaskList.tsx
│   │   └── TaskForm.tsx
│   ├── lib/
│   │   └── api.ts
│   ├── types/
│   │   └── task.ts
│   └── styles/
│       └── globals.css
├── public/
├── package.json
├── next.config.js
├── tailwind.config.js
└── tsconfig.json
```

### 7. Start Development Server
```bash
npm run dev
```

The application will be available at http://localhost:3000

## API Integration

The frontend will connect to the existing backend API. You'll need to ensure the backend is running and accessible at the configured API URL.

## Key Components to Implement

1. **TaskItem Component**: Displays a single task with controls
2. **TaskList Component**: Manages the list of tasks with filtering/sorting
3. **TaskForm Component**: Handles creating and updating tasks
4. **FilterControls Component**: Provides UI for filtering and sorting options
5. **Layout Component**: Main application layout with navigation

## API Endpoints to Implement

Based on the existing CLI functionality, you'll need to implement or connect to:
- GET `/tasks` - Retrieve all tasks
- POST `/tasks` - Create a new task
- PUT `/tasks/:id` - Update a task
- DELETE `/tasks/:id` - Delete a task
- GET `/tasks?completed=true` - Filter tasks by completion status
- Additional query parameters for filtering by priority, tags, etc.