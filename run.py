#!/usr/bin/env python3
"""
Complete Governor Dossier Generator v1.0.0

Main CLI interface for generating comprehensive governor research profiles,
chat prompts, and analysis reports from Enochian Governor data sources.
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Optional
from tqdm import tqdm
from loguru import logger

from generator.config import setup_logging
from generator.io_loader import load_all_data_sources
from generator.merger import merge_governor_profiles, GovernorProfile
from generator.question_engine import QuestionEngine
from generator.validator import ProfileValidator
from generator.exporter import DossierExporter


def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser"""
    parser = argparse.ArgumentParser(
        description="Complete Governor Dossier Generator - Create comprehensive research profiles for Enochian Governors",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --all                          # Generate all outputs for all governors
  %(prog)s --governors OCCODON VALGARS    # Generate for specific governors
  %(prog)s --elements Fire Water          # Generate for Fire and Water governors
  %(prog)s --format dossier               # Generate only dossier files
  %(prog)s --validate-only                # Run validation and generate reports only
  %(prog)s --output-dir my_output         # Use custom output directory
        """
    )
    
    # Governor selection
    parser.add_argument(
        "--governors", 
        nargs="*", 
        metavar="NAME",
        help="Specific governor names to process (e.g., OCCODON VALGARS)"
    )
    
    parser.add_argument(
        "--elements", 
        nargs="*", 
        choices=["Air", "Earth", "Fire", "Water", "Spirit"], 
        metavar="ELEMENT",
        help="Filter by elements (Air, Earth, Fire, Water, Spirit)"
    )
    
    parser.add_argument(
        "--all",
        action="store_true",
        help="Process all governors (default if no specific selection)"
    )
    
    # Output options
    parser.add_argument(
        "--output-dir", 
        default="output_complete",
        metavar="DIR",
        help="Output directory (default: output_complete)"
    )
    
    parser.add_argument(
        "--format", 
        choices=["dossier", "chat", "csv", "reports", "all"], 
        default="all",
        help="Output format (default: all)"
    )
    
    # Operation modes
    parser.add_argument(
        "--validate-only", 
        action="store_true", 
        help="Only run validation and generate reports"
    )
    
    parser.add_argument(
        "--force", 
        action="store_true", 
        help="Overwrite existing files without prompting"
    )
    
    # Logging and debug
    parser.add_argument(
        "--verbose", "-v", 
        action="store_true", 
        help="Enable verbose logging"
    )
    
    parser.add_argument(
        "--quiet", "-q", 
        action="store_true", 
        help="Suppress progress bars and non-essential output"
    )
    
    return parser


def filter_profiles(profiles: Dict[str, GovernorProfile], 
                   governor_names: Optional[List[str]] = None, 
                   elements: Optional[List[str]] = None) -> Dict[str, GovernorProfile]:
    """Filter profiles based on criteria"""
    filtered = {}
    
    for name, profile in profiles.items():
        # Filter by governor names
        if governor_names and name not in governor_names:
            continue
            
        # Filter by elements
        if elements and profile.element not in elements:
            continue
            
        filtered[name] = profile
    
    return filtered


def run_validation_only(profiles: Dict[str, GovernorProfile], 
                       question_engine: QuestionEngine,
                       output_dir: Path) -> bool:
    """Run validation and generate reports only"""
    logger.info("🔍 Running validation-only mode...")
    
    # Initialize components
    validator = ProfileValidator()
    exporter = DossierExporter()
    
    # Run validation
    validation_results = validator.validate_all_profiles(profiles)
    
    # Generate reports
    reports_dir = output_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    success = True
    
    # Completeness report
    completeness_report = validator.generate_completeness_report(profiles)
    completeness_path = reports_dir / "completeness_report.md"
    with open(completeness_path, 'w', encoding='utf-8') as f:
        f.write(completeness_report)
    logger.info(f"📋 Generated completeness report: {completeness_path}")
    
    # Validation report
    validation_path = reports_dir / "validation_report.md"
    if not exporter.export_validation_report(validation_results, validation_path):
        success = False
    
    # Question analysis
    question_analysis_path = reports_dir / "question_analysis.md"
    if not exporter.export_question_analysis(profiles, question_engine, question_analysis_path):
        success = False
    
    # CSV export
    csv_path = reports_dir / "governor_profiles.csv"
    if not exporter.export_csv_report(profiles, csv_path):
        success = False
    
    if success:
        logger.success(f"🎉 Validation complete! Reports generated in {reports_dir}")
    else:
        logger.error("💥 Some reports failed to generate")
    
    return success


def generate_outputs(profiles: Dict[str, GovernorProfile], 
                    bundle, 
                    question_engine: QuestionEngine,
                    args) -> bool:
    """Generate all requested outputs"""
    logger.info(f"📝 Generating outputs for {len(profiles)} governors...")
    
    # Initialize components
    validator = ProfileValidator()
    exporter = DossierExporter()
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Run validation for all profiles
    validation_results = validator.validate_all_profiles(profiles)
    
    success_count = 0
    total_count = len(profiles)
    
    # Process each governor
    progress_bar = tqdm(profiles.items(), desc="Processing governors", disable=args.quiet)
    
    for name, profile in progress_bar:
        progress_bar.set_description(f"Processing {name}")
        
        try:
            # Get relevant questions
            question_sets = question_engine.get_questions_for_governor(profile)
            
            # Get validation results for this profile
            profile_validation = validation_results.get(name, {'errors': [], 'warnings': [], 'suggestions': []})
            
            # Generate outputs based on format selection
            if args.format in ["dossier", "all"]:
                dossier_path = output_dir / f"{name}_dossier.md"
                if exporter.export_dossier(profile, question_sets, dossier_path, profile_validation):
                    success_count += 1
            
            if args.format in ["chat", "all"]:
                chat_path = output_dir / f"{name}_chat_prompt.txt"
                exporter.export_chat_prompt(profile, chat_path)
            
        except Exception as e:
            logger.error(f"💥 Failed to process {name}: {e}")
            continue
    
    progress_bar.close()
    
    # Generate summary reports
    if args.format in ["reports", "all"]:
        reports_dir = output_dir / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Completeness report
        completeness_report = validator.generate_completeness_report(profiles)
        with open(reports_dir / "completeness_report.md", 'w', encoding='utf-8') as f:
            f.write(completeness_report)
        
        # Other reports
        exporter.export_validation_report(validation_results, reports_dir / "validation_report.md")
        exporter.export_question_analysis(profiles, question_engine, reports_dir / "question_analysis.md")
    
    if args.format in ["csv", "all"]:
        csv_path = output_dir / "governor_profiles.csv"
        exporter.export_csv_report(profiles, csv_path)
    
    logger.success(f"🎉 Generated outputs for {success_count}/{total_count} governors in {output_dir}")
    return success_count == total_count


def main():
    """Main entry point"""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Setup logging
    setup_logging()
    
    if not args.quiet:
        logger.info("🚀 Complete Governor Dossier Generator v1.0.0")
        logger.info("📁 Loading data sources...")
    
    try:
        # Load all data sources
        bundle = load_all_data_sources()
        
        # Merge profiles
        profiles = merge_governor_profiles(bundle)
        
        if not profiles:
            logger.error("💥 No profiles were successfully merged")
            return 1
        
        # Initialize question engine
        question_engine = QuestionEngine(bundle.questions_data)
        
        # Apply filters
        if not args.all and not args.governors and not args.elements:
            # Default to all if no specific selection
            args.all = True
        
        if not args.all:
            original_count = len(profiles)
            profiles = filter_profiles(profiles, args.governors, args.elements)
            if not args.quiet:
                logger.info(f"🔍 Filtered to {len(profiles)} governors (from {original_count} total)")
        
        if not profiles:
            logger.error("💥 No governors match the specified criteria")
            return 1
        
        # Run requested operation
        if args.validate_only:
            success = run_validation_only(profiles, question_engine, Path(args.output_dir))
        else:
            success = generate_outputs(profiles, bundle, question_engine, args)
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        logger.warning("⚠️  Operation cancelled by user")
        return 130
    except Exception as e:
        logger.exception(f"💥 Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 