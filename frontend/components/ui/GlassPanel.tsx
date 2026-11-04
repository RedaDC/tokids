'use client';

import React from 'react';

interface GlassPanelProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  className?: string;
  glow?: 'none' | 'purple' | 'cyan' | 'emerald';
  interactive?: boolean;
}

export const GlassPanel: React.FC<GlassPanelProps> = ({
  children,
  className = '',
  glow = 'none',
  interactive = false,
  ...props
}) => {
  const glowStyles = {
    none: '',
    purple: 'shadow-glow border-purple-500/30',
    cyan: 'shadow-glow-cyan border-cyan-500/30',
    emerald: 'shadow-glow-emerald border-emerald-500/30',
  };

  const interactiveStyles = interactive
    ? 'hover:border-purple-500/30 hover:bg-opacity-80 transition-all duration-300 hover:translate-y-[-2px]'
    : '';

  return (
    <div
      className={`relative overflow-hidden rounded-xl border border-white/5 bg-background-card p-6 backdrop-blur-xl ${glowStyles[glow]} ${interactiveStyles} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
};

export default GlassPanel;
