import React from 'react';

interface TextareaProps {
  id?: string;
  name?: string;
  value?: string;
  label?: string;
  placeholder?: string;
  onChange?: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
  onBlur?: (e: React.FocusEvent<HTMLTextAreaElement>) => void;
  error?: string;
  required?: boolean;
  disabled?: boolean;
  className?: string;
  textareaClassName?: string;
  rows?: number;
}

const Textarea: React.FC<TextareaProps> = ({
  id,
  name,
  value,
  label,
  placeholder,
  onChange,
  onBlur,
  error,
  required = false,
  disabled = false,
  className = '',
  textareaClassName = '',
  rows = 3
}) => {
  const baseContainerClasses = 'w-full';
  const containerClasses = `${baseContainerClasses} ${className}`;

  const baseTextareaClasses = 'block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm disabled:bg-gray-100 disabled:text-gray-500';
  const textareaClasses = `${baseTextareaClasses} ${error ? 'border-red-500' : 'border-gray-300'} ${textareaClassName}`;

  return (
    <div className={containerClasses}>
      {label && (
        <label htmlFor={id} className="block text-sm font-medium text-gray-700 mb-1">
          {label} {required && <span className="text-red-500">*</span>}
        </label>
      )}
      <textarea
        id={id}
        name={name}
        value={value}
        placeholder={placeholder}
        onChange={onChange}
        onBlur={onBlur}
        required={required}
        disabled={disabled}
        className={textareaClasses}
        rows={rows}
      />
      {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
    </div>
  );
};

export default Textarea;