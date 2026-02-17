import React, { useState, useMemo } from 'react';
import Map, { NavigationControl, Source, Layer, ScaleControl, FullscreenControl, Popup } from 'react-map-gl/maplibre';
import 'maplibre-gl/dist/maplibre-gl.css';

const MapComponent = ({ data }) => {
    const [hoverInfo, setHoverInfo] = useState(null);
    const [selectedProperty, setSelectedProperty] = useState(null);

    const totalUnits = useMemo(() => {
        if (!data || !data.features) return 0;
        return data.features.reduce((acc, f) => acc + (f.properties.units || 0), 0);
    }, [data]);

    // Center roughly on Florida
    const initialViewState = {
        longitude: -81.5,
        latitude: 27.8,
        zoom: 7
    };

    const mapStyle = {
        version: 8,
        sources: {
            'osm': {
                type: 'raster',
                tiles: ['https://a.tile.openstreetmap.org/{z}/{x}/{y}.png'],
                tileSize: 256,
                attribution: '&copy; OpenStreetMap Contributors'
            }
        },
        layers: [
            {
                id: 'osm',
                type: 'raster',
                source: 'osm',
                minzoom: 0,
                maxzoom: 19
            }
        ]
    };

    const clusterLayer = {
        id: 'clusters',
        type: 'circle',
        source: 'properties',
        filter: ['has', 'point_count'],
        paint: {
            'circle-color': ['step', ['get', 'point_count'], '#0f766e', 100, '#0d9488', 750, '#14b8a6'],
            'circle-radius': ['step', ['get', 'point_count'], 20, 100, 30, 750, 40],
            'circle-stroke-width': 2,
            'circle-stroke-color': '#fff'
        }
    };

    const clusterCountLayer = {
        id: 'cluster-count',
        type: 'symbol',
        source: 'properties',
        filter: ['has', 'point_count'],
        layout: {
            'text-field': '{point_count_abbreviated}',
            'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Bold'],
            'text-size': 12
        },
        paint: {
            'text-color': '#ffffff'
        }
    };

    const unclusteredPointLayer = {
        id: 'unclustered-point',
        type: 'circle',
        source: 'properties',
        filter: ['!', ['has', 'point_count']],
        paint: {
            'circle-color': '#0f766e', // Brand color
            'circle-radius': 5,
            'circle-stroke-width': 1,
            'circle-stroke-color': '#fff'
        }
    };

    return (
        <div className="relative w-full h-full bg-slate-100 overflow-hidden">
            <Map
                initialViewState={initialViewState}
                style={{ width: '100%', height: '100%' }}
                mapStyle={mapStyle} // Using OSM raster tiles for free, no-token map
                attributionControl={true}
                interactiveLayerIds={['clusters', 'unclustered-point']}
                onMouseEnter={(e) => {
                    if (e.features[0]?.properties?.id) {
                        setHoverInfo({
                            feature: e.features[0],
                            x: e.point.x,
                            y: e.point.y
                        });
                    }
                }}
                onMouseLeave={() => setHoverInfo(null)}
                onClick={(e) => {
                    // If we clicked a cluster, we could zoom (optional)
                    // If we clicked a point (unclustered), show popup
                    const feature = e.features?.[0];
                    if (feature && feature.layer.id === 'unclustered-point') {
                        setHoverInfo(null); // Hide hover tooltip
                        setSelectedProperty(feature.properties); // Show popup
                    } else if (feature && feature.layer.id === 'clusters') {
                        // Optional: Zoom into cluster
                        // const clusterId = feature.properties.cluster_id;
                        // const mapboxSource = e.target.getSource('properties');
                        // mapboxSource.getClusterExpansionZoom(clusterId, (err, zoom) => {
                        //     if (err) return;
                        //     e.target.easeTo({
                        //         center: feature.geometry.coordinates,
                        //         zoom,
                        //         duration: 500
                        //     });
                        // });
                    }
                }}
            >
                <NavigationControl position="top-right" />
                <FullscreenControl position="top-right" />
                <ScaleControl />

                {data && (
                    <Source
                        id="properties"
                        type="geojson"
                        data={data}
                        cluster={true}
                        clusterMaxZoom={14}
                        clusterRadius={50}
                    >
                        <Layer {...clusterLayer} />
                        <Layer {...clusterCountLayer} />
                        <Layer {...unclusteredPointLayer} />
                    </Source>
                )}

                {/* Selected Property Popup */}
                {selectedProperty && (
                    <Popup
                        longitude={selectedProperty.longitude}
                        latitude={selectedProperty.latitude}
                        anchor="bottom"
                        onClose={() => setSelectedProperty(null)}
                        closeOnClick={false}
                        className="z-30"
                    >
                        <div className="p-1 min-w-[200px]">
                            <h3 className="font-bold text-slate-900 text-sm mb-1">{selectedProperty.owner}</h3>
                            <div className="text-xs text-slate-600 space-y-1">
                                <p>{selectedProperty.address}</p>
                                <p>{selectedProperty.city}, FL {selectedProperty.zip}</p>
                                <div className="flex gap-2 mt-2 pt-2 border-t border-slate-100">
                                    <div className="text-center">
                                        <span className="block font-bold text-emerald-600">{selectedProperty.units}</span>
                                        <span className="text-[10px] uppercase text-slate-400">Units</span>
                                    </div>
                                    <div className="text-center pl-2 border-l border-slate-100">
                                        <span className="block font-bold text-brand-600">{selectedProperty.year || 'N/A'}</span>
                                        <span className="text-[10px] uppercase text-slate-400">Built</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </Popup>
                )}

                {hoverInfo && !selectedProperty && (
                    <div className="absolute z-20 bg-white p-3 rounded-lg shadow-xl text-sm pointer-events-none border border-slate-100" style={{ left: hoverInfo.x + 10, top: hoverInfo.y + 10 }}>
                        <div className="font-bold text-slate-800">{hoverInfo.feature.properties.owner}</div>
                        <div className="text-slate-600">{hoverInfo.feature.properties.address}</div>
                        <div className="mt-1 flex items-center gap-2">
                            <span className="bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded-full text-xs font-medium">
                                {hoverInfo.feature.properties.units} Units
                            </span>
                            <span className="text-slate-400 text-xs">{hoverInfo.feature.properties.city}</span>
                        </div>
                    </div>
                )}
            </Map>

            {/* Stats Card Overlay (Real Data) */}
            <div className="absolute top-4 left-4 bg-white/90 backdrop-blur-md p-4 rounded-xl shadow-lg border border-white/20 z-10 min-w-[200px]">
                <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Market Snapshot</h3>
                <div className="flex gap-6">
                    <div>
                        <div className="text-2xl font-bold text-slate-800">{data ? data.features.length.toLocaleString() : 'Loading...'}</div>
                        <div className="text-xs text-slate-500 font-medium">Properties</div>
                    </div>
                    <div>
                        <div className="text-2xl font-bold text-emerald-600">
                            {data ? Math.round(totalUnits / 1000) + 'k' : '-'}
                        </div>
                        <div className="text-xs text-slate-500 font-medium">Total Units</div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default MapComponent;
