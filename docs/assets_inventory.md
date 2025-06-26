# Assets & Datasets Inventory for Governor Storylines Creation

## Core Data Assets ✅ (Available)

### Primary Governor Data
- **`governors_ultra_clean.json`** - Clean, ASCII-safe JSON with all 91 governors
- **`governors_ultra_clean.csv`** - CSV format of governor data
- **`governors_ultra_clean.jsonl`** - JSON Lines format
- **`governors_dossier.json`** - Original working file with interpretive traits
- **`personality_traits.json`** - Canonical personality trait definitions

### Individual Column Data Files
- **`csv_columns/aethyr.txt`** - Updated canonical aethyr assignments (91 entries)
- **`csv_columns/element.txt`** - Updated canonical element assignments (91 entries)
- **`csv_columns/name.txt`** - Governor names
- **`csv_columns/number.txt`** - Governor numbers (1-91)
- **`csv_columns/translation.txt`** - Name translations
- **`csv_columns/personality_traits.txt`** - Trait lists
- **`csv_columns/domains.txt`** - Domain specialties
- **`csv_columns/tarot.txt`** - Tarot correspondences
- **`csv_columns/sephirah.txt`** - Sephirah assignments
- **`csv_columns/zodiac_angel.txt`** - Zodiac angel associations
- **`csv_columns/visual_emblem.txt`** - Visual emblems
- **`csv_columns/essence.txt`** - Essence descriptions
- **`csv_columns/themes.txt`** - Themes and virtues/vices
- **`csv_columns/tokens.txt`** - Ritual tokens and offerings
- **`csv_columns/boon.txt`** - Mystical boons
- **`csv_columns/verse.txt`** - Sacred verses
- **`csv_columns/angelic_role.txt`** - Angelic hierarchy roles
- **`csv_columns/challenge.txt`** - On-chain challenges
- **`csv_columns/wisdom.txt`** - Wisdom sayings

### Reference Data
- **`csv_columns/enochian_governors_comparison.json`** - Canonical vs current data comparison
- **`visual_description.json`** - Visual design guidelines and descriptions

## Framework & Template Assets ✅ (Available)

### Research & Question Framework
- **`questions.md`** - 97 research questions organized by theme
- **`TEMPLATE_CONSTRUCTION_CHECKLIST.md`** - Quality requirements checklist
- **`utility_application_matrix.md`** - Game mechanics and utility mappings

### Templates & Generation System
- **`templates/dossier_template.md`** - Markdown template for governor dossiers
- **`templates/chat_prompt_template.txt`** - Chat prompt template for AI interactions
- **`generator/` directory** - Python generation system
  - **`config.py`** - Configuration and validation rules
  - **`io_loader.py`** - Data loading utilities
  - **`merger.py`** - Data merging logic
  - **`question_engine.py`** - Question processing
  - **`validator.py`** - Data validation
  - **`exporter.py`** - Output file generation

### Lore & Background References
- **`ENOCHIAN_GOVERNORS_LORE_COMPENDIUM.md`** - Comprehensive lore reference
- **`descriptive_formula.md`** - Style and formatting guidelines
- **`dossier_sample.json`** - Example dossier structure

## Existing Output Assets ✅ (Available)

### Generated Dossiers
- **`output_complete/` directory** - Complete generated dossiers
  - 91 x `{GOVERNOR}_dossier.md` files
  - 91 x `{GOVERNOR}_chat_prompt.txt` files
- **`output/` directory** - Previous generation outputs
- **`reports/` directory** - Quality and validation reports

### Supporting Files
- **`requirements.txt`** - Python dependencies
- **`run.py`** - Main execution script
- **`parse_csv.py`** - CSV parsing utilities

## Required New Assets 🆕 (To Be Created)

### AI Interview System
- **`interview_pipeline.py`** - Main interview automation script
- **`interview_prompts.json`** - Structured prompts for each content category
- **`system_prompt_template.txt`** - Template for governor-specific system prompts
- **`question_sequences.json`** - Ordered question sets for different content types

