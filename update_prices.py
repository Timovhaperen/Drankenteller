import csv
import json
import urllib.request

# Google Sheet als CSV URL
SHEET_ID = "1dkgtS8fqWggD2-za5gD2U2gtiT1OsVG0yvXyEnxMCGs"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

# Download CSV
try:
    with urllib.request.urlopen(CSV_URL) as response:
        csv_data = response.read().decode('utf-8')
    
    # Parse CSV naar JSON
    prices = {}
    reader = csv.DictReader(csv_data.strip().split('\n'))
    
    for row in reader:
        if row and 'Drank' in row and 'Prijs' in row:
            drank = row['Drank'].strip()
            try:
                prijs = float(row['Prijs'].strip())
                if drank and prijs >= 0:
                    prices[drank] = prijs
            except ValueError:
                pass
    
    # Schrijf naar prices.json
    with open('prices.json', 'w', encoding='utf-8') as f:
        json.dump(prices, f, ensure_ascii=False, indent=2)
    
    print(f"✅ {len(prices)} prijzen opgeslagen in prices.json")

except Exception as e:
    print(f"❌ Fout: {e}")
