import os
import requests
import zipfile
import io
import time
from pathlib import Path
from urllib.parse import quote

# Base URL for the 2025 Final NAL files
BASE_URL = "https://floridarevenue.com/property/dataportal/Documents/PTO%20Data%20Portal/Tax%20Roll%20Data%20Files/NAL/2025F/"

# List of filenames provided by user
# Note: Filenames must match exactly what is on the server.
NAL_FILES = [
    "Alachua 11 Final NAL 2025.zip", "Baker 12 Final NAL 2025.zip", "Bay 13 Final NAL 2025.zip",
    "Bradford 14 Final NAL 2025.zip", "Brevard 15 Final NAL 2025.zip", "Broward 16 Final NAL 2025.zip",
    "Calhoun 17 Final NAL 2025.zip", "Charlotte 18 Final NAL 2025.zip", "Citrus 19 Final NAL 2025.zip",
    "Clay 20 Final NAL 2025.zip", "Collier 21 Final NAL 2025.zip", "Columbia 22 Final NAL 2025.zip",
    "Dade 23 Final NAL 2025.zip", "Desoto 24 Final NAL 2025.zip", "Dixie 25 Final NAL 2025.zip",
    "Duval 26 Final NAL 2025.zip", "Escambia 27 Final NAL 2025.zip", "Flagler 28 Final NAL 2025.zip",
    "Franklin 29 Final NAL 2025.zip", "Gadsden 30 Final NAL 2025.zip", "Gilchrist 31 Final NAL 2025.zip",
    "Glades 32 Final NAL 2025.zip", "Gulf 33 Final NAL 2025.zip", "Hamilton 34 Final NAL 2025.zip",
    "Hardee 35 Final NAL 2025.zip", "Hendry 36 Final NAL 2025.zip", "Hernando 37 Final NAL 2025.zip",
    "Highlands 38 Final NAL 2025.zip", "Hillsborough 39 Final NAL 2025.zip", "Holmes 40 Final NAL 2025.zip",
    "Indian River 41 Final NAL 2025.zip", "Jackson 42 Final NAL 2025.zip", "Jefferson 43 Final NAL 2025.zip",
    "Lafayette 44 Final NAL 2025.zip", "Lake 45 Final NAL 2025.zip", "Lee 46 Final NAL 2025.zip",
    "Leon 47 Final NAL 2025.zip", "Levy 48 Final NAL 2025.zip", "Liberty 49 Final NAL 2025.zip",
    "Madison 50 Final NAL 2025.zip", "Manatee 51 Final NAL 2025.zip", "Marion 52 Final NAL 2025.zip",
    "Martin 53 Final NAL 2025.zip", "Monroe 54 Final NAL 2025.zip", "Nassau 55 Final NAL 2025.zip",
    "Okaloosa 56 Final NAL 2025.zip", "Okeechobee 57 Final NAL 2025.zip", "Orange 58 Final NAL 2025.zip",
    "Osceola 59 Final NAL 2025.zip", "Palm Beach 60 Final NAL 2025.zip", "Pasco 61 Final NAL 2025.zip",
    "Pinellas 62 Final NAL 2025.zip", "Polk 63 Final NAL 2025.zip", "Putnam 64 Final NAL 2025.zip",
    "Saint Johns 65 Final NAL 2025.zip", "Saint Lucie 66 Final NAL 2025.zip", "Santa Rosa 67 Final NAL 2025.zip",
    "Sarasota 68 Final NAL 2025.zip", "Seminole 69 Final NAL 2025.zip", "Sumter 70 Final NAL 2025.zip",
    "Suwannee 71 Final NAL 2025.zip", "Taylor 72 Final NAL 2025.zip", "Union 73 Final NAL 2025.zip",
    "Volusia 74 Final NAL 2025.zip", "Wakulla 75 Final NAL 2025.zip", "Walton 76 Final NAL 2025.zip",
    "Washington 77 Final NAL 2025.zip"
]

def download_and_extract(output_dir):
    """Download extract NAL files."""
    
    raw_dir = Path(output_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    # Session headers to look like a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for filename in NAL_FILES:
        # Construct URL (handling spaces)
        # We need to quote the component parts
        # The path part .../NAL/2025F/ is fixed. The filename needs encoding.
        encoded_filename = quote(filename) 
        # But wait, python requests handles full url, but spaces in URL string are invalid.
        # "Documents/PTO Data Portal/..." also has spaces.
        # Let's quote the whole path segment or just handle the filename if base is standard.
        # safely construct the full url
        # The base url in browser usually has %20 for spaces.
        
        # Let's try fully encoded URL construction manually or use requests to handle params?
        # Parameters? No, it's a path.
        
        # Let's clean the base url
        clean_base = BASE_URL.replace(" ", "%20")
        clean_filename = filename.replace(" ", "%20")
        
        file_url = f"{clean_base}{clean_filename}"
        
        print(f"Downloading {filename}...")
        
        try:
            r = requests.get(file_url, headers=headers, stream=True)
            if r.status_code == 200:
                # Save zip
                zip_path = raw_dir / filename
                with open(zip_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                print(f"  Saved zip. Extracting...")
                
                # Extract
                try:
                    with zipfile.ZipFile(zip_path, 'r') as z:
                        z.extractall(raw_dir)
                    print(f"  Extracted.")
                    
                    # Optional: Remove zip to save space
                    os.remove(zip_path)
                    
                except zipfile.BadZipFile:
                    print(f"  Error: Bad zip file.")
            else:
                print(f"  Failed: HTTP {r.status_code}")
                # Try fallback for 'Dade' -> 'Miami-Dade' or vice-versa?
                if "Dade" in filename:
                    print("  Retrying with 'Miami-Dade' prefix...")
                    alt_name = filename.replace("Dade", "Miami-Dade")
                    clean_alt = alt_name.replace(" ", "%20")
                    alt_url = f"{clean_base}{clean_alt}"
                    r_alt = requests.get(alt_url, headers=headers)
                    if r_alt.status_code == 200:
                         zip_path = raw_dir / alt_name
                         with open(zip_path, 'wb') as f:
                            f.write(r_alt.content)
                         with zipfile.ZipFile(zip_path, 'r') as z:
                            z.extractall(raw_dir)
                         os.remove(zip_path)
                         print("  Success with Miami-Dade.")
                    else:
                        print(f"  Retry failed: {r_alt.status_code}")

        except Exception as e:
            print(f"  Exception: {e}")
            
        time.sleep(1) # Be nice to server

if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent
    download_and_extract(str(base_dir / 'data/raw/dor_nal'))
