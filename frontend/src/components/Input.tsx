import React from 'react';

interface InputProps {
  id?: string;
  name?: string;
  value?: string;
  label?: string;
  placeholder?: string;
  type?: 'text' | 'email' | 'password' | 'number' | 'date' | 'tel' | 'url';
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onBlur?: (e: React.FocusEvent<HTMLInputElement>) => void;
  error?: string;
  required?: boolean;
  disabled?: boolean;
  className?: string;
  inputClassName?: string;
}

const Input: React.FC<InputProps> = ({
  id,
  name,
  value,
  label,
  placeholder,
  type = 'text',
  onChange,
  onBlur,
  error,
  required = false,
  disabled = false,
  className = '',
  inputClassName = ''
}) => {
  const baseContainerClasses = 'w-full';
  const containerClasses = `${baseContainerClasses} ${className}`;

  const baseInputClasses = 'block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm disabled:bg-gray-100 disabled:text-gray-500';
  const inputClasses = `${baseInputClasses} ${error ? 'border-red-500' : 'border-gray-300'} ${inputClassName}`;

  return (
    <div className={containerClasses}>
      {label && (
        <label htmlFor={id} className="block text-sm font-medium text-gray-700 mb-1">
          {label} {required && <span className="text-red-500">*</span>}
        </label>
      )}
      <input
        id={id}
        name={name}
        type={type}
        value={value}
        placeholder={placeholder}
        onChange={onChange}
        onBlur={onBlur}
        required={required}
        disabled={disabled}
        className={inputClasses}
      />
      {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
    </div>
  );
};

export default Input;