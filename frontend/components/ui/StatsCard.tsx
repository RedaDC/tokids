'use client';

import React, { useEffect, useState } from 'react';
import { LucideIcon, TrendingUp, TrendingDown } from 'lucide-react';

interface StatsCardProps {
  label: string;
  value: string | number;
  change?: {
    value: number;
    isPositive?: boolean;
    label?: string;
  };
  icon: LucideIcon;
  gradient?: 'purple' | 'blue' | 'cyan' | 'emerald' | 'amber' | 'rose';
  loading?: boolean;
}

const gradientColors = {
  purple: 'from-purple-500 via-indigo-500 to-purple-600',
  blue: 'from-blue-500 via-sky-500 to-indigo-500',
  cyan: 'from-cyan-400 via-teal-500 to-blue-500',
  emerald: 'from-emerald-400 via-teal-500 to-emerald-600',
  amber: 'from-amber-400 via-orange-500 to-amber-600',
  rose: 'from-rose-500 via-pink-500 to-rose-600',
};

const iconColors = {
  purple: 'text-purple-400 bg-purple-500/10 border-purple-500/20',
  blue: 'text-blue-400 bg-blue-500/10 border-blue-500/20',
  cyan: 'text-cyan-400 bg-cyan-500/10 border-cyan-500/20',
  emerald: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20',
  amber: 'text-amber-400 bg-amber-500/10 border-amber-500/20',
  rose: 'text-rose-400 bg-rose-500/10 border-rose-500/20',
};

export const StatsCard: React.FC<StatsCardProps> = ({
  label,
  value,
  change,
  icon: Icon,
  gradient = 'purple',
  loading = false,
}) => {
  const [displayValue, setDisplayValue] = useState<string | number>(
    typeof value === 'number' ? 0 : value
  );

  useEffect(() => {
    if (typeof value === 'number' && !loading) {
      const duration = 800;
      const steps = 30;
      const stepTime = duration / steps;
      let currentStep = 0;

      const timer = setInterval(() => {
        currentStep++;
        const progress = currentStep / steps;
        const currentVal = Math.round(value * progress);
        setDisplayValue(currentVal);

        if (currentStep >= steps) {
          clearInterval(timer);
          setDisplayValue(value);
        }
      }, stepTime);

      return () => clearInterval(timer);
    } else {
      setDisplayValue(value);
    }
  }, [value, loading]);

  if (loading) {
    return (
      <div className="relative overflow-hidden rounded-xl border border-white/5 bg-background-card p-5 backdrop-blur-md">
        <div className="h-1 w-full bg-white/5 shimmer-effect absolute top-0 left-0" />
        <div className="flex items-center justify-between">
          <div className="h-4 w-24 bg-white/5 rounded shimmer-effect" />
          <div className="h-10 w-10 rounded-lg bg-white/5 shimmer-effect" />
        </div>
        <div className="mt-4 h-8 w-32 bg-white/5 rounded shimmer-effect" />
        <div className="mt-3 h-4 w-20 bg-white/5 rounded shimmer-effect" />
      </div>
    );
  }

  return (
    <div className="group relative overflow-hidden rounded-xl border border-white/5 bg-background-card p-5 backdrop-blur-md transition-all duration-300 hover:border-white/10 hover:shadow-glass hover:translate-y-[-2px]">
      {/* Top accent gradient line */}
      <div
        className={`absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r ${gradientColors[gradient]} opacity-70 group-hover:opacity-100 transition-opacity`}
      />

      <div className="flex items-center justify-between">
        <span className="text-xs font-medium uppercase tracking-wider text-slate-400">
          {label}
        </span>
        <div
          className={`flex h-10 w-10 items-center justify-center rounded-lg border ${iconColors[gradient]} transition-transform duration-300 group-hover:scale-110`}
        >
          <Icon className="h-5 w-5" />
        </div>
      </div>

      <div className="mt-2 flex items-baseline justify-between">
        <div className="text-2xl font-bold tracking-tight text-white font-heading">
          {displayValue}
        </div>

        {change && (
          <div
            className={`flex items-center text-xs font-semibold ${
              change.isPositive !== false ? 'text-emerald-400' : 'text-rose-400'
            }`}
          >
            {change.isPositive !== false ? (
              <TrendingUp className="mr-1 h-3.5 w-3.5" />
            ) : (
              <TrendingDown className="mr-1 h-3.5 w-3.5" />
            )}
            <span>
              {change.isPositive !== false ? '+' : ''}
              {change.value}%
            </span>
          </div>
        )}
      </div>

      {change?.label && (
        <p className="mt-1 text-[11px] text-slate-400">{change.label}</p>
      )}
    </div>
  );
};

export default StatsCard;
