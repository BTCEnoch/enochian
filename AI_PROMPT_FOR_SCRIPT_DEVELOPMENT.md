# AI Development Prompt: Complete Enochian Governor Dossier Generator

## Project Overview
You are tasked with creating a comprehensive Python script that generates complete interactive character profiles for 91 Enochian Governors. Each governor needs a full dossier that serves as a research foundation for AI roleplay sessions, enabling systematic collection of interpretive and creative data to build comprehensive lore.

### Ultimate Goal Context
The complete dossier system serves as a **research platform for systematic lore collection** through structured AI character interactions. Each governor profile must enable:

- **Authentic AI Character Roleplay**: Comprehensive personality matrices and historical context for believable character interactions
- **Systematic Data Collection**: Structured research protocols that guide conversations toward specific lore development areas
- **Organized Knowledge Building**: Consistent frameworks across all 91 governors for building a comprehensive lore database
- **Research Reproducibility**: Standardized approaches that allow multiple researchers to collect comparable data
- **Creative Expansion**: Guided exploration that builds upon canonical foundations while encouraging interpretive development

The generated dossiers will be used by researchers to conduct AI interviews with each governor character, systematically collecting responses that expand the lore database through structured interactions.

## Core Objectives

### 1. **Comprehensive Data Integration**
- Merge ALL available data sources into unified governor profiles
- Ensure no canonical information is lost or duplicated
- Create consistent structure across all 91 governors
- Maintain data integrity and relationships

### 2. **Interactive Research Framework**
- Generate conversation starter questions for each governor
- Create structured interview protocols for lore collection
- Provide thematic research directions based on each governor's domains
- Include follow-up question trees for deep exploration

### 3. **AI Roleplay Preparation**
- Create complete ChatGPT customization blocks (4 fields)
- Include comprehensive personality matrices
- Provide historical/mythological context for authentic responses
- Generate conversation flow guidelines

### 4. **Uniform Output Standards**
- Every governor must have identical section structure
- Consistent formatting across all outputs
- Standardized research protocols
- Quality assurance mechanisms

## Technical Requirements

### Input Processing
```
AVAILABLE DATA SOURCES (ALL READY):
✅ governors_dossier.json (canonical traits + interpretive data) - 121KB, 2915 lines
✅ personality_traits.json (extracted personality matrices) - NEWLY CREATED
✅ questions.md (research question frameworks) - 97 questions across 11 thematic blocks
✅ utility_application_matrix.md (practical application guides) - 77KB, 167 lines
✅ ENOCHIAN_GOVERNORS_LORE_COMPENDIUM.md (historical context) - 133KB, 2951 lines
✅ prompt_approach_adaptation.md (template structure) - NEWLY CREATED
✅ visual_description.json (visual design specifications) - 6KB, 92 lines
✅ descriptive_formula.md (content generation guidelines) - 2.8KB, 38 lines
✅ TEMPLATE_CONSTRUCTION_CHECKLIST.md (quality control reference) - 3KB, 76 lines
✅ output/ directory (current format examples) - 91 existing dossiers + chat prompts
```

### Output Specifications
```
FOR EACH GOVERNOR, GENERATE:
1. <GOVERNOR>_complete_dossier.md
   - Full canonical profile
   - Interpretive characteristics
   - Historical context from compendium
   - Research question sets
   - Conversation starters
   - Thematic exploration paths
   - Personality interaction guidelines

2. <GOVERNOR>_chat_setup.txt
   - ChatGPT 4-field customization block
   - Initial conversation primer
   - Roleplay context establishment
   - Response collection framework

3. <GOVERNOR>_research_protocol.json
   - Structured interview questions
   - Follow-up question trees
   - Data collection categories
   - Lore development tracking

4. master_governor_index.csv
   - Quick reference for all governors
   - Key attributes summary
   - Research status tracking
```

## Critical Implementation Rules

### 1. **NO PSEUDOCODE**
- Remove all pseudocode sections from templates
- Replace with actual research questions
- Use real conversation starters
- Provide concrete interaction examples

### 2. **Complete Data Utilization**
- Extract ALL personality traits from personality_traits.json
- Include ALL canonical data from governors_dossier.json
- Reference relevant sections from ENOCHIAN_GOVERNORS_LORE_COMPENDIUM.md
- Apply question frameworks from questions.md
- Integrate utility applications from utility_application_matrix.md

### 3. **Research Framework Integration**
- Convert abstract questions into governor-specific inquiries
- Create thematic question sets based on domains of knowledge
- Generate conversation flow charts for systematic exploration
- Include lore collection categories for organized data gathering

### 4. **Uniform Structure Enforcement**
```
EVERY GOVERNOR DOSSIER MUST CONTAIN:
□ Complete canonical profile
□ Full personality trait matrix
□ Historical/mythological context
□ Domain-specific research questions
□ Conversation starter sets
□ Interaction guidelines
□ Response collection framework
□ Lore development tracking
□ ChatGPT setup instructions
```

## Script Architecture Requirements

### Core Functions Needed:
1. `load_all_data_sources()` - Unified data ingestion
2. `merge_governor_profiles()` - Combine all data per governor
3. `generate_research_questions()` - Create governor-specific inquiries
4. `build_conversation_framework()` - Structure interaction protocols
5. `create_chatgpt_setup()` - Generate AI customization blocks
6. `validate_completeness()` - Ensure uniform output quality
7. `generate_master_index()` - Create summary documentation

### Quality Assurance:
- Verify all 91 governors processed
- Check for missing data fields
- Validate question set completeness
- Ensure uniform formatting
- Test ChatGPT setup blocks

## Expected Deliverables

### Primary Outputs:
- 91 complete governor dossiers (markdown)
- 91 ChatGPT setup files (text)
- 91 research protocol files (JSON)
- Master index and tracking files (CSV)
- Quality assurance report

### Success Criteria:
- Every governor has complete, uniform profile
- All source data integrated without loss
- Research frameworks are actionable
- ChatGPT setups enable authentic roleplay
- System supports systematic lore collection

## Implementation Notes

**ALL ASSETS AVAILABLE**: The workspace contains all required data sources and templates. Implementation can begin immediately.

**Key Advantages:**
- **Complete Data Set**: governors_dossier.json contains standardized nested structure for all 91 governors
- **Comprehensive Questions**: questions.md provides 97 research questions across 11 thematic blocks  
- **Rich Context**: ENOCHIAN_GOVERNORS_LORE_COMPENDIUM.md offers extensive historical background
- **Existing Examples**: output/ directory shows current format for enhancement reference
- **Visual Integration**: visual_description.json enables rich visual context integration

**Technical Implementation:**
- Use Jinja2 for template processing with prompt_approach_adaptation.md
- Implement comprehensive error handling and progress logging with loguru
- Support batch processing with resume capability for all 91 governors
- Generate validation reports for quality control and completeness checking
- Create backup systems for data integrity during processing

**Success Criteria:**
- Every governor has complete, uniform research profile
- All source data integrated without loss
- Research frameworks are immediately actionable for AI character interviews
- ChatGPT setups enable authentic roleplay sessions
- System supports systematic lore collection and database expansion

Build this as a production-ready research platform that enables systematic collection of interpretive data from AI governor characters, creating a comprehensive lore database through structured, reproducible interactions. 