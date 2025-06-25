"""
Configuration module for Complete Governor Dossier Generator
Contains all constants, file paths, and logger setup.
"""
import sys
from pathlib import Path
from datetime import datetime
from loguru import logger

# Version and metadata
VERSION = "1.0.0"
PROJECT_NAME = "Complete Governor Dossier Generator"

# Base paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
TEMPLATES_DIR = PROJECT_ROOT / "templates"
OUTPUT_DIR = PROJECT_ROOT / "output"
LOGS_DIR = PROJECT_ROOT / "logs"
REPORTS_DIR = PROJECT_ROOT / "reports"

# Source data files (relative to project root)
SOURCE_FILES = {
    "governors_dossier": "governors_dossier.json",
    "personality_traits": "personality_traits.json", 
    "questions": "questions.md",
    "utility_matrix": "utility_application_matrix.md",
    "lore_compendium": "ENOCHIAN_GOVERNORS_LORE_COMPENDIUM.md",
    "template_adaptation": "prompt_approach_adaptation.md",
    "visual_description": "visual_description.json",
    "descriptive_formula": "descriptive_formula.md",
    "construction_checklist": "TEMPLATE_CONSTRUCTION_CHECKLIST.md"
}

# Template files
TEMPLATE_FILES = {
    "dossier": "dossier.md.j2",
    "chat_setup": "chat_setup.txt.j2", 
    "research_protocol": "research_protocol.json.j2"
}

# Output file patterns
OUTPUT_PATTERNS = {
    "complete_dossier": "{name}_complete_dossier.md",
    "chat_setup": "{name}_chat_setup.txt",
    "research_protocol": "{name}_research_protocol.json",
    "master_index": "master_governor_index.csv",
    "qa_report": "quality_assurance_report.md",
    "research_tracking": "research_tracking.xlsx"
}

# Quality assurance checklist items
QA_CHECKLIST = [
    "all_canonical_data_integrated",
    "research_questions_domain_specific", 
    "conversation_flows_structured",
    "chatgpt_setup_functional",
    "visual_elements_included",
    "historical_context_provided",
    "questions_enable_deep_exploration",
    "personality_matrix_comprehensive",
    "interaction_guidelines_clear",
    "data_collection_organized",
    "tracking_systems_functional"
]

# Default values for missing data
DEFAULTS = {
    "element": "Spirit",
    "aethyr": "Unknown",
    "translation": "Unnamed Governor",
    "personality_traits": ["enigmatic", "ancient", "wise"],
    "domains": ["liminal studies", "hermetic synthesis"],
    "essence": "A mysterious guardian of ancient wisdom.",
    "themes": "Transformation, mystery, hidden knowledge.",
    "verse": "In silence, wisdom speaks.",
    "boon": "Grants insight balanced by responsibility.",
    "historical_context": "References to be researched.",
    "source_references": "Primary sources pending compilation."
}

def setup_logging():
    """Initialize loguru logger with file and console output"""
    # Remove default handler
    logger.remove()
    
    # Console handler with colors
    logger.add(
        sys.stdout,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO",
        colorize=True
    )
    
    # File handler
    log_file = LOGS_DIR / f"generator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logger.add(
        log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG",
        rotation="10 MB",
        retention="30 days"
    )
    
    logger.info(f"🚀 {PROJECT_NAME} v{VERSION} - Logging initialized")
    logger.info(f"📁 Project root: {PROJECT_ROOT}")
    logger.info(f"📝 Log file: {log_file}")
    
    return logger

# Initialize logger when module is imported
setup_logging() 