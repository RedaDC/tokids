'use client';

import React from 'react';
import { Agent } from '@/lib/types';
import StatusBadge from '@/components/ui/StatusBadge';
import { Cpu, Activity, Zap, CheckCircle2 } from 'lucide-react';

interface WorkforceGridProps {
  agents: Agent[];
  onSelectAgent: (agent: Agent) => void;
}

export const WorkforceGrid: React.FC<WorkforceGridProps> = ({ agents, onSelectAgent }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
      {agents.map((agent) => {
        const isWorking = agent.status === 'working';

        return (
          <div
            key={agent.id}
            onClick={() => onSelectAgent(agent)}
            className="group relative cursor-pointer overflow-hidden rounded-2xl border border-white/5 bg-background-card p-6 backdrop-blur-xl transition-all duration-300 hover:border-purple-500/40 hover:shadow-glow hover:-translate-y-1"
          >
            {/* Top status bar indicator */}
            <div
              className={`absolute top-0 left-0 right-0 h-1 transition-all ${
                isWorking
                  ? 'bg-gradient-to-r from-purple-500 via-cyan-400 to-purple-600 animate-pulse'
                  : 'bg-white/10'
              }`}
            />

            {/* Avatar & Header */}
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-3">
                <div className="relative flex h-14 w-14 items-center justify-center rounded-2xl bg-purple-950/40 border border-purple-500/30 text-2xl group-hover:scale-110 transition-transform">
                  {agent.avatar}
                  {isWorking && (
                    <span className="absolute -top-1 -right-1 flex h-3.5 w-3.5">
                      <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-purple-400 opacity-75" />
                      <span className="relative inline-flex rounded-full h-3.5 w-3.5 bg-purple-500 ring-2 ring-background-dark" />
                    </span>
                  )}
                </div>
                <div>
                  <h3 className="font-heading text-lg font-bold text-white group-hover:text-purple-300 transition-colors">
                    {agent.name}
                  </h3>
                  <p className="text-xs font-medium text-slate-400">{agent.displayName}</p>
                </div>
              </div>
              <StatusBadge status={agent.status} />
            </div>

            {/* Description */}
            <p className="mt-4 text-xs text-slate-300 line-clamp-2 leading-relaxed">
              {agent.description}
            </p>

            {/* Current Active Task */}
            <div className="mt-4 rounded-xl border border-white/5 bg-slate-950/60 p-3">
              <div className="flex items-center gap-1.5 text-[11px] font-semibold text-purple-400">
                <Zap className="h-3 w-3" />
                Active Focus:
              </div>
              <p className="mt-1 text-xs text-slate-200 truncate font-mono">
                {agent.currentTask || 'Idle — Standing by for batch'}
              </p>
            </div>

            {/* Bottom Performance Stats */}
            <div className="mt-4 grid grid-cols-3 gap-2 border-t border-white/5 pt-3 text-center">
              <div>
                <span className="text-[10px] text-slate-500 block uppercase">Success</span>
                <span className="text-xs font-bold text-emerald-400 font-mono">
                  {agent.successRate}%
                </span>
              </div>
              <div>
                <span className="text-[10px] text-slate-500 block uppercase">Tasks</span>
                <span className="text-xs font-bold text-white font-mono">
                  {agent.completedTasksCount}
                </span>
              </div>
              <div>
                <span className="text-[10px] text-slate-500 block uppercase">Engine</span>
                <span className="text-[11px] font-bold text-cyan-400 truncate block">
                  {agent.model.split('-')[0]}
                </span>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default WorkforceGrid;
