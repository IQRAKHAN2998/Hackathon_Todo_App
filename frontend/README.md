# Todo App Frontend

This is the frontend for the Todo application built with Next.js and Tailwind CSS.

## Features

- Task management (create, read, update, delete)
- Filter and sort tasks by various criteria
- Visual indicators for task priority levels
- Responsive design for all device sizes
- Clean and intuitive user interface

## Tech Stack

- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Axios for API requests

## Getting Started

First, install the dependencies:

```bash
npm install
```

Then, run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Environment Variables

Create a `.env.local` file in the root directory with the following content:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Build for Production

To build the application for production:

```bash
npm run build
```

Then, run the production server:

```bash
npm start
```

## API Integration

This frontend connects to the existing backend API. Make sure the backend is running at the configured API URL.