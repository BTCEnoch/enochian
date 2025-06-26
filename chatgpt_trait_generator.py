#!/usr/bin/env python3
"""
ChatGPT Trait Generator for Enochian Governors
This script generates trait justifications for governors using ChatGPT's built-in capabilities.
No API keys required - designed to be run directly by ChatGPT.
"""

import json
import os

def load_governors_data():
    """Load the complete governors data"""
    try:
        # Try the enhanced file first
        if os.path.exists('csv_columns/enochian_governors_advanced.json'):
            with open('csv_columns/enochian_governors_advanced.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        # Fallback to main dossier
        elif os.path.exists('governors_dossier.json'):
            with open('governors_dossier.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print("Error: Could not find governor data files")
            return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None

def create_character_prompt(gov_data):
    """Generate complete character embodiment prompt"""
    name = gov_data.get("name", "Unknown")
    number = gov_data.get("number", "Unknown")
    
    # Handle different data structures
    if "canonical_traits" in gov_data:
        # New structure
        canonical = gov_data.get("canonical_traits", {})
        interpretive = gov_data.get("interpretive_traits", {})
        
        translation = canonical.get("translation", "")
        aethyr = canonical.get("aethyr", "")
        element = canonical.get("element", "")
        essence = interpretive.get("essence", "")
        role = interpretive.get("angelic_role", "")
        traits = canonical.get("personality_traits", [])
        
        # Archetypal data
        tarot = canonical.get("tarot", "")
        sephirot = canonical.get("sephirah", "")
        zodiac_angel = canonical.get("zodiac_angel", "")
        visual_emblem = canonical.get("visual_emblem", "")
        
    else:
        # Legacy structure
        translation = gov_data.get("translation", "")
        aethyr = gov_data.get("aethyr", "")
        element = gov_data.get("element", "")
        essence = gov_data.get("essence", "")
        role = gov_data.get("angelic role", "")
        traits = gov_data.get("traits", [])
        
        archetypal = gov_data.get("archetypal", {})
        tarot = archetypal.get("tarot", "")
        sephirot = archetypal.get("sephirot", "")
        zodiac_angel = archetypal.get("zodiac_angel", "")
        visual_emblem = ""
    
    # Visual description data (if available)
    visual = gov_data.get("visual_description", {})
    clothing = visual.get("clothing", "")
    aura = visual.get("aura", "")
    physical_features = visual.get("physical_features", "")
    familiars = visual.get("familiars", "")
    artifacts = visual.get("artifacts", "")
    voice = visual.get("voice", "")
    movement = visual.get("movement", "")
    environment = visual.get("environment", "")
    
    prompt = f"""CHARACTER EMBODIMENT REQUEST:

You are {name}, the {number}th Enochian Governor. Fully embody this character and respond from their first-person perspective.

CANONICAL IDENTITY:
Name: {name} (#{number})
Translation: {translation}
Aethyr: {aethyr}
Element: {element}
Essence: {essence}
Angelic Role: {role}

ARCHETYPAL CORRESPONDENCES:
Tarot: {tarot}
Sephirot: {sephirot}
Zodiac Angel: {zodiac_angel}
Visual Emblem: {visual_emblem}

PHYSICAL MANIFESTATION:
Clothing: {clothing}
Aura: {aura}
Physical Features: {physical_features}
Familiars: {familiars}
Artifacts: {artifacts}
Voice: {voice}
Movement: {movement}
Environment: {environment}

TRAITS TO JUSTIFY:
{', '.join(traits)}

TASK: As {name}, provide a one-sentence first-person justification for each trait above. Explain why this trait manifests in your character based on your complete canonical nature. Respond as the character would, using "I" statements.

FORMAT: Respond with ONLY a valid JSON object like this:
{{
  "trait_name": "I [first-person justification based on your essence, role, and manifestation]",
  "trait_name": "I [first-person justification based on your essence, role, and manifestation]"
}}"""
    
    return prompt

def process_single_governor(governor_name=None, governor_number=None):
    """Process a single governor and return the prompt"""
    governors = load_governors_data()
    if not governors:
        return None
    
    # Find the specified governor
    target_gov = None
    if governor_name:
        target_gov = next((gov for gov in governors if gov.get("name", "").upper() == governor_name.upper()), None)
    elif governor_number:
        target_gov = next((gov for gov in governors if gov.get("number") == governor_number), None)
    
    if not target_gov:
        print(f"Governor not found: {governor_name or governor_number}")
        return None
    
    return create_character_prompt(target_gov)

def process_all_governors():
    """Generate prompts for all governors"""
    governors = load_governors_data()
    if not governors:
        return None
    
    print(f"Loaded {len(governors)} governors")
    
    # Create output directory
    os.makedirs("governor_profiles", exist_ok=True)
    
    results = []
    for gov in governors:
        prompt = create_character_prompt(gov)
        results.append({
            "governor": gov.get("name"),
            "number": gov.get("number"),
            "prompt": prompt
        })
    
    return results

def save_prompts_to_file(results, filename="governor_prompts.json"):
    """Save all prompts to a file for ChatGPT processing"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(results)} governor prompts to {filename}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Process single governor
        governor_identifier = sys.argv[1]
        
        # Check if it's a number or name
        if governor_identifier.isdigit():
            prompt = process_single_governor(governor_number=int(governor_identifier))
        else:
            prompt = process_single_governor(governor_name=governor_identifier)
        
        if prompt:
            print("="*80)
            print("COPY THIS PROMPT TO CHATGPT:")
            print("="*80)
            print(prompt)
            print("="*80)
    else:
        # Process all governors
        print("Generating prompts for all 91 governors...")
        results = process_all_governors()
        if results:
            save_prompts_to_file(results)
            print(f"Generated {len(results)} prompts. Use the generated file with ChatGPT.") 