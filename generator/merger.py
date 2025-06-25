"""
Data merger module for Complete Governor Dossier Generator
Combines all data sources into unified GovernorProfile objects.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from loguru import logger

from .config import DEFAULTS
from .io_loader import DataBundle


@dataclass
class VisualSpec:
    """Visual design specifications for a governor"""
    color_palette: List[str] = field(default_factory=list)
    emblem: str = ""
    aura: str = ""


@dataclass 
class GovernorProfile:
    """Complete profile for an Enochian Governor"""
    # Core identity
    name: str = ""
    number: int = 0
    element: str = ""
    aethyr: str = ""
    translation: str = ""
    
    # Personality and domains
    personality_traits: List[str] = field(default_factory=list)
    domains: List[str] = field(default_factory=list)
    
    # Interpretive characteristics
    essence: str = ""
    themes: str = ""
    verse: str = ""
    boon: str = ""
    
    # Correspondences
    tarot: str = ""
    sephirah: str = ""
    zodiac_angel: str = ""
    
    # Context and references
    historical_context: str = ""
    source_references: str = ""
    
    # Visual design
    visual: VisualSpec = field(default_factory=VisualSpec)
    
    # Additional attributes (for template flexibility)
    extra_attributes: Dict[str, Any] = field(default_factory=dict)


def create_personality_lookup(personality_traits: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Create a quick lookup dictionary for personality traits by governor name"""
    lookup = {}
    for entry in personality_traits:
        if entry.get('name'):
            lookup[entry['name']] = entry
    logger.debug(f"📚 Created personality lookup for {len(lookup)} governors")
    return lookup


def extract_visual_spec(visual_data: Dict[str, Any], gov_name: str) -> VisualSpec:
    """Extract visual specifications for a governor from visual_description.json"""
    visual_spec = VisualSpec()
    
    if not isinstance(visual_data, dict):
        return visual_spec
    
    # Look for governor-specific data
    gov_visual = visual_data.get(gov_name)
    if not gov_visual:
        # Try lowercase
        gov_visual = visual_data.get(gov_name.lower())
    
    if not gov_visual:
        logger.warning(f"⚠️  No visual data found for {gov_name}")
        return visual_spec
    
    # Handle string format: "Element gender angel; appearance; traits"
    if isinstance(gov_visual, str):
        parts = gov_visual.split(';')
        if len(parts) >= 3:
            element_gender = parts[0].strip()  # e.g., "Water male angel"
            appearance = parts[1].strip()      # e.g., "mechanical"
            traits = parts[2].strip()          # e.g., "integrative, mercurial"
            
            # Extract element from first part
            element_parts = element_gender.split()
            if len(element_parts) >= 1:
                element = element_parts[0]  # Water, Fire, Air, Earth, Spirit
                visual_spec.color_palette = [element.lower()]
            
            # Use appearance as emblem description
            visual_spec.emblem = appearance
            
            # Use traits as aura description
            visual_spec.aura = traits
        else:
            # Fallback: use entire string as aura
            visual_spec.aura = gov_visual
    else:
        # Handle structured format (if it exists)
        visual_spec.color_palette = gov_visual.get('colors', gov_visual.get('color_palette', []))
        visual_spec.emblem = gov_visual.get('emblem', gov_visual.get('symbol', ''))
        visual_spec.aura = gov_visual.get('aura', gov_visual.get('aura_description', ''))
    
    return visual_spec


def extract_historical_context(lore_compendium: str, gov_name: str) -> str:
    """Extract relevant historical context for a governor from the lore compendium"""
    # Simple text search for now - could be enhanced with more sophisticated parsing
    lines = lore_compendium.split('\n')
    context_lines = []
    
    # Look for sections mentioning this governor
    in_relevant_section = False
    for line in lines:
        if gov_name in line:
            in_relevant_section = True
            context_lines.append(line.strip())
        elif in_relevant_section and line.strip() == '':
            # End of section
            break
        elif in_relevant_section:
            context_lines.append(line.strip())
    
    if context_lines:
        return '\n'.join(context_lines[:5])  # Limit to first 5 relevant lines
    
    return DEFAULTS["historical_context"]


def merge_governor_profile(
    gov_data: Dict[str, Any], 
    personality_lookup: Dict[str, Dict[str, Any]],
    visual_data: Dict[str, Any],
    lore_compendium: str
) -> GovernorProfile:
    """Merge data from all sources into a single GovernorProfile"""
    
    name = gov_data.get('name', '')
    canonical = gov_data.get('canonical_traits', {})
    interpretive = gov_data.get('interpretive_traits', {})
    
    # Get personality data
    personality_data = personality_lookup.get(name, {})
    
    # Create profile with data from all sources
    profile = GovernorProfile(
        # Core identity
        name=name,
        number=gov_data.get('number', 0),
        element=canonical.get('element', DEFAULTS['element']),
        aethyr=canonical.get('aethyr', DEFAULTS['aethyr']),
        translation=canonical.get('translation', DEFAULTS['translation']),
        
        # Personality and domains
        personality_traits=canonical.get('personality_traits', 
                                       personality_data.get('personality_traits', 
                                                           DEFAULTS['personality_traits'])),
        domains=canonical.get('domains', 
                             canonical.get('domains_of_knowledge',
                                         personality_data.get('domains_of_knowledge',
                                                            DEFAULTS['domains']))),
        
        # Interpretive characteristics (prioritize rich content from governors_dossier)
        essence=interpretive.get('essence') or 
                personality_data.get('essence') or 
                DEFAULTS['essence'],
        themes=interpretive.get('themes') or
               personality_data.get('themes') or
               DEFAULTS['themes'],
        verse=interpretive.get('verse') or
              personality_data.get('verse') or
              DEFAULTS['verse'],
        boon=interpretive.get('boon') or
             personality_data.get('boon') or
             DEFAULTS['boon'],
        
        # Correspondences
        tarot=canonical.get('tarot_attribution', canonical.get('tarot', '')),
        sephirah=canonical.get('sephirah', ''),
        zodiac_angel=canonical.get('zodiac_angel', ''),
        
        # Context
        historical_context=extract_historical_context(lore_compendium, name),
        source_references=DEFAULTS['source_references'],
        
        # Visual design
        visual=extract_visual_spec(visual_data, name)
    )
    
    # Log any missing critical fields
    missing_fields = []
    if not profile.name:
        missing_fields.append('name')
    if not profile.element or profile.element == DEFAULTS['element']:
        missing_fields.append('element')
    if not profile.personality_traits or profile.personality_traits == DEFAULTS['personality_traits']:
        missing_fields.append('personality_traits')
    
    if missing_fields:
        logger.warning(f"⚠️  {name} missing fields: {', '.join(missing_fields)} - using defaults")
    
    return profile


def merge_governor_profiles(bundle: DataBundle) -> Dict[str, GovernorProfile]:
    """
    Merge all data sources into a dictionary of GovernorProfile objects
    
    Args:
        bundle: DataBundle containing all loaded source data
        
    Returns:
        Dictionary mapping governor names to GovernorProfile objects
    """
    logger.info("🔄 Merging governor profiles from all data sources...")
    
    # Create lookup tables
    personality_lookup = create_personality_lookup(bundle.personality_traits)
    
    # Process each governor
    profiles = {}
    
    for gov_data in bundle.governors_dossier:
        if not gov_data.get('name'):
            continue
            
        try:
            profile = merge_governor_profile(
                gov_data,
                personality_lookup,
                bundle.visual_description,
                bundle.lore_compendium
            )
            profiles[profile.name] = profile
            logger.debug(f"✅ Merged profile for {profile.name}")
            
        except Exception as e:
            gov_name = gov_data.get('name', 'UNKNOWN')
            logger.exception(f"💥 Failed to merge profile for {gov_name}: {e}")
            continue
    
    logger.success(f"🎉 Successfully merged {len(profiles)} governor profiles")
    
    # Log summary statistics
    elements = {}
    for profile in profiles.values():
        element = profile.element or "Unknown"
        elements[element] = elements.get(element, 0) + 1
    
    logger.info(f"📊 Element distribution: {dict(sorted(elements.items()))}")
    
    return profiles


def validate_profile_completeness(profile: GovernorProfile) -> List[str]:
    """Validate that a profile has all required fields and return list of missing items"""
    missing = []
    
    # Check core fields
    if not profile.name:
        missing.append('name')
    if not profile.element:
        missing.append('element')
    if not profile.personality_traits:
        missing.append('personality_traits')
    if not profile.domains:
        missing.append('domains')
    if not profile.essence:
        missing.append('essence')
    
    return missing 