# Florida Multifamily Property Directory — Project Plan v2

## Scope: All 67 Florida Counties — All Multifamily

Build a comprehensive database and interactive dashboard of **all multifamily apartment properties currently in operation across all 67 Florida counties**, with enrichment priority for seven key metros: Miami-Dade, Tampa, Orlando, Jacksonville, Boca Raton, Fort Lauderdale, and Hollywood.

**DOR Use Codes captured:**
- `003` — Multi-family, 10 units or more (classified as Commercial)
- `008` — Multi-family, fewer than 10 units (classified as Residential)

**Estimated total properties statewide:** 40,000–60,000 (all multifamily)  
**Of which 50+ units:** ~8,000–10,000  
**Priority metros:** ~25,000–35,000 of the total  

**Dashboard filter:** Users can set their own unit threshold (e.g., 50+, 100+, 200+) via slider. No data is excluded at ingestion.

---

## Target Schema Per Property

| Field | Column | Source | Phase |
|---|---|---|---|
| County Number | `CO_NO` | FL DOR NAL | 1 |
| County Name | derived | Lookup table | 1 |
| Parcel ID | `PARCEL_ID` | FL DOR NAL | 1 |
| Property Name | — | Google Places API / Apartments.com | 2 |
| Street Address Line 1 | `PHY_ADDR1` | FL DOR NAL | 1 |
| Street Address Line 2 | `PHY_ADDR2` | FL DOR NAL | 1 |
| City | `PHY_CITY` | FL DOR NAL | 1 |
| ZIP Code | `PHY_ZIPCD` | FL DOR NAL | 1 |
| Latitude | — | County GIS → Census → Nominatim | 1 |
| Longitude | — | County GIS → Census → Nominatim | 1 |
| Number of Units | `NO_RES_UNTS` | FL DOR NAL | 1 |
| Number of Buildings | `NO_BULDNG` | FL DOR NAL | 1 |
| Year Built | `ACT_YR_BLT` | FL DOR NAL | 1 |
| Total Living Area (sqft) | `TOT_LVG_AREA` | FL DOR NAL | 1 |
| Land Value | `LND_VAL` | FL DOR NAL | 1 |
| Just Value (Market) | `JV` | FL DOR NAL | 1 |
| Assessed Value | `AV_NSD` | FL DOR NAL | 1 |
| Owner Name | `OWN_NAME` | FL DOR NAL | 1 |
| Owner Address | `OWN_ADDR1/2` | FL DOR NAL | 1 |
| Owner City/State/ZIP | `OWN_CITY/STATE/ZIPCD` | FL DOR NAL | 1 |
| Management Company | — | Apartments.com / REIT portfolios / ALN | 3 |
| Property Website URL | — | Google Places API / Apartments.com | 2 |
| DOR Use Code | `DOR_UC` | FL DOR NAL | 1 |
| Geocode Source | — | Derived ('county_gis', 'census', 'nominatim') | 1 |

---

## FL DOR NAL File — Complete Column Reference (2025)

The NAL CSV files have **165 columns**. Below are the ones relevant to this project:

### Parcel Identification (Fields 1–4)
```
CO_NO          County number (2-digit, see lookup table)
PARCEL_ID      Unique parcel ID (format varies by county, up to 26 chars)
FILE_T         Always "R" for real property
ASMNT_YR       Assessment year (4-digit)
```

### Use Information (Fields 8–10)
```
DOR_UC         DOR Land Use Code (3-digit: "003" = multifamily 10+ units)
PA_UC          Property Appraiser local use code (optional)
SPASS_CD       Special assessment code
```

### Parcel Values (Fields 11–17)
```
JV             Just Value (market value estimate)
JV_CHNG        Just value change from preliminary to final roll
AV_SD          Assessed value — school district
AV_NSD         Assessed value — non-school district
TV_SD          Taxable value — school district
TV_NSD         Taxable value — non-school district
```

