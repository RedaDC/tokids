'use client';

import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { X, Activity, Cpu, CheckCircle2, Zap, Clock, Terminal } from 'lucide-react';
import { Agent } from '@/lib/types';
import { api } from '@/lib/api';
import StatusBadge from '@/components/ui/StatusBadge';
import Button from '@/components/ui/Button';

interface AgentDetailModalProps {
  agent: Agent | null;
  onClose: () => void;
}

export const AgentDetailModal: React.FC<AgentDetailModalProps> = ({ agent, onClose }) => {
  const { data: logs, isLoading: loadingLogs } = useQuery({
    queryKey: ['agent-logs', agent?.id],
    queryFn: () => (agent ? api.agents.getAgentLogs(agent.id) : []),
    enabled: !!agent,
    refetchInterval: 4000,
  });

  if (!agent) return null;

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-black/60 backdrop-blur-sm animate-fade-in">
      <div className="relative h-full w-full max-w-md bg-slate-950/95 border-l border-white/10 p-6 shadow-2xl backdrop-blur-2xl flex flex-col overflow-y-auto animate-slide-in">
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-white/5">
          <div className="flex items-center gap-3">
            <span className="text-3xl p-2 rounded-xl bg-purple-500/10 border border-purple-500/20">
              {agent.avatar}
            </span>
            <div>
              <h3 className="font-heading text-lg font-bold text-white flex items-center gap-2">
                {agent.name}
                <span className="text-xs font-normal text-slate-400">({agent.role})</span>
              </h3>
              <p className="text-xs text-purple-400 font-medium">{agent.displayName}</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-white/5 transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Status & Quick Stats */}
        <div className="mt-6 space-y-4">
          <div className="flex items-center justify-between p-3 rounded-xl bg-white/[0.02] border border-white/5">
            <span className="text-xs text-slate-400">Operational Status</span>
            <StatusBadge status={agent.status} />
          </div>

          <div className="p-3 rounded-xl bg-purple-950/20 border border-purple-500/20">
            <div className="flex items-center gap-2 text-xs font-semibold text-purple-300 mb-1">
              <Zap className="h-3.5 w-3.5 text-purple-400" />
              Active Subtask
            </div>
            <p className="text-xs text-slate-200">
              {agent.currentTask || 'Agent standing by for pipeline dispatch.'}
            </p>
          </div>

          {/* Vitals Grid */}
          <div className="grid grid-cols-2 gap-2.5">
            <div className="p-3 rounded-xl bg-white/[0.02] border border-white/5">
              <span className="text-[10px] text-slate-400 uppercase tracking-wider block">
                Model Engine
              </span>
              <span className="text-xs font-bold text-white mt-0.5 block font-mono">
                {agent.model}
              </span>
            </div>
            <div className="p-3 rounded-xl bg-white/[0.02] border border-white/5">
              <span className="text-[10px] text-slate-400 uppercase tracking-wider block">
                Success Rate
              </span>
              <span className="text-xs font-bold text-emerald-400 mt-0.5 block font-mono">
                {agent.successRate}%
              </span>
            </div>
            <div className="p-3 rounded-xl bg-white/[0.02] border border-white/5">
              <span className="text-[10px] text-slate-400 uppercase tracking-wider block">
                Tasks Completed
              </span>
              <span className="text-xs font-bold text-white mt-0.5 block font-mono">
                {agent.completedTasksCount.toLocaleString()}
              </span>
            </div>
            <div className="p-3 rounded-xl bg-white/[0.02] border border-white/5">
              <span className="text-[10px] text-slate-400 uppercase tracking-wider block">
                System Uptime
              </span>
              <span className="text-xs font-bold text-cyan-400 mt-0.5 block font-mono">
                {agent.uptime}
              </span>
            </div>
          </div>
        </div>

        {/* Real-time Task Log Terminal */}
        <div className="mt-6 flex-1 flex flex-col min-h-[220px]">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center gap-1.5">
              <Terminal className="h-3.5 w-3.5 text-purple-400" />
              Execution Logs
            </span>
            <span className="text-[10px] text-slate-500 font-mono">Live stream</span>
          </div>

          <div className="flex-1 rounded-xl border border-white/5 bg-[#050810] p-3 font-mono text-[11px] overflow-y-auto space-y-2">
            {loadingLogs ? (
              <p className="text-slate-500 animate-pulse">Connecting to agent daemon...</p>
            ) : logs && logs.length > 0 ? (
              logs.map((log) => (
                <div key={log.id} className="leading-relaxed">
                  <span className="text-slate-500 mr-2">[{log.timestamp}]</span>
                  <span
                    className={
                      log.level === 'success'
                        ? 'text-emerald-400'
                        : log.level === 'warn'
                        ? 'text-amber-400'
                        : log.level === 'error'
                        ? 'text-rose-400'
                        : 'text-slate-300'
                    }
                  >
                    {log.message}
                  </span>
                </div>
              ))
            ) : (
              <p className="text-slate-500">No recent logs recorded.</p>
            )}
          </div>
        </div>

        {/* Footer Actions */}
        <div className="mt-6 pt-4 border-t border-white/5 flex gap-3">
          <Button variant="secondary" className="flex-1" onClick={onClose}>
            Close
          </Button>
          <Button
            variant="primary"
            className="flex-1"
            onClick={() => {
              alert(`Diagnostic ping sent to ${agent.name} (${agent.role})`);
            }}
          >
            Dispatch Ping
          </Button>
        </div>
      </div>
    </div>
  );
};

export default AgentDetailModal;
