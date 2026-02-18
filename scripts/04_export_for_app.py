import pandas as pd
import json
import shutil
from pathlib import Path

def export_for_app(input_path, output_path):
    """Export geocoded roster to app public folder."""
    
    if not Path(input_path).exists():
        print(f"Error: {input_path} not found.")
        return

    print(f"Reading {input_path}...")
    df = pd.read_parquet(input_path)
    
    # Filter for valid coordinates
    # Ensure they are numeric
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    
    valid_mask = df['latitude'].notna() & df['longitude'].notna()
    export_df = df[valid_mask].copy()
    
    print(f"Found {len(export_df)} items with coordinates out of {len(df)} total.")
    
    if len(export_df) == 0:
        print("No geocoded data to export yet.")
        # Create a dummy file so frontend doesn't crash?
        # Or just return
        return

    # Select columns for frontend
    cols = [
        'PARCEL_ID', 'COUNTY_NAME', 'PHY_ADDR1', 'PHY_CITY', 'PHY_ZIPCD',
        'NO_RES_UNTS', 'ACT_YR_BLT', 'OWN_NAME', 'latitude', 'longitude',
        'SALE_PRC1', 'SALE_YR1', 'JV', 'TOT_LVG_AREA'
    ]
    
    # Rename for lighter JSON keys if desired, or keep as is.
    # Let's keep simpler keys
    rename_map = {
        'PHY_ADDR1': 'address',
        'PHY_CITY': 'city',
        'PHY_ZIPCD': 'zip',
        'NO_RES_UNTS': 'units',
        'ACT_YR_BLT': 'year',
        'OWN_NAME': 'owner',
        'COUNTY_NAME': 'county',
        'PARCEL_ID': 'id',
        'SALE_PRC1': 'sale_price',
        'SALE_YR1': 'sale_year',
        'JV': 'value',
        'TOT_LVG_AREA': 'sqft'
    }
    
    final_df = export_df[cols].rename(columns=rename_map)
    
    # Save as JSON
    # Orient 'records' saves a list of objects
    print(f"Exporting to {output_path}...")
    final_df.to_json(output_path, orient='records')
    print("Done.")

if __name__ == '__main__':
    base_dir = Path(__file__).parent.parent
    export_for_app(
        input_path=str(base_dir / 'data/processed/geocoded.parquet'),
        output_path=str(base_dir / 'app/public/properties.json')
    )
