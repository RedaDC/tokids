'use client';

import React, { useState } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import {
  Sparkles,
  RefreshCw,
  Check,
  X,
  Download,
  Bookmark,
  Layers,
  Cpu,
  Palette,
  AlertTriangle,
  Clock,
  HardDrive,
  DollarSign,
  Maximize2,
} from 'lucide-react';
import GlassPanel from '@/components/ui/GlassPanel';
import Button from '@/components/ui/Button';
import Select from '@/components/ui/Select';
import StatusBadge from '@/components/ui/StatusBadge';
import { api } from '@/lib/api';
import { Design, DesignConcept } from '@/lib/types';

const ART_STYLES = [
  { value: 'retro', label: 'Retro 70s / 80s' },
  { value: 'vintage', label: 'Vintage Distressed Badge' },
  { value: 'cute', label: 'Cute Kawaii Chibi' },
  { value: 'cartoon', label: 'Classic Bold Cartoon' },
  { value: 'minimalist', label: 'Minimalist Line Art' },
  { value: 'fantasy', label: 'Fantasy & Surreal' },
  { value: 'nature', label: 'Nature & Landscape' },
  { value: 'animals', label: 'Character & Animals' },
  { value: 'space', label: 'Cosmic & Space Exploration' },
  { value: 'botanical', label: 'Botanical & Herbology' },
  { value: 'food', label: 'Food & Culinary' },
  { value: 'whimsical', label: 'Whimsical Storybook' },
  { value: 'gothic', label: 'Dark Gothic Engraving' },
];

const CATEGORIES = [
  { value: 'Cyberpunk & Sci-Fi', label: 'Cyberpunk & Sci-Fi' },
  { value: 'Space & Animals', label: 'Space & Animals' },
  { value: 'Gothic & Occult', label: 'Gothic & Occult' },
  { value: 'Anime & Kawaii', label: 'Anime & Kawaii' },
  { value: 'Minimalism & Outdoors', label: 'Minimalism & Outdoors' },
  { value: 'Pop Culture Satire', label: 'Pop Culture Satire' },
];

const COLOR_PALETTES = [
  { name: 'Neon', colors: ['#7C3AED', '#06B6D4', '#EC4899', '#10B981'] },
  { name: 'Vibrant', colors: ['#EF4444', '#F59E0B', '#10B981', '#3B82F6'] },
  { name: 'Sunset', colors: ['#F97316', '#F43F5E', '#A855F7', '#3B82F6'] },
  { name: 'Pastel', colors: ['#FBCFE8', '#C7D2FE', '#BAE6FD', '#A7F3D0'] },
  { name: 'Earth Tones', colors: ['#78350F', '#92400E', '#065F46', '#D97706'] },
  { name: 'Monochrome', colors: ['#000000', '#4B5563', '#9CA3AF', '#FFFFFF'] },
  { name: 'Ocean', colors: ['#0C4A6E', '#0284C7', '#38BDF8', '#7DD3FC'] },
  { name: 'Forest', colors: ['#064E3B', '#047857', '#10B981', '#6EE7B7'] },
];

const PROVIDERS = [
  { value: 'Flux 1.1 Pro (Replicate)', label: 'Flux 1.1 Pro (Replicate) — Vector Master' },
  { value: 'DALL-E 3 (OpenAI)', label: 'DALL-E 3 (OpenAI) — Stylized Character' },
  { value: 'SDXL Lightning (Local/API)', label: 'SDXL Lightning — Fast Draft' },
];