### Land & Improvement Info (Fields 41–53)
```
LND_VAL        Land value
LND_UNTS_CD    Land units code (1=front foot, 2=sqft, 3=acres, 4=units/lots)
NO_LND_UNTS    Number of land units
LND_SQFOOT     Land square footage
DT_LAST_INSPT  Date of last physical inspection (MMYY)
IMP_QUAL       Improvement quality code (1=Minimum, 5=Excellent)
CONST_CLASS    Construction class code
EFF_YR_BLT     Effective year built
ACT_YR_BLT     Actual year built
TOT_LVG_AREA   Total living area (sq ft)
NO_BULDNG      Number of buildings
NO_RES_UNTS    Number of residential units  ← KEY FILTER FIELD
SPEC_FEAT_VAL  Special feature value
```

### Owner Information (Fields 74–90)
```
OWN_NAME       Owner name (typically LLC for apartments)
OWN_ADDR1      Owner mailing address line 1
OWN_ADDR2      Owner mailing address line 2
OWN_CITY       Owner city
OWN_STATE      Owner state
OWN_ZIPCD      Owner ZIP code
OWN_COUNTRY    Owner country (if non-US)
FID_NAME       Fiduciary name
FID_ADDR1      Fiduciary address line 1
FID_ADDR2      Fiduciary address line 2
FID_CITY       Fiduciary city
FID_STATE      Fiduciary state
FID_ZIPCD      Fiduciary ZIP code
```

### Physical Location (Fields 91–102)
```
PHY_ADDR1      Physical address line 1 ← STREET ADDRESS
PHY_ADDR2      Physical address line 2
PHY_CITY       Physical city ← CITY
PHY_ZIPCD      Physical ZIP code ← ZIP CODE
PHY_COUNTY     Physical county (if different from CO_NO)
ASS_TRNSFR_FG  Assessment transfer flag
SPEC_FEAT_CD   Special feature code list
```

---

## County Number Lookup Table (All 67)

| CO_NO | County | CO_NO | County |
|---|---|---|---|
| 11 | Alachua | 45 | Lake |
| 12 | Baker | 46 | Lee |
| 13 | Bay | 47 | Leon |
| 14 | Bradford | 48 | Levy |
| 15 | Brevard | 49 | Liberty |
| 16 | Broward ★ | 50 | Madison |
| 17 | Calhoun | 51 | Manatee |
| 18 | Charlotte | 52 | Marion |
| 19 | Citrus | 53 | Martin |
| 20 | Clay | 54 | Monroe |
| 21 | Collier | 55 | Nassau |
| 22 | Columbia | 56 | Okaloosa |
| 23 | Miami-Dade ★ | 57 | Okeechobee |
| 24 | DeSoto | 58 | Orange ★ |
| 25 | Dixie | 59 | Osceola |
| 26 | Duval ★ | 60 | Palm Beach ★ |
| 27 | Escambia | 61 | Pasco |
| 28 | Flagler | 62 | Pinellas |
| 29 | Franklin | 63 | Polk |
| 30 | Gadsden | 64 | Putnam |
| 31 | Gilchrist | 65 | Saint Johns |
| 32 | Glades | 66 | Saint Lucie |
| 33 | Gulf | 67 | Santa Rosa |
| 34 | Hamilton | 68 | Sarasota |
| 35 | Hardee | 69 | Seminole |
| 36 | Hendry | 70 | Sumter |
| 37 | Hernando | 71 | Suwannee |
| 38 | Highlands | 72 | Taylor |
| 39 | Hillsborough ★ | 73 | Union |
| 40 | Holmes | 74 | Volusia |
| 41 | Indian River | 75 | Wakulla |
| 42 | Jackson | 76 | Walton |
| 43 | Jefferson | 77 | Washington |
| 44 | Lafayette | | |

★ = Priority enrichment metro

---

## Phase 1 — Statewide Base Roster + Geocoding (Week 1–2)

### Step 1.1: Acquire NAL Data

