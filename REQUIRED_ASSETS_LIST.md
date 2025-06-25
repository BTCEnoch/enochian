# Required Assets for AI Script Development

## Core Data Files (Must Provide)

### 1. **governors_dossier.json**
- **Purpose**: Primary canonical data source
- **Contains**: Complete governor profiles with canonical_traits and interpretive_traits
- **Critical Fields**: name, number, element, aethyr, personality_traits, domains_of_knowledge, translations, correspondences
- **Status**: ✅ Available - standardized nested structure

### 2. **personality_traits.json** 
- **Purpose**: Comprehensive personality matrices for all governors
- **Contains**: Detailed personality traits and domains of knowledge
- **Critical Fields**: name, personality_traits[], domains_of_knowledge[]
- **Status**: ✅ Available - 132 entries (91 named governors + 41 unnamed)

### 3. **questions.md**
- **Purpose**: Research question frameworks and methodologies
- **Contains**: Universal question sets, research approaches, interview protocols
- **Critical Sections**: Question categories, research methodologies, data collection frameworks
- **Status**: ✅ Available - needs integration into governor-specific contexts

### 4. **utility_application_matrix.md**
- **Purpose**: Practical application guides and utility frameworks
- **Contains**: Application methodologies, utility matrices, practical implementations
- **Critical Sections**: Application categories, utility frameworks, implementation guides
- **Status**: ✅ Available - needs mapping to individual governors

### 5. **ENOCHIAN_GOVERNORS_LORE_COMPENDIUM.md**
- **Purpose**: Historical context and mythological background
- **Contains**: Traditional lore, historical references, mythological contexts
- **Critical Sections**: Historical backgrounds, traditional attributions, source materials
- **Status**: ✅ Available - needs extraction and governor-specific application

### 6. **prompt_approach_adaptation.md**
- **Purpose**: Template structure and formatting guidelines
- **Contains**: Handoff templates, formatting specifications, structure guidelines
- **Critical Sections**: <handoff> template sections, formatting rules
- **Status**: ✅ Available - needs enhancement for complete profiles

## Reference Files (For Context)

### 7. **enochian_governors_91.json**
- **Purpose**: Original governor data (backup reference)
- **Status**: ✅ Available - superseded by governors_dossier.json

### 8. **Current Output Examples**
- **Files**: output_test2/ADVORPT_dossier.md, output_test2/ADVORPT_chat_prompt.txt
- **Purpose**: Current format examples showing gaps and requirements
- **Status**: ✅ Available - shows what needs enhancement

## Additional Requirements

### 9. **Python Dependencies**
```bash
pip install jinja2 loguru pandas openpyxl
```

### 10. **Template Enhancements Needed**
- Remove all pseudocode sections
- Add comprehensive research question integration
- Include conversation starter frameworks
- Expand personality interaction guidelines
- Add lore collection tracking mechanisms

### 11. **New Output Specifications**
```
REQUIRED OUTPUTS PER GOVERNOR:
├── <GOVERNOR>_complete_dossier.md
├── <GOVERNOR>_chat_setup.txt  
├── <GOVERNOR>_research_protocol.json
└── Supporting files:
    ├── master_governor_index.csv
    ├── research_tracking.xlsx
    └── quality_assurance_report.md
```

## Data Integration Requirements

### Cross-Reference Mapping
- **governors_dossier.json** ↔ **personality_traits.json**: Match by name field
- **questions.md** frameworks → governor-specific question sets
- **utility_application_matrix.md** → domain-specific applications
- **ENOCHIAN_GOVERNORS_LORE_COMPENDIUM.md** → relevant historical context per governor

### Quality Assurance Checkpoints
1. All 91 governors have complete profiles
2. No data loss from source files
3. Uniform structure across all outputs
4. Research frameworks are actionable
5. ChatGPT setups enable authentic roleplay

## File Validation Requirements

### Data Completeness Check
```python
REQUIRED_FIELDS_PER_GOVERNOR = {
    'canonical_traits': ['element', 'aethyr', 'translation', 'domains'],
    'interpretive_traits': ['essence', 'themes', 'boon', 'verse'],
    'personality_traits': ['traits_list'],
    'research_framework': ['questions', 'conversation_starters'],
    'chatgpt_setup': ['nickname', 'role', 'traits', 'context']
}
```

### Output Validation
- Verify markdown formatting consistency
- Check JSON structure validity
- Ensure CSV completeness
- Validate cross-references

## Implementation Priority

### Phase 1: Data Integration
1. Load and merge all data sources
2. Create unified governor profiles
3. Validate data completeness

### Phase 2: Content Generation
1. Generate research question sets
2. Create conversation frameworks
3. Build ChatGPT setup blocks

### Phase 3: Quality Assurance
1. Validate uniform structure
2. Test output completeness
3. Generate tracking systems

**Note**: All listed files must be provided to the AI for complete system development. Missing any file will result in incomplete functionality. 