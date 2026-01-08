import React from 'react';
import Select from './Select';
import Input from './Input';
import { FilterCriteria } from '@/types/task';

interface FilterControlsProps {
  filters: FilterCriteria;
  onFilterChange: (filters: FilterCriteria) => void;
}

const FilterControls: React.FC<FilterControlsProps> = ({ filters, onFilterChange }) => {
  const handleCompletedChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value;
    onFilterChange({
      ...filters,
      completed: value === '' ? null : value === 'true'
    });
  };

  const handlePriorityChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value;
    onFilterChange({
      ...filters,
      priority: value === '' ? null : value as 'low' | 'medium' | 'high'
    });
  };

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    onFilterChange({
      ...filters,
      searchQuery: value || null
    });
  };

  const handleClearFilters = () => {
    onFilterChange({
      completed: null,
      priority: null,
      tags: [],
      searchQuery: null
    });
  };

  const priorityOptions = [
    { value: '', label: 'All Priorities' },
    { value: 'low', label: 'Low' },
    { value: 'medium', label: 'Medium' },
    { value: 'high', label: 'High' }
  ];

  return (
    <div className="bg-white p-4 rounded-lg shadow-sm mb-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <Select
            id="filter-completed"
            label="Status"
            value={filters.completed === null ? '' : String(filters.completed)}
            onChange={handleCompletedChange}
            options={[
              { value: '', label: 'All Statuses' },
              { value: 'true', label: 'Completed' },
              { value: 'false', label: 'Incomplete' }
            ]}
          />
        </div>
        <div>
          <Select
            id="filter-priority"
            label="Priority"
            value={filters.priority || ''}
            onChange={handlePriorityChange}
            options={priorityOptions}
          />
        </div>
        <div>
          <Input
            id="filter-search"
            label="Search"
            value={filters.searchQuery || ''}
            onChange={(e) => handleSearchChange(e)}
            placeholder="Search tasks..."
          />
        </div>
        <div className="flex items-end">
          <button
            onClick={handleClearFilters}
            className="w-full bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-2 px-4 rounded-md transition-colors"
          >
            Clear Filters
          </button>
        </div>
      </div>
    </div>
  );
};

export default FilterControls;