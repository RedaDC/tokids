'use client';

import React from 'react';
import { AgentStatus } from '@/lib/types';

interface StatusBadgeProps {
  status: AgentStatus | 'pending' | 'in_progress' | 'approved' | 'rejected' | 'draft' | 'ready';
  label?: string;
  className?: string;
  pulse?: boolean;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({
  status,
  label,
  className = '',
  pulse = true,
}) => {
  const getStatusConfig = () => {
    switch (status) {
      case 'working':
      case 'in_progress':
        return {
          dotColor: 'bg-purple-400',
          textColor: 'text-purple-300',
          bgBorder: 'bg-purple-500/10 border-purple-500/30',
          defaultLabel: 'Working',
          pulseEffect: true,
        };
      case 'idle':
        return {
          dotColor: 'bg-blue-400',
          textColor: 'text-blue-300',
          bgBorder: 'bg-blue-500/10 border-blue-500/30',
          defaultLabel: 'Idle',
          pulseEffect: false,
        };
      case 'completed':
      case 'approved':
      case 'ready':
        return {
          dotColor: 'bg-emerald-400',
          textColor: 'text-emerald-300',
          bgBorder: 'bg-emerald-500/10 border-emerald-500/30',
          defaultLabel: 'Completed',
          pulseEffect: false,
        };
      case 'failed':
      case 'rejected':
        return {
          dotColor: 'bg-rose-400',
          textColor: 'text-rose-300',
          bgBorder: 'bg-rose-500/10 border-rose-500/30',
          defaultLabel: 'Failed',
          pulseEffect: false,
        };
      case 'draft':
      case 'pending':
      case 'paused':
      default:
        return {
          dotColor: 'bg-amber-400',
          textColor: 'text-amber-300',
          bgBorder: 'bg-amber-500/10 border-amber-500/30',
          defaultLabel: status,
          pulseEffect: false,
        };
    }
  };

  const config = getStatusConfig();
  const displayLabel = label || config.defaultLabel;

  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium border backdrop-blur-sm ${config.bgBorder} ${config.textColor} ${className}`}
    >
      <span className="relative flex h-2 w-2">
        {pulse && config.pulseEffect && (
          <span
            className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${config.dotColor}`}
          />
        )}
        <span
          className={`relative inline-flex rounded-full h-2 w-2 ${config.dotColor}`}
        />
      </span>
      <span className="capitalize">{displayLabel}</span>
    </span>
  );
};

export default StatusBadge;
