"""
Profile Validator for Governor Dossier Generation

Validates governor profiles for completeness and data quality,
generating detailed reports and recommendations.
"""

from typing import Dict, List, Set
from loguru import logger

from .merger import GovernorProfile


class ProfileValidator:
    """Validator for governor profiles with comprehensive quality checks"""
    
    def __init__(self):
        """Initialize validator with validation rules"""
        self.required_fields = {
            'name', 'element', 'personality_traits', 'domains', 'essence'
        }
        
        self.recommended_fields = {
            'number', 'aethyr', 'translation', 'themes', 'verse', 'boon',
            'tarot', 'sephirah', 'historical_context'
        }
        
        self.valid_elements = {'Air', 'Earth', 'Fire', 'Water', 'Spirit'}
        
        logger.info("🔧 Initialized ProfileValidator")
    
    def validate_profile(self, profile: GovernorProfile) -> Dict[str, List[str]]:
        """Return validation results: {'errors': [...], 'warnings': [...], 'suggestions': [...]}"""
        results = {
            'errors': [],
            'warnings': [],
            'suggestions': []
        }
        
        # Check required fields
        for field_name in self.required_fields:
            field_value = getattr(profile, field_name, None)
            if not field_value:
                results['errors'].append(f"Missing required field: {field_name}")
            elif isinstance(field_value, list) and len(field_value) == 0:
                results['errors'].append(f"Empty required list field: {field_name}")
        
        # Check recommended fields
        for field_name in self.recommended_fields:
            field_value = getattr(profile, field_name, None)
            if not field_value:
                results['warnings'].append(f"Missing recommended field: {field_name}")
        
        # Validate element
        if profile.element and profile.element not in self.valid_elements:
            results['errors'].append(f"Invalid element '{profile.element}'. Must be one of: {', '.join(self.valid_elements)}")
        
        # Check personality traits quality
        if profile.personality_traits:
            if len(profile.personality_traits) < 2:
                results['warnings'].append("Less than 2 personality traits - consider adding more for depth")
            if len(profile.personality_traits) > 6:
                results['suggestions'].append("More than 6 personality traits - consider consolidating for focus")
        
        # Check domains quality
        if profile.domains:
            if len(profile.domains) < 1:
                results['warnings'].append("No domains of knowledge specified")
            if len(profile.domains) > 4:
                results['suggestions'].append("More than 4 domains - consider focusing on primary areas")
        
        # Check text field lengths
        text_fields = {
            'essence': (50, 500),
            'themes': (30, 300),
            'verse': (10, 200),
            'boon': (20, 300),
            'historical_context': (50, 1000)
        }
        
        for field_name, (min_len, max_len) in text_fields.items():
            field_value = getattr(profile, field_name, '')
            if field_value:
                if len(field_value) < min_len:
                    results['warnings'].append(f"{field_name} is quite short ({len(field_value)} chars) - consider expanding")
                elif len(field_value) > max_len:
                    results['suggestions'].append(f"{field_name} is quite long ({len(field_value)} chars) - consider condensing")
        
        # Check for placeholder/default content
        placeholder_indicators = ['default', 'placeholder', 'tbd', 'todo', '...', 'unknown']
        for field_name in ['essence', 'themes', 'verse', 'boon']:
            field_value = getattr(profile, field_name, '').lower()
            if any(indicator in field_value for indicator in placeholder_indicators):
                results['warnings'].append(f"{field_name} contains placeholder content")
        
        # Visual specification checks
        if profile.visual:
            if not profile.visual.color_palette:
                results['suggestions'].append("No color palette specified in visual design")
            if not profile.visual.emblem:
                results['suggestions'].append("No emblem/symbol specified in visual design")
            if not profile.visual.aura:
                results['suggestions'].append("No aura description specified in visual design")
        else:
            results['warnings'].append("No visual specifications provided")
        
        # Cross-field consistency checks
        if profile.element and profile.visual and profile.visual.color_palette:
            element_lower = profile.element.lower()
            if element_lower not in [color.lower() for color in profile.visual.color_palette]:
                results['suggestions'].append(f"Element '{profile.element}' not reflected in color palette")
        
        return results
    
    def validate_all_profiles(self, profiles: Dict[str, GovernorProfile]) -> Dict[str, Dict[str, List[str]]]:
        """Validate all profiles and return comprehensive report"""
        logger.info(f"🔍 Validating {len(profiles)} governor profiles...")
        
        all_results = {}
        
        for name, profile in profiles.items():
            results = self.validate_profile(profile)
            all_results[name] = results
            
            error_count = len(results['errors'])
            warning_count = len(results['warnings'])
            suggestion_count = len(results['suggestions'])
            
            if error_count > 0:
                logger.error(f"💥 {name}: {error_count} errors, {warning_count} warnings")
            elif warning_count > 0:
                logger.warning(f"⚠️  {name}: {warning_count} warnings, {suggestion_count} suggestions")
            else:
                logger.debug(f"✅ {name}: validated successfully")
        
        # Summary statistics
        total_errors = sum(len(results['errors']) for results in all_results.values())
        total_warnings = sum(len(results['warnings']) for results in all_results.values())
        total_suggestions = sum(len(results['suggestions']) for results in all_results.values())
        
        logger.info(f"📊 Validation summary: {total_errors} errors, {total_warnings} warnings, {total_suggestions} suggestions")
        
        return all_results
    
    def generate_completeness_report(self, profiles: Dict[str, GovernorProfile]) -> str:
        """Generate detailed completeness analysis"""
        logger.info("📋 Generating completeness report...")
        
        report_lines = []
        report_lines.append("# Governor Profile Completeness Report")
        report_lines.append(f"Generated for {len(profiles)} profiles\n")
        
        # Field completeness analysis
        field_stats = {}
        all_fields = self.required_fields.union(self.recommended_fields)
        
        for field_name in all_fields:
            complete_count = 0
            for profile in profiles.values():
                field_value = getattr(profile, field_name, None)
                if field_value and (not isinstance(field_value, list) or len(field_value) > 0):
                    complete_count += 1
            
            field_stats[field_name] = {
                'complete': complete_count,
                'percentage': (complete_count / len(profiles)) * 100,
                'missing': len(profiles) - complete_count
            }
        
        # Required fields section
        report_lines.append("## Required Fields Completeness")
        for field_name in sorted(self.required_fields):
            stats = field_stats[field_name]
            status = "✅" if stats['percentage'] == 100 else "❌" if stats['percentage'] < 50 else "⚠️"
            report_lines.append(f"- {status} **{field_name}**: {stats['complete']}/{len(profiles)} ({stats['percentage']:.1f}%)")
        
        report_lines.append("\n## Recommended Fields Completeness")
        for field_name in sorted(self.recommended_fields):
            stats = field_stats[field_name]
            status = "✅" if stats['percentage'] > 80 else "⚠️" if stats['percentage'] > 50 else "❌"
            report_lines.append(f"- {status} **{field_name}**: {stats['complete']}/{len(profiles)} ({stats['percentage']:.1f}%)")
        
        # Element distribution
        report_lines.append("\n## Element Distribution")
        element_counts = {}
        for profile in profiles.values():
            element = profile.element or "Unknown"
            element_counts[element] = element_counts.get(element, 0) + 1
        
        for element in sorted(element_counts.keys()):
            count = element_counts[element]
            percentage = (count / len(profiles)) * 100
            report_lines.append(f"- **{element}**: {count} governors ({percentage:.1f}%)")
        
        # Quality metrics
        report_lines.append("\n## Quality Metrics")
        
        # Personality traits analysis
        trait_counts = [len(p.personality_traits) for p in profiles.values() if p.personality_traits]
        if trait_counts:
            avg_traits = sum(trait_counts) / len(trait_counts)
            report_lines.append(f"- **Average personality traits per governor**: {avg_traits:.1f}")
        
        # Domain analysis
        domain_counts = [len(p.domains) for p in profiles.values() if p.domains]
        if domain_counts:
            avg_domains = sum(domain_counts) / len(domain_counts)
            report_lines.append(f"- **Average domains per governor**: {avg_domains:.1f}")
        
        # Text content analysis
        essence_lengths = [len(p.essence) for p in profiles.values() if p.essence]
        if essence_lengths:
            avg_essence_length = sum(essence_lengths) / len(essence_lengths)
            report_lines.append(f"- **Average essence description length**: {avg_essence_length:.0f} characters")
        
        # Profiles needing attention
        validation_results = self.validate_all_profiles(profiles)
        
        profiles_with_errors = [name for name, results in validation_results.items() if results['errors']]
        profiles_with_warnings = [name for name, results in validation_results.items() if results['warnings'] and not results['errors']]
        
        if profiles_with_errors:
            report_lines.append(f"\n## Profiles with Errors ({len(profiles_with_errors)})")
            for name in sorted(profiles_with_errors):
                error_count = len(validation_results[name]['errors'])
                report_lines.append(f"- **{name}**: {error_count} errors")
        
        if profiles_with_warnings:
            report_lines.append(f"\n## Profiles with Warnings ({len(profiles_with_warnings)})")
            for name in sorted(profiles_with_warnings):
                warning_count = len(validation_results[name]['warnings'])
                report_lines.append(f"- **{name}**: {warning_count} warnings")
        
        # Recommendations
        report_lines.append("\n## Recommendations")
        
        # Find fields with lowest completion rates
        incomplete_fields = [(field, stats) for field, stats in field_stats.items() if stats['percentage'] < 80]
        incomplete_fields.sort(key=lambda x: x[1]['percentage'])
        
        if incomplete_fields:
            report_lines.append("### Priority Fields for Completion:")
            for field_name, stats in incomplete_fields[:5]:  # Top 5 most incomplete
                report_lines.append(f"- **{field_name}**: {stats['missing']} profiles missing ({100-stats['percentage']:.1f}% incomplete)")
        
        # Identify governors needing most attention
        governor_scores = {}
        for name, results in validation_results.items():
            score = len(results['errors']) * 3 + len(results['warnings']) * 1
            if score > 0:
                governor_scores[name] = score
        
        if governor_scores:
            top_attention_needed = sorted(governor_scores.items(), key=lambda x: x[1], reverse=True)[:10]
            report_lines.append("\n### Governors Needing Most Attention:")
            for name, score in top_attention_needed:
                errors = len(validation_results[name]['errors'])
                warnings = len(validation_results[name]['warnings'])
                report_lines.append(f"- **{name}**: {errors} errors, {warnings} warnings (score: {score})")
        
        report = "\n".join(report_lines)
        logger.success("📋 Generated completeness report")
        return report 