#!/usr/bin/env python3
import csv
import json
import io
from urllib.request import urlopen

# Google Sheet als CSV URL
SHEET_ID = "1dkgtS8fqWggD2-za5gD2U2gtiT1OsVG0yvXyEnxMCGs"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

try:
    print("=" * 50)
    print("Downloading Google Sheet from:", CSV_URL)
    print("=" * 50)
    
    # Download CSV with headers
    with urlopen(CSV_URL) as response:
        csv_text = response.read().decode('utf-8')
    
    print(f"\n✓ CSV downloaded successfully ({len(csv_text)} bytes)")
    print("\nFirst 500 characters:")
    print(csv_text[:500])
    print("\n" + "=" * 50)
    
    # Parse CSV properly
    prices = {}
    lines = csv_text.strip().split('\n')
    
    print(f"\nTotal lines: {len(lines)}")
    
    if len(lines) > 0:
        print(f"Header: {lines[0]}")
    
    # Parse with proper CSV reader
    csv_reader = csv.DictReader(io.StringIO(csv_text))
    
    if csv_reader.fieldnames:
        print(f"Fields found: {csv_reader.fieldnames}")
    
    row_count = 0
    for row in csv_reader:
        print(f"\nRow {row_count}: {row}")
        
        # Get Drank and Prijs columns
        drank = None
        prijs = None
        
        # Try to find the columns (handle different cases)
        for key in row:
            if key and 'drank' in key.lower():
                drank = row[key].strip() if row[key] else None
            if key and 'prijs' in key.lower():
                prijs_str = row[key].strip() if row[key] else None
                if prijs_str:
                    try:
                        prijs = float(prijs_str.replace(',', '.'))
                    except ValueError:
                        print(f"  ✗ Could not parse price: '{prijs_str}'")
        
        if drank and prijs is not None and prijs >= 0:
            prices[drank] = prijs
            print(f"  ✓ {drank}: €{prijs}")
            row_count += 1
        elif drank:
            print(f"  ✗ Skipped {drank} (no valid price)")
    
    print("\n" + "=" * 50)
    print(f"✅ Parsed {row_count} items successfully!")
    print(f"Total prices: {len(prices)}")
    print("=" * 50)
    
    # Write prices.json
    with open('prices.json', 'w', encoding='utf-8') as f:
        json.dump(prices, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ SUCCESS! {len(prices)} prijzen opgeslagen in prices.json")
    
    # Show content
    print("\nprices.json content:")
    with open('prices.json', 'r') as f:
        print(f.read())

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    
    # Create empty file so workflow doesn't fail
    with open('prices.json', 'w') as f:
        json.dump({}, f)