**Option A — Direct download from Data Portal (preferred):**
Navigate to the FL DOR Data Portal's NAL file listing page. The 2025 Final NAL files are published as individual ZIP files per county (e.g., `Miami-Dade 23 Final NAL 2025.zip`). Each ZIP contains one CSV.

**URL pattern:**
```
https://floridarevenue.com/property/dataportal/Documents/PTO Data Portal/Tax Roll Data Files/NAL/2025F/
```

**Option B — Email request (if direct download unavailable):**
Email `PTOTechnology@floridarevenue.com` requesting:
> "2025 Final NAL files for all 67 Florida counties in CSV format."

They typically respond within 1–3 business days with download links or FTP access.

**Option C — FTP access (historical):**
```
ftp://sdrftp03.dor.state.fl.us/Tax Roll Data Files/
```
Note: FTP availability may vary; the web portal is now the primary distribution channel.

### Step 1.2: Ingest & Filter (Script: `01_ingest_dor.py`)

```python
import pandas as pd
import os
from pathlib import Path

# County lookup
COUNTY_NAMES = {
    11: 'Alachua', 12: 'Baker', 13: 'Bay', 14: 'Bradford', 15: 'Brevard',
    16: 'Broward', 17: 'Calhoun', 18: 'Charlotte', 19: 'Citrus', 20: 'Clay',
    21: 'Collier', 22: 'Columbia', 23: 'Miami-Dade', 24: 'DeSoto', 25: 'Dixie',
    26: 'Duval', 27: 'Escambia', 28: 'Flagler', 29: 'Franklin', 30: 'Gadsden',
    31: 'Gilchrist', 32: 'Glades', 33: 'Gulf', 34: 'Hamilton', 35: 'Hardee',
    36: 'Hendry', 37: 'Hernando', 38: 'Highlands', 39: 'Hillsborough',
    40: 'Holmes', 41: 'Indian River', 42: 'Jackson', 43: 'Jefferson',
    44: 'Lafayette', 45: 'Lake', 46: 'Lee', 47: 'Leon', 48: 'Levy',
    49: 'Liberty', 50: 'Madison', 51: 'Manatee', 52: 'Marion', 53: 'Martin',
    54: 'Monroe', 55: 'Nassau', 56: 'Okaloosa', 57: 'Okeechobee', 58: 'Orange',
    59: 'Osceola', 60: 'Palm Beach', 61: 'Pasco', 62: 'Pinellas', 63: 'Polk',
    64: 'Putnam', 65: 'Saint Johns', 66: 'Saint Lucie', 67: 'Santa Rosa',
    68: 'Sarasota', 69: 'Seminole', 70: 'Sumter', 71: 'Suwannee', 72: 'Taylor',
    73: 'Union', 74: 'Volusia', 75: 'Wakulla', 76: 'Walton', 77: 'Washington'
}

PRIORITY_COUNTIES = {16, 23, 26, 39, 58, 60}  # Broward, Miami-Dade, Duval, Hillsborough, Orange, Palm Beach

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
    
    for csv_file in sorted(nal_path.glob('*.csv')):
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
        dor_uc_clean = df['DOR_UC'].astype(str).str.strip().str.zfill(3)
        mask = dor_uc_clean.isin(['003', '008'])
        filtered = df[mask].copy()
        
        if len(filtered) > 0:
            county_name = COUNTY_NAMES.get(filtered['CO_NO'].iloc[0], 'Unknown')
            print(f"  → {len(filtered)} properties with 50+ units in {county_name}")
            frames.append(filtered)
        else:
            print(f"  → 0 properties with 50+ units")
    
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
    print(f"  200+ units: {(result['NO_RES_UNTS'] >= 200).sum()}")
    print(f"Priority metros: {result[result['IS_PRIORITY']].shape[0]}")
    print(f"\nTop 10 counties by property count:")
    print(result.groupby('COUNTY_NAME').size().sort_values(ascending=False).head(10))
    print(f"\nUnit distribution:")
    print(result['NO_RES_UNTS'].describe())
    print(f"\nSaved to: {output_path}")
    
    return result

if __name__ == '__main__':
    df = ingest_all_counties(
        nal_dir='data/raw/dor_nal/',
        output_path='data/processed/base_roster.parquet'
    )
```

