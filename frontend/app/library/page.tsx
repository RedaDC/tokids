'use client';

import React, { useState, useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import {
  Image as ImageIcon,
  Search,
  Filter,
  LayoutGrid,
  List,
  Sparkles,
  Download,
  Trash2,
  RefreshCw,
} from 'lucide-react';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import Select from '@/components/ui/Select';
import StatusBadge from '@/components/ui/StatusBadge';
import DesignCard from '@/components/library/DesignCard';
import DesignDetailModal from '@/components/library/DesignDetailModal';
import { api } from '@/lib/api';
import { Design } from '@/lib/types';

export default function DesignLibraryPage() {
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [styleFilter, setStyleFilter] = useState('all');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [selectedDesign, setSelectedDesign] = useState<Design | null>(null);
  const [visibleCount, setVisibleCount] = useState(6);

  const { data: designs = [], isLoading, refetch, isFetching } = useQuery({
    queryKey: ['designs-library'],
    queryFn: () => api.designs.getDesigns(),
  });

  const [localDesigns, setLocalDesigns] = useState<Design[]>([]);

  React.useEffect(() => {
    if (designs.length > 0) {
      setLocalDesigns(designs);
    }
  }, [designs]);

  // Filtered designs
  const filteredDesigns = useMemo(() => {
    return localDesigns.filter((d) => {
      const matchSearch =
        d.title.toLowerCase().includes(search.toLowerCase()) ||
        d.niche.toLowerCase().includes(search.toLowerCase()) ||
        d.tags.some((t) => t.toLowerCase().includes(search.toLowerCase()));

      const matchStatus = statusFilter === 'all' || d.status === statusFilter;
      const matchStyle = styleFilter === 'all' || d.artStyle === styleFilter;

      return matchSearch && matchStatus && matchStyle;
    });
  }, [localDesigns, search, statusFilter, styleFilter]);

  const handleDelete = (id: string) => {
    setLocalDesigns((prev) => prev.filter((d) => d.id !== id));
    api.designs.deleteDesign(id);
  };

  const handleDownload = (e: React.MouseEvent, design: Design) => {
    e.stopPropagation();
    const link = document.createElement('a');
    link.href = design.imageUrl;
    link.download = `${design.title.toLowerCase().replace(/[^a-z0-9]+/g, '-')}-4500x5400.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="font-heading text-2xl font-bold text-white flex items-center gap-2">
            <ImageIcon className="h-6 w-6 text-purple-400" />
            Master Design Vault
          </h2>
          <p className="text-xs text-slate-400">
            {localDesigns.length} direct-to-garment 4500x5400 vector designs cataloged and reviewed
          </p>
        </div>

        <div className="flex items-center gap-2">
          {/* View toggle */}
          <div className="flex items-center rounded-xl border border-white/10 bg-slate-900/80 p-1">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-1.5 rounded-lg text-xs transition-all ${
                viewMode === 'grid' ? 'bg-purple-600 text-white' : 'text-slate-400 hover:text-white'
              }`}
              title="Grid View"
            >
              <LayoutGrid className="h-4 w-4" />
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`p-1.5 rounded-lg text-xs transition-all ${
                viewMode === 'list' ? 'bg-purple-600 text-white' : 'text-slate-400 hover:text-white'
              }`}
              title="List View"
            >
              <List className="h-4 w-4" />
            </button>
          </div>

          <Button
            variant="secondary"
            size="sm"
            icon={RefreshCw}
            onClick={() => refetch()}
            loading={isFetching}
          >
            Refresh
          </Button>
        </div>
      </div>

      {/* Filter & Search Bar */}
      <div className="grid grid-cols-1 sm:grid-cols-12 gap-3 p-4 rounded-2xl border border-white/5 bg-background-card backdrop-blur-xl">
        <div className="sm:col-span-6">
          <Input
            icon={Search}
            placeholder="Search by title, niche, or keywords..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        <div className="sm:col-span-3">
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="w-full rounded-xl border border-white/10 bg-slate-900/80 px-3 py-2.5 text-xs text-white backdrop-blur-md focus:border-purple-500 focus:outline-none"
          >
            <option value="all">All Approval Statuses</option>
            <option value="approved">Approved Only</option>
            <option value="review">Pending Review</option>
            <option value="rejected">Rejected</option>
          </select>
        </div>

        <div className="sm:col-span-3">
          <select
            value={styleFilter}
            onChange={(e) => setStyleFilter(e.target.value)}
            className="w-full rounded-xl border border-white/10 bg-slate-900/80 px-3 py-2.5 text-xs text-white backdrop-blur-md focus:border-purple-500 focus:outline-none"
          >
            <option value="all">All Visual Styles</option>
            <option value="retro">Retro</option>
            <option value="vintage">Vintage</option>
            <option value="cute">Cute / Kawaii</option>
            <option value="minimalist">Minimalist</option>
            <option value="whimsical">Whimsical</option>
            <option value="gothic">Gothic</option>
          </select>
        </div>
      </div>

      {/* Main Designs View: Grid or List */}
      {viewMode === 'grid' ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3 gap-6">
          {filteredDesigns.slice(0, visibleCount).map((design) => (
            <DesignCard
              key={design.id}
              design={design}
              onClick={() => setSelectedDesign(design)}
              onDelete={(e) => {
                e.stopPropagation();
                handleDelete(design.id);
              }}
              onDownload={(e) => handleDownload(e, design)}
            />
          ))}
        </div>
      ) : (
        <div className="space-y-3">
          {filteredDesigns.slice(0, visibleCount).map((design) => (
            <div
              key={design.id}
              onClick={() => setSelectedDesign(design)}
              className="flex items-center justify-between p-3.5 rounded-xl border border-white/5 bg-background-card hover:border-purple-500/40 hover:bg-slate-900/80 transition-all cursor-pointer backdrop-blur-md"
            >
              <div className="flex items-center gap-3.5 min-w-0">
                <img
                  src={design.thumbnailUrl}
                  alt={design.title}
                  className="h-12 w-12 rounded-lg object-cover"
                />
                <div className="min-w-0">
                  <h4 className="text-sm font-bold text-white truncate">{design.title}</h4>
                  <p className="text-xs text-purple-400">{design.niche} • {design.artStyle}</p>
                </div>
              </div>

              <div className="flex items-center gap-4 shrink-0">
                <StatusBadge status={design.status} />
                <span className="font-mono text-xs text-slate-300">
                  QA: {design.qualityScore}/100
                </span>
                <span className="font-mono text-xs text-emerald-400">
                  ${design.cost.toFixed(3)}
                </span>
                <button
                  onClick={(e) => handleDownload(e, design)}
                  className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-white/5"
                >
                  <Download className="h-4 w-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Pagination Load More */}
      {visibleCount < filteredDesigns.length && (
        <div className="flex justify-center pt-6">
          <Button
            variant="secondary"
            size="md"
            onClick={() => setVisibleCount((prev) => prev + 6)}
          >
            Load More Designs ({filteredDesigns.length - visibleCount} remaining)
          </Button>
        </div>
      )}

      {/* Detail Modal */}
      <DesignDetailModal
        design={selectedDesign}
        isOpen={!!selectedDesign}
        onClose={() => setSelectedDesign(null)}
        onDelete={handleDelete}
      />
    </div>
  );
}
