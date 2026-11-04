'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard,
  Users,
  Palette,
  TrendingUp,
  Image as ImageIcon,
  Shield,
  Search,
  BarChart3,
  DollarSign,
  Settings,
  ChevronLeft,
  ChevronRight,
  Sparkles,
  LogOut,
  Cpu,
} from 'lucide-react';

const NAV_ITEMS = [
  { name: 'Command Center', href: '/', icon: LayoutDashboard },
  { name: 'AI Workforce', href: '/workforce', icon: Users },
  { name: 'Creative Studio', href: '/studio', icon: Palette },
  { name: 'Market Research', href: '/research', icon: TrendingUp },
  { name: 'Design Library', href: '/library', icon: ImageIcon },
  { name: 'Quality Control', href: '/quality', icon: Shield },
  { name: 'SEO Manager', href: '/seo', icon: Search },
  { name: 'Analytics', href: '/analytics', icon: BarChart3 },
  { name: 'Cost Management', href: '/costs', icon: DollarSign },
  { name: 'Settings', href: '/settings', icon: Settings },
];

export const Sidebar: React.FC = () => {
  const [collapsed, setCollapsed] = useState(false);
  const pathname = usePathname();

  return (
    <aside
      className={`fixed top-0 left-0 bottom-0 z-40 flex flex-col border-r border-white/5 bg-[#070B14]/90 backdrop-blur-2xl transition-all duration-300 ${
        collapsed ? 'w-20' : 'w-64'
      }`}
    >
      {/* Logo & Brand Header */}
      <div className="flex h-16 items-center justify-between px-4 border-b border-white/5">
        {!collapsed && (
          <Link href="/" className="flex items-center gap-2.5 group">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-tr from-brand-purple to-brand-blue shadow-glow-sm group-hover:shadow-glow transition-all">
              <Cpu className="h-5 w-5 text-white" />
            </div>
            <div>
              <span className="font-heading font-extrabold text-base tracking-tight bg-gradient-to-r from-white via-slate-200 to-purple-300 bg-clip-text text-transparent">
                TeeDesign
              </span>
              <span className="ml-1 text-xs font-semibold uppercase px-1.5 py-0.5 rounded-md bg-purple-500/20 text-purple-300 border border-purple-500/30">
                AI
              </span>
            </div>
          </Link>
        )}

        {collapsed && (
          <Link href="/" className="mx-auto flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-tr from-brand-purple to-brand-blue shadow-glow-sm">
            <Cpu className="h-5 w-5 text-white" />
          </Link>
        )}

        <button
          onClick={() => setCollapsed(!collapsed)}
          className={`hidden lg:flex h-7 w-7 items-center justify-center rounded-lg border border-white/5 text-slate-400 hover:text-white hover:bg-white/5 transition-all ${
            collapsed ? 'mx-auto mt-2' : ''
          }`}
          title={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {collapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
        </button>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-1.5">
        {NAV_ITEMS.map((item) => {
          const isActive = pathname === item.href;
          const Icon = item.icon;

          return (
            <Link
              key={item.name}
              href={item.href}
              className={`group flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 relative ${
                isActive
                  ? 'bg-purple-600/15 text-purple-300 border border-purple-500/30 shadow-glow-sm'
                  : 'text-slate-400 hover:text-white hover:bg-white/5'
              } ${collapsed ? 'justify-center' : ''}`}
              title={collapsed ? item.name : undefined}
            >
              {isActive && (
                <div className="absolute left-0 top-1.5 bottom-1.5 w-1 bg-purple-500 rounded-r-full shadow-glow" />
              )}
              <Icon
                className={`h-5 w-5 shrink-0 transition-transform duration-200 group-hover:scale-110 ${
                  isActive ? 'text-purple-400' : 'text-slate-400 group-hover:text-purple-300'
                }`}
              />
              {!collapsed && <span className="truncate">{item.name}</span>}
              {!collapsed && item.name === 'Creative Studio' && (
                <Sparkles className="ml-auto h-3.5 w-3.5 text-amber-400 animate-pulse" />
              )}
            </Link>
          );
        })}
      </nav>

      {/* User Info & Footer */}
      <div className="border-t border-white/5 p-3">
        <div
          className={`flex items-center gap-3 p-2 rounded-xl bg-white/[0.02] border border-white/5 ${
            collapsed ? 'justify-center' : ''
          }`}
        >
          <div className="relative flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-gradient-to-tr from-purple-500 to-indigo-600 text-white font-bold text-xs ring-2 ring-purple-500/30">
            TD
            <span className="absolute bottom-0 right-0 h-2.5 w-2.5 rounded-full bg-emerald-400 ring-2 ring-background-dark" />
          </div>
          {!collapsed && (
            <div className="flex-1 min-w-0">
              <p className="text-xs font-semibold text-white truncate">Studio Director</p>
              <p className="text-[10px] text-slate-400 truncate">Autonomous Hub</p>
            </div>
          )}
          {!collapsed && (
            <button
              onClick={() => {
                if (typeof window !== 'undefined') {
                  localStorage.removeItem('teedesign_token');
                  window.location.reload();
                }
              }}
              title="Sign Out"
              className="p-1.5 text-slate-400 hover:text-rose-400 rounded-lg hover:bg-rose-500/10 transition-colors"
            >
              <LogOut className="h-4 w-4" />
            </button>
          )}
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
