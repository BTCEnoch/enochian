import json

# Load the main governors data
with open('governors_dossier.json', 'r', encoding='utf-8') as f:
    main_data = json.load(f)

# Load the enriched data
with open('governors_47_91_dossier_enriched.json', 'r', encoding='utf-8') as f:
    enriched_data = json.load(f)

print("Checking for mismatches between main and enriched data...")
print("=" * 70)

# Check governor #52 specifically
main_52 = next((gov for gov in main_data if gov.get('number') == 52), None)
enriched_52 = next((gov for gov in enriched_data if gov.get('number') == 52), None)

print(f"Main file #52: {main_52.get('name') if main_52 else 'NOT FOUND'}")
print(f"Enriched file #52: {enriched_52.get('name') if enriched_52 else 'NOT FOUND'}")

if main_52 and enriched_52:
    print(f"\nMismatch detected!")
    print(f"Main #52 has tarot: {main_52.get('canonical_traits', {}).get('tarot')}")
    print(f"Enriched #52 has tarot: {enriched_52.get('canonical_traits', {}).get('tarot')}")

# Check all governors 47-91 for name mismatches
print(f"\nChecking all governors 47-91 for name mismatches:")
mismatches = []

for num in range(47, 92):
    main_gov = next((gov for gov in main_data if gov.get('number') == num), None)
    enriched_gov = next((gov for gov in enriched_data if gov.get('number') == num), None)
    
    main_name = main_gov.get('name') if main_gov else 'MISSING'
    enriched_name = enriched_gov.get('name') if enriched_gov else 'MISSING'
    
    if main_name != enriched_name:
        mismatches.append((num, main_name, enriched_name))
        print(f"  {num:2d}: Main='{main_name}' vs Enriched='{enriched_name}'")

print(f"\nTotal mismatches: {len(mismatches)}")

# Check current tarot/sephirah coverage
print(f"\nCurrent tarot/sephirah coverage:")
total_with_tarot = sum(1 for gov in main_data if gov.get('canonical_traits', {}).get('tarot'))
total_with_sephirah = sum(1 for gov in main_data if gov.get('canonical_traits', {}).get('sephirah'))

range_47_91_with_tarot = sum(1 for gov in main_data 
                           if 47 <= gov.get('number', 0) <= 91 
                           and gov.get('canonical_traits', {}).get('tarot'))

print(f"Total governors with tarot: {total_with_tarot}/{len(main_data)}")
print(f"Total governors with sephirah: {total_with_sephirah}/{len(main_data)}")
print(f"Governors 47-91 with tarot: {range_47_91_with_tarot}/45")

# Show the specific issue with NABAOMI
if main_52:
    canonical = main_52.get('canonical_traits', {})
    print(f"\nNABAOMI (#52) current data:")
    print(f"  tarot: {canonical.get('tarot')}")
    print(f"  sephirah: {canonical.get('sephirah')}")
    print(f"  Has complete data: {bool(canonical.get('tarot') and canonical.get('sephirah'))}") 