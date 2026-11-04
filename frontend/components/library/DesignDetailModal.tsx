'use client';

import React, { useState } from 'react';
import Modal from '@/components/ui/Modal';
import Button from '@/components/ui/Button';
import StatusBadge from '@/components/ui/StatusBadge';
import { Design } from '@/lib/types';
import {
  Download,
  Trash2,
  ExternalLink,
  Award,
  Layers,
  Sparkles,
  Search,
  CheckCircle2,
  Calendar,
  Clock,
  HardDrive,
  DollarSign,
} from 'lucide-react';

interface DesignDetailModalProps {
  design: Design | null;
  isOpen: boolean;
  onClose: () => void;
  onDelete: (id: string) => void;
}

export const DesignDetailModal: React.FC<DesignDetailModalProps> = ({
  design,
  isOpen,
  onClose,
  onDelete,
}) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'quality' | 'seo' | 'history'>('overview');
  const [confirmDelete, setConfirmDelete] = useState(false);

  if (!design) return null;

  const handleDelete = () => {
    onDelete(design.id);
    setConfirmDelete(false);
    onClose();
  };

  const handleDownload = () => {
    const link = document.createElement('a');
    link.href = design.imageUrl;
    link.download = `${design.title.toLowerCase().replace(/[^a-z0-9]+/g, '-')}-4500x5400.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} maxWidth="4xl">
      <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
        {/* Left: Artwork Preview */}
        <div className="md:col-span-5 space-y-3">
          <div className="relative aspect-[4/5] w-full overflow-hidden rounded-2xl border border-white/10 bg-slate-950">
            <img
              src={design.imageUrl}
              alt={design.title}
              className="h-full w-full object-cover"
            />
          </div>
          <div className="flex gap-2">
            <Button
              variant="glow"
              size="sm"
              icon={Download}
              className="flex-1"
              onClick={handleDownload}
            >
              Download PNG
            </Button>
            {confirmDelete ? (
              <Button
                variant="danger"
                size="sm"
                onClick={handleDelete}
              >
                Confirm?
              </Button>
            ) : (
              <Button
                variant="ghost"
                size="sm"
                icon={Trash2}
                className="text-rose-400 hover:bg-rose-500/10"
                onClick={() => setConfirmDelete(true)}
              >
                Delete
              </Button>
            )}
          </div>
        </div>

        {/* Right: Tabbed Detail Content */}
        <div className="md:col-span-7 flex flex-col justify-between">
          <div>
            <div className="flex items-start justify-between gap-3">
              <div>
                <h3 className="font-heading text-xl font-bold text-white">
                  {design.title}
                </h3>
                <p className="text-xs text-purple-400 font-medium mt-0.5">
                  {design.niche} • {design.artStyle}
                </p>
              </div>
              <StatusBadge status={design.status} />
            </div>

            {/* Navigation Tabs */}
            <div className="flex items-center gap-2 border-b border-white/10 mt-4 pb-2 text-xs font-semibold">
              <button
                onClick={() => setActiveTab('overview')}
                className={`px-3 py-1.5 rounded-lg transition-all ${
                  activeTab === 'overview'
                    ? 'bg-purple-600/20 text-purple-300 border border-purple-500/30'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                Overview
              </button>
              <button
                onClick={() => setActiveTab('quality')}
                className={`px-3 py-1.5 rounded-lg transition-all ${
                  activeTab === 'quality'
                    ? 'bg-purple-600/20 text-purple-300 border border-purple-500/30'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                Quality QA
              </button>
              <button
                onClick={() => setActiveTab('seo')}
                className={`px-3 py-1.5 rounded-lg transition-all ${
                  activeTab === 'seo'
                    ? 'bg-purple-600/20 text-purple-300 border border-purple-500/30'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                SEO Metadata
              </button>
              <button
                onClick={() => setActiveTab('history')}
                className={`px-3 py-1.5 rounded-lg transition-all ${
                  activeTab === 'history'
                    ? 'bg-purple-600/20 text-purple-300 border border-purple-500/30'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                Version Log
              </button>
            </div>

            {/* Tab: Overview */}
            {activeTab === 'overview' && (
              <div className="mt-4 space-y-4">
                <div>
                  <label className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 block mb-1">
                    Synthesized Prompt
                  </label>
                  <p className="p-3 rounded-xl bg-slate-900/60 border border-white/5 text-xs text-slate-200 leading-relaxed font-mono">
                    {design.prompt}
                  </p>
                </div>

                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                  <div className="p-2.5 rounded-xl bg-white/[0.02] border border-white/5">
                    <span className="text-[10px] text-slate-400 block uppercase">Canvas</span>
                    <span className="text-xs font-bold text-white font-mono">
                      {design.dimensions.width}×{design.dimensions.height}
                    </span>
                  </div>
                  <div className="p-2.5 rounded-xl bg-white/[0.02] border border-white/5">
                    <span className="text-[10px] text-slate-400 block uppercase">File Size</span>
                    <span className="text-xs font-bold text-white font-mono">
                      {(design.fileSizeKb / 1024).toFixed(1)} MB
                    </span>
                  </div>
                  <div className="p-2.5 rounded-xl bg-white/[0.02] border border-white/5">
                    <span className="text-[10px] text-slate-400 block uppercase">Gen Time</span>
                    <span className="text-xs font-bold text-cyan-400 font-mono">
                      {(design.generationTimeMs / 1000).toFixed(1)}s
                    </span>
                  </div>
                  <div className="p-2.5 rounded-xl bg-white/[0.02] border border-white/5">
                    <span className="text-[10px] text-slate-400 block uppercase">Unit Cost</span>
                    <span className="text-xs font-bold text-emerald-400 font-mono">
                      ${design.cost.toFixed(3)}
                    </span>
                  </div>
                </div>

                <div>
                  <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 block mb-1.5">
                    Tags & Taxonomy
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {design.tags.map((t) => (
                      <span
                        key={t}
                        className="px-2.5 py-1 rounded-lg text-xs bg-purple-500/10 border border-purple-500/20 text-purple-300"
                      >
                        #{t}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* Tab: Quality */}
            {activeTab === 'quality' && (
              <div className="mt-4 space-y-4">
                <div className="flex items-center justify-between p-3 rounded-xl bg-purple-950/30 border border-purple-500/20">
                  <div className="flex items-center gap-2">
                    <Award className="h-5 w-5 text-purple-400" />
                    <span className="text-xs font-bold text-white">Overall Vision QA Score</span>
                  </div>
                  <span className="text-base font-extrabold text-emerald-400 font-mono">
                    {design.qualityScore}/100
                  </span>
                </div>

                {design.qualityBreakdown && (
                  <div className="space-y-2.5">
                    {Object.entries(design.qualityBreakdown.dimensions).map(([key, score]) => (
                      <div key={key}>
                        <div className="flex justify-between text-xs font-medium mb-1 capitalize">
                          <span className="text-slate-300">
                            {key.replace(/([A-Z])/g, ' $1')}
                          </span>
                          <span className="text-purple-300 font-mono">{score}/100</span>
                        </div>
                        <div className="h-2 w-full rounded-full bg-slate-900 overflow-hidden">
                          <div
                            className="h-full rounded-full bg-gradient-to-r from-purple-500 to-cyan-400"
                            style={{ width: `${score}%` }}
                          />
                        </div>
                      </div>
                    ))}

                    <div className="pt-2 text-xs text-slate-300 italic border-t border-white/5">
                      "{design.qualityBreakdown.critique}"
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Tab: SEO */}
            {activeTab === 'seo' && (
              <div className="mt-4 space-y-3 text-xs">
                <div>
                  <span className="font-semibold text-slate-400 uppercase block mb-1">
                    Marketplace Title
                  </span>
                  <p className="p-2.5 rounded-xl bg-slate-900 border border-white/5 text-slate-200">
                    {design.seo?.title || `${design.title} Apparel T-Shirt`}
                  </p>
                </div>
                <div>
                  <span className="font-semibold text-slate-400 uppercase block mb-1">
                    Primary Keyword
                  </span>
                  <p className="p-2.5 rounded-xl bg-slate-900 border border-white/5 text-purple-300 font-mono">
                    {design.seo?.primaryKeyword || `${design.niche} shirt`}
                  </p>
                </div>
                <div>
                  <span className="font-semibold text-slate-400 uppercase block mb-1">
                    Search Volume
                  </span>
                  <span className="px-2 py-1 rounded bg-emerald-500/10 text-emerald-400 font-mono">
                    {design.seo?.searchVolumeEstimate || '15.4K / month'}
                  </span>
                </div>
              </div>
            )}

            {/* Tab: History */}
            {activeTab === 'history' && (
              <div className="mt-4 space-y-2 text-xs">
                <div className="p-2.5 rounded-xl bg-slate-900 border border-white/5 flex items-center justify-between">
                  <span className="text-slate-200">v1.0 — Initial Master Generation</span>
                  <span className="text-slate-500 font-mono">Forge Engine</span>
                </div>
                <div className="p-2.5 rounded-xl bg-slate-900 border border-white/5 flex items-center justify-between">
                  <span className="text-slate-200">v1.1 — Vision QA Passed & Certified</span>
                  <span className="text-slate-500 font-mono">Sentinel QA</span>
                </div>
                <div className="p-2.5 rounded-xl bg-slate-900 border border-white/5 flex items-center justify-between">
                  <span className="text-slate-200">v1.2 — Merch SEO Strategy Generated</span>
                  <span className="text-slate-500 font-mono">Apex SEO</span>
                </div>
              </div>
            )}
          </div>

          <div className="mt-6 pt-4 border-t border-white/5 flex justify-end">
            <Button variant="secondary" size="sm" onClick={onClose}>
              Close Window
            </Button>
          </div>
        </div>
      </div>
    </Modal>
  );
};

export default DesignDetailModal;
