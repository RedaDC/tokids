'use client';

import React, { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  Settings,
  Key,
  Shield,
  Sliders,
  DollarSign,
  Save,
  CheckCircle2,
  RefreshCw,
  Cpu,
  Layers,
  Database,
  Eye,
  EyeOff,
} from 'lucide-react';
import GlassPanel from '@/components/ui/GlassPanel';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import { api } from '@/lib/api';
import { SystemSettings } from '@/lib/types';

export default function SettingsPage() {
  const queryClient = useQueryClient();
  const [showKeys, setShowKeys] = useState<Record<string, boolean>>({});
  const [saveSuccess, setSaveSuccess] = useState(false);

  // Local state form fields
  const [openaiKey, setOpenaiKey] = useState('');
  const [replicateKey, setReplicateKey] = useState('');
  const [anthropicKey, setAnthropicKey] = useState('');
  const [dailyBudget, setDailyBudget] = useState(15.0);
  const [minQualityScore, setMinQualityScore] = useState(90);
  const [maxRetries, setMaxRetries] = useState(2);
  const [preferredProvider, setPreferredProvider] = useState('replicate');
  const [exportWidth, setExportWidth] = useState(4500);
  const [exportHeight, setExportHeight] = useState(5400);

  const { data: currentSettings, isLoading } = useQuery({
    queryKey: ['system-settings'],
    queryFn: () => api.settings.getSettings(),
  });

  useEffect(() => {
    if (currentSettings) {
      setOpenaiKey(currentSettings.apiKeys?.openai || '');
      setReplicateKey(currentSettings.apiKeys?.replicate || '');
      setAnthropicKey(currentSettings.apiKeys?.anthropic || '');
      setDailyBudget(currentSettings.dailyBudgetUsd || 15.0);
      setMinQualityScore(currentSettings.minQualityScore || 90);
      setMaxRetries(currentSettings.maxRetriesPerDesign || 2);
      setPreferredProvider(currentSettings.preferredImageProvider || 'replicate');
      setExportWidth(currentSettings.defaultDimensions?.width || 4500);
      setExportHeight(currentSettings.defaultDimensions?.height || 5400);
    }
  }, [currentSettings]);

  const updateMutation = useMutation({
    mutationFn: (newSettings: Partial<SystemSettings>) =>
      api.settings.updateSettings(newSettings),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['system-settings'] });
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
    },
  });

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    updateMutation.mutate({
      apiKeys: {
        openai: openaiKey,
        replicate: replicateKey,
        anthropic: anthropicKey,
      },
      dailyBudgetUsd: Number(dailyBudget),
      minQualityScore: Number(minQualityScore),
      maxRetriesPerDesign: Number(maxRetries),
      preferredImageProvider: preferredProvider,
      defaultDimensions: {
        width: Number(exportWidth),
        height: Number(exportHeight),
      },
    });
  };

  const toggleShowKey = (name: string) => {
    setShowKeys((prev) => ({ ...prev, [name]: !prev[name] }));
  };

  return (
    <div className="space-y-8 pb-12">
      {/* Page Header */}
      <div className="relative overflow-hidden rounded-2xl border border-white/5 bg-gradient-to-r from-purple-950/40 via-slate-900/60 to-blue-950/40 p-6 md:p-8 backdrop-blur-xl">
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-300 text-xs font-semibold uppercase tracking-wider mb-2">
              <Sliders className="h-3.5 w-3.5 text-purple-400" />
              Autonomous Studio Configuration
            </div>
            <h1 className="font-heading text-2xl md:text-3xl font-extrabold text-white tracking-tight">
              Settings & Production Policies
            </h1>
            <p className="text-sm text-slate-300 mt-1 max-w-2xl">
              Configure provider credentials, spending thresholds, quality review minimums, and standard apparel export dimensions.
            </p>
          </div>
          {saveSuccess && (
            <div className="flex items-center gap-2 px-4 py-2 rounded-xl bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-sm font-semibold animate-fade-in">
              <CheckCircle2 className="h-4 w-4" />
              Settings Saved Successfully
            </div>
          )}
        </div>
      </div>

      <form onSubmit={handleSave} className="space-y-6">
        {/* API Credentials */}
        <GlassPanel className="p-6 space-y-4">
          <div className="flex items-center gap-2 pb-3 border-b border-white/5">
            <Key className="h-5 w-5 text-purple-400" />
            <h3 className="text-base font-bold text-white">AI Provider API Keys</h3>
          </div>
          <p className="text-xs text-slate-400">
            Keys are encrypted at rest. If left blank, TeeDesign AI operates in transparent mock mode with local synthesis fallback.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-300">Replicate API Key (Flux 1.1 Pro)</label>
              <div className="relative">
                <input
                  type={showKeys['replicate'] ? 'text' : 'password'}
                  value={replicateKey}
                  onChange={(e) => setReplicateKey(e.target.value)}
                  placeholder="r8_..."
                  className="w-full px-4 py-2.5 bg-[#0A0F1D] border border-white/10 rounded-xl text-white text-sm focus:outline-none focus:border-purple-500 font-mono"
                />
                <button
                  type="button"
                  onClick={() => toggleShowKey('replicate')}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white"
                >
                  {showKeys['replicate'] ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-300">OpenAI API Key (DALL-E 3 & GPT-4o)</label>
              <div className="relative">
                <input
                  type={showKeys['openai'] ? 'text' : 'password'}
                  value={openaiKey}
                  onChange={(e) => setOpenaiKey(e.target.value)}
                  placeholder="sk-proj-..."
                  className="w-full px-4 py-2.5 bg-[#0A0F1D] border border-white/10 rounded-xl text-white text-sm focus:outline-none focus:border-purple-500 font-mono"
                />
                <button
                  type="button"
                  onClick={() => toggleShowKey('openai')}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white"
                >
                  {showKeys['openai'] ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
            </div>

            <div className="space-y-1.5 md:col-span-2">
              <label className="text-xs font-semibold text-slate-300">Anthropic API Key (Claude 3.5 Sonnet)</label>
              <div className="relative">
                <input
                  type={showKeys['anthropic'] ? 'text' : 'password'}
                  value={anthropicKey}
                  onChange={(e) => setAnthropicKey(e.target.value)}
                  placeholder="sk-ant-..."
                  className="w-full px-4 py-2.5 bg-[#0A0F1D] border border-white/10 rounded-xl text-white text-sm focus:outline-none focus:border-purple-500 font-mono"
                />
                <button
                  type="button"
                  onClick={() => toggleShowKey('anthropic')}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white"
                >
                  {showKeys['anthropic'] ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
            </div>
          </div>
        </GlassPanel>

        {/* Studio Production Policies */}
        <GlassPanel className="p-6 space-y-4">
          <div className="flex items-center gap-2 pb-3 border-b border-white/5">
            <Shield className="h-5 w-5 text-indigo-400" />
            <h3 className="text-base font-bold text-white">Quality Thresholds & Spending Limits</h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-300">Daily Spending Limit (USD)</label>
              <input
                type="number"
                step="0.5"
                min="1"
                max="500"
                value={dailyBudget}
                onChange={(e) => setDailyBudget(Number(e.target.value))}
                className="w-full px-4 py-2.5 bg-[#0A0F1D] border border-white/10 rounded-xl text-white text-sm focus:outline-none focus:border-purple-500 font-mono"
              />
              <p className="text-[10px] text-slate-500">Autonomous loop halts when this cap is reached</p>
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-300">Minimum Approval Score (0-100)</label>
              <input
                type="number"
                min="50"
                max="99"
                value={minQualityScore}
                onChange={(e) => setMinQualityScore(Number(e.target.value))}
                className="w-full px-4 py-2.5 bg-[#0A0F1D] border border-white/10 rounded-xl text-white text-sm focus:outline-none focus:border-purple-500 font-mono"
              />
              <p className="text-[10px] text-slate-500">Artwork scoring below this triggers revision or discard</p>
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-300">Max Revisions Per Concept</label>
              <input
                type="number"
                min="1"
                max="5"
                value={maxRetries}
                onChange={(e) => setMaxRetries(Number(e.target.value))}
                className="w-full px-4 py-2.5 bg-[#0A0F1D] border border-white/10 rounded-xl text-white text-sm focus:outline-none focus:border-purple-500 font-mono"
              />
              <p className="text-[10px] text-slate-500">Prevents runaway generative retry loops</p>
            </div>
          </div>
        </GlassPanel>

        {/* Canvas & Canvas Resolution */}
        <GlassPanel className="p-6 space-y-4">
          <div className="flex items-center gap-2 pb-3 border-b border-white/5">
            <Cpu className="h-5 w-5 text-emerald-400" />
            <h3 className="text-base font-bold text-white">Default Export Format (TeePublic)</h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-300">Preferred Primary Provider</label>
              <select
                value={preferredProvider}
                onChange={(e) => setPreferredProvider(e.target.value)}
                className="w-full px-4 py-2.5 bg-[#0A0F1D] border border-white/10 rounded-xl text-white text-sm focus:outline-none focus:border-purple-500"
              >
                <option value="replicate">Flux 1.1 Pro (Replicate)</option>
                <option value="openai">OpenAI DALL-E 3</option>
                <option value="stub">Stub Provider (Zero Cost Local)</option>
              </select>
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-300">Export Canvas Width (px)</label>
              <input
                type="number"
                value={exportWidth}
                onChange={(e) => setExportWidth(Number(e.target.value))}
                className="w-full px-4 py-2.5 bg-[#0A0F1D] border border-white/10 rounded-xl text-white text-sm focus:outline-none focus:border-purple-500 font-mono"
              />
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-300">Export Canvas Height (px)</label>
              <input
                type="number"
                value={exportHeight}
                onChange={(e) => setExportHeight(Number(e.target.value))}
                className="w-full px-4 py-2.5 bg-[#0A0F1D] border border-white/10 rounded-xl text-white text-sm focus:outline-none focus:border-purple-500 font-mono"
              />
            </div>
          </div>
        </GlassPanel>

        {/* Submit Bar */}
        <div className="flex justify-end pt-2">
          <Button
            type="submit"
            variant="primary"
            size="lg"
            loading={updateMutation.isPending}
            icon={<Save className="h-4 w-4" />}
          >
            Save All Configurations
          </Button>
        </div>
      </form>
    </div>
  );
}
