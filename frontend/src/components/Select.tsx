import React from 'react';

interface Option {
  value: string;
  label: string;
}

interface SelectProps {
  id?: string;
  name?: string;
  value?: string;
  label?: string;
  options: Option[];
  placeholder?: string;
  onChange?: (e: React.ChangeEvent<HTMLSelectElement>) => void;
  onBlur?: (e: React.FocusEvent<HTMLSelectElement>) => void;
  error?: string;
  required?: boolean;
  disabled?: boolean;
  className?: string;
  selectClassName?: string;
}

const Select: React.FC<SelectProps> = ({
  id,
  name,
  value,
  label,
  options,
  placeholder,
  onChange,
  onBlur,
  error,
  required = false,
  disabled = false,
  className = '',
  selectClassName = ''
}) => {
  const baseContainerClasses = 'w-full';
  const containerClasses = `${baseContainerClasses} ${className}`;

  const baseSelectClasses = 'block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm disabled:bg-gray-100 disabled:text-gray-500';
  const selectClasses = `${baseSelectClasses} ${error ? 'border-red-500' : 'border-gray-300'} ${selectClassName}`;

  return (
    <div className={containerClasses}>
      {label && (
        <label htmlFor={id} className="block text-sm font-medium text-gray-700 mb-1">
          {label} {required && <span className="text-red-500">*</span>}
        </label>
      )}
      <select
        id={id}
        name={name}
        value={value}
        onChange={onChange}
        onBlur={onBlur}
        required={required}
        disabled={disabled}
        className={selectClasses}
      >
        {placeholder && (
          <option value="">{placeholder}</option>
        )}
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
    </div>
  );
};

export default Select;