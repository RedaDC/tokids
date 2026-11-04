'use client';

import React from 'react';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  className?: string;
  label?: string;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = 'md',
  className = '',
  label,
}) => {
  const sizeMap = {
    sm: 'h-4 w-4 border-2',
    md: 'h-8 w-8 border-2',
    lg: 'h-12 w-12 border-3',
    xl: 'h-16 w-16 border-4',
  };

  return (
    <div className={`flex flex-col items-center justify-center gap-3 ${className}`}>
      <div className="relative">
        <div
          className={`${sizeMap[size]} rounded-full border-purple-500/20 animate-spin border-t-purple-500`}
        />
        <div
          className={`absolute inset-0 ${sizeMap[size]} rounded-full border-transparent border-b-cyan-400 animate-spin`}
          style={{ animationDirection: 'reverse', animationDuration: '1.2s' }}
        />
      </div>
      {label && (
        <span className="text-xs font-medium tracking-wide text-slate-400 animate-pulse">
          {label}
        </span>
      )}
    </div>
  );
};

export default LoadingSpinner;