### Data Processing Tools
- **`content_parser.py`** - Parse and clean AI interview responses
- **`data_enricher.py`** - Integrate new content into existing structures
- **`quality_validator.py`** - Validate completeness and consistency
- **`gap_analyzer.py`** - Identify missing or placeholder content

### Enhanced Templates
- **`enhanced_dossier_template.md`** - Updated template with new content sections
- **`research_protocol_template.json`** - Governor-specific research protocols
- **`master_index_template.csv`** - Template for summary index

### Output Management
- **`output_manager.py`** - Organize and package final outputs
- **`backup_system.py`** - Version control and backup utilities
- **`report_generator.py`** - Generate completion and quality reports

## External API Dependencies 🌐

### AI Service Integration
- **OpenAI API Access** - For automated governor interviews
- **API Rate Limiting Tools** - To manage 91 x 8+ question sequences
- **Response Validation Tools** - To ensure AI responses meet requirements

### Optional Enhancements
- **Anthropic Claude API** - Alternative AI service for comparison
- **Local LLM Integration** - For offline processing if needed

## Configuration & Settings 📋

### Interview Configuration
- **`interview_config.json`** - Settings for AI interviews
  - API endpoints and keys
  - Rate limiting parameters
  - Response validation rules
  - Retry and error handling settings

### Quality Assurance Settings
- **`qa_config.json`** - Quality validation parameters
  - Content length requirements
  - Uniqueness validation rules
  - Format compliance checks
  - Completeness verification criteria

### Template Settings
- **`template_config.json`** - Template rendering configuration
  - Field mapping definitions
  - Format specifications
  - Output file naming conventions

## Data Flow Architecture 🔄

### Input Pipeline
```
Canonical Data → Column Files → Interview System → AI Responses → Content Parser
```

### Processing Pipeline
```
Parsed Content → Data Enricher → Template Renderer → Quality Validator → Output Manager
```

### Output Pipeline
```
Enriched Data → Enhanced Dossiers → Chat Prompts → Research Protocols → Master Index
```

## Storage & Organization 📁

### Required Directory Structure
```
/project-root/
├── data/
│   ├── canonical/          # Original canonical data
│   ├── enriched/          # AI-enhanced data
│   └── intermediate/      # Processing intermediate files
├── templates/
│   ├── base/              # Original templates
│   └── enhanced/          # Updated templates with new sections
├── interviews/
│   ├── transcripts/       # Raw AI interview transcripts
│   ├── parsed/            # Processed interview responses
│   └── logs/              # Interview process logs
├── output/
│   ├── dossiers/          # Final enhanced dossiers
│   ├── prompts/           # Updated chat prompts
│   ├── protocols/         # Research protocols
│   └── reports/           # Quality and completion reports
└── tools/
    ├── interview/         # Interview automation tools
    ├── processing/        # Data processing utilities
    └── validation/        # Quality assurance tools
```

## Success Metrics & Validation 📊

### Completion Metrics
- **91 governors** with fully populated, unique dossiers
- **Zero placeholder content** remaining in any field
- **100% unique** essence descriptions, verses, and boons
- **Complete correspondences** for all applicable fields

### Quality Metrics
- **Consistent formatting** across all 91 dossiers
- **Domain-appropriate content** aligned with canonical traits
- **Mythic depth** meeting lore compendium standards
- **Functional integration** with existing game mechanics

### Technical Metrics
- **Automated pipeline** capable of regenerating all content
- **Version control** tracking all changes and sources
- **Quality assurance** reports confirming all requirements met
- **Documentation completeness** for ongoing maintenance

---

## Ready to Proceed? ✅

**Available Assets**: Sufficient canonical data, framework, and templates exist
**Missing Assets**: Primarily automation tools and AI integration systems
**Estimated Development**: 2-3 weeks for full pipeline implementation
**Primary Dependency**: OpenAI API access for automated interviews 