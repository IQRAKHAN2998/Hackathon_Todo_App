export type Priority = 'low' | 'medium' | 'high';

// Define the base task interface
export interface Task {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  priority: Priority;
  tags: string[];
  dueDate?: string | null;
  createdAt: string;
  updatedAt: string;
}

// Define a type for task updates where fields can be optional
export type TaskUpdate = Partial<Omit<Task, 'id'>> & Pick<Task, 'id'>;

// Define a type for new task creation (excluding id, createdAt, updatedAt)
export type NewTask = Omit<Task, 'id' | 'createdAt' | 'updatedAt'>;

export interface FilterCriteria {
  completed?: boolean | null;
  priority?: Priority | null;
  tags?: string[];
  searchQuery?: string | null;
}

export interface SortCriteria {
  field: 'title' | 'priority' | 'dueDate' | 'createdAt' | 'completed';
  direction: 'asc' | 'desc';
}

export interface TaskResponse {
  success: boolean;
  data: Task | Task[];
  message?: string;
}

export interface ErrorResponse {
  error: string;
  code: string;
  details?: any;
}