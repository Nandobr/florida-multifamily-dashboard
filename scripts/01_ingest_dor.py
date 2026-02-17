import pandas as pd
import os
import sys
from pathlib import Path

# Add project root to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from scripts.utils.county_lookup import COUNTY_NAMES, PRIORITY_COUNTIES

# Columns to keep (saves memory — NAL has 165 columns)
KEEP_COLS = [
    'CO_NO', 'PARCEL_ID', 'ASMNT_YR', 'DOR_UC', 'PA_UC',
    'JV', 'AV_NSD', 'TV_NSD',
    'LND_VAL', 'NO_LND_UNTS', 'LND_SQFOOT',
    'ACT_YR_BLT', 'EFF_YR_BLT', 'TOT_LVG_AREA',
    'NO_BULDNG', 'NO_RES_UNTS',
    'OWN_NAME', 'OWN_ADDR1', 'OWN_ADDR2', 'OWN_CITY', 'OWN_STATE', 'OWN_ZIPCD',
    'PHY_ADDR1', 'PHY_ADDR2', 'PHY_CITY', 'PHY_ZIPCD',
]

def ingest_all_counties(nal_dir: str, output_path: str):
    """Load all 67 county NAL files, filter to multifamily 50+ units."""
    
    frames = []
    nal_path = Path(nal_dir)
    
    # Ensure processed directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if not nal_path.exists():
        print(f"Warning: Raw NAL directory not found: {nal_dir}")
        return None

    csv_files = sorted(nal_path.glob('*.csv')) + sorted(nal_path.glob('*.txt'))
    
    if not csv_files:
        print(f"No CSV files found in {nal_dir}")
        return None

    for csv_file in csv_files:
        print(f"Processing: {csv_file.name}")
        
        # Read only needed columns (handles large files efficiently)
        try:
            df = pd.read_csv(
                csv_file,
                usecols=lambda c: c.upper() in [col.upper() for col in KEEP_COLS],
                dtype=str,
                low_memory=False,
                encoding='latin-1'  # Some counties use non-UTF8 characters
            )
        except Exception as e:
            print(f"  ERROR reading {csv_file.name}: {e}")
            continue
        
        # Normalize column names to uppercase
        df.columns = df.columns.str.upper().str.strip()
        
        # Convert numeric fields
        df['NO_RES_UNTS'] = pd.to_numeric(df.get('NO_RES_UNTS', 0), errors='coerce').fillna(0).astype(int)
        df['CO_NO'] = pd.to_numeric(df.get('CO_NO', 0), errors='coerce').fillna(0).astype(int)
        
        # Filter: DOR_UC in ('003', '008') — ALL multifamily properties
        # 003 = Multi-family 10+ units (Commercial)
        # 008 = Multi-family fewer than 10 units (Residential)
        if 'DOR_UC' in df.columns:
            dor_uc_clean = df['DOR_UC'].astype(str).str.strip().str.zfill(3)
            mask = dor_uc_clean.isin(['003', '008'])
            filtered = df[mask].copy()
        else:
            print("  Warning: DOR_UC column missing")
            continue
        
        if len(filtered) > 0:
            county_name = COUNTY_NAMES.get(filtered['CO_NO'].iloc[0], 'Unknown')
            print(f"  -> {len(filtered)} properties in {county_name}")
            frames.append(filtered)
        else:
            print(f"  -> 0 multifamily properties found")
    
    if not frames:
        print("No data found matching criteria.")
        return None

    # Combine all counties
    result = pd.concat(frames, ignore_index=True)
    
    # Add county name
    result['COUNTY_NAME'] = result['CO_NO'].map(COUNTY_NAMES)
    
    # Flag priority metros
    result['IS_PRIORITY'] = result['CO_NO'].isin(PRIORITY_COUNTIES)
    
    # Convert remaining numeric fields
    for col in ['JV', 'AV_NSD', 'TV_NSD', 'LND_VAL', 'LND_SQFOOT',
                'TOT_LVG_AREA', 'NO_BULDNG', 'ACT_YR_BLT', 'EFF_YR_BLT']:
        if col in result.columns:
            result[col] = pd.to_numeric(result[col], errors='coerce')
    
    # Clean address fields
    for col in ['PHY_ADDR1', 'PHY_ADDR2', 'PHY_CITY', 'PHY_ZIPCD']:
        if col in result.columns:
            result[col] = result[col].fillna('').str.strip()
    
    # Build full address for geocoding
    result['FULL_ADDRESS'] = (
        result['PHY_ADDR1'].str.strip() + ' ' +
        result['PHY_ADDR2'].fillna('').str.strip()
    ).str.strip() + ', ' + result['PHY_CITY'] + ', FL ' + result['PHY_ZIPCD'].str[:5]
    
    # Save
    result.to_parquet(output_path, index=False)
    print(f"\n{'='*60}")
    print(f"TOTAL: {len(result)} multifamily properties across {result['CO_NO'].nunique()} counties")
    print(f"  DOR_UC 003 (10+ units): {(result['DOR_UC'].str.zfill(3) == '003').sum()}")
    print(f"  DOR_UC 008 (<10 units): {(result['DOR_UC'].str.zfill(3) == '008').sum()}")
    print(f"  50+ units: {(result['NO_RES_UNTS'] >= 50).sum()}")
    print(f"  100+ units: {(result['NO_RES_UNTS'] >= 100).sum()}")
    print(f"Priority metros: {result[result['IS_PRIORITY']].shape[0]}")
    print(f"\nSaved to: {output_path}")
    
    return result

if __name__ == '__main__':
    # Use relative paths for portability
    base_dir = Path(__file__).parent.parent
    df = ingest_all_counties(
        nal_dir=str(base_dir / 'data/raw/dor_nal'),
        output_path=str(base_dir / 'data/processed/base_roster.parquet')
    )
