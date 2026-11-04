'use client';

import React from 'react';
import { Design } from '@/lib/types';
import StatusBadge from '@/components/ui/StatusBadge';
import { Eye, Download, Trash2, Award } from 'lucide-react';

interface DesignCardProps {
  design: Design;
  onClick: () => void;
  onDelete: (e: React.MouseEvent) => void;
  onDownload: (e: React.MouseEvent) => void;
}

export const DesignCard: React.FC<DesignCardProps> = ({
  design,
  onClick,
  onDelete,
  onDownload,
}) => {
  return (
    <div
      onClick={onClick}
      className="group relative cursor-pointer overflow-hidden rounded-2xl border border-white/5 bg-background-card backdrop-blur-xl transition-all duration-300 hover:border-purple-500/40 hover:shadow-glass hover:-translate-y-1.5"
    >
      {/* Thumbnail Aspect Box */}
      <div className="relative aspect-[4/5] w-full overflow-hidden bg-slate-950">
        <img
          src={design.thumbnailUrl || design.imageUrl}
          alt={design.title}
          className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
        />

        {/* Top Badges Overlay */}
        <div className="absolute top-3 left-3 right-3 flex items-center justify-between pointer-events-none">
          <StatusBadge status={design.status} />

          {/* Quality Score Badge */}
          <div className="flex items-center gap-1 rounded-full border border-purple-500/30 bg-purple-950/80 px-2.5 py-1 text-xs font-bold text-purple-300 backdrop-blur-md">
            <Award className="h-3 w-3 text-purple-400" />
            <span>{design.qualityScore}</span>
          </div>
        </div>

        {/* Hover Action Overlay */}
        <div className="absolute inset-0 flex items-center justify-center gap-3 bg-black/60 opacity-0 backdrop-blur-sm transition-opacity duration-300 group-hover:opacity-100">
          <button
            onClick={(e) => {
              e.stopPropagation();
              onClick();
            }}
            className="flex h-10 w-10 items-center justify-center rounded-xl bg-purple-600 text-white shadow-glow hover:bg-purple-500 transition-transform active:scale-95"
            title="Preview & Details"
          >
            <Eye className="h-5 w-5" />
          </button>
          <button
            onClick={onDownload}
            className="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-800 text-slate-200 hover:bg-slate-700 hover:text-white transition-transform active:scale-95"
            title="Download PNG"
          >
            <Download className="h-5 w-5" />
          </button>
          <button
            onClick={onDelete}
            className="flex h-10 w-10 items-center justify-center rounded-xl bg-rose-500/20 border border-rose-500/30 text-rose-300 hover:bg-rose-500/30 transition-transform active:scale-95"
            title="Delete Artwork"
          >
            <Trash2 className="h-5 w-5" />
          </button>
        </div>
      </div>

      {/* Info Footer */}
      <div className="p-4">
        <h4 className="font-heading text-sm font-bold text-white truncate group-hover:text-purple-300 transition-colors">
          {design.title}
        </h4>
        <div className="mt-2 flex items-center justify-between text-xs text-slate-400">
          <span className="truncate max-w-[140px] text-purple-400 font-medium">
            {design.niche}
          </span>
          <span className="font-mono text-[11px]">${design.cost.toFixed(3)}</span>
        </div>
      </div>
    </div>
  );
};

export default DesignCard;
