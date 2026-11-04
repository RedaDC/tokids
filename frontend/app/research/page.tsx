'use client';

import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  TrendingUp,
  Search,
  Sparkles,
  Target,
  ShieldAlert,
  BarChart2,
  Calendar,
  ArrowRight,
  Flame,
  CheckCircle2,
  RefreshCw,
  Lightbulb,
} from 'lucide-react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
} from 'recharts';
import GlassPanel from '@/components/ui/GlassPanel';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import StatusBadge from '@/components/ui/StatusBadge';
import { api } from '@/lib/api';
import Link from 'next/link';

export default function MarketResearchPage() {
  const queryClient = useQueryClient();
  const [searchQuery, setSearchQuery] = useState('');
  const [activeNiche, setActiveNiche] = useState<string | null>(null);

  const { data: reports = [], isLoading, isFetching } = useQuery({
    queryKey: ['research-reports'],
    queryFn: () => api.research.getResearchReports(),
  });

  const researchMutation = useMutation({
    mutationFn: (query: string) => api.research.startResearch(query),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['research-reports'] });
      setSearchQuery('');
    },
  });

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;
    researchMutation.mutate(searchQuery.trim());
  };

  const selectedReport = activeNiche
    ? reports.find((r) => r.id === activeNiche) || reports[0]
    : reports[0];

  return (
    <div className="space-y-8 pb-12">
      {/* Page Header */}
      <div className="relative overflow-hidden rounded-2xl border border-white/5 bg-gradient-to-r from-purple-950/40 via-slate-900/60 to-blue-950/40 p-6 md:p-8 backdrop-blur-xl">
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-xs font-semibold uppercase tracking-wider mb-2">
              <TrendingUp className="h-3.5 w-3.5 text-emerald-400" />
              Market Intelligence Agent (Scout)
            </div>
            <h1 className="font-heading text-2xl md:text-3xl font-extrabold text-white tracking-tight">
              Market Research & Niche Discovery
            </h1>
            <p className="text-sm text-slate-300 mt-1 max-w-2xl">
              Autonomous identification of high-velocity illustration niches on TeePublic with search velocity analysis, target audience profiling, and competition screening.
            </p>
          </div>
          <div className="flex items-center gap-3">
            <Button
              variant="outline"
              size="sm"
              onClick={() => queryClient.invalidateQueries({ queryKey: ['research-reports'] })}
              loading={isFetching}
              icon={<RefreshCw className="h-4 w-4" />}
            >
              Refresh Trends
            </Button>
          </div>
        </div>
      </div>

      {/* Query Bar */}
      <GlassPanel className="p-4 md:p-6">
        <form onSubmit={handleSearchSubmit} className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-5 w-5 text-slate-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Enter merchandise topic (e.g. 'Cozy Cottagecore', 'Space Cats', 'Retro Cyberpunk')..."
              className="w-full pl-11 pr-4 py-3 bg-[#0A0F1D] border border-white/10 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:border-purple-500/50 focus:ring-1 focus:ring-purple-500 transition-all text-sm"
            />
          </div>
          <Button
            type="submit"
            variant="primary"
            loading={researchMutation.isPending}
            icon={<Sparkles className="h-4 w-4" />}
            className="shrink-0"
          >
            Launch Deep Research
          </Button>
        </form>
      </GlassPanel>

      {/* Main Grid: Niche List vs Niche Deep Dive */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Discovered Niches List */}
        <div className="lg:col-span-5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-400">
              Identified Opportunities ({reports.length})
            </h3>
            <span className="text-xs text-purple-400 font-medium">Ranked by Confidence</span>
          </div>

          {isLoading ? (
            <div className="space-y-3">
              {[1, 2, 3].map((i) => (
                <div key={i} className="h-28 rounded-xl bg-white/[0.02] border border-white/5 animate-pulse" />
              ))}
            </div>
          ) : reports.length === 0 ? (
            <GlassPanel className="p-8 text-center text-slate-400">
              <Search className="h-8 w-8 mx-auto mb-2 opacity-50" />
              <p>No research reports found yet. Launch a search above!</p>
            </GlassPanel>
          ) : (
            <div className="space-y-3">
              {reports.map((report) => {
                const isSelected = selectedReport?.id === report.id;
                return (
                  <div
                    key={report.id}
                    onClick={() => setActiveNiche(report.id)}
                    className={`cursor-pointer rounded-xl p-4 transition-all duration-200 border ${
                      isSelected
                        ? 'bg-purple-950/20 border-purple-500/40 shadow-glow-sm'
                        : 'bg-[#0B1120]/60 hover:bg-[#0E1628]/80 border-white/5'
                    }`}
                  >
                    <div className="flex items-start justify-between gap-2 mb-2">
                      <div className="font-heading font-bold text-white text-base">
                        {report.name}
                      </div>
                      <div className="flex items-center gap-1.5 px-2 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-xs font-semibold">
                        <Flame className="h-3 w-3 text-emerald-400" />
                        {report.confidenceScore}% Score
                      </div>
                    </div>

                    <p className="text-xs text-slate-400 line-clamp-2 mb-3">
                      {report.creativeOpportunity}
                    </p>

                    <div className="flex items-center justify-between text-xs">
                      <div className="flex items-center gap-2">
                        <span className="text-slate-500">Competition:</span>
                        <span
                          className={`font-semibold ${
                            report.competitionLevel === 'Low'
                              ? 'text-emerald-400'
                              : report.competitionLevel === 'Medium'
                              ? 'text-amber-400'
                              : 'text-rose-400'
                          }`}
                        >
                          {report.competitionLevel}
                        </span>
                      </div>
                      <span className="text-purple-400 group-hover:translate-x-1 transition-transform flex items-center gap-1">
                        Inspect <ArrowRight className="h-3 w-3" />
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Right Column: Detailed Niche Analysis */}
        <div className="lg:col-span-7">
          {selectedReport ? (
            <GlassPanel className="p-6 space-y-6">
              {/* Header */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-white/5">
                <div>
                  <div className="text-xs uppercase font-semibold text-purple-400 tracking-wider">
                    Niche Dossier
                  </div>
                  <h2 className="font-heading text-2xl font-extrabold text-white mt-0.5">
                    {selectedReport.name}
                  </h2>
                </div>
                <Link
                  href={`/studio?niche=${encodeURIComponent(selectedReport.name)}`}
                  className="inline-flex items-center justify-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-medium text-sm shadow-glow transition-all"
                >
                  <Sparkles className="h-4 w-4" />
                  Generate in Studio
                </Link>
              </div>

              {/* Trend Chart */}
              {selectedReport.searchTrends && (
                <div>
                  <h4 className="text-xs uppercase font-semibold text-slate-400 tracking-wider mb-2 flex items-center gap-1.5">
                    <BarChart2 className="h-4 w-4 text-purple-400" />
                    Market Search Velocity Trend
                  </h4>
                  <div className="h-44 w-full rounded-xl bg-[#070B14]/80 p-3 border border-white/5">
                    <ResponsiveContainer width="100%" height="100%">
                      <AreaChart data={selectedReport.searchTrends}>
                        <defs>
                          <linearGradient id="trendGradient" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#A855F7" stopOpacity={0.4} />
                            <stop offset="95%" stopColor="#A855F7" stopOpacity={0} />
                          </linearGradient>
                        </defs>
                        <XAxis dataKey="month" stroke="#64748B" fontSize={11} tickLine={false} />
                        <YAxis stroke="#64748B" fontSize={11} tickLine={false} axisLine={false} />
                        <Tooltip
                          contentStyle={{
                            backgroundColor: '#0F172A',
                            borderColor: 'rgba(255,255,255,0.1)',
                            borderRadius: '0.75rem',
                            color: '#fff',
                            fontSize: '12px',
                          }}
                        />
                        <Area
                          type="monotone"
                          dataKey="volume"
                          stroke="#A855F7"
                          strokeWidth={2}
                          fillOpacity={1}
                          fill="url(#trendGradient)"
                        />
                      </AreaChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              )}

              {/* Target Audience & Creative Opportunity Cards */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="rounded-xl bg-[#0A0F1D] p-4 border border-white/5 space-y-2">
                  <div className="flex items-center gap-2 text-xs font-semibold text-slate-300 uppercase tracking-wider">
                    <Target className="h-4 w-4 text-indigo-400" />
                    Target Audience Demographics
                  </div>
                  <p className="text-sm text-slate-300 leading-relaxed">
                    {selectedReport.targetAudience}
                  </p>
                </div>

                <div className="rounded-xl bg-[#0A0F1D] p-4 border border-white/5 space-y-2">
                  <div className="flex items-center gap-2 text-xs font-semibold text-slate-300 uppercase tracking-wider">
                    <Lightbulb className="h-4 w-4 text-amber-400" />
                    Creative White Space
                  </div>
                  <p className="text-sm text-slate-300 leading-relaxed">
                    {selectedReport.creativeOpportunity}
                  </p>
                </div>
              </div>

              {/* Evidence & Verification Summary */}
              <div className="rounded-xl bg-[#0A0F1D] p-4 border border-white/5 space-y-2">
                <div className="flex items-center gap-2 text-xs font-semibold text-slate-300 uppercase tracking-wider">
                  <CheckCircle2 className="h-4 w-4 text-emerald-400" />
                  Public Market Evidence
                </div>
                <p className="text-sm text-slate-300 leading-relaxed">
                  {selectedReport.evidenceSummary}
                </p>
              </div>

              {/* High-Affinity Tags */}
              {selectedReport.suggestedTags && selectedReport.suggestedTags.length > 0 && (
                <div>
                  <h4 className="text-xs uppercase font-semibold text-slate-400 tracking-wider mb-2">
                    High-Affinity Keyword Tags
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {selectedReport.suggestedTags.map((tag, idx) => (
                      <span
                        key={idx}
                        className="px-2.5 py-1 rounded-lg bg-purple-500/10 border border-purple-500/20 text-purple-300 text-xs font-mono"
                      >
                        #{tag}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </GlassPanel>
          ) : (
            <GlassPanel className="p-12 text-center text-slate-500">
              Select a niche report from the left to inspect detailed intelligence.
            </GlassPanel>
          )}
        </div>
      </div>
    </div>
  );
}
