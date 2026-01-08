# Data Model: Backend API for Todo App with FastAPI and SQLModel

## Task Entity

**Description**: Represents a user's to-do item

**Fields**:
- `id`: UUID or integer (primary key, auto-generated)
- `title`: string (required, max length 255)
- `description`: string (optional, max length 1000)
- `completed`: boolean (default false)
- `priority`: string enum ('low', 'medium', 'high') (default 'medium')
- `tags`: JSON array of strings (optional)
- `due_date`: datetime (optional)
- `created_at`: datetime (auto-generated)
- `updated_at`: datetime (auto-generated)
- `user_id`: string/UUID (foreign key to User, required)

**Validation Rules**:
- Title must not be empty
- Priority must be one of 'low', 'medium', 'high'
- Due date must be in the future if provided
- Tags array items must be non-empty strings

**State Transitions**:
- `completed: false` → `completed: true` (via completion toggle endpoint)
- `completed: true` → `completed: false` (via completion toggle endpoint)

## User Entity

**Description**: Represents a user in the system

**Fields**:
- `id`: UUID or integer (primary key, auto-generated)
- `created_at`: datetime (auto-generated)
- `updated_at`: datetime (auto-generated)

**Validation Rules**:
- User ID must be unique
- Created/updated timestamps are automatically managed