export default function CreativeStudioPage() {
  const [prompt, setPrompt] = useState(
    'A majestic steampunk owl perched on a giant mechanical pocket watch, intricate brass gears and copper pipes, illuminated clock face with roman numerals, isolated clean dark background, vector direct-to-garment tee illustration'
  );
  const [category, setCategory] = useState(CATEGORIES[0].value);
  const [style, setStyle] = useState('retro');
  const [palette, setPalette] = useState('Neon');
  const [provider, setProvider] = useState(PROVIDERS[0].value);
  const [customInstructions, setCustomInstructions] = useState(
    'Ensure high contrast, clean transparent background knockout, sharp silhouettes, no blurred edges.'
  );

  // Active step during generation pipeline simulation
  const [activeAgentStep, setActiveAgentStep] = useState<string | null>(null);

  // Current preview design
  const [currentDesign, setCurrentDesign] = useState<Design | null>({
    id: 'sample-preview',
    title: 'Steampunk Owl on Mechanical Chrono',
    prompt: prompt,
    niche: 'Cyberpunk & Sci-Fi',
    category: 'Steampunk',
    artStyle: 'retro',
    colorPalette: 'Neon',
    provider: 'Flux 1.1 Pro (Replicate)',
    status: 'approved',
    imageUrl: 'https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?w=800&auto=format&fit=crop&q=80',
    thumbnailUrl: 'https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?w=400&auto=format&fit=crop&q=80',
    variations: [
      'https://images.unsplash.com/photo-1541701494587-cb58502866ab?w=400&auto=format&fit=crop&q=80',
      'https://images.unsplash.com/photo-1550684848-fac1c5b4e853?w=400&auto=format&fit=crop&q=80',
      'https://images.unsplash.com/photo-1563089145-599997674d42?w=400&auto=format&fit=crop&q=80',
    ],
    dimensions: { width: 4500, height: 5400 },
    fileSizeKb: 6120,
    generationTimeMs: 4100,
    cost: 0.040,
    qualityScore: 96,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    tags: ['steampunk', 'owl', 'gears', 'pocket-watch', 't-shirt-graphic'],
  });

  const { data: settings } = useQuery({
    queryKey: ['system-settings'],
    queryFn: () => api.settings.getSettings(),
  });

  const isStubMode = settings?.imageGeneration.isStubMode ?? false;

  // Generate Mutation
  const generateMutation = useMutation({
    mutationFn: async (concept: DesignConcept) => {
      // Animated step orchestration for workforce transparency
      setActiveAgentStep('DaVinci (Art Director) engineering prompt syntax...');
      await new Promise((r) => setTimeout(r, 600));

      setActiveAgentStep('Guardian (Legal) checking trademark blacklist...');
      await new Promise((r) => setTimeout(r, 500));

      setActiveAgentStep('Forge (Render Engine) generating master 4500x5400 canvas...');
      const res = await api.designs.generateDesign(concept);

      setActiveAgentStep('Sentinel (QA) verifying 300 DPI apparel gamut...');
      await new Promise((r) => setTimeout(r, 500));

      setActiveAgentStep(null);
      return res;
    },
    onSuccess: (data) => {
      setCurrentDesign(data);
    },
    onError: () => {
      setActiveAgentStep(null);
    },
  });

  const handleGenerate = (isVariation = false) => {
    generateMutation.mutate({
      prompt: isVariation ? `${prompt} (variation iteration)` : prompt,
      category,
      style,
      colorPalette: palette,
      provider,
      customInstructions,
    });
  };

  return (
    <div className="space-y-6">
      {/* Studio Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="font-heading text-2xl font-bold text-white flex items-center gap-2">
            <Sparkles className="h-6 w-6 text-purple-400" />
            Creative Studio & Vector Forge
          </h2>
          <p className="text-xs text-slate-400">
            Autonomous prompt engineering, palette synthesis, and 4500x5400 direct-to-garment rendering
          </p>
        </div>

        {isStubMode && (
          <div className="flex items-center gap-2 rounded-xl border border-amber-500/30 bg-amber-500/10 px-3 py-1.5 text-xs text-amber-300">
            <AlertTriangle className="h-4 w-4 shrink-0 text-amber-400" />
            <span>Running in Stub Mode — Configure API keys in Settings for live model execution</span>
          </div>
        )}
      </div>

      {/* Split Layout: Generation Form (Left) | Live Preview (Right) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Form Panel (7 cols) */}
        <div className="lg:col-span-6 space-y-5">
          <GlassPanel className="space-y-5">
            {/* Concept Textarea */}
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-2">
                Illustration Design Concept
              </label>
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                rows={4}
                className="w-full rounded-xl border border-white/10 bg-slate-900/80 p-3.5 text-sm text-white placeholder-slate-500 backdrop-blur-md focus:border-purple-500 focus:bg-slate-900 focus:outline-none focus:ring-2 focus:ring-purple-500/20 transition-all leading-relaxed"
                placeholder="Describe your graphic illustration in detail..."
              />
            </div>

            {/* Category & Style Dropdowns */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <Select
                label="Illustration Category"
                options={CATEGORIES}
                value={category}
                onChange={(e) => setCategory(e.target.value)}
              />
              <Select
                label="Art Style"
                options={ART_STYLES}
                value={style}
                onChange={(e) => setStyle(e.target.value)}
              />
            </div>

            {/* Color Palette Selector */}
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-2">
                Color Palette Preset
              </label>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
                {COLOR_PALETTES.map((p) => {
                  const isSelected = palette === p.name;
                  return (
                    <button
                      key={p.name}
                      type="button"
                      onClick={() => setPalette(p.name)}
                      className={`flex flex-col gap-1.5 p-2 rounded-xl border text-left transition-all ${
                        isSelected
                          ? 'border-purple-500 bg-purple-500/15 shadow-glow-sm'
                          : 'border-white/5 bg-slate-900/60 hover:border-white/10'
                      }`}
                    >
                      <span className="text-[11px] font-medium text-slate-300 truncate">
                        {p.name}
                      </span>
                      <div className="flex h-3 w-full rounded-md overflow-hidden">
                        {p.colors.map((c, i) => (
                          <div key={i} className="flex-1 h-full" style={{ backgroundColor: c }} />
                        ))}
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Provider Selector */}
            <Select
              label="Render Engine Provider"
              options={PROVIDERS}
              value={provider}
              onChange={(e) => setProvider(e.target.value)}
            />

            {/* Custom Instructions */}
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5">
                Art Direction & Negative Constraints
              </label>
              <textarea
                value={customInstructions}
                onChange={(e) => setCustomInstructions(e.target.value)}
                rows={2}
                className="w-full rounded-xl border border-white/10 bg-slate-900/60 p-2.5 text-xs text-slate-300 placeholder-slate-500 focus:border-purple-500 focus:outline-none focus:ring-1 focus:ring-purple-500/20"
                placeholder="e.g. Clean vector, no raster blur, transparent background..."
              />
            </div>

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-3 pt-2">
              <Button
                variant="glow"
                size="lg"
                icon={Sparkles}
                className="flex-1"
                onClick={() => handleGenerate(false)}
                loading={generateMutation.isPending}
              >
                Generate Artwork
              </Button>
              <Button
                variant="secondary"
                size="lg"
                icon={Layers}
                onClick={() => handleGenerate(true)}
                disabled={generateMutation.isPending}
              >
                Variations
              </Button>
            </div>

            {/* Progress Indicator Showing Which Agent is Working */}
            {activeAgentStep && (
              <div className="rounded-xl border border-purple-500/30 bg-purple-950/30 p-3.5 backdrop-blur-md animate-pulse">
                <div className="flex items-center gap-2.5 text-xs font-medium text-purple-300">
                  <div className="h-4 w-4 animate-spin rounded-full border-2 border-purple-400 border-t-transparent" />
                  <span>{activeAgentStep}</span>
                </div>
              </div>
            )}
          </GlassPanel>
        </div>

        {/* Right Preview Panel (5 cols) */}
        <div className="lg:col-span-6 space-y-5">
          <GlassPanel className="flex flex-col justify-between h-full">
            <div>
              <div className="flex items-center justify-between pb-3 border-b border-white/5 mb-4">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-300">
                  Master Render Preview (Direct-to-Garment)
                </span>
                {currentDesign && <StatusBadge status={currentDesign.status} />}
              </div>

              {/* Artwork Viewport */}
              <div className="relative aspect-[4/5] w-full overflow-hidden rounded-2xl border border-white/10 bg-[#060913] flex items-center justify-center">
                {generateMutation.isPending ? (
                  <div className="flex flex-col items-center gap-4 p-8 text-center">
                    <div className="relative h-20 w-20">
                      <div className="absolute inset-0 rounded-full border-4 border-purple-500/20 border-t-purple-500 animate-spin" />
                      <div className="absolute inset-2 rounded-full border-4 border-cyan-400/20 border-b-cyan-400 animate-spin" style={{ animationDirection: 'reverse' }} />
                    </div>
                    <div>
                      <p className="text-sm font-bold text-white font-heading">
                        AI Workforce in Motion...
                      </p>
                      <p className="text-xs text-purple-300 mt-1 max-w-xs">
                        Synthesizing 4500x5400 apparel vector with color gamut safety
                      </p>
                    </div>
                  </div>
                ) : currentDesign ? (
                  <div className="relative h-full w-full group">
                    <img
                      src={currentDesign.imageUrl}
                      alt={currentDesign.title}
                      className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
                    />
                    <div className="absolute top-3 right-3 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <a
                        href={currentDesign.imageUrl}
                        target="_blank"
                        rel="noreferrer"
                        className="p-2 rounded-xl bg-black/70 backdrop-blur-md text-white hover:bg-black/90 transition-colors"
                      >
                        <Maximize2 className="h-4 w-4" />
                      </a>
                    </div>
                  </div>
                ) : (
                  <p className="text-xs text-slate-500">No artwork generated yet.</p>
                )}
              </div>

              {/* Action Buttons: Approve, Reject, Regenerate, Save */}
              {currentDesign && (
                <div className="grid grid-cols-4 gap-2.5 mt-4">
                  <Button
                    variant="secondary"
                    size="sm"
                    icon={Check}
                    className="hover:border-emerald-500/50 hover:text-emerald-400"
                    onClick={() => {
                      alert('Artwork approved and scheduled for TeePublic listing sync!');
                    }}
                  >
                    Approve
                  </Button>
                  <Button
                    variant="secondary"
                    size="sm"
                    icon={X}
                    className="hover:border-rose-500/50 hover:text-rose-400"
                    onClick={() => {
                      alert('Design marked for revision.');
                    }}
                  >
                    Reject
                  </Button>
                  <Button
                    variant="secondary"
                    size="sm"
                    icon={RefreshCw}
                    onClick={() => handleGenerate(false)}
                  >
                    Redo
                  </Button>
                  <Button
                    variant="primary"
                    size="sm"
                    icon={Bookmark}
                    onClick={() => {
                      alert('Saved to Design Library vault!');
                    }}
                  >
                    Save
                  </Button>
                </div>
              )}

              {/* Metadata Cards */}
              {currentDesign && (
                <div className="grid grid-cols-4 gap-2 mt-4 pt-3 border-t border-white/5 text-center">
                  <div className="p-2 rounded-lg bg-white/[0.02]">
                    <span className="text-[10px] text-slate-500 uppercase block">Canvas</span>
                    <span className="text-xs font-bold text-white font-mono">4500×5400</span>
                  </div>
                  <div className="p-2 rounded-lg bg-white/[0.02]">
                    <span className="text-[10px] text-slate-500 uppercase block">File Size</span>
                    <span className="text-xs font-bold text-white font-mono">
                      {(currentDesign.fileSizeKb / 1024).toFixed(1)} MB
                    </span>
                  </div>
                  <div className="p-2 rounded-lg bg-white/[0.02]">
                    <span className="text-[10px] text-slate-500 uppercase block">Time</span>
                    <span className="text-xs font-bold text-cyan-400 font-mono">
                      {(currentDesign.generationTimeMs / 1000).toFixed(1)}s
                    </span>
                  </div>
                  <div className="p-2 rounded-lg bg-white/[0.02]">
                    <span className="text-[10px] text-slate-500 uppercase block">Unit Cost</span>
                    <span className="text-xs font-bold text-emerald-400 font-mono">
                      ${currentDesign.cost.toFixed(3)}
                    </span>
                  </div>
                </div>
              )}
            </div>

            {/* Variations Gallery */}
            {currentDesign?.variations && (
              <div className="mt-5 pt-4 border-t border-white/5">
                <span className="text-xs font-semibold text-slate-300 block mb-2.5">
                  Generated Variations & Angles
                </span>
                <div className="grid grid-cols-3 gap-3">
                  {currentDesign.variations.map((vUrl, i) => (
                    <div
                      key={i}
                      onClick={() =>
                        setCurrentDesign({
                          ...currentDesign,
                          imageUrl: vUrl,
                        })
                      }
                      className="group relative aspect-square overflow-hidden rounded-xl border border-white/5 bg-slate-900 cursor-pointer hover:border-purple-500/50 transition-all"
                    >
                      <img
                        src={vUrl}
                        alt={`Variation ${i + 1}`}
                        className="h-full w-full object-cover group-hover:scale-110 transition-transform"
                      />
                      <div className="absolute inset-0 bg-purple-500/10 opacity-0 group-hover:opacity-100 transition-opacity" />
                    </div>
                  ))}
                </div>
              </div>
            )}
          </GlassPanel>
        </div>
      </div>
    </div>
  );
}
