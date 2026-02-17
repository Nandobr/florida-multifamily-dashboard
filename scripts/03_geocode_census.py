import requests
import pandas as pd
import io
import time
import sys
from pathlib import Path

# Add project root to path for imports
sys.path.append(str(Path(__file__).parent.parent))

CENSUS_URL = 'https://geocoding.geo.census.gov/geocoder/geographies/addressbatch'

def geocode_census_batch(roster_path, output_path, batch_size=500):
    """Geocode addresses using US Census Bureau batch geocoder.
    Max 10,000 addresses per batch officially, but smaller batches are more reliable.
    """
    
    if not Path(roster_path).exists():
        print(f"Error: File not found at {roster_path}")
        return None

    df = pd.read_parquet(roster_path)
    
    # Initialize columns if they don't exist
    for col in ['latitude', 'longitude', 'geocode_source']:
        if col not in df.columns:
            df[col] = None

    # Filter for rows that need geocoding (no lat/lon)
    missing_mask = df['latitude'].isna() | df['longitude'].isna()
    to_geocode = df[missing_mask].copy()
    
    print(f"Found {len(to_geocode)} properties missing coordinates.")
    
    if len(to_geocode) == 0:
        return df

    results = []
    
    # Prepare data for census format: ID, Street, City, State, ZIP
    # We need a temporary unique ID for the batch
    to_geocode['temp_id'] = range(len(to_geocode))
    
    for start in range(0, len(to_geocode), batch_size):
        batch = to_geocode.iloc[start:start + batch_size]
        print(f"  Processing batch {start}-{start+len(batch)}...")
        
        # Create CSV buffer
        # Columns: ID, Street, City, State, ZIP
        batch_csv = batch[['temp_id', 'PHY_ADDR1', 'PHY_CITY', 'OWN_STATE', 'PHY_ZIPCD']].copy()
        # Ensure state is FL (PHY_ADDR doesn't have state col in this extraction usually, assume FL)
        # Wait, previous script constructed FULL_ADDRESS but individual cols exist.
        # PHY_CITY is present. State is FL.
        batch_csv['State'] = 'FL'
        
        # Rename for clarity (though csv structure matters, not headers)
        submit_df = batch_csv[['temp_id', 'PHY_ADDR1', 'PHY_CITY', 'State', 'PHY_ZIPCD']]
        
        csv_buffer = io.StringIO()
        submit_df.to_csv(csv_buffer, index=False, header=False)
        csv_data = csv_buffer.getvalue()
        
        try:
            response = requests.post(
                CENSUS_URL,
                files={'addressFile': ('batch.csv', csv_data, 'text/csv')},
                data={'benchmark': 'Public_AR_Current', 'vintage': 'Current_Current'},
                timeout=120
            )
            
            if response.status_code == 200:
                # Response format: "id, input_addr, match_flag, match_type, matched_addr, lon,lat, ..."
                # Note: Census returns lon,lat (x,y)
                result_df = pd.read_csv(
                    io.StringIO(response.text),
                    header=None,
                    names=['id', 'input_addr', 'match_flag', 'match_type', 
                           'matched_addr', 'lonlat', 'tiger_id', 'side',
                           'state_fips', 'county_fips', 'tract', 'block'],
                    on_bad_lines='skip'
                )
                
                matched = result_df[result_df['match_flag'] == 'Match'].copy()
                if not matched.empty:
                    # Split lon,lat
                    matched[['longitude', 'latitude']] = matched['lonlat'].str.split(',', expand=True).astype(float)
                    results.append(matched[['id', 'latitude', 'longitude']])
            else:
                print(f"    Error: Status {response.status_code}")
                
        except Exception as e:
            print(f"    Exception: {e}")
            
        time.sleep(1) # Rate limit courtesy
        
    # Update main dataframe
    if results:
        all_matches = pd.concat(results, ignore_index=True)
        # Join back on temp_id
        # We need to map temp_id back to the original index
        
        # Create a mapping dictionary from results
        lat_map = all_matches.set_index('id')['latitude'].to_dict()
        lon_map = all_matches.set_index('id')['longitude'].to_dict()
        
        # Apply to to_geocode first using map on temp_id
        to_geocode['new_lat'] = to_geocode['temp_id'].map(lat_map)
        to_geocode['new_lon'] = to_geocode['temp_id'].map(lon_map)
        
        # Now update original df
        # Iterate or use update.
        # Using index alignment
        df.loc[to_geocode.index, 'latitude'] = df.loc[to_geocode.index, 'latitude'].fillna(to_geocode['new_lat'])
        df.loc[to_geocode.index, 'longitude'] = df.loc[to_geocode.index, 'longitude'].fillna(to_geocode['new_lon'])
        
        # Update source
        updated_mask = df['latitude'].notna() & df['geocode_source'].isna()
        df.loc[updated_mask, 'geocode_source'] = 'census'
        
        print(f"Total new matches: {len(all_matches)}")
    
    df.to_parquet(output_path, index=False)
    print(f"Saved updated roster to {output_path}")
    return df

if __name__ == '__main__':
    base_dir = Path(__file__).parent.parent
    geocode_census_batch(
        roster_path=str(base_dir / 'data/processed/geocoded.parquet'), # Input: output of prev step
        output_path=str(base_dir / 'data/processed/geocoded.parquet')  # Overwrite or separate? Plan implies separate but usually strictly cumulative.
        # Let's overwrite to keep it simple, or use distinct filenames if debugging. 
        # The script input was 'geocoded.parquet' in the call, assuming it exists?
        # Actually in the plan, Tier 1 produces 'geocoded.parquet'. Tier 2 should probably refine it.
    )
