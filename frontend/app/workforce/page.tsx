'use client';

import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Box, LayoutGrid, RefreshCw, Zap, Users, ShieldCheck } from 'lucide-react';
import Button from '@/components/ui/Button';
import GlassPanel from '@/components/ui/GlassPanel';
import WorkforceGrid from '@/components/workforce/WorkforceGrid';
import AgentDetailModal from '@/components/workforce/AgentDetailModal';
import { api } from '@/lib/api';
import { Agent } from '@/lib/types';
import dynamic from 'next/dynamic';

// Dynamic import with SSR disabled for Three.js Canvas to prevent hydration issues
const Office3D = dynamic(() => import('@/components/workforce/Office3D'), {
  ssr: false,
  loading: () => (
    <div className="flex h-[650px] w-full items-center justify-center rounded-2xl border border-white/5 bg-[#040711]">
      <div className="flex flex-col items-center gap-3">
        <div className="h-10 w-10 animate-spin rounded-full border-2 border-purple-500 border-t-transparent" />
        <p className="text-xs font-mono text-purple-300">Initializing 3D Cyber Office...</p>
      </div>
    </div>
  ),
});

export default function WorkforcePage() {
  const [viewMode, setViewMode] = useState<'3d' | '2d'>('3d');
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);

  const { data: agents = [], isLoading, refetch, isFetching } = useQuery({
    queryKey: ['agents-list'],
    queryFn: () => api.agents.getAgents(),
    refetchInterval: 5000, // Poll every 5s for live status updates
  });

  const activeCount = agents.filter((a) => a.status === 'working').length;

  return (
    <div className="space-y-6">
      {/* Top Controls Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="font-heading text-2xl font-bold text-white flex items-center gap-2">
            <Users className="h-6 w-6 text-purple-400" />
            Autonomous Workforce Matrix
          </h2>
          <p className="text-xs text-slate-400">
            {activeCount} of 9 specialized agents actively executing real-time subtasks
          </p>
        </div>

        <div className="flex items-center gap-3">
          {/* View Mode Toggle */}
          <div className="flex items-center rounded-xl border border-white/10 bg-slate-900/80 p-1 backdrop-blur-md">
            <button
              onClick={() => setViewMode('3d')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                viewMode === '3d'
                  ? 'bg-purple-600 text-white shadow-glow-sm'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <Box className="h-3.5 w-3.5" />
              3D Office
            </button>
            <button
              onClick={() => setViewMode('2d')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                viewMode === '2d'
                  ? 'bg-purple-600 text-white shadow-glow-sm'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <LayoutGrid className="h-3.5 w-3.5" />
              2D Grid
            </button>
          </div>

          <Button
            variant="secondary"
            size="sm"
            icon={RefreshCw}
            onClick={() => refetch()}
            loading={isFetching}
          >
            Poll Daemons
          </Button>
        </div>
      </div>

      {/* Main Content: 3D Scene or 2D Grid */}
      {viewMode === '3d' ? (
        <Office3D agents={agents} onSelectAgent={(agent) => setSelectedAgent(agent)} />
      ) : (
        <WorkforceGrid agents={agents} onSelectAgent={(agent) => setSelectedAgent(agent)} />
      )}

      {/* Slide-in Agent Detail Drawer */}
      <AgentDetailModal
        agent={selectedAgent}
        onClose={() => setSelectedAgent(null)}
      />
    </div>
  );
}
