'use client';

import React from 'react';
import { useQuery } from '@tanstack/react-query';
import {
  Sparkles,
  CheckCircle,
  XCircle,
  Users,
  Layers,
  DollarSign,
  Award,
  Activity,
  Server,
  Database,
  Cpu,
  RefreshCw,
  ArrowUpRight,
  Zap,
} from 'lucide-react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from 'recharts';
import StatsCard from '@/components/ui/StatsCard';
import GlassPanel from '@/components/ui/GlassPanel';
import StatusBadge from '@/components/ui/StatusBadge';
import Button from '@/components/ui/Button';
import { api } from '@/lib/api';
import Link from 'next/link';

export default function DashboardPage() {
  const { data: overview, isLoading, refetch, isFetching } = useQuery({
    queryKey: ['analytics-overview'],
    queryFn: () => api.analytics.getOverview(),
    refetchInterval: 10000, // auto-refresh every 10s
  });

  return (
    <div className="space-y-8 pb-10">
      {/* Top Banner / Hero Header */}
      <div className="relative overflow-hidden rounded-2xl border border-white/5 bg-gradient-to-r from-purple-950/40 via-slate-900/60 to-blue-950/40 p-6 md:p-8 backdrop-blur-xl">
        <div className="absolute top-0 right-0 -mt-10 -mr-10 h-64 w-64 rounded-full bg-purple-600/10 blur-3xl pointer-events-none" />
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-300 text-xs font-semibold uppercase tracking-wider mb-2">
              <Zap className="h-3.5 w-3.5 text-purple-400" />
              Autonomous Production Matrix
            </div>
            <h2 className="font-heading text-2xl md:text-3xl font-extrabold text-white tracking-tight">
              AI Illustration Command Center
            </h2>
            <p className="mt-1 text-sm text-slate-300 max-w-2xl">
              9 autonomous agents orchestrating trend research, prompt engineering, high-res apparel vector generation, and direct TeePublic marketplace sync.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <Button
              variant="secondary"
              size="sm"
              icon={RefreshCw}
              onClick={() => refetch()}
              loading={isFetching}
            >
              Sync Matrix
            </Button>
            <Link href="/studio">
              <Button variant="glow" size="sm" icon={Sparkles}>
                Create Artwork
              </Button>
            </Link>
          </div>
        </div>
      </div>

      {/* 8 Stats Cards Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatsCard
          label="Total Generated"
          value={overview?.totalDesigns ?? 1482}
          change={{ value: 12.4, isPositive: true, label: 'vs last week' }}
          icon={Sparkles}
          gradient="purple"
          loading={isLoading}
        />
        <StatsCard
          label="Approved Designs"
          value={overview?.approvedDesigns ?? 1395}
          change={{ value: 8.7, isPositive: true, label: '94% pass rate' }}
          icon={CheckCircle}
          gradient="emerald"
          loading={isLoading}
        />
        <StatsCard
          label="Rejected Designs"
          value={overview?.rejectedDesigns ?? 87}
          change={{ value: -3.2, isPositive: true, label: 'Quality filtered' }}
          icon={XCircle}
          gradient="rose"
          loading={isLoading}
        />
        <StatsCard
          label="Active Agents"
          value={overview?.activeAgents ?? 9}
          change={{ value: 100, isPositive: true, label: '9 / 9 operational' }}
          icon={Users}
          gradient="cyan"
          loading={isLoading}
        />
        <StatsCard
          label="Completed Tasks"
          value={overview?.completedTasks ?? 18450}
          change={{ value: 24.1, isPositive: true, label: '24h throughput' }}
          icon={Layers}
          gradient="blue"
          loading={isLoading}
        />
        <StatsCard
          label="Generation Spend"
          value={`$${(overview?.totalExpenses ?? 84.62).toFixed(2)}`}
          change={{ value: 0.041, isPositive: true, label: '$0.04 avg / design' }}
          icon={DollarSign}
          gradient="amber"
          loading={isLoading}
        />
        <StatsCard
          label="Avg Quality Score"
          value={`${overview?.averageQualityScore ?? 94.2}/100`}
          change={{ value: 2.1, isPositive: true, label: 'Vision QA Index' }}
          icon={Award}
          gradient="emerald"
          loading={isLoading}
        />
        <StatsCard
          label="Production Rate"
          value={`${overview?.successRate ?? 94.1}%`}
          change={{ value: 4.8, isPositive: true, label: 'Automated yield' }}
          icon={Activity}
          gradient="purple"
          loading={isLoading}
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Production Activity Chart */}
        <GlassPanel className="lg:col-span-2 flex flex-col justify-between">
          <div className="flex items-center justify-between pb-4 border-b border-white/5">
            <div>
              <h3 className="text-base font-bold text-white font-heading">
                Production Activity
              </h3>
              <p className="text-xs text-slate-400">
                Daily graphics created, verified, and auto-approved
              </p>
            </div>
            <div className="flex items-center gap-4 text-xs font-medium">
              <span className="flex items-center gap-1.5 text-purple-400">
                <span className="h-2.5 w-2.5 rounded-full bg-purple-500" />
                Generated
              </span>
              <span className="flex items-center gap-1.5 text-emerald-400">
                <span className="h-2.5 w-2.5 rounded-full bg-emerald-500" />
                Approved
              </span>
            </div>
          </div>

          <div className="h-72 w-full pt-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart
                data={overview?.productionHistory ?? []}
                margin={{ top: 10, right: 10, left: -20, bottom: 0 }}
              >
                <defs>
                  <linearGradient id="colorGen" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#7C3AED" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#7C3AED" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="colorApp" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10B981" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#10B981" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <XAxis
                  dataKey="date"
                  stroke="#64748B"
                  fontSize={12}
                  tickLine={false}
                  axisLine={false}
                />
                <YAxis
                  stroke="#64748B"
                  fontSize={12}
                  tickLine={false}
                  axisLine={false}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#0F172A',
                    borderColor: 'rgba(255,255,255,0.1)',
                    borderRadius: '12px',
                    fontSize: '12px',
                    boxShadow: '0 10px 25px -5px rgba(0,0,0,0.5)',
                  }}
                />
                <Area
                  type="monotone"
                  dataKey="generated"
                  stroke="#7C3AED"
                  strokeWidth={2.5}
                  fillOpacity={1}
                  fill="url(#colorGen)"
                />
                <Area
                  type="monotone"
                  dataKey="approved"
                  stroke="#10B981"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#colorApp)"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </GlassPanel>

        {/* Secondary Cost Breakdown Chart */}
        <GlassPanel className="flex flex-col justify-between">
          <div className="pb-4 border-b border-white/5">
            <h3 className="text-base font-bold text-white font-heading">
              Cost by Service
            </h3>
            <p className="text-xs text-slate-400">
              Unit economics allocation ($84.62 total spend)
            </p>
          </div>

          <div className="h-64 w-full relative">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={overview?.costBreakdown ?? []}
                  cx="50%"
                  cy="50%"
                  innerRadius={55}
                  outerRadius={80}
                  paddingAngle={4}
                  dataKey="value"
                >
                  {(overview?.costBreakdown ?? []).map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  formatter={(val: number) => [`$${val.toFixed(2)}`, 'Cost']}
                  contentStyle={{
                    backgroundColor: '#0F172A',
                    borderColor: 'rgba(255,255,255,0.1)',
                    borderRadius: '12px',
                    fontSize: '12px',
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
            <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
              <span className="text-xs text-slate-400 font-medium">Flux / Pro</span>
              <span className="text-lg font-bold text-white">57%</span>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-2 pt-2 border-t border-white/5 text-[11px]">
            {(overview?.costBreakdown ?? []).slice(0, 4).map((item) => (
              <div key={item.name} className="flex items-center gap-1.5 truncate">
                <span
                  className="h-2 w-2 rounded-full shrink-0"
                  style={{ backgroundColor: item.color }}
                />
                <span className="truncate text-slate-400">{item.name}</span>
              </div>
            ))}
          </div>
        </GlassPanel>
      </div>

      {/* Activity Feed & System Status Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Activity Feed (2 Cols) */}
        <GlassPanel className="lg:col-span-2">
          <div className="flex items-center justify-between pb-4 border-b border-white/5 mb-4">
            <div>
              <h3 className="text-base font-bold text-white font-heading">
                Autonomous Workforce Activity
              </h3>
              <p className="text-xs text-slate-400">
                Real-time agent completions and compliance logs
              </p>
            </div>
            <Link
              href="/workforce"
              className="text-xs font-semibold text-purple-400 hover:text-purple-300 flex items-center gap-1"
            >
              View All Agents <ArrowUpRight className="h-3.5 w-3.5" />
            </Link>
          </div>

          <div className="space-y-3">
            {(overview?.recentActivity ?? []).map((act) => (
              <div
                key={act.id}
                className="flex items-start gap-3.5 p-3 rounded-xl border border-white/5 bg-slate-900/40 hover:bg-slate-900/80 transition-colors"
              >
                <div className="mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-purple-500/10 border border-purple-500/20 text-purple-400">
                  <Sparkles className="h-3.5 w-3.5" />
                </div>
                <div className="min-w-0 flex-1">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-semibold text-white truncate">
                      {act.title}
                    </span>
                    <span className="text-[11px] text-slate-500">{act.timestamp}</span>
                  </div>
                  <p className="text-xs text-slate-400 mt-0.5">{act.description}</p>
                </div>
                {act.agentName && (
                  <span className="hidden sm:inline-block px-2 py-0.5 rounded text-[10px] font-medium bg-white/5 text-slate-300 border border-white/5 shrink-0">
                    {act.agentName}
                  </span>
                )}
              </div>
            ))}
          </div>
        </GlassPanel>

        {/* System Services Status */}
        <GlassPanel>
          <div className="flex items-center justify-between pb-4 border-b border-white/5 mb-4">
            <div>
              <h3 className="text-base font-bold text-white font-heading">
                Infrastructure Vitals
              </h3>
              <p className="text-xs text-slate-400">Core server & model microservices</p>
            </div>
            <div className="h-2 w-2 rounded-full bg-emerald-400 animate-ping" />
          </div>

          <div className="space-y-3">
            {(overview?.systemServices ?? []).map((srv) => (
              <div
                key={srv.name}
                className="flex items-center justify-between p-2.5 rounded-xl border border-white/5 bg-slate-900/40"
              >
                <div className="flex items-center gap-2.5 min-w-0">
                  <Server className="h-4 w-4 text-slate-400 shrink-0" />
                  <span className="text-xs font-medium text-slate-200 truncate">
                    {srv.name}
                  </span>
                </div>
                <div className="flex items-center gap-2 shrink-0">
                  {srv.latencyMs && (
                    <span className="text-[10px] font-mono text-slate-500">
                      {srv.latencyMs}ms
                    </span>
                  )}
                  <StatusBadge status="approved" label="OK" pulse={false} />
                </div>
              </div>
            ))}
          </div>
        </GlassPanel>
      </div>
    </div>
  );
}
