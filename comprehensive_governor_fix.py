import json
from copy import deepcopy

# Load the current data
with open('governors_dossier.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("🔧 COMPREHENSIVE GOVERNOR FORMATTING FIX")
print("=" * 60)

# Track what we're fixing
structural_fixes = []
missing_data_report = []

def generate_template_content(governor_name, element, field_type):
    """Generate template content for missing fields"""
    templates = {
        'angelic_role': f"Guardian of {element.lower()} mysteries; commands legions of elemental spirits in service of the cosmic order.",
        'challenge': f"On-chain quest unique to {governor_name} requiring alignment with {element.lower()} cycles and demonstration of elemental mastery.",
        'wisdom': f"In the words of {governor_name}, 'True power lies in balanced mastery of {element.lower()}'s sacred mysteries.'",
        'essence': f"{governor_name} channels the archetypal potency of {element.lower()} toward mastery of their sacred domains.",
        'themes': "Transformation, mastery, balance; shadowed by the perils of elemental excess.",
        'tokens': f"Offer ritual tokens attuned to {element.lower()}; avoid discordant offerings that disturb elemental harmony.",
        'boon': f"Grants boon aligned with {element.lower()}, balanced by a commensurate sacrifice to maintain cosmic equilibrium.",
        'verse': f"{governor_name} whispers, 'As above, so below—within the {element.lower()}, eternal wisdom flows.'"
    }
    return templates.get(field_type, f"[Template content for {field_type}]")

# Process each governor
for i, gov in enumerate(data):
    name = gov.get('name', 'UNKNOWN')
    number = gov.get('number', 'UNKNOWN')
    
    # Skip NABAOMI - it's already perfect
    if name == 'NABAOMI':
        continue
    
    governor_missing = []
    
    # Check if this is a flat structure governor (47-91 except NABAOMI)
    if number >= 47 and 'canonical_traits' not in gov:
        print(f"🔄 Converting {name} (#{number}) from flat to nested structure...")
        
        # Create new nested structure
        new_gov = {
            'number': number,
            'name': name,
            'canonical_traits': {},
            'interpretive_traits': {},
            'visual_description': gov.get('visual_description', '')
        }
        
        # Map flat fields to canonical_traits
        canonical_mapping = {
            'aethyr': 'aethyr',
            'element': 'element', 
            'personality_traits': 'personality_traits',
            'domains_of_knowledge': 'domains',
            'tarot_attribution': 'tarot',
            'kabbalistic_correspondence': 'sephirah',
            'zodiac_angel': 'zodiac_angel',
            'translation': 'translation'
        }
        
        for old_field, new_field in canonical_mapping.items():
            if old_field in gov:
                new_gov['canonical_traits'][new_field] = gov[old_field]
        
        # Extract visual_emblem from visual_description if needed
        visual_desc = gov.get('visual_description', '')
        if visual_desc and 'visual_emblem' not in new_gov['canonical_traits']:
            # Try to extract emblem from description
            if '—' in visual_desc:
                emblem = visual_desc.split('—')[0].strip()
                new_gov['canonical_traits']['visual_emblem'] = emblem
        
        # Map interpretive fields
        interpretive_mapping = {
            'essence': 'essence',
            'themes': 'themes', 
            'wisdom': 'wisdom',
            'tokens': 'tokens',
            'challenge': 'challenge',
            'boon': 'boon',
            'verse': 'verse',
            'angelic_role': 'angelic_role'
        }
        
        # Get existing interpretive traits or create empty dict
        existing_interpretive = gov.get('interpretive_traits', {})
        
        for field in interpretive_mapping:
            if field in existing_interpretive:
                new_gov['interpretive_traits'][field] = existing_interpretive[field]
            else:
                # Generate template content
                element = new_gov['canonical_traits'].get('element', 'Spirit')
                new_gov['interpretive_traits'][field] = generate_template_content(name, element, field)
                governor_missing.append(f"{field} (template generated)")
        
        # Replace the old governor with new structure
        data[i] = new_gov
        structural_fixes.append(f"#{number} {name}")
        
    else:
        # This is a governors 1-46 - check for missing interpretive fields
        interpretive = gov.get('interpretive_traits', {})
        element = gov.get('canonical_traits', {}).get('element', 'Spirit')
        
        required_interpretive = ['angelic_role', 'challenge', 'wisdom', 'essence', 'themes', 'tokens', 'boon', 'verse']
        
        for field in required_interpretive:
            if field not in interpretive:
                interpretive[field] = generate_template_content(name, element, field)
                governor_missing.append(f"{field} (template generated)")
    
    # Add to missing data report if anything was missing
    if governor_missing:
        missing_data_report.append({
            'number': number,
            'name': name,
            'missing_fields': governor_missing
        })

# Save the fixed data
with open('governors_dossier.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\n✅ STRUCTURAL FIXES COMPLETED: {len(structural_fixes)} governors")
print("-" * 50)
for fix in structural_fixes:
    print(f"  {fix}")

print(f"\n📋 MISSING DATA REPORT")
print("=" * 60)
print(f"Total governors with missing data: {len(missing_data_report)}")

# Group by type of missing data
missing_by_field = {}
for gov_report in missing_data_report:
    for field in gov_report['missing_fields']:
        field_name = field.split(' (')[0]  # Remove "(template generated)"
        if field_name not in missing_by_field:
            missing_by_field[field_name] = []
        missing_by_field[field_name].append(f"#{gov_report['number']} {gov_report['name']}")

print("\n📊 MISSING DATA BY FIELD:")
print("-" * 30)
for field, governors in sorted(missing_by_field.items()):
    print(f"\n{field.upper()} - {len(governors)} governors:")
    for gov in sorted(governors):
        print(f"  {gov}")

print(f"\n🎉 SUMMARY:")
print(f"  Total governors processed: {len(data)}")
print(f"  Structural conversions: {len(structural_fixes)}")
print(f"  Template content generated: {sum(len(report['missing_fields']) for report in missing_data_report)} fields")
print(f"  All governors now have complete structure!")

print(f"\n💡 NEXT STEPS:")
print("  1. Run the generator to test the new structure")
print("  2. Review template content and replace with rich content as desired")
print("  3. All governors now have uniform formatting!") 