### Step 1.3: Geocoding — Three-Tier Strategy ($0)

#### Tier 1: County GIS Parcel Centroids (~90% coverage)

**Statewide approach:** The FL DOR also publishes GIS parcel shapefiles for all 67 counties at the same data portal (Map Data section). Download all county shapefiles, compute centroids, and join to NAL data on `PARCEL_ID`.

**Script: `02_geocode_gis.py`**
```python
import geopandas as gpd
import pandas as pd
from pathlib import Path

def geocode_from_gis(roster_path, gis_dir, output_path):
    """Join parcel centroids from county GIS shapefiles to base roster."""
    
    roster = pd.read_parquet(roster_path)
    roster['latitude'] = None
    roster['longitude'] = None
    roster['geocode_source'] = None
    
    gis_path = Path(gis_dir)
    
    for county_no in roster['CO_NO'].unique():
        county_name = COUNTY_NAMES.get(county_no, str(county_no))
        
        # Find matching shapefile (naming varies by county)
        shp_files = list(gis_path.glob(f'*{county_no}*/*.shp')) + \
                    list(gis_path.glob(f'*{county_name.lower()}*/*.shp'))
        
        if not shp_files:
            print(f"  No GIS data for {county_name} ({county_no})")
            continue
        
        parcels_gis = gpd.read_file(shp_files[0])
        
        # Standardize parcel ID column name (varies: PARCELNO, PARCEL_ID, FOLIO, etc.)
        parcel_col = None
        for candidate in ['PARCELNO', 'PARCEL_ID', 'FOLIO', 'PIN', 'PARCEL']:
            if candidate in parcels_gis.columns:
                parcel_col = candidate
                break
        
        if not parcel_col:
            print(f"  Cannot find parcel ID column in {county_name} GIS data")
            continue
        
        # Calculate centroids (reproject to WGS84 if needed)
        if parcels_gis.crs and parcels_gis.crs.to_epsg() != 4326:
            parcels_gis = parcels_gis.to_crs(epsg=4326)
        
        parcels_gis['_centroid_lat'] = parcels_gis.geometry.centroid.y
        parcels_gis['_centroid_lng'] = parcels_gis.geometry.centroid.x
        
        # Join
        county_mask = roster['CO_NO'] == county_no
        county_parcels = roster.loc[county_mask, 'PARCEL_ID'].str.strip()
        gis_lookup = parcels_gis.set_index(parcel_col)[['_centroid_lat', '_centroid_lng']]
        
        matched = county_parcels.map(lambda pid: gis_lookup.loc[pid] if pid in gis_lookup.index else None)
        # ... (apply matched lat/lng to roster)
        
        match_count = matched.notna().sum()
        print(f"  {county_name}: {match_count}/{county_mask.sum()} matched via GIS")
    
    roster.to_parquet(output_path, index=False)
    return roster
```

#### Tier 2: US Census Batch Geocoder (fallback, free)

