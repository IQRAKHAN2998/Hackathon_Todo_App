# Data Model: Next.js Frontend for Todo App

## Task Entity

**Definition**: Represents a single todo item with attributes that match the existing CLI functionality

**Fields**:
- `id`: string - Unique identifier for the task (UUID from backend)
- `title`: string - Title of the task (required, non-empty)
- `description`: string - Optional description of the task
- `completed`: boolean - Completion status (default: false)
- `priority`: string - Priority level (values: "low", "medium", "high", default: "medium")
- `tags`: string[] - Array of tags associated with the task
- `dueDate`: string | null - Due date in ISO format (optional)
- `createdAt`: string - Creation timestamp in ISO format
- `updatedAt`: string - Last update timestamp in ISO format

**Validation Rules**:
- `title` must be non-empty
- `priority` must be one of "low", "medium", "high"
- `completed` must be boolean
- `tags` must be an array of strings
- `dueDate` must be a valid ISO date string if provided

## Task List Entity

**Definition**: Collection of tasks with filtering and sorting capabilities

**Fields**:
- `tasks`: Task[] - Array of Task entities
- `filterCriteria`: FilterCriteria - Current filtering parameters
- `sortCriteria`: SortCriteria - Current sorting parameters

## Filter Criteria Entity

**Definition**: Parameters that determine which tasks are displayed

**Fields**:
- `completed`: boolean | null - Filter by completion status (null = show all)
- `priority`: string | null - Filter by priority level (null = show all)
- `tags`: string[] - Filter by tags (show tasks with any of these tags)
- `searchQuery`: string | null - Text search in title or description

## Sort Criteria Entity

**Definition**: Parameters that determine the order of displayed tasks

**Fields**:
- `field`: string - Field to sort by ("title", "priority", "dueDate", "createdAt", "completed")
- `direction`: string - Sort direction ("asc", "desc")

## API Response Entities

**TaskResponse**:
- `data`: Task | Task[] - Single task or array of tasks
- `success`: boolean - Whether the request was successful
- `message`: string | null - Optional message about the operation

**ErrorResponse**:
- `error`: string - Error message
- `code`: string - Error code
- `details`: any - Additional error details