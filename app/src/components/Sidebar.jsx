import React from 'react';
import { Building2, Map, BarChart3, Filter, Settings } from 'lucide-react';

const Sidebar = ({ filters, setFilters, counties = [], currentView, onNavigate }) => {
    return (
        <div className="w-64 bg-white border-r border-slate-200 h-screen flex flex-col shadow-sm z-20">
            <div className="p-6 border-b border-slate-100">
                <div className="flex items-center gap-2 text-brand-700 font-bold text-xl">
                    <Building2 className="w-6 h-6" />
                    <span>FL Multifamily</span>
                </div>
                <p className="text-xs text-slate-500 mt-1">Market Directory</p>
            </div>

            <div className="flex-1 overflow-y-auto p-4 space-y-6">
                {/* Navigation */}
                <nav className="space-y-1">
                    <NavItem
                        icon={<Map size={20} />}
                        label="Map View"
                        active={currentView === 'map'}
                        onClick={() => onNavigate('map')}
                    />
                    <NavItem
                        icon={<BarChart3 size={20} />}
                        label="Analytics"
                        active={currentView === 'analytics'}
                        onClick={() => onNavigate('analytics')}
                    />
                    <NavItem icon={<Settings size={20} />} label="Settings" />
                </nav>

                {/* Filters Section */}
                <div>
                    <div className="flex items-center justify-between mb-3">
                        <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wider flex items-center gap-2">
                            <Filter size={14} /> Filters
                        </h3>
                        <button
                            onClick={() => setFilters({ county: 'All Counties', minUnits: 10, yearMin: '', yearMax: '', citySearch: '' })}
                            className="text-[10px] font-medium text-red-500 hover:text-red-700 hover:bg-red-50 px-2 py-0.5 rounded transition-colors"
                        >
                            Reset
                        </button>
                    </div>

                    <div className="space-y-4">
                        {/* County Filter */}
                        <div>
                            <label className="block text-sm font-medium text-slate-700 mb-1">County</label>
                            <select
                                value={filters.county}
                                onChange={(e) => setFilters(prev => ({ ...prev, county: e.target.value }))}
                                className="w-full text-sm border-slate-300 rounded-md shadow-sm focus:border-brand-500 focus:ring-brand-500 bg-slate-50 p-2 border"
                            >
                                <option value="All Counties">All Counties</option>
                                {counties.map(c => (
                                    <option key={c} value={c}>{c}</option>
                                ))}
                            </select>
                        </div>

                        {/* City Search */}
                        <div>
                            <label className="block text-sm font-medium text-slate-700 mb-1">City</label>
                            <input
                                type="text"
                                placeholder="Search city..."
                                value={filters.citySearch}
                                onChange={(e) => setFilters(prev => ({ ...prev, citySearch: e.target.value }))}
                                className="w-full text-sm p-2 border border-slate-300 rounded-md bg-slate-50 placeholder-slate-400 focus:border-brand-500 focus:ring-brand-500"
                            />
                        </div>

                        {/* Units Filter */}
                        <div>
                            <label className="block text-sm font-medium text-slate-700 mb-1">
                                Min Units: <span className="text-brand-600 font-bold">{filters.minUnits}</span>
                            </label>
                            <input
                                type="range"
                                min="10"
                                max="500"
                                value={filters.minUnits}
                                onChange={(e) => setFilters(prev => ({ ...prev, minUnits: Number(e.target.value) }))}
                                className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-brand-600"
                            />
                            <div className="flex justify-between text-xs text-slate-400 mt-1">
                                <span>10</span>
                                <span>500+</span>
                            </div>
                        </div>

                        {/* Year Built */}
                        <div>
                            <label className="block text-sm font-medium text-slate-700 mb-1">Year Built</label>
                            <div className="grid grid-cols-2 gap-2">
                                <input
                                    type="number"
                                    placeholder="Min"
                                    value={filters.yearMin}
                                    onChange={(e) => setFilters(prev => ({ ...prev, yearMin: e.target.value }))}
                                    className="text-sm p-2 border border-slate-300 rounded-md w-full"
                                />
                                <input
                                    type="number"
                                    placeholder="Max"
                                    value={filters.yearMax}
                                    onChange={(e) => setFilters(prev => ({ ...prev, yearMax: e.target.value }))}
                                    className="text-sm p-2 border border-slate-300 rounded-md w-full"
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div className="p-4 border-t border-slate-100">
                <button className="w-full bg-brand-600 hover:bg-brand-700 text-white font-medium py-2 px-4 rounded-lg transition-colors text-sm shadow-sm">
                    Export Report
                </button>
            </div>
        </div>
    );
};

const NavItem = ({ icon, label, active = false, onClick }) => (
    <button
        onClick={onClick}
        className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors ${active
            ? 'bg-brand-50 text-brand-700 font-medium'
            : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
            }`}>
        {icon}
        {label}
    </button>
);

export default Sidebar;