**Script: `03_geocode_census.py`**
```python
import requests
import pandas as pd
import io
import time

CENSUS_URL = 'https://geocoding.geo.census.gov/geocoder/geographies/addressbatch'

def geocode_census_batch(addresses_df, batch_size=9999):
    """Geocode addresses using US Census Bureau batch geocoder.
    
    Input df must have columns: id, street, city, state, zip
    Max 10,000 addresses per batch.
    """
    results = []
    
    for start in range(0, len(addresses_df), batch_size):
        batch = addresses_df.iloc[start:start + batch_size]
        
        # Format: id, street, city, state, zip (no header)
        csv_data = batch[['id', 'street', 'city', 'state', 'zip']].to_csv(
            index=False, header=False
        )
        
        response = requests.post(
            CENSUS_URL,
            files={'addressFile': ('batch.csv', csv_data, 'text/csv')},
            data={'benchmark': 'Public_AR_Current', 'vintage': 'Current_Current'}
        )
        
        if response.status_code == 200:
            result_df = pd.read_csv(
                io.StringIO(response.text),
                header=None,
                names=['id', 'input_addr', 'match_flag', 'match_type', 
                       'matched_addr', 'lonlat', 'tiger_id', 'side',
                       'state_fips', 'county_fips', 'tract', 'block']
            )
            
            # Parse lon,lat from combined field
            matched = result_df[result_df['match_flag'] == 'Match'].copy()
            matched[['longitude', 'latitude']] = matched['lonlat'].str.split(',', expand=True).astype(float)
            results.append(matched[['id', 'latitude', 'longitude']])
        
        print(f"  Batch {start//batch_size + 1}: {len(batch)} submitted")
        time.sleep(2)  # Be respectful
    
    return pd.concat(results, ignore_index=True) if results else pd.DataFrame()
```

#### Tier 3: Nominatim/OpenStreetMap (last resort, free, rate-limited)

**Script: `04_geocode_nominatim.py`**

Same as previous plan — 1 req/sec, `geopy.geocoders.Nominatim` with `RateLimiter`. Only used for the ~2–5% not matched by tiers 1–2.

**Expected final coverage: 97–99%**

---

## Phase 2 — Property Names + Website URLs (Week 2–3)

**Enrichment priority strategy:** With 40,000–60,000 total properties, enriching all of them via Google Places would cost ~$700–$1,000. Instead, use a tiered approach:

1. **First pass:** Enrich only properties with 50+ units in priority metros (~5,000–6,000 props = ~$100, within free credit)
2. **Second pass:** Expand to all 50+ unit properties statewide (~8,000–10,000 props = ~$170)
3. **Third pass:** Expand to 10–49 unit properties in priority metros if needed
4. **Skip or defer:** Sub-10-unit properties (DOR_UC 008) — these rarely have marketing names or websites

Same approach as v1:
- **Google Places API** `find_place()` with physical address → returns property marketing name, website URL, phone, Google rating
- Cost: ~$17/1,000 requests. For 10,000 statewide properties ≈ $170 (covered by $200/mo free credit)
- **Apartments.com** scraping as supplement for unmatched properties

---

## Phase 3 — Management Company Enrichment (Week 3–4)

Same as v1 plan:
1. REIT portfolio pages (free, ~40% coverage)
2. HUD/FHFC databases for subsidized properties
3. Apartments.com detail scraping for remaining gaps
4. Optional: ALN Apartment Data commercial subscription (~$31K/yr)

---

## Phase 4 — Database + Dashboard (Week 4–5)

### PostgreSQL Schema (updated for statewide)

