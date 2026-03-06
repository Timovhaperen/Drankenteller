import csv
import json
import io
from urllib.request import urlopen

# Google Sheet als CSV URL
SHEET_ID = "1dkgtS8fqWggD2-za5gD2U2gtiT1OsVG0yvXyEnxMCGs"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

try:
    print("Downloading Google Sheet...")
    
    # Download CSV
    with urlopen(CSV_URL) as response:
        csv_text = response.read().decode('utf-8')
    
    print(f"CSV downloaded, length: {len(csv_text)}")
    print("First 200 chars:")
    print(csv_text[:200])
    
    # Parse CSV
    prices = {}
    lines = csv_text.strip().split('\n')
    
    # Skip header (eerste regel)
    for i, line in enumerate(lines[1:], 1):
        parts = line.split(',')
        if len(parts) >= 2:
            drank = parts[0].strip().strip('"')
            prijs_str = parts[1].strip().strip('"')
            
            try:
                prijs = float(prijs_str)
                if drank and prijs >= 0:
                    prices[drank] = prijs
                    print(f"✓ {drank}: €{prijs}")
            except ValueError:
                print(f"✗ Could not parse price for {drank}: '{prijs_str}'")
    
    # Write prices.json
    with open('prices.json', 'w', encoding='utf-8') as f:
        json.dump(prices, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Success! {len(prices)} prijzen opgeslagen in prices.json")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
