import React, { useState, useEffect, useMemo } from 'react';
import Sidebar from './components/Sidebar';
import MapComponent from './components/MapComponent';
import AnalyticsView from './components/AnalyticsView';

function App() {
  const [allData, setAllData] = useState([]);
  const [currentView, setCurrentView] = useState('map'); // 'map' or 'analytics'
  const [filters, setFilters] = useState({
    county: 'All Counties',
    minUnits: 10,
    yearMin: '',
    yearMax: ''
  });

  // Fetch Data once
  useEffect(() => {
    fetch(import.meta.env.BASE_URL + 'properties.json?t=' + Date.now())
      .then(res => res.json())
      .then(data => {
        setAllData(data);
      })
      .catch(err => console.error(err));
  }, []);

  // Derived: Unique Counties
  const counties = useMemo(() => {
    const unique = new Set(allData.map(d => d.county).filter(Boolean));
    return Array.from(unique).sort();
  }, [allData]);

  // Derived: Filtered Data
  const filteredData = useMemo(() => {
    return allData.filter(d => {
      // County Filter
      if (filters.county !== 'All Counties' && d.county !== filters.county) return false;

      // Units Filter
      if ((d.units || 0) < filters.minUnits) return false;

      // Year Built Filter
      const year = d.year || 0;
      if (filters.yearMin && year < parseInt(filters.yearMin)) return false;
      if (filters.yearMax && year > parseInt(filters.yearMax)) return false;

      return true;
    });
  }, [allData, filters]);

  // Prepare GeoJSON for Map
  const mapData = useMemo(() => {
    return {
      type: 'FeatureCollection',
      features: filteredData.map(item => ({
        type: 'Feature',
        geometry: {
          type: 'Point',
          coordinates: [item.longitude, item.latitude]
        },
        properties: item
      }))
    };
  }, [filteredData]);

  return (
    <div className="flex h-screen w-screen bg-slate-50 text-slate-900 overflow-hidden">
      <Sidebar
        filters={filters}
        setFilters={setFilters}
        counties={counties}
        currentView={currentView}
        onNavigate={setCurrentView}
      />
      <main className="flex-1 shadow-inner relative z-0">
        {currentView === 'map' ? (
          <MapComponent data={mapData} />
        ) : (
          <AnalyticsView data={filteredData} />
        )}
      </main>
    </div>
  );
}

export default App;
