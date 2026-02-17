import requests
import zipfile
import io
import os
from pathlib import Path

# URL for Florida Statewide Parcels 2025 (Shapefile download)
# Sourced from Florida Geographic Information Office (FGIO) Open Data Portal
# Using the direct download link for the Shapefile format if available, or the Feature Service query.
# Actually, FGIO typically offers a direct download for "Florida Statewide Parcels".
# Let's use the 2024 export (often labeled "2025" in NAL context if assessment year is 2025)
# or just "Florida Statewide Parcels". 
# Found URL pattern from similar open data portals:
# https://floridagio.gov/datasets/[ID]_0/explore -> Download -> Shapefile
#
# A reliable direct link for the statewide zip is preferred.
# The search results mentioned "2025 authoritative statewide parcel data".
#
# Let's try downloading the "Florida Statewide Parcels" zip from the standard FGIO/ArcGIS hub URL.
# If that fails, we might need to download county by county if they are separated.
# But often there is a "Statewide" unified file.

# URL from typical FGIO structure (feature server export)
# https://www.arcgis.com/sharing/rest/content/items/[ITEM_ID]/data
# We need the Item ID for "Florida Statewide Parcels".
#
# Alternatively, use the user's portal structure if it exists.
# The user's portal "Tax Roll Data Files" might have a "Map Data" folder.
# Let's check if we can guess the URL: 
# https://floridarevenue.com/property/dataportal/Documents/PTO%20Data%20Portal/Map%20Data/
#
# Let's try to probe that path in the script first.

URL_DOR_MAP_DATA = "https://floridarevenue.com/property/dataportal/Documents/PTO%20Data%20Portal/Map%20Data/"
# It usually contains county zips like "11_Alachua_2025.zip" or similar.

def download_gis_data(output_dir):
    """Download GIS shapefiles."""
    
    gis_dir = Path(output_dir)
    gis_dir.mkdir(parents=True, exist_ok=True)
    
    print("Checking FL DOR Map Data directory...")
    
    # Since we can't easily list files on the IIS server without directory browsing enabled (which seemed to fail in browser),
    # we might need to rely on the valid NAL logic: County Name + ID.
    # The search result said: "Department typically collects county GIS parcel shapefiles every April".
    # And "Map Data directory".
    
    # Let's try a test download for Alachua to see the naming convention.
    # Possible names:
    # "Alachua 11 2025.zip"
    # "11 Alachua 2025.zip"
    # "11_Alachua_2025.zip"
    # "Alachua 2025.zip"
    
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    
    # User's NAL pattern: "Alachua 11 Final NAL 2025.zip"
    # Maybe GIS is "Alachua 11 Final GIS 2025.zip"?
    # Or "Alachua 11 Map 2025.zip"?
    
    # Let's try to query the Statewide Parcels from FGIO instead which is a single giant file? 
    # Or per county. The geocoding script `02_geocode_gis.py` expects per-county files (or folders).
    # "list(gis_path.glob(f'*{county_no}*/*.shp'))"
    
    # Let's try to download Alachua from DOR with a few guesses.
    base_url = "https://floridarevenue.com/property/dataportal/Documents/PTO%20Data%20Portal/Map%20Data/"
    years = ["2025", "2024"]
    patterns = [
        "{county} {id} Parcel Data {year}.zip",
        "{id} {county} Parcel Data {year}.zip",
        "{county}_{id}_{year}.zip",
        "{county} {id} Final SDF {year}.zip"  # SDF is Standard Data File (often has geometry?) No, SDF is textual.
    ]
    
    # Actually, FGIO is the safer bet for 2025.
    # https://floridagio.gov/search?q=parcels
    
    print("For now, please manually download the GIS files if automatic guess fails.")
    print("Trying Alachua test...")
    
    test_url = base_url + "Alachua%2011%20Parcel%20Data%202025.zip" # Guess
    r = requests.head(test_url, headers=headers)
    print(f"Guess 1 ({test_url}): {r.status_code}")
    
    # If the user can provide the link from the "Map Data" section of the portal, that would be best.
    
if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent
    download_gis_data(str(base_dir / 'data/raw/dor_gis'))
