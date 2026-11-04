'use client';

import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import {
  DollarSign,
  TrendingDown,
  PieChart as PieIcon,
  Layers,
  CreditCard,
  AlertCircle,
  Clock,
  Shield,
  Download,
  CheckCircle2,
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import GlassPanel from '@/components/ui/GlassPanel';
import StatsCard from '@/components/ui/StatsCard';
import Button from '@/components/ui/Button';
import { api } from '@/lib/api';
import { CostRecord } from '@/lib/types';

const COLORS = ['#A855F7', '#3B82F6', '#10B981', '#F59E0B', '#EC4899'];

export default function CostManagementPage() {
  const { data: costs = [], isLoading } = useQuery({
    queryKey: ['costs-records'],
    queryFn: () => api.analytics.getCosts(),
  });

  const { data: settings } = useQuery({
    queryKey: ['settings-budget'],
    queryFn: () => api.settings.getSettings(),
  });

  const dailyBudgetLimit = settings?.dailyBudgetUsd || 15.0;

  // Aggregate costs
  const totalSpend = costs.reduce((acc, c) => acc + (c.cost || 0), 0);
  const todaySpend = costs
    .filter((c) => {
      const recordDate = new Date(c.timestamp).toDateString();
      const today = new Date().toDateString();
      return recordDate === today;
    })
    .reduce((acc, c) => acc + (c.cost || 0), 0);

  const budgetUsagePercent = Math.min(100, Math.round((todaySpend / dailyBudgetLimit) * 100));

  // Provider breakdown
  const providerSpendMap: Record<string, number> = {};
  costs.forEach((c) => {
    providerSpendMap[c.provider] = (providerSpendMap[c.provider] || 0) + c.cost;
  });

  const providerChartData = Object.entries(providerSpendMap).map(([provider, amount]) => ({
    name: provider,
    value: parseFloat(amount.toFixed(3)),
  }));

  return (
    <div className="space-y-8 pb-12">
      {/* Page Header */}
      <div className="relative overflow-hidden rounded-2xl border border-white/5 bg-gradient-to-r from-purple-950/40 via-slate-900/60 to-blue-950/40 p-6 md:p-8 backdrop-blur-xl">
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-xs font-semibold uppercase tracking-wider mb-2">
              <DollarSign className="h-3.5 w-3.5 text-emerald-400" />
              Financial & API Expense Auditor
            </div>
            <h1 className="font-heading text-2xl md:text-3xl font-extrabold text-white tracking-tight">
              Cost Management & Budget Guardrails
            </h1>
            <p className="text-sm text-slate-300 mt-1 max-w-2xl">
              Transparent, real-time auditing of image synthesis compute and token expenses with strict daily ceiling enforcement.
            </p>
          </div>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatsCard
          title="Total Lifetime Spend"
          value={`$${totalSpend.toFixed(3)}`}
          change="Across all agents"
          trend="neutral"
          icon={<DollarSign className="h-5 w-5 text-purple-400" />}
        />
        <StatsCard
          title="Today's Spend"
          value={`$${todaySpend.toFixed(3)}`}
          change={`${budgetUsagePercent}% of daily limit`}
          trend={budgetUsagePercent > 80 ? 'up' : 'neutral'}
          icon={<CreditCard className="h-5 w-5 text-indigo-400" />}
        />
        <StatsCard
          title="Daily Budget Ceiling"
          value={`$${dailyBudgetLimit.toFixed(2)}`}
          change="Hard safety cutoff"
          trend="neutral"
          icon={<Shield className="h-5 w-5 text-emerald-400" />}
        />
        <StatsCard
          title="Avg Cost Per Render"
          value="$0.040"
          change="Flux 1.1 Pro average"
          trend="down"
          icon={<TrendingDown className="h-5 w-5 text-emerald-400" />}
        />
      </div>

      {/* Budget Guardrail Bar */}
      <GlassPanel className="p-6 space-y-3">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <h3 className="text-sm font-bold text-white">Daily Spending Safety Threshold</h3>
            <p className="text-xs text-slate-400">
              Autonomous jobs halt immediately if daily spend reaches the ${dailyBudgetLimit} ceiling.
            </p>
          </div>
          <div className="text-sm font-bold text-purple-300">
            ${todaySpend.toFixed(3)} / ${dailyBudgetLimit.toFixed(2)} USD ({budgetUsagePercent}%)
          </div>
        </div>
        <div className="h-2.5 w-full bg-white/5 rounded-full overflow-hidden">
          <div
            className={`h-full rounded-full transition-all duration-500 ${
              budgetUsagePercent > 85
                ? 'bg-gradient-to-r from-amber-500 to-rose-500'
                : 'bg-gradient-to-r from-purple-500 to-emerald-400'
            }`}
            style={{ width: `${budgetUsagePercent}%` }}
          />
        </div>
      </GlassPanel>

      {/* Breakdown Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-6">
          <GlassPanel className="p-6 space-y-4">
            <h3 className="text-base font-bold text-white">Expenditure by API Provider</h3>
            <p className="text-xs text-slate-400">Distribution across image engines and LLM reasoning</p>

            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={providerChartData}>
                  <XAxis dataKey="name" stroke="#64748B" fontSize={11} tickLine={false} />
                  <YAxis stroke="#64748B" fontSize={11} tickLine={false} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#0F172A',
                      borderColor: 'rgba(255,255,255,0.1)',
                      borderRadius: '0.75rem',
                      color: '#fff',
                      fontSize: '12px',
                    }}
                    formatter={(val: number) => [`$${val.toFixed(3)}`, 'Spend']}
                  />
                  <Bar dataKey="value" fill="#8B5CF6" radius={[6, 6, 0, 0]}>
                    {providerChartData.map((_, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </GlassPanel>
        </div>

        <div className="lg:col-span-6">
          <GlassPanel className="p-6 space-y-4">
            <h3 className="text-base font-bold text-white">Unit Economics & Efficiency</h3>
            <p className="text-xs text-slate-400">Standardized model rates on TeeDesign AI</p>

            <div className="space-y-3 pt-2">
              <div className="flex items-center justify-between p-3 rounded-xl bg-[#0A0F1D] border border-white/5">
                <div>
                  <div className="text-xs font-semibold text-white">Flux 1.1 Pro (Replicate)</div>
                  <div className="text-[10px] text-slate-400">High precision raster vector illustration</div>
                </div>
                <div className="text-sm font-mono font-bold text-emerald-400">$0.040 / img</div>
              </div>

              <div className="flex items-center justify-between p-3 rounded-xl bg-[#0A0F1D] border border-white/5">
                <div>
                  <div className="text-xs font-semibold text-white">OpenAI DALL-E 3 (HD)</div>
                  <div className="text-[10px] text-slate-400">1024x1024 HD merchandise generation</div>
                </div>
                <div className="text-sm font-mono font-bold text-purple-300">$0.080 / img</div>
              </div>

              <div className="flex items-center justify-between p-3 rounded-xl bg-[#0A0F1D] border border-white/5">
                <div>
                  <div className="text-xs font-semibold text-white">Claude 3.5 Sonnet / GPT-4o</div>
                  <div className="text-[10px] text-slate-400">Prompt synthesis & SEO listing tags</div>
                </div>
                <div className="text-sm font-mono font-bold text-indigo-400">~$0.003 / design</div>
              </div>
            </div>
          </GlassPanel>
        </div>
      </div>

      {/* Real-time Ledger */}
      <GlassPanel className="p-6 space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-base font-bold text-white">Recent API Billing Ledger</h3>
            <p className="text-xs text-slate-400">Itemized chronological transactions</p>
          </div>
          <span className="text-xs text-purple-400 font-mono">Showing {costs.length} records</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="border-b border-white/5 text-slate-400 font-semibold uppercase">
              <tr>
                <th className="py-3 px-4">Timestamp</th>
                <th className="py-3 px-4">Provider / Model</th>
                <th className="py-3 px-4">Service Category</th>
                <th className="py-3 px-4 text-right">Cost (USD)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {costs.map((c) => (
                <tr key={c.id} className="hover:bg-white/[0.02] transition-colors">
                  <td className="py-3 px-4 text-slate-400 font-mono">
                    {new Date(c.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
                  </td>
                  <td className="py-3 px-4 font-medium text-white">{c.provider}</td>
                  <td className="py-3 px-4 text-slate-300">{c.service}</td>
                  <td className="py-3 px-4 text-right font-mono font-bold text-emerald-400">
                    ${c.cost.toFixed(3)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </GlassPanel>
    </div>
  );
}
