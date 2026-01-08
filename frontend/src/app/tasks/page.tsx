'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Layout from '@/components/Layout';
import TaskList from '@/components/TaskList';
import TaskForm from '@/components/TaskForm';
import FilterControls from '@/components/FilterControls';
import SortControls from '@/components/SortControls';
import { Task, FilterCriteria, SortCriteria, NewTask, TaskUpdate } from '@/types/task';
import { taskApi } from '@/services/api';

const TasksPage: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filteredTasks, setFilteredTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [showForm, setShowForm] = useState<boolean>(false);
  const [filters, setFilters] = useState<FilterCriteria>({
    completed: null,
    priority: null,
    tags: [],
    searchQuery: null
  });
  const [sort, setSort] = useState<SortCriteria>({
    field: 'createdAt',
    direction: 'asc'
  });

  const router = useRouter();

  // Check authentication on component mount
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/auth/login');
      return;
    }
    fetchTasks();
  }, []);

  // Apply filters and sorting when tasks, filters, or sort criteria change
  useEffect(() => {
    let result = [...tasks];

    // Apply filters
    if (filters.completed !== null && filters.completed !== undefined) {
      result = result.filter(task => task.completed === filters.completed);
    }
    if (filters.priority) {
      result = result.filter(task => task.priority === filters.priority);
    }
    if (filters.searchQuery) {
      const query = filters.searchQuery.toLowerCase();
      result = result.filter(task =>
        task.title.toLowerCase().includes(query) ||
        task.description.toLowerCase().includes(query)
      );
    }

    // Apply sorting
    result.sort((a, b) => {
      let aValue: any = a[sort.field];
      let bValue: any = b[sort.field];

      // Handle date comparison
      if (sort.field === 'dueDate' || sort.field === 'createdAt') {
        if (aValue && bValue) {
          aValue = new Date(aValue).getTime();
          bValue = new Date(bValue).getTime();
        } else if (aValue) {
          return sort.direction === 'asc' ? -1 : 1;
        } else if (bValue) {
          return sort.direction === 'asc' ? 1 : -1;
        } else {
          return 0;
        }
      }

      // Handle boolean comparison
      if (sort.field === 'completed') {
        return sort.direction === 'asc' ? (aValue ? 1 : -1) : (aValue ? -1 : 1);
      }

      // Handle string comparison
      if (typeof aValue === 'string' && typeof bValue === 'string') {
        aValue = aValue.toLowerCase();
        bValue = bValue.toLowerCase();
      }

      if (aValue < bValue) {
        return sort.direction === 'asc' ? -1 : 1;
      }
      if (aValue > bValue) {
        return sort.direction === 'asc' ? 1 : -1;
      }
      return 0;
    });

    setFilteredTasks(result);
  }, [tasks, filters, sort]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await taskApi.getTasks();
      if (response.success && Array.isArray(response.data)) {
        setTasks(response.data as Task[]);
      } else {
        setError('Failed to fetch tasks: Invalid response format');
      }
    } catch (err: any) {
      setError(err.error || 'Failed to fetch tasks');
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddTask = async (taskData: NewTask) => {
    try {
      const response = await taskApi.createTask(taskData);
      if (response.success) {
        // Re-fetch tasks to ensure state comes from backend data
        await fetchTasks();
        setShowForm(false);
      } else {
        setError('Failed to add task');
      }
    } catch (err: any) {
      setError(err.error || 'Failed to add task');
      console.error('Error adding task:', err);
    }
  };

  const handleUpdateTask = async (taskData: Partial<Task>) => {
    if (!editingTask) return;

    try {
      const response = await taskApi.updateTask(editingTask.id, taskData);
      if (response.success) {
        // Re-fetch tasks to ensure state comes from backend data
        await fetchTasks();
        setEditingTask(null);
        setShowForm(false);
      } else {
        setError('Failed to update task');
      }
    } catch (err: any) {
      setError(err.error || 'Failed to update task');
      console.error('Error updating task:', err);
    }
  };

  const handleToggleComplete = async (id: string) => {
    const task = tasks.find(t => t.id === id);
    if (!task) return;

    try {
      const response = await taskApi.toggleTaskCompletion(id, !task.completed);
      if (response.success) {
        // Re-fetch tasks to ensure state comes from backend data
        await fetchTasks();
      } else {
        setError('Failed to update task status');
      }
    } catch (err: any) {
      setError(err.error || 'Failed to update task status');
      console.error('Error toggling task:', err);
    }
  };

  const handleDeleteTask = async (id: string) => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }

    try {
      const response = await taskApi.deleteTask(id);
      if (response.success) {
        // Re-fetch tasks to ensure state comes from backend data
        await fetchTasks();
      } else {
        setError('Failed to delete task');
      }
    } catch (err: any) {
      setError(err.error || 'Failed to delete task');
      console.error('Error deleting task:', err);
    }
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setShowForm(true);
  };

  const handleCancelForm = () => {
    setShowForm(false);
    setEditingTask(null);
  };

  if (loading) {
    return (
      <Layout>
        <div className="flex justify-center items-center h-64">
          <p className="text-lg">Loading tasks...</p>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold text-gray-800">My Tasks</h1>
          <button
            onClick={() => setShowForm(true)}
            className="bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-4 rounded-md transition-colors"
          >
            Add Task
          </button>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        {showForm && (
          <TaskForm
            task={editingTask || undefined}
            onSubmit={(taskData) => {
              if (editingTask) {
                handleUpdateTask(taskData as Partial<Task>);
              } else {
                handleAddTask(taskData as NewTask);
              }
            }}
            onCancel={handleCancelForm}
          />
        )}

        <FilterControls
          filters={filters}
          onFilterChange={setFilters}
        />

        <SortControls
          sort={sort}
          onSortChange={setSort}
        />

        <TaskList
          tasks={filteredTasks}
          onToggleComplete={handleToggleComplete}
          onDelete={handleDeleteTask}
          onEdit={handleEditTask}
        />
      </div>
    </Layout>
  );
};

export default TasksPage;