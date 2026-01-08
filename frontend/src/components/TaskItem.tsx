import React from 'react';
import { Task } from '@/types/task';
import Button from './Button';

interface TaskItemProps {
  task: Task;
  onToggleComplete: (id: string) => void;
  onDelete: (id: string) => void;
  onEdit: (task: Task) => void;
}

const TaskItem: React.FC<TaskItemProps> = ({ task, onToggleComplete, onDelete, onEdit }) => {
  const getPriorityClass = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'border-l-danger-500 bg-red-50';
      case 'medium':
        return 'border-l-warning-500 bg-yellow-50';
      case 'low':
      default:
        return 'border-l-success-500 bg-green-50';
    }
  };

  const getPriorityLabel = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'High';
      case 'medium':
        return 'Medium';
      case 'low':
        return 'Low';
      default:
        return priority;
    }
  };

  return (
    <div className={`p-4 mb-3 rounded-lg border-l-4 shadow-sm ${getPriorityClass(task.priority)}`}>
      <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3">
        <div className="flex items-start space-x-3 flex-grow">
          <input
            type="checkbox"
            checked={task.completed}
            onChange={() => onToggleComplete(task.id)}
            className="mt-1 h-5 w-5 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
          />
          <div className="flex-grow">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <h3 className={`text-lg font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                {task.title}
              </h3>
              <span className={`text-xs px-2 py-1 rounded-full ${
                task.priority === 'high' ? 'bg-danger-100 text-danger-800' :
                task.priority === 'medium' ? 'bg-warning-100 text-warning-800' :
                'bg-success-100 text-success-800'
              }`}>
                {getPriorityLabel(task.priority)}
              </span>
            </div>
            {task.description && (
              <p className={`mt-1 text-sm ${task.completed ? 'text-gray-400' : 'text-gray-600'}`}>
                {task.description}
              </p>
            )}
            {task.dueDate && (
              <p className="mt-1 text-xs text-gray-500">
                Due: {new Date(task.dueDate).toLocaleDateString()}
              </p>
            )}
            {task.tags && task.tags.length > 0 && (
              <div className="mt-2 flex flex-wrap gap-1">
                {task.tags.map((tag, index) => (
                  <span key={index} className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                    {tag}
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>
        <div className="flex space-x-2 justify-end">
          <Button
            variant="secondary"
            size="sm"
            onClick={() => onEdit(task)}
            className="text-xs"
          >
            Edit
          </Button>
          <Button
            variant="danger"
            size="sm"
            onClick={() => onDelete(task.id)}
            className="text-xs"
          >
            Delete
          </Button>
        </div>
      </div>
    </div>
  );
};

export default TaskItem;