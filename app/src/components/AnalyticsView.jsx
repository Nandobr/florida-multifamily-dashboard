import React, { useMemo } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { Search } from 'lucide-react';

const AnalyticsView = ({ data }) => {
    // Aggregation: Top 10 Counties by Unit Count
    const countyData = useMemo(() => {
        const counts = {};
        data.forEach(d => {
            const county = d.county || 'Unknown';
            counts[county] = (counts[county] || 0) + (d.units || 0);
        });
        return Object.entries(counts)
            .map(([name, value]) => ({ name, value }))
            .sort((a, b) => b.value - a.value)
            .slice(0, 10);
    }, [data]);

    // Aggregation: Year Built Distribution (Decades)
    const yearData = useMemo(() => {
        const counts = {};
        data.forEach(d => {
            if (!d.year) return;
            const decade = Math.floor(d.year / 10) * 10;
            counts[decade] = (counts[decade] || 0) + 1;
        });
        return Object.entries(counts)
            .map(([name, value]) => ({ name: `${name}s`, value }))
            .sort((a, b) => a.name.localeCompare(b.name));
    }, [data]);

    // Aggregation: Top 5 Owners
    // Aggregation: Top Owners (Filtered by Search)
    const [searchTerm, setSearchTerm] = React.useState('');
    const topOwners = useMemo(() => {
        const counts = {};
        data.forEach(d => {
            const owner = d.owner || 'Unknown';
            counts[owner] = (counts[owner] || 0) + (d.units || 0);
        });

        return Object.entries(counts)
            .map(([name, value]) => ({ name, value }))
            .sort((a, b) => b.value - a.value)
            .filter(item => item.name.toLowerCase().includes(searchTerm.toLowerCase()))
            .slice(0, 100); // Increased limit to 100
    }, [data, searchTerm]);

    const totalUnits = data.reduce((acc, d) => acc + (d.units || 0), 0);

    return (
        <div className="p-8 bg-slate-50 h-full overflow-y-auto">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-slate-900">Market Analytics</h1>
                <p className="text-slate-500">
                    Analyzing <strong className="text-brand-600">{data.length.toLocaleString()}</strong> properties
                    with <strong className="text-emerald-600">{totalUnits.toLocaleString()}</strong> units in current view.
                </p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
                {/* Chart 1: Market Size by County */}
                <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                    <h3 className="text-lg font-bold text-slate-800 mb-4">Top Markets by Unit Count</h3>
                    <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={countyData} layout="vertical" margin={{ left: 40 }}>
                                <XAxis type="number" hide />
                                <YAxis dataKey="name" type="category" width={100} tick={{ fontSize: 12 }} />
                                <Tooltip cursor={{ fill: '#f1f5f9' }} formatter={(value) => value.toLocaleString()} />
                                <Bar dataKey="value" fill="#0d9488" radius={[0, 4, 4, 0]} barSize={20} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Chart 2: Inventory Age */}
                <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                    <h3 className="text-lg font-bold text-slate-800 mb-4">Inventory by Decade Built</h3>
                    <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={yearData}>
                                <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                                <YAxis hide />
                                <Tooltip cursor={{ fill: '#f1f5f9' }} />
                                <Bar dataKey="value" fill="#64748b" radius={[4, 4, 0, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </div>

            {/* Table: Top Owners */}
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden flex flex-col max-h-[500px]">
                <div className="p-6 border-b border-slate-100 flex justify-between items-center sticky top-0 bg-white z-10">
                    <h3 className="text-lg font-bold text-slate-800">Top Owners in View</h3>
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 w-4 h-4" />
                        <input
                            type="text"
                            placeholder="Search owners..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            className="pl-9 pr-4 py-2 text-sm border border-slate-200 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-brand-500 w-64"
                        />
                    </div>
                </div>

                <div className="overflow-y-auto flex-1">
                    <table className="w-full text-sm text-left">
                        <thead className="bg-slate-50 text-slate-500 font-medium sticky top-0 shadow-sm z-10">
                            <tr>
                                <th className="px-6 py-3 bg-slate-50">Owner Name</th>
                                <th className="px-6 py-3 text-right bg-slate-50">Total Units</th>
                                <th className="px-6 py-3 text-right text-slate-400 bg-slate-50">% of View</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100">
                            {topOwners.map((owner, i) => (
                                <tr key={owner.name} className="hover:bg-slate-50">
                                    <td className="px-6 py-3 font-medium text-slate-900">
                                        {i + 1}. {owner.name}
                                    </td>
                                    <td className="px-6 py-3 text-right font-mono text-emerald-600">
                                        {owner.value.toLocaleString()}
                                    </td>
                                    <td className="px-6 py-3 text-right text-slate-400">
                                        {((owner.value / totalUnits) * 100).toFixed(1)}%
                                    </td>
                                </tr>
                            ))}
                            {topOwners.length === 0 && (
                                <tr>
                                    <td colSpan="3" className="px-6 py-8 text-center text-slate-500">
                                        No owners found matching "{searchTerm}"
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default AnalyticsView;
