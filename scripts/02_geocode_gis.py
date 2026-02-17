import geopandas as gpd
import pandas as pd
import sys
from pathlib import Path

# Add project root to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from scripts.utils.county_lookup import COUNTY_NAMES

def geocode_from_gis(roster_path, gis_dir, output_path):
    """Join parcel centroids from county GIS shapefiles to base roster."""
    
    if not Path(roster_path).exists():
        print(f"Error: Roster file not found at {roster_path}")
        return None

    roster = pd.read_parquet(roster_path)
    
    # Initialize columns if they don't exist
    for col in ['latitude', 'longitude', 'geocode_source']:
        if col not in roster.columns:
            roster[col] = None
    
    gis_path = Path(gis_dir)
    
    for county_no in roster['CO_NO'].unique():
        county_name = COUNTY_NAMES.get(county_no, str(county_no))
        
        # Find matching shapefile (naming varies by county)
        # Look for subdirectories first
        shp_files = list(gis_path.glob(f'*{county_no}*/*.shp')) + \
                    list(gis_path.glob(f'*{county_name.lower()}*/*.shp')) + \
                    list(gis_path.glob(f'*{county_name}*/*.shp'))
        
        if not shp_files:
            print(f"  No GIS data directory found for {county_name} ({county_no})")
            continue
        
        try:
            parcels_gis = gpd.read_file(shp_files[0])
        except Exception as e:
            print(f"  Error reading shapefile for {county_name}: {e}")
            continue
        
        # Standardize parcel ID column name
        parcel_col = None
        for candidate in ['PARCELNO', 'PARCEL_ID', 'FOLIO', 'PIN', 'PARCEL', 'STRAP']:
            # Case insensitive check
            match = next((col for col in parcels_gis.columns if col.upper() == candidate), None)
            if match:
                parcel_col = match
                break
        
        if not parcel_col:
            print(f"  Cannot find parcel ID column in {county_name} GIS data. Columns: {parcels_gis.columns.tolist()[:5]}...")
            continue
        
        # Re-project to WGS84 (Lat/Lon) if needed
        if parcels_gis.crs and parcels_gis.crs.to_epsg() != 4326:
            parcels_gis = parcels_gis.to_crs(epsg=4326)
        
        # Calculate centroids
        parcels_gis['_centroid_lat'] = parcels_gis.geometry.centroid.y
        parcels_gis['_centroid_lng'] = parcels_gis.geometry.centroid.x
        
        # Create lookup dictionary (Parcel ID -> (Lat, Lng))
        # Ensure parcel IDs are strings and stripped
        parcels_gis['clean_pid'] = parcels_gis[parcel_col].astype(str).str.strip()
        gis_lookup = parcels_gis.set_index('clean_pid')[['_centroid_lat', '_centroid_lng']].to_dict('index')
        
        # Update roster for this county
        county_mask = roster['CO_NO'] == county_no
        
        def get_lat_lng(pid):
            clean_pid = str(pid).strip()
            if clean_pid in gis_lookup:
                val = gis_lookup[clean_pid]
                return val['_centroid_lat'], val['_centroid_lng'], 'county_gis'
            return None, None, None

        # Apply mapping
        # This can be slow; for large datasets, a merge is faster.
        # But doing it iteratively per county to handle memory.
        
        # Let's do a merge for speed on the slice
        county_df = roster.loc[county_mask].copy()
        county_df['PARCEL_ID_CLEAN'] = county_df['PARCEL_ID'].astype(str).str.strip()
        
        # Prepare GIS DF for merge
        gis_merge = parcels_gis[['clean_pid', '_centroid_lat', '_centroid_lng']].rename(
            columns={'clean_pid': 'PARCEL_ID_CLEAN'}
        )
        
        merged = county_df.merge(gis_merge, on='PARCEL_ID_CLEAN', how='left')
        
        # Update original roster using index
        roster.loc[county_mask, 'latitude'] = roster.loc[county_mask, 'latitude'].fillna(merged['_centroid_lat'].values)
        roster.loc[county_mask, 'longitude'] = roster.loc[county_mask, 'longitude'].fillna(merged['_centroid_lng'].values)
        
        # Set source only where we found a match and it wasn't already set
        # (Though here we are overwriting or filling na, logic depends on precedence. Tier 1 has highest precedence)
        updated_mask = county_mask & (roster['latitude'].notna()) & (roster['geocode_source'].isna())
        roster.loc[updated_mask, 'geocode_source'] = 'county_gis'
        
        match_count = merged['_centroid_lat'].notna().sum()
        print(f"  {county_name}: {match_count}/{county_mask.sum()} matched via GIS")
    
    roster.to_parquet(output_path, index=False)
    print(f"Saved geocoded roster to {output_path}")
    return roster

if __name__ == '__main__':
    base_dir = Path(__file__).parent.parent
    geocode_from_gis(
        roster_path=str(base_dir / 'data/processed/base_roster.parquet'),
        gis_dir=str(base_dir / 'data/raw/dor_gis'),
        output_path=str(base_dir / 'data/processed/geocoded.parquet')
    )
