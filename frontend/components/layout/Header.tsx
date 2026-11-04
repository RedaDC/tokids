'use client';

import React, { useState } from 'react';
import { usePathname } from 'next/navigation';
import {
  Bell,
  Search,
  CheckCircle2,
  AlertTriangle,
  Sparkles,
  Command,
  ExternalLink,
} from 'lucide-react';

const PAGE_TITLES: Record<string, { title: string; subtitle: string }> = {
  '/': { title: 'Command Center', subtitle: 'Autonomous illustration operations & system vitals' },
  '/workforce': { title: 'AI Workforce', subtitle: 'Live agent pods, 3D command studio & task distribution' },
  '/studio': { title: 'Creative Studio', subtitle: 'Autonomous vector & raster apparel generation' },
  '/research': { title: 'Market Research', subtitle: 'Marketplace niche intelligence, trend spikes & tags' },
  '/library': { title: 'Design Library', subtitle: 'Master vector print assets, variations & review status' },
  '/quality': { title: 'Quality Control', subtitle: 'Computer-vision QA, print-readiness & compliance' },
  '/seo': { title: 'SEO Manager', subtitle: 'Algorithmic titles, high-conversion tags & marketplace sync' },
  '/analytics': { title: 'Analytics & Trends', subtitle: 'Unit economics, generation volume & quality trends' },
  '/costs': { title: 'Cost Management', subtitle: 'Token spend rates, API budget limits & unit burn rate' },
  '/settings': { title: 'System Settings', subtitle: 'Model providers, API credentials & threshold tuning' },
};

export const Header: React.FC = () => {
  const pathname = usePathname();
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const currentMeta = PAGE_TITLES[pathname] || {
    title: 'TeeDesign AI',
    subtitle: 'Autonomous Apparel Illustration Engine',
  };

  const sampleNotifications = [
    {
      id: '1',
      title: 'Batch Auto-Approved',
      time: '2m ago',
      desc: 'Cyberpunk Neon Bonsai passed 96/100 QA score.',
      icon: CheckCircle2,
      color: 'text-emerald-400',
    },
    {
      id: '2',
      title: 'Trending Niche Alert',
      time: '18m ago',
      desc: 'Japanese Retro Synthwave surged +48% on TeePublic.',
      icon: Sparkles,
      color: 'text-purple-400',
    },
    {
      id: '3',
      title: 'Model Swapped',
      time: '1h ago',
      desc: 'Forge switched to Flux 1.1 Pro for ultra-sharp vectors.',
      icon: AlertTriangle,
      color: 'text-amber-400',
    },
  ];

  return (
    <header className="sticky top-0 z-30 flex h-16 w-full items-center justify-between border-b border-white/5 bg-[#0A0E1A]/80 px-6 backdrop-blur-xl">
      {/* Dynamic Title */}
      <div>
        <h1 className="font-heading text-lg font-bold text-white tracking-tight">
          {currentMeta.title}
        </h1>
        <p className="hidden md:block text-xs text-slate-400">
          {currentMeta.subtitle}
        </p>
      </div>

      {/* Global Search & Actions */}
      <div className="flex items-center gap-4">
        {/* Global Search Bar */}
        <div className="relative hidden md:block w-72">
          <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3 text-slate-400">
            <Search className="h-4 w-4" />
          </div>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search designs, niches, agents..."
            className="w-full rounded-xl border border-white/5 bg-slate-900/60 pl-9 pr-8 py-1.5 text-xs text-white placeholder-slate-500 backdrop-blur-md focus:border-purple-500 focus:bg-slate-900 focus:outline-none focus:ring-1 focus:ring-purple-500/30 transition-all"
          />
          <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2.5">
            <kbd className="rounded border border-white/10 bg-white/5 px-1.5 py-0.5 text-[10px] font-mono text-slate-400">
              ⌘K
            </kbd>
          </div>
        </div>

        {/* System Status Indicator */}
        <div className="flex items-center gap-2 rounded-full border border-emerald-500/20 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-400">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-400" />
          </span>
          <span className="hidden sm:inline">Systems Operational</span>
        </div>

        {/* Notifications Popover */}
        <div className="relative">
          <button
            onClick={() => setNotificationsOpen(!notificationsOpen)}
            className="relative flex h-9 w-9 items-center justify-center rounded-xl border border-white/5 text-slate-300 hover:border-purple-500/30 hover:bg-white/5 hover:text-white transition-all"
          >
            <Bell className="h-4 w-4" />
            <span className="absolute top-1.5 right-1.5 h-2 w-2 rounded-full bg-purple-500 ring-2 ring-background" />
          </button>

          {notificationsOpen && (
            <div className="absolute right-0 mt-2 w-80 rounded-2xl border border-white/10 bg-slate-950/95 p-4 shadow-2xl shadow-purple-500/10 backdrop-blur-2xl z-50 animate-fade-in">
              <div className="flex items-center justify-between pb-3 border-b border-white/5">
                <span className="text-xs font-semibold text-white uppercase tracking-wider">
                  Live Notifications
                </span>
                <span className="text-[10px] text-purple-400 cursor-pointer hover:underline">
                  Mark all read
                </span>
              </div>
              <div className="mt-3 space-y-2.5">
                {sampleNotifications.map((n) => {
                  const NIcon = n.icon;
                  return (
                    <div
                      key={n.id}
                      className="flex gap-3 rounded-xl p-2.5 hover:bg-white/5 transition-colors cursor-pointer"
                    >
                      <NIcon className={`h-4 w-4 shrink-0 mt-0.5 ${n.color}`} />
                      <div className="min-w-0 flex-1">
                        <div className="flex items-center justify-between">
                          <p className="text-xs font-medium text-white">{n.title}</p>
                          <span className="text-[10px] text-slate-500">{n.time}</span>
                        </div>
                        <p className="text-[11px] text-slate-400 mt-0.5 line-clamp-2">
                          {n.desc}
                        </p>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;
