'use client';

import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  Search,
  Tag,
  FileText,
  Sparkles,
  Save,
  CheckCircle2,
  Copy,
  ExternalLink,
  Download,
  Flame,
  BarChart,
  RefreshCw,
} from 'lucide-react';
import GlassPanel from '@/components/ui/GlassPanel';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import StatusBadge from '@/components/ui/StatusBadge';
import { api } from '@/lib/api';
import { Listing, SEOData } from '@/lib/types';

export default function SEOManagerPage() {
  const queryClient = useQueryClient();
  const [selectedListingId, setSelectedListingId] = useState<string | null>(null);
  const [copiedField, setCopiedField] = useState<string | null>(null);

  // Form edit states
  const [editTitle, setEditTitle] = useState('');
  const [editDesc, setEditDesc] = useState('');
  const [editKeyword, setEditKeyword] = useState('');
  const [editTags, setEditTags] = useState<string[]>([]);
  const [tagInput, setTagInput] = useState('');

  const { data: listings = [], isLoading, isFetching } = useQuery({
    queryKey: ['seo-listings'],
    queryFn: () => api.seo.getListings(),
  });

  const activeListing = selectedListingId
    ? listings.find((l) => l.id === selectedListingId) || listings[0]
    : listings[0];

  // Initialize edit fields when active listing changes
  React.useEffect(() => {
    if (activeListing?.seo) {
      setEditTitle(activeListing.seo.title);
      setEditDesc(activeListing.seo.description);
      setEditKeyword(activeListing.seo.primaryKeyword);
      setEditTags(activeListing.seo.tags || []);
    }
  }, [activeListing]);

  const updateMutation = useMutation({
    mutationFn: (data: { id: string; payload: Partial<SEOData> }) =>
      api.seo.updateListing(data.id, data.payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['seo-listings'] });
    },
  });

  const handleSave = () => {
    if (!activeListing) return;
    updateMutation.mutate({
      id: activeListing.id,
      payload: {
        title: editTitle,
        description: editDesc,
        primaryKeyword: editKeyword,
        tags: editTags,
      },
    });
  };

  const handleAddTag = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && tagInput.trim()) {
      e.preventDefault();
      if (!editTags.includes(tagInput.trim())) {
        setEditTags([...editTags, tagInput.trim()]);
      }
      setTagInput('');
    }
  };

  const handleRemoveTag = (tagToRemove: string) => {
    setEditTags(editTags.filter((t) => t !== tagToRemove));
  };

  const copyToClipboard = (text: string, fieldName: string) => {
    navigator.clipboard.writeText(text);
    setCopiedField(fieldName);
    setTimeout(() => setCopiedField(null), 2000);
  };

  const exportListingData = () => {
    if (!activeListing) return;
    const exportObj = {
      title: editTitle,
      description: editDesc,
      primaryKeyword: editKeyword,
      tags: editTags,
      category: activeListing.seo.category,
      healthScore: activeListing.seo.healthScore,
      platform: 'TeePublic',
      exportedAt: new Date().toISOString(),
    };
    const blob = new Blob([JSON.stringify(exportObj, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `teepublic_seo_${activeListing.designId}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-8 pb-12">
      {/* Page Header */}
      <div className="relative overflow-hidden rounded-2xl border border-white/5 bg-gradient-to-r from-purple-950/40 via-slate-900/60 to-blue-950/40 p-6 md:p-8 backdrop-blur-xl">
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-300 text-xs font-semibold uppercase tracking-wider mb-2">
              <Search className="h-3.5 w-3.5 text-purple-400" />
              Listing Optimization Agent (Keywordsmith)
            </div>
            <h1 className="font-heading text-2xl md:text-3xl font-extrabold text-white tracking-tight">
              SEO & TeePublic Listing Manager
            </h1>
            <p className="text-sm text-slate-300 mt-1 max-w-2xl">
              Natural keyword enrichment, optimized titles under 60 characters, natural consumer descriptions, and high-velocity tag generation.
            </p>
          </div>
          <div className="flex items-center gap-3">
            <Button
              variant="outline"
              size="sm"
              onClick={exportListingData}
              disabled={!activeListing}
              icon={<Download className="h-4 w-4" />}
            >
              Export JSON Package
            </Button>
          </div>
        </div>
      </div>

      {/* Main Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Listings Directory */}
        <div className="lg:col-span-4 space-y-4">
          <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-400">
            Catalog Listings ({listings.length})
          </h3>

          <div className="space-y-3">
            {isLoading ? (
              [1, 2, 3].map((i) => (
                <div key={i} className="h-24 rounded-xl bg-white/[0.02] border border-white/5 animate-pulse" />
              ))
            ) : (
              listings.map((item) => {
                const isSelected = activeListing?.id === item.id;
                return (
                  <div
                    key={item.id}
                    onClick={() => setSelectedListingId(item.id)}
                    className={`cursor-pointer flex items-center gap-3 p-3 rounded-xl border transition-all ${
                      isSelected
                        ? 'bg-purple-950/20 border-purple-500/40 shadow-glow-sm'
                        : 'bg-[#0B1120]/60 hover:bg-[#0E1628]/80 border-white/5'
                    }`}
                  >
                    <div className="h-14 w-14 rounded-lg overflow-hidden bg-black/40 border border-white/10 shrink-0">
                      <img
                        src={item.designImageUrl}
                        alt={item.designTitle}
                        className="h-full w-full object-cover"
                      />
                    </div>
                    <div className="flex-1 min-w-0">
                      <h4 className="text-sm font-bold text-white truncate">{item.seo.title}</h4>
                      <p className="text-xs text-purple-300 truncate mt-0.5">{item.seo.primaryKeyword}</p>
                      <div className="flex items-center gap-2 mt-1.5">
                        <span className="text-[10px] font-semibold text-emerald-400 bg-emerald-500/10 px-1.5 py-0.5 rounded border border-emerald-500/20">
                          {item.seo.healthScore}% SEO Health
                        </span>
                        <span className="text-[10px] text-slate-400 font-mono">
                          {item.seo.tags.length} tags
                        </span>
                      </div>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>

        {/* Right Column: Active Listing Editor */}
        <div className="lg:col-span-8">
          {activeListing ? (
            <GlassPanel className="p-6 space-y-6">
              {/* Header */}
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-4 border-b border-white/5">
                <div>
                  <span className="text-xs uppercase font-semibold text-purple-400">
                    Listing Editor • TeePublic Standard Format
                  </span>
                  <h2 className="font-heading text-xl font-bold text-white mt-0.5">
                    {activeListing.designTitle}
                  </h2>
                </div>
                <div className="flex items-center gap-2">
                  <Button
                    variant="primary"
                    size="sm"
                    loading={updateMutation.isPending}
                    onClick={handleSave}
                    icon={<Save className="h-4 w-4" />}
                  >
                    Save Changes
                  </Button>
                </div>
              </div>

              {/* Title Field */}
              <div className="space-y-1.5">
                <div className="flex items-center justify-between text-xs">
                  <label className="font-semibold text-slate-300">Product Title (Max 60 Chars)</label>
                  <span className={`font-mono ${editTitle.length > 60 ? 'text-rose-400' : 'text-slate-500'}`}>
                    {editTitle.length}/60
                  </span>
                </div>
                <div className="relative">
                  <input
                    type="text"
                    value={editTitle}
                    onChange={(e) => setEditTitle(e.target.value)}
                    className="w-full px-4 py-2.5 bg-[#0A0F1D] border border-white/10 rounded-xl text-white text-sm focus:outline-none focus:border-purple-500 transition-all"
                  />
                  <button
                    onClick={() => copyToClipboard(editTitle, 'title')}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white"
                    title="Copy Title"
                  >
                    {copiedField === 'title' ? <CheckCircle2 className="h-4 w-4 text-emerald-400" /> : <Copy className="h-4 w-4" />}
                  </button>
                </div>
              </div>

              {/* Primary Keyword Field */}
              <div className="space-y-1.5">
                <label className="text-xs font-semibold text-slate-300">Primary Targeted Keyword</label>
                <div className="relative">
                  <input
                    type="text"
                    value={editKeyword}
                    onChange={(e) => setEditKeyword(e.target.value)}
                    className="w-full px-4 py-2.5 bg-[#0A0F1D] border border-white/10 rounded-xl text-white text-sm focus:outline-none focus:border-purple-500 transition-all"
                  />
                  <button
                    onClick={() => copyToClipboard(editKeyword, 'keyword')}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white"
                    title="Copy Keyword"
                  >
                    {copiedField === 'keyword' ? <CheckCircle2 className="h-4 w-4 text-emerald-400" /> : <Copy className="h-4 w-4" />}
                  </button>
                </div>
              </div>

              {/* Description Field */}
              <div className="space-y-1.5">
                <div className="flex items-center justify-between text-xs">
                  <label className="font-semibold text-slate-300">Natural Product Description</label>
                  <span className="text-slate-500 font-mono">{editDesc.length} chars</span>
                </div>
                <div className="relative">
                  <textarea
                    rows={4}
                    value={editDesc}
                    onChange={(e) => setEditDesc(e.target.value)}
                    className="w-full px-4 py-2.5 bg-[#0A0F1D] border border-white/10 rounded-xl text-white text-sm focus:outline-none focus:border-purple-500 transition-all resize-none"
                  />
                  <button
                    onClick={() => copyToClipboard(editDesc, 'desc')}
                    className="absolute right-3 top-3 text-slate-400 hover:text-white"
                    title="Copy Description"
                  >
                    {copiedField === 'desc' ? <CheckCircle2 className="h-4 w-4 text-emerald-400" /> : <Copy className="h-4 w-4" />}
                  </button>
                </div>
              </div>

              {/* Tags Section */}
              <div className="space-y-3">
                <div className="flex items-center justify-between text-xs">
                  <label className="font-semibold text-slate-300">Optimized Tags (Press Enter to Add)</label>
                  <span className="text-slate-500 font-mono">{editTags.length}/20 tags</span>
                </div>

                <input
                  type="text"
                  value={tagInput}
                  onChange={(e) => setTagInput(e.target.value)}
                  onKeyDown={handleAddTag}
                  placeholder="Type tag name and hit Enter..."
                  className="w-full px-4 py-2 bg-[#0A0F1D] border border-white/10 rounded-xl text-white text-sm focus:outline-none focus:border-purple-500 transition-all"
                />

                <div className="flex flex-wrap gap-2 pt-1">
                  {editTags.map((tag, idx) => (
                    <span
                      key={idx}
                      className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg bg-purple-500/10 border border-purple-500/20 text-purple-300 text-xs font-mono"
                    >
                      #{tag}
                      <button
                        onClick={() => handleRemoveTag(tag)}
                        className="text-purple-400 hover:text-rose-400 text-sm ml-1"
                      >
                        ×
                      </button>
                    </span>
                  ))}
                </div>
              </div>

              {/* SEO Score & Analysis */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2">
                <div className="p-3 rounded-xl bg-[#0A0F1D] border border-white/5">
                  <div className="text-[10px] uppercase font-semibold text-slate-400">Listing Health Score</div>
                  <div className="text-lg font-bold text-emerald-400 mt-0.5">
                    {activeListing.seo.healthScore}%
                  </div>
                </div>
                <div className="p-3 rounded-xl bg-[#0A0F1D] border border-white/5">
                  <div className="text-[10px] uppercase font-semibold text-slate-400">Search Volume Est.</div>
                  <div className="text-lg font-bold text-purple-300 mt-0.5">
                    {activeListing.seo.searchVolumeEstimate || '18.4K / mo'}
                  </div>
                </div>
                <div className="p-3 rounded-xl bg-[#0A0F1D] border border-white/5">
                  <div className="text-[10px] uppercase font-semibold text-slate-400">Platform Target</div>
                  <div className="text-lg font-bold text-white mt-0.5">
                    {activeListing.platform}
                  </div>
                </div>
              </div>
            </GlassPanel>
          ) : (
            <GlassPanel className="p-12 text-center text-slate-500">
              Select a catalog listing to inspect and edit its SEO metadata.
            </GlassPanel>
          )}
        </div>
      </div>
    </div>
  );
}