```sql
CREATE TABLE fl_multifamily (
    id SERIAL PRIMARY KEY,
    co_no SMALLINT NOT NULL,
    county_name VARCHAR(50) NOT NULL,
    parcel_id VARCHAR(30) NOT NULL,
    is_priority_metro BOOLEAN DEFAULT FALSE,
    
    -- Property identity
    property_name VARCHAR(255),
    
    -- Physical location
    phy_addr1 VARCHAR(255),
    phy_addr2 VARCHAR(100),
    phy_city VARCHAR(100) NOT NULL,
    phy_zipcd VARCHAR(10) NOT NULL,
    latitude DECIMAL(10, 7),
    longitude DECIMAL(10, 7),
    geocode_source VARCHAR(20),  -- 'county_gis', 'census', 'nominatim', 'google'
    
    -- Property characteristics
    dor_uc VARCHAR(3) DEFAULT '003',
    no_res_units INTEGER NOT NULL,
    no_buildings INTEGER,
    act_yr_built INTEGER,
    eff_yr_built INTEGER,
    tot_lvg_area INTEGER,  -- total living sqft
    
    -- Valuation
    just_value BIGINT,
    assessed_value BIGINT,
    taxable_value BIGINT,
    land_value BIGINT,
    
    -- Ownership
    owner_name VARCHAR(255),
    owner_addr1 VARCHAR(255),
    owner_city VARCHAR(100),
    owner_state VARCHAR(2),
    owner_zipcd VARCHAR(10),
    
    -- Enriched fields
    management_company VARCHAR(255),
    website_url VARCHAR(500),
    google_place_id VARCHAR(100),
    google_rating DECIMAL(2, 1),
    
    -- Metadata
    data_year INTEGER,
    last_enriched TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE (co_no, parcel_id)
);

-- Indexes for common dashboard queries
CREATE INDEX idx_county ON fl_multifamily(co_no);
CREATE INDEX idx_county_name ON fl_multifamily(county_name);
CREATE INDEX idx_city ON fl_multifamily(phy_city);
CREATE INDEX idx_zipcode ON fl_multifamily(phy_zipcd);
CREATE INDEX idx_units ON fl_multifamily(no_res_units);
CREATE INDEX idx_mgmt ON fl_multifamily(management_company);
CREATE INDEX idx_year_built ON fl_multifamily(act_yr_built);
CREATE INDEX idx_priority ON fl_multifamily(is_priority_metro);
CREATE INDEX idx_value ON fl_multifamily(just_value);

-- PostGIS spatial index (requires PostGIS extension)
-- CREATE EXTENSION IF NOT EXISTS postgis;
-- CREATE INDEX idx_geo ON fl_multifamily USING GIST (
--     ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)
-- );
```

### Dashboard: Streamlit + Pydeck

**Layout:**

```
┌──────────────────────────────────────────────────────────────┐
│  🏢 Florida Multifamily Directory          [Export CSV] [⚙️]  │
├────────────┬─────────────────────────────────────────────────┤
│ FILTERS    │                                                 │
│            │        Interactive Map (Pydeck)                 │
│ View:      │     • ScatterplotLayer with size = units        │
│ ○ State    │     • Color-coded by county or mgmt company     │
│ ● Priority │     • Click for property detail popup           │
│ ○ County   │     • Cluster at zoom-out levels                │
│            │                                                 │
│ County: [▼]│                                                 │
│ City:   [▼]│                                                 │
│ ZIP:    [▼]│                                                 │
│ Units: [==]│     • Min 2 units → slider default, user picks threshold│
│ Year:  [==]│                                                 │
│ Mgmt:  [▼]│                                                 │
│ Value: [==]│                                                 │
├────────────┴─────────────────────────────────────────────────┤
│  KPIs: Total Props │ Total Units │ Avg Units │ Median Value  │
├──────────────────────────────────────────────────────────────┤
│  Sortable/Searchable Data Table                               │
│  Name | Address | City | ZIP | Units | Mgmt | Year | Value   │
├──────────────────────────────────────────────────────────────┤
│  Charts: Top Mgmt Cos │ Units by County │ Year Built Dist    │
└──────────────────────────────────────────────────────────────┘
```

**Key libraries:**
```
streamlit
pydeck
pandas
geopandas
pyarrow  # for parquet
plotly   # for charts
rapidfuzz  # for fuzzy matching
requests
geopy
```

---

## Project File Structure

```
fl-multifamily-directory/
├── data/
│   ├── raw/
│   │   ├── dor_nal/              # All 67 county NAL CSVs
│   │   ├── dor_gis/              # All 67 county GIS shapefiles
│   │   ├── hud_lihtc/            # HUD LIHTC database
│   │   └── shimberg/             # Shimberg AHI data
│   ├── processed/
│   │   ├── base_roster.parquet   # After Phase 1.2
│   │   ├── geocoded.parquet      # After Phase 1.3
│   │   └── enriched.parquet      # After Phase 2–3
│   └── final/
│       └── fl_multifamily.parquet
├── scripts/
│   ├── 01_ingest_dor.py          # Ingest all 67 counties
│   ├── 02_geocode_gis.py         # Tier 1: County GIS centroids
│   ├── 03_geocode_census.py      # Tier 2: Census batch geocoder
│   ├── 04_geocode_nominatim.py   # Tier 3: OSM Nominatim
│   ├── 05_enrich_google_places.py
│   ├── 06_scrape_reit_portfolios.py
│   ├── 07_scrape_apartments_com.py
│   ├── 08_enrich_hud_fhfc.py
│   ├── 09_merge_deduplicate.py
│   ├── 10_load_postgres.py
│   └── utils/
│       ├── county_lookup.py
│       ├── address_cleaner.py
│       └── fuzzy_matcher.py
├── dashboard/
│   ├── app.py
│   ├── pages/
│   │   ├── 1_🗺️_Map.py
│   │   ├── 2_📊_Analytics.py
│   │   └── 3_🔍_Search.py
│   ├── components/
│   │   ├── filters.py
│   │   ├── map_layer.py
│   │   └── data_table.py
│   └── requirements.txt
├── notebooks/
│   ├── 00_explore_nal_schema.ipynb
│   ├── 01_eda_base_roster.ipynb
│   ├── 02_geocode_quality.ipynb
│   └── 03_enrichment_coverage.ipynb
├── config.py
├── requirements.txt
└── README.md
```

---

## Budget Summary (Statewide — All Multifamily)

| Item | Cost | Notes |
|---|---|---|
| FL DOR NAL data (67 counties) | Free | CSV downloads from Data Portal |
| FL DOR GIS shapefiles (67 counties) | Free | From same Data Portal |
| US Census Geocoder | Free | Batch API, no key needed |
| Nominatim | Free | 1 req/sec rate limit |
| Google Places API (tiered) | ~$100–$1,000 | Start with 50+ unit priority metros ($100 within free credit); expand as needed |
| HUD/FHFC/Shimberg data | Free | CSV downloads |
| Apartments.com scraping | Free | Time + optional proxy cost |
| REIT portfolio scraping | Free | Time |
| PostgreSQL | Free | Local or Supabase free tier |
| Streamlit Cloud | Free | 1 app on community tier |
| **Total (MVP)** | **~$0–$100** | **Priority metros 50+ units only** |
| **Total (Full enrichment)** | **~$500–$1,000** | **All properties statewide** |

---

## Timeline

| Week | Phase | Deliverable |
|---|---|---|
| 1 | Download NAL + GIS for 67 counties | Raw data acquired |
| 1–2 | Ingest, filter, geocode | `base_roster.parquet` with lat/lng |
| 2–3 | Google Places enrichment | Property names + URLs added |
| 3–4 | Management company enrichment | REIT + HUD + scraping |
| 4 | Merge, deduplicate, load to DB | `fl_multifamily.parquet` + PostgreSQL |
| 5 | Dashboard build | Streamlit app deployed |
| Ongoing | Quarterly refresh | Re-download NAL, re-enrich new props |

---

## Key Data Acquisition Contacts

| Resource | Contact/URL |
|---|---|
| FL DOR NAL data requests | PTOTechnology@floridarevenue.com |
| FL DOR Data Portal | https://floridarevenue.com/property/Pages/DataPortal.aspx |
| FL DOR GIS downloads | Same portal, "Map Data" section |
| 2025 NAL User's Guide | https://floridarevenue.com/property/dataportal/Documents/PTO%20Data%20Portal/User%20Guides/2025%20Users%20guide%20and%20quick%20reference/2025_NAL_SDF_NAP_Users_Guide.pdf |
| HUD LIHTC Database | https://www.huduser.gov/portal/datasets/lihtc/property.html |
| Shimberg Center | http://flhousingdata.shimberg.ufl.edu |
| US Census Geocoder | https://geocoding.geo.census.gov/geocoder/ |
