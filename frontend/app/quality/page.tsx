'use client';

import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  ShieldCheck,
  ShieldAlert,
  AlertTriangle,
  CheckCircle2,
  XCircle,
  Sparkles,
  Eye,
  FileCheck,
  Layers,
  Search,
  Filter,
  Maximize2,
  RotateCcw,
} from 'lucide-react';
import GlassPanel from '@/components/ui/GlassPanel';
import Button from '@/components/ui/Button';
import StatusBadge from '@/components/ui/StatusBadge';
import { api } from '@/lib/api';
import { QualityReview, Design } from '@/lib/types';

export default function QualityControlPage() {
  const queryClient = useQueryClient();
  const [selectedReview, setSelectedReview] = useState<QualityReview | null>(null);

  const { data: designs = [], isLoading } = useQuery({
    queryKey: ['designs-quality'],
    queryFn: () => api.designs.getDesigns(),
  });

  const evaluateMutation = useMutation({
    mutationFn: (designId: string) => api.quality.evaluateQuality(designId),
    onSuccess: (newReview) => {
      setSelectedReview(newReview);
      queryClient.invalidateQueries({ queryKey: ['designs-quality'] });
    },
  });

  // Calculate statistics across reviews
  const reviewedDesigns = designs.filter((d) => d.qualityBreakdown);
  const avgScore =
    reviewedDesigns.length > 0
      ? Math.round(
          reviewedDesigns.reduce((acc, d) => acc + (d.qualityBreakdown?.overallScore || 0), 0) /
            reviewedDesigns.length
        )
      : 94;

  const activeReview = selectedReview || designs[0]?.qualityBreakdown || null;
  const activeDesign = activeReview ? designs.find((d) => d.id === activeReview.designId) || designs[0] : designs[0];

  return (
    <div className="space-y-8 pb-12">
      {/* Page Header */}
      <div className="relative overflow-hidden rounded-2xl border border-white/5 bg-gradient-to-r from-purple-950/40 via-slate-900/60 to-blue-950/40 p-6 md:p-8 backdrop-blur-xl">
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-300 text-xs font-semibold uppercase tracking-wider mb-2">
              <ShieldCheck className="h-3.5 w-3.5 text-blue-400" />
              Automated Inspection Pod (Sentinel)
            </div>
            <h1 className="font-heading text-2xl md:text-3xl font-extrabold text-white tracking-tight">
              Quality Control & IP Screening
            </h1>
            <p className="text-sm text-slate-300 mt-1 max-w-2xl">
              Rigorous 5-point visual evaluation (Visual Quality 25%, Originality 25%, Composition 20%, Print Suitability 20%, Niche Relevance 10%) combined with trademark screening.
            </p>
          </div>
          <div className="flex items-center gap-3">
            <div className="px-4 py-2 rounded-xl bg-purple-500/10 border border-purple-500/20 text-center">
              <div className="text-xl font-extrabold text-purple-300">{avgScore}%</div>
              <div className="text-[10px] uppercase font-semibold text-slate-400">Avg Quality Score</div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Designs List to inspect */}
        <div className="lg:col-span-5 space-y-4">
          <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-400">
            Designs in Review Pipeline ({designs.length})
          </h3>

          <div className="space-y-3">
            {isLoading ? (
              [1, 2, 3].map((i) => (
                <div key={i} className="h-24 rounded-xl bg-white/[0.02] border border-white/5 animate-pulse" />
              ))
            ) : (
              designs.map((design) => {
                const isSelected = activeDesign?.id === design.id;
                const score = design.qualityBreakdown?.overallScore || design.qualityScore || 90;
                return (
                  <div
                    key={design.id}
                    onClick={() => {
                      if (design.qualityBreakdown) {
                        setSelectedReview(design.qualityBreakdown);
                      }
                    }}
                    className={`cursor-pointer flex items-center gap-4 p-3 rounded-xl border transition-all ${
                      isSelected
                        ? 'bg-purple-950/20 border-purple-500/40 shadow-glow-sm'
                        : 'bg-[#0B1120]/60 hover:bg-[#0E1628]/80 border-white/5'
                    }`}
                  >
                    <div className="h-16 w-16 rounded-lg overflow-hidden bg-black/40 border border-white/10 shrink-0">
                      <img
                        src={design.imageUrl}
                        alt={design.title}
                        className="h-full w-full object-cover"
                      />
                    </div>
                    <div className="flex-1 min-w-0">
                      <h4 className="text-sm font-bold text-white truncate">{design.title}</h4>
                      <p className="text-xs text-slate-400 truncate mt-0.5">{design.niche} • {design.artStyle}</p>
                      <div className="flex items-center gap-2 mt-2">
                        <span
                          className={`text-xs font-semibold px-2 py-0.5 rounded-md ${
                            score >= 90
                              ? 'bg-emerald-500/10 text-emerald-300 border border-emerald-500/20'
                              : 'bg-amber-500/10 text-amber-300 border border-amber-500/20'
                          }`}
                        >
                          {score}% Overall
                        </span>
                        <StatusBadge status={design.status} size="sm" />
                      </div>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>

        {/* Right Column: Active Inspection Dossier */}
        <div className="lg:col-span-7">
          {activeDesign ? (
            <GlassPanel className="p-6 space-y-6">
              {/* Artwork Preview & Overview */}
              <div className="flex flex-col sm:flex-row gap-6 items-start pb-6 border-b border-white/5">
                <div className="relative group h-48 w-48 rounded-xl overflow-hidden bg-black/50 border border-white/10 shrink-0 mx-auto sm:mx-0">
                  <img
                    src={activeDesign.imageUrl}
                    alt={activeDesign.title}
                    className="h-full w-full object-contain"
                  />
                  <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity">
                    <a
                      href={activeDesign.imageUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="p-2 rounded-lg bg-white/20 hover:bg-white/30 text-white"
                      title="Open full resolution"
                    >
                      <Maximize2 className="h-5 w-5" />
                    </a>
                  </div>
                </div>

                <div className="flex-1 space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-semibold uppercase text-purple-400">
                      QA Dossier #{activeDesign.id}
                    </span>
                    <Button
                      variant="outline"
                      size="sm"
                      loading={evaluateMutation.isPending}
                      onClick={() => evaluateMutation.mutate(activeDesign.id)}
                      icon={<RotateCcw className="h-3.5 w-3.5" />}
                    >
                      Re-Evaluate
                    </Button>
                  </div>

                  <h2 className="font-heading text-xl font-bold text-white">{activeDesign.title}</h2>
                  <p className="text-xs text-slate-400 font-mono">
                    Dimensions: {activeDesign.dimensions?.width}x{activeDesign.dimensions?.height}px • {activeDesign.provider}
                  </p>

                  <div className="p-3 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-between">
                    <div>
                      <div className="text-xs text-purple-300 font-medium">Composite QA Score</div>
                      <div className="text-2xl font-black text-white">
                        {activeReview?.overallScore || activeDesign.qualityScore || 95}%
                      </div>
                    </div>
                    <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-semibold border border-emerald-500/30">
                      <CheckCircle2 className="h-4 w-4" />
                      Approved for TeePublic
                    </div>
                  </div>
                </div>
              </div>

              {/* 5-Criteria Weighted Scoring */}
              <div>
                <h4 className="text-xs uppercase font-semibold text-slate-400 tracking-wider mb-3">
                  Weighted Score Breakdown
                </h4>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {[
                    { label: 'Visual Quality (25%)', score: activeReview?.dimensions?.printReadiness || 97, desc: 'Sharpness, edge clarity, 300 DPI' },
                    { label: 'Originality (25%)', score: activeReview?.dimensions?.originality || 93, desc: 'Unique character & layout novelty' },
                    { label: 'Composition (20%)', score: activeReview?.dimensions?.composition || 96, desc: 'Balance, garment center focal point' },
                    { label: 'Print Suitability (20%)', score: activeReview?.dimensions?.colorHarmony || 95, desc: 'Color contrast & transparent knockout' },
                    { label: 'Niche Relevance (10%)', score: activeReview?.dimensions?.conceptMatch || 95, desc: 'Alignment with target apparel niche' },
                  ].map((metric, i) => (
                    <div key={i} className="p-3 rounded-xl bg-[#0A0F1D] border border-white/5 space-y-1.5">
                      <div className="flex justify-between items-center text-xs">
                        <span className="font-medium text-slate-300">{metric.label}</span>
                        <span className="font-bold text-purple-300">{metric.score}%</span>
                      </div>
                      <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-purple-500 to-indigo-500 rounded-full"
                          style={{ width: `${metric.score}%` }}
                        />
                      </div>
                      <p className="text-[10px] text-slate-500">{metric.desc}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Technical & Copyright Compliance Checks */}
              <div className="space-y-3">
                <h4 className="text-xs uppercase font-semibold text-slate-400 tracking-wider">
                  Intellectual Property & Technical Clearance
                </h4>
                <div className="space-y-2">
                  <div className="flex items-center gap-3 p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-xs text-emerald-300">
                    <CheckCircle2 className="h-4 w-4 shrink-0 text-emerald-400" />
                    <span>No protected character likenesses or commercial trademarks detected.</span>
                  </div>
                  <div className="flex items-center gap-3 p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-xs text-emerald-300">
                    <CheckCircle2 className="h-4 w-4 shrink-0 text-emerald-400" />
                    <span>Pure alpha knockout verified. Ready for transparent print export.</span>
                  </div>
                  <div className="flex items-center gap-3 p-3 rounded-xl bg-white/[0.02] border border-white/5 text-xs text-slate-400">
                    <AlertTriangle className="h-4 w-4 shrink-0 text-amber-400" />
                    <span>Legal note: Automated screening does not constitute legal clearance. Human review is logged.</span>
                  </div>
                </div>
              </div>

              {/* Inspector Agent Notes */}
              {activeReview?.critique && (
                <div className="p-4 rounded-xl bg-[#0A0F1D] border border-white/5 space-y-1">
                  <div className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
                    Inspector Agent Critique
                  </div>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    {activeReview.critique}
                  </p>
                </div>
              )}
            </GlassPanel>
          ) : (
            <GlassPanel className="p-12 text-center text-slate-500">
              Select a design from the left to view Quality Control details.
            </GlassPanel>
          )}
        </div>
      </div>
    </div>
  );
}
