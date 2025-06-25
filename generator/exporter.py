"""
Exporter for Governor Dossier Generation

Handles template-based export of comprehensive dossiers, chat prompts,
and CSV reports using Jinja2 templates.
"""

import os
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from jinja2 import Environment, FileSystemLoader, Template
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
from loguru import logger

from .merger import GovernorProfile
from .question_engine import QuestionSet


class DossierExporter:
    """Exporter for governor dossiers and related files"""
    
    def __init__(self, template_dir: str = "templates"):
        """Initialize with Jinja2 templates directory"""
        self.template_dir = Path(template_dir)
        
        if not self.template_dir.exists():
            raise FileNotFoundError(f"Template directory not found: {template_dir}")
        
        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        logger.info(f"🔧 Initialized DossierExporter with templates from {template_dir}")
    
    def export_dossier(self, 
                      profile: GovernorProfile, 
                      question_sets: List[QuestionSet], 
                      output_path: str,
                      validation_results: Dict[str, List[str]] = None,
                      utility_applications: str = None) -> bool:
        """Export complete dossier using template"""
        try:
            template = self.env.get_template('dossier_template.md')
            
            rendered = template.render(
                profile=profile,
                question_sets=question_sets,
                validation_results=validation_results,
                utility_applications=utility_applications,
                timestamp=datetime.now()
            )
            
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(rendered)
            
            logger.info(f"📄 Exported dossier for {profile.name} to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"💥 Failed to export dossier for {profile.name}: {e}")
            return False
    
    def export_chat_prompt(self, 
                          profile: GovernorProfile, 
                          output_path: str) -> bool:
        """Export chat prompt file"""
        try:
            template = self.env.get_template('chat_prompt_template.txt')
            
            rendered = template.render(
                profile=profile,
                timestamp=datetime.now()
            )
            
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(rendered)
            
            logger.info(f"💬 Exported chat prompt for {profile.name} to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"💥 Failed to export chat prompt for {profile.name}: {e}")
            return False
    
    def export_csv_report(self, 
                         profiles: Dict[str, GovernorProfile], 
                         output_path: str) -> bool:
        """Export CSV with all governor fields for analysis"""
        try:
            # Prepare data for CSV
            csv_data = []
            
            for name, profile in profiles.items():
                row = {
                    'name': profile.name,
                    'number': profile.number,
                    'element': profile.element,
                    'aethyr': profile.aethyr,
                    'translation': profile.translation,
                    'personality_traits': ', '.join(profile.personality_traits) if profile.personality_traits else '',
                    'domains': ', '.join(profile.domains) if profile.domains else '',
                    'essence': profile.essence,
                    'themes': profile.themes,
                    'verse': profile.verse,
                    'boon': profile.boon,
                    'tarot': profile.tarot,
                    'sephirah': profile.sephirah,
                    'zodiac_angel': profile.zodiac_angel,
                    'historical_context': profile.historical_context,
                    'source_references': profile.source_references,
                    'visual_color_palette': ', '.join(profile.visual.color_palette) if profile.visual and profile.visual.color_palette else '',
                    'visual_emblem': profile.visual.emblem if profile.visual else '',
                    'visual_aura': profile.visual.aura if profile.visual else '',
                    'personality_trait_count': len(profile.personality_traits) if profile.personality_traits else 0,
                    'domain_count': len(profile.domains) if profile.domains else 0,
                    'essence_length': len(profile.essence) if profile.essence else 0,
                    'themes_length': len(profile.themes) if profile.themes else 0,
                    'verse_length': len(profile.verse) if profile.verse else 0,
                    'boon_length': len(profile.boon) if profile.boon else 0,
                    'historical_context_length': len(profile.historical_context) if profile.historical_context else 0
                }
                csv_data.append(row)
            
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            if HAS_PANDAS:
                # Use pandas for better CSV handling with proper quoting
                df = pd.DataFrame(csv_data)
                df.to_csv(output_file, index=False, encoding='utf-8', quoting=csv.QUOTE_ALL)
            else:
                # Fallback to basic CSV writer with proper quoting
                with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                    if csv_data:
                        fieldnames = csv_data[0].keys()
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
                        writer.writeheader()
                        writer.writerows(csv_data)
            
            logger.success(f"📊 Exported CSV report with {len(csv_data)} governors to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"💥 Failed to export CSV report: {e}")
            return False
    
    def export_validation_report(self, 
                                validation_results: Dict[str, Dict[str, List[str]]], 
                                output_path: str) -> bool:
        """Export detailed validation report"""
        try:
            report_lines = []
            report_lines.append("# Governor Profile Validation Report")
            report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            # Summary statistics
            total_profiles = len(validation_results)
            profiles_with_errors = sum(1 for results in validation_results.values() if results['errors'])
            profiles_with_warnings = sum(1 for results in validation_results.values() if results['warnings'])
            total_errors = sum(len(results['errors']) for results in validation_results.values())
            total_warnings = sum(len(results['warnings']) for results in validation_results.values())
            total_suggestions = sum(len(results['suggestions']) for results in validation_results.values())
            
            report_lines.append("## Summary")
            report_lines.append(f"- **Total Profiles:** {total_profiles}")
            report_lines.append(f"- **Profiles with Errors:** {profiles_with_errors}")
            report_lines.append(f"- **Profiles with Warnings:** {profiles_with_warnings}")
            report_lines.append(f"- **Total Errors:** {total_errors}")
            report_lines.append(f"- **Total Warnings:** {total_warnings}")
            report_lines.append(f"- **Total Suggestions:** {total_suggestions}\n")
            
            # Detailed results
            if profiles_with_errors > 0:
                report_lines.append("## Profiles with Errors")
                for name, results in validation_results.items():
                    if results['errors']:
                        report_lines.append(f"\n### {name}")
                        for error in results['errors']:
                            report_lines.append(f"- ❌ {error}")
            
            if profiles_with_warnings > 0:
                report_lines.append("\n## Profiles with Warnings")
                for name, results in validation_results.items():
                    if results['warnings'] and not results['errors']:
                        report_lines.append(f"\n### {name}")
                        for warning in results['warnings']:
                            report_lines.append(f"- ⚠️ {warning}")
                        if results['suggestions']:
                            for suggestion in results['suggestions']:
                                report_lines.append(f"- 💡 {suggestion}")
            
            # Write report
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(report_lines))
            
            logger.success(f"📋 Exported validation report to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"💥 Failed to export validation report: {e}")
            return False
    
    def export_question_analysis(self, 
                                profiles: Dict[str, GovernorProfile],
                                question_engine: Any,
                                output_path: str) -> bool:
        """Export analysis of question distribution and relevance"""
        try:
            report_lines = []
            report_lines.append("# Question Relevance Analysis")
            report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            # Overall question statistics
            total_questions = question_engine.get_all_questions_count()
            thematic_blocks = question_engine.get_thematic_blocks()
            
            report_lines.append("## Overview")
            report_lines.append(f"- **Total Questions:** {total_questions}")
            report_lines.append(f"- **Thematic Blocks:** {len(thematic_blocks)}")
            report_lines.append(f"- **Governors Analyzed:** {len(profiles)}\n")
            
            # Question relevance by governor
            report_lines.append("## Question Relevance by Governor")
            
            governor_question_stats = {}
            for name, profile in profiles.items():
                relevant_sets = question_engine.get_questions_for_governor(profile)
                total_relevant = sum(len(qs.questions) for qs in relevant_sets)
                governor_question_stats[name] = {
                    'relevant_sets': len(relevant_sets),
                    'total_questions': total_relevant,
                    'percentage': (total_relevant / total_questions) * 100 if total_questions > 0 else 0
                }
            
            # Sort by relevance percentage
            sorted_governors = sorted(governor_question_stats.items(), 
                                    key=lambda x: x[1]['percentage'], reverse=True)
            
            for name, stats in sorted_governors:
                report_lines.append(f"- **{name}**: {stats['total_questions']}/{total_questions} questions "
                                  f"({stats['percentage']:.1f}%) across {stats['relevant_sets']} thematic blocks")
            
            # Thematic block analysis
            report_lines.append("\n## Thematic Block Coverage")
            block_coverage = {}
            
            for block_name in thematic_blocks:
                governors_with_block = 0
                for profile in profiles.values():
                    relevant_sets = question_engine.get_questions_for_governor(profile)
                    if any(qs.thematic_block == block_name for qs in relevant_sets):
                        governors_with_block += 1
                
                coverage_percentage = (governors_with_block / len(profiles)) * 100
                block_coverage[block_name] = {
                    'governors': governors_with_block,
                    'percentage': coverage_percentage
                }
            
            # Sort by coverage
            sorted_blocks = sorted(block_coverage.items(), 
                                 key=lambda x: x[1]['percentage'], reverse=True)
            
            for block_name, stats in sorted_blocks:
                report_lines.append(f"- **{block_name}**: Relevant to {stats['governors']}/{len(profiles)} "
                                  f"governors ({stats['percentage']:.1f}%)")
            
            # Write report
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(report_lines))
            
            logger.success(f"🔍 Exported question analysis to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"💥 Failed to export question analysis: {e}")
            return False 