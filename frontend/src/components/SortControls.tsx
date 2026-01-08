import React from 'react';
import Select from './Select';
import { SortCriteria } from '@/types/task';

interface SortControlsProps {
  sort: SortCriteria;
  onSortChange: (sort: SortCriteria) => void;
}

const SortControls: React.FC<SortControlsProps> = ({ sort, onSortChange }) => {
  const handleFieldChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const field = e.target.value as 'title' | 'priority' | 'dueDate' | 'createdAt' | 'completed';
    onSortChange({
      ...sort,
      field
    });
  };

  const handleDirectionChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const direction = e.target.value as 'asc' | 'desc';
    onSortChange({
      ...sort,
      direction
    });
  };

  const fieldOptions = [
    { value: 'createdAt', label: 'Created Date' },
    { value: 'title', label: 'Title' },
    { value: 'priority', label: 'Priority' },
    { value: 'dueDate', label: 'Due Date' },
    { value: 'completed', label: 'Status' }
  ];

  const directionOptions = [
    { value: 'asc', label: 'Ascending' },
    { value: 'desc', label: 'Descending' }
  ];

  return (
    <div className="bg-white p-4 rounded-lg shadow-sm mb-6 flex flex-col sm:flex-row gap-4">
      <div className="w-full sm:w-auto">
        <Select
          id="sort-field"
          label="Sort By"
          value={sort.field}
          onChange={handleFieldChange}
          options={fieldOptions}
        />
      </div>
      <div className="w-full sm:w-auto">
        <Select
          id="sort-direction"
          label="Direction"
          value={sort.direction}
          onChange={handleDirectionChange}
          options={directionOptions}
        />
      </div>
    </div>
  );
};

export default SortControls;