import React from 'react';

interface MessageBubbleProps {
  message: string;
  isUser: boolean;
  timestamp?: Date;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message, isUser, timestamp }) => {
  const positionClass = isUser ? 'ml-auto bg-blue-500 text-white' : 'mr-auto bg-gray-200 text-gray-800';
  const alignmentClass = isUser ? 'justify-end' : 'justify-start';

  return (
    <div className={`flex ${alignmentClass} mb-4`}>
      <div className={`${positionClass} rounded-lg px-4 py-2 max-w-xs md:max-w-md lg:max-w-lg xl:max-w-xl break-words`}>
        <div className="whitespace-pre-wrap">{message}</div>
        {timestamp && (
          <div className={`text-xs mt-1 ${isUser ? 'text-blue-200' : 'text-gray-500'}`}>
            {timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </div>
        )}
      </div>
    </div>
  );
};

export default MessageBubble;