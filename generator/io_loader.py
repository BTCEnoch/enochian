"""
Data loading module for Complete Governor Dossier Generator
Handles loading and initial processing of all source data files.
"""
import json
from pathlib import Path
from typing import NamedTuple, Dict, Any, List
from loguru import logger

from .config import PROJECT_ROOT, SOURCE_FILES, DEFAULTS


class DataBundle(NamedTuple):
    """Container for all loaded source data"""
    governors_dossier: List[Dict[str, Any]]
    personality_traits: List[Dict[str, Any]]
    questions_data: str  # Raw markdown content
    utility_matrix: str  # Raw markdown content
    lore_compendium: str  # Raw markdown content
    template_adaptation: str  # Raw markdown content
    visual_description: Dict[str, Any]
    descriptive_formula: str  # Raw markdown content
    construction_checklist: str  # Raw markdown content


def load_json_file(filepath: Path) -> Dict[str, Any] | List[Dict[str, Any]]:
    """Load and parse a JSON file with error handling"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.debug(f"✅ Loaded JSON: {filepath} ({len(str(data))} chars)")
        return data
    except FileNotFoundError:
        logger.error(f"❌ File not found: {filepath}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"❌ JSON decode error in {filepath}: {e}")
        raise
    except Exception as e:
        logger.error(f"❌ Error loading {filepath}: {e}")
        raise


def load_text_file(filepath: Path) -> str:
    """Load a text/markdown file with error handling"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        logger.debug(f"✅ Loaded text: {filepath} ({len(content)} chars)")
        return content
    except FileNotFoundError:
        logger.error(f"❌ File not found: {filepath}")
        raise
    except Exception as e:
        logger.error(f"❌ Error loading {filepath}: {e}")
        raise


def validate_governors_data(governors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Validate and normalize governors data structure"""
    validated = []
    
    for i, gov in enumerate(governors):
        if not gov.get('name'):
            logger.warning(f"⚠️  Governor at index {i} missing name, skipping")
            continue
            
        # Ensure canonical_traits exists
        if 'canonical_traits' not in gov:
            logger.warning(f"⚠️  {gov['name']} missing canonical_traits, creating empty")
            gov['canonical_traits'] = {}
            
        # Ensure interpretive_traits exists  
        if 'interpretive_traits' not in gov:
            logger.warning(f"⚠️  {gov['name']} missing interpretive_traits, creating empty")
            gov['interpretive_traits'] = {}
            
        validated.append(gov)
    
    logger.info(f"✅ Validated {len(validated)} governors from {len(governors)} total")
    return validated


def load_all_data_sources(paths: Dict[str, str] = None) -> DataBundle:
    """
    Load all source data files into a structured DataBundle
    
    Args:
        paths: Optional custom file paths, defaults to SOURCE_FILES config
        
    Returns:
        DataBundle containing all loaded data
    """
    if paths is None:
        paths = {key: PROJECT_ROOT / filename for key, filename in SOURCE_FILES.items()}
    else:
        paths = {key: Path(path) for key, path in paths.items()}
    
    logger.info("📂 Loading all data sources...")
    
    try:
        # Load JSON files
        governors_dossier = load_json_file(paths["governors_dossier"])
        personality_traits = load_json_file(paths["personality_traits"])
        visual_description = load_json_file(paths["visual_description"])
        
        # Validate governors data
        governors_dossier = validate_governors_data(governors_dossier)
        
        # Load markdown/text files
        questions_data = load_text_file(paths["questions"])
        utility_matrix = load_text_file(paths["utility_matrix"])
        lore_compendium = load_text_file(paths["lore_compendium"])
        template_adaptation = load_text_file(paths["template_adaptation"])
        descriptive_formula = load_text_file(paths["descriptive_formula"])
        construction_checklist = load_text_file(paths["construction_checklist"])
        
        # Create and return data bundle
        bundle = DataBundle(
            governors_dossier=governors_dossier,
            personality_traits=personality_traits,
            questions_data=questions_data,
            utility_matrix=utility_matrix,
            lore_compendium=lore_compendium,
            template_adaptation=template_adaptation,
            visual_description=visual_description,
            descriptive_formula=descriptive_formula,
            construction_checklist=construction_checklist
        )
        
        logger.success(f"🎉 Successfully loaded all {len(SOURCE_FILES)} data sources")
        logger.info(f"📊 Found {len(governors_dossier)} governors")
        logger.info(f"📊 Found {len(personality_traits)} personality profiles")
        
        return bundle
        
    except Exception as e:
        logger.exception(f"💥 Failed to load data sources: {e}")
        raise


def get_data_summary(bundle: DataBundle) -> Dict[str, Any]:
    """Generate summary statistics for loaded data"""
    return {
        "governors_count": len(bundle.governors_dossier),
        "personality_count": len(bundle.personality_traits),
        "questions_length": len(bundle.questions_data),
        "utility_matrix_length": len(bundle.utility_matrix),
        "lore_compendium_length": len(bundle.lore_compendium),
        "visual_specs_count": len(bundle.visual_description) if isinstance(bundle.visual_description, dict) else 0
    } 