import React, { useState, useEffect } from 'react';
import { Task, Priority, NewTask, TaskUpdate } from '@/types/task';
import Input from './Input';
import Textarea from './Textarea';
import Select from './Select';
import Button from './Button';

interface TaskFormProps {
  task?: Task;
  onSubmit: (taskData: NewTask | Partial<Task>) => void;
  onCancel: () => void;
}

const TaskForm: React.FC<TaskFormProps> = ({ task, onSubmit, onCancel }) => {
  const [title, setTitle] = useState(task?.title || '');
  const [description, setDescription] = useState(task?.description || '');
  const [priority, setPriority] = useState<Priority>(task?.priority || 'medium');
  const [dueDate, setDueDate] = useState(task?.dueDate || '');
  const [tags, setTags] = useState(
    Array.isArray(task?.tags)
      ? task.tags.join(', ')
      : typeof task?.tags === 'string'
        ? task.tags
        : ''
  );
  const [completed, setCompleted] = useState(task?.completed || false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Transform data to match backend field names and format
    const transformedTaskData = {
      title: title.trim(),
      description,
      priority,
      due_date: dueDate || null,  // Changed to match backend field name
      tags: JSON.stringify(tags.split(',').map(tag => tag.trim()).filter(tag => tag)), // Serialize tags as JSON string for backend
      completed
    };

    if (task) {
      // Update existing task - cast to Partial<Task>
      onSubmit(transformedTaskData as Partial<Task>);
    } else {
      // Create new task - cast to NewTask
      onSubmit(transformedTaskData as NewTask);
    }
  };

  const priorityOptions = [
    { value: 'low', label: 'Low' },
    { value: 'medium', label: 'Medium' },
    { value: 'high', label: 'High' }
  ];

  return (
    <div className="bg-white p-6 rounded-lg shadow-md mb-6">
      <h2 className="text-xl font-semibold mb-4">
        {task ? 'Edit Task' : 'Add New Task'}
      </h2>
      <form onSubmit={handleSubmit}>
        <div className="grid grid-cols-1 gap-4">
          <div>
            <Input
              id="title"
              name="title"
              label="Title *"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
              placeholder="Task title"
            />
          </div>
          <div>
            <Textarea
              id="description"
              name="description"
              label="Description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Task description"
            />
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Select
                id="priority"
                name="priority"
                label="Priority"
                value={priority}
                onChange={(e) => setPriority(e.target.value as Priority)}
                options={priorityOptions}
              />
            </div>
            <div>
              <Input
                id="dueDate"
                name="dueDate"
                label="Due Date"
                value={dueDate}
                onChange={(e) => setDueDate(e.target.value)}
                type="date"
                placeholder="YYYY-MM-DD"
              />
            </div>
          </div>
          <div>
            <Input
              id="tags"
              name="tags"
              label="Tags"
              value={tags}
              onChange={(e) => setTags(e.target.value)}
              placeholder="tag1, tag2, tag3"
            />
          </div>
          <div className="flex items-center">
            <input
              type="checkbox"
              id="completed"
              checked={completed}
              onChange={(e) => setCompleted(e.target.checked)}
              className="h-4 w-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
            />
            <label htmlFor="completed" className="ml-2 block text-sm text-gray-700">
              Completed
            </label>
          </div>
        </div>
        <div className="mt-6 flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-3">
          <Button type="submit" variant="primary">
            {task ? 'Update Task' : 'Add Task'}
          </Button>
          <Button type="button" variant="secondary" onClick={onCancel}>
            Cancel
          </Button>
        </div>
      </form>
    </div>
  );
};

export default TaskForm;