"""
Question Engine for Governor Dossier Generation

Parses questions.md and provides prioritized questions for each governor
based on their domains and personality traits.
"""

from dataclasses import dataclass
from typing import List, Dict, Set
import re
from loguru import logger

from .merger import GovernorProfile


@dataclass
class QuestionSet:
    """A thematic set of questions with priority"""
    thematic_block: str
    questions: List[str]
    priority: int  # 1-5, where 1 is highest priority
    keywords: Set[str]  # Keywords for matching to governor domains


class QuestionEngine:
    """Engine for parsing and prioritizing research questions"""
    
    def __init__(self, questions_data: str):
        """Parse questions.md into structured question sets"""
        self.question_sets = self._parse_questions(questions_data)
        logger.info(f"🔧 Initialized QuestionEngine with {len(self.question_sets)} thematic blocks")
    
    def _parse_questions(self, questions_data: str) -> List[QuestionSet]:
        """Parse the questions.md file into structured question sets"""
        question_sets = []
        lines = questions_data.split('\n')
        
        current_block = None
        current_questions = []
        current_keywords = set()
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check for thematic block headers (## or ###)
            if line.startswith('##') and not line.startswith('###'):
                # Save previous block if exists
                if current_block and current_questions:
                    priority = self._determine_priority(current_block, current_keywords)
                    question_sets.append(QuestionSet(
                        thematic_block=current_block,
                        questions=current_questions.copy(),
                        priority=priority,
                        keywords=current_keywords.copy()
                    ))
                
                # Start new block
                current_block = line.replace('#', '').strip()
                current_questions = []
                current_keywords = self._extract_keywords(current_block)
                logger.debug(f"📋 Found thematic block: {current_block}")
                
            # Check for questions (lines starting with numbers or bullets)
            elif re.match(r'^\d+\.|\*|\-', line):
                question = re.sub(r'^\d+\.\s*|\*\s*|\-\s*', '', line)
                if question and len(question) > 10:  # Filter out very short items
                    current_questions.append(question)
                    # Extract keywords from question
                    current_keywords.update(self._extract_keywords(question))
        
        # Don't forget the last block
        if current_block and current_questions:
            priority = self._determine_priority(current_block, current_keywords)
            question_sets.append(QuestionSet(
                thematic_block=current_block,
                questions=current_questions.copy(),
                priority=priority,
                keywords=current_keywords.copy()
            ))
        
        logger.success(f"🎉 Parsed {len(question_sets)} question sets with {sum(len(qs.questions) for qs in question_sets)} total questions")
        return question_sets
    
    def _extract_keywords(self, text: str) -> Set[str]:
        """Extract relevant keywords from text for matching"""
        # Common domain-related keywords
        keywords = set()
        text_lower = text.lower()
        
        # Magical/esoteric terms
        magical_terms = [
            'magic', 'ritual', 'ceremony', 'invocation', 'evocation',
            'divination', 'scrying', 'vision', 'dream', 'meditation',
            'energy', 'power', 'force', 'essence', 'spirit', 'soul',
            'astral', 'etheric', 'mental', 'causal', 'akashic',
            'chakra', 'aura', 'vibration', 'frequency', 'resonance',
            'alchemy', 'transmutation', 'transformation', 'healing',
            'protection', 'banishing', 'binding', 'manifestation'
        ]
        
        # Elemental terms
        elemental_terms = [
            'fire', 'water', 'air', 'earth', 'spirit',
            'flame', 'ember', 'burn', 'heat', 'solar',
            'flow', 'tide', 'current', 'wave', 'lunar',
            'wind', 'breath', 'sky', 'cloud', 'storm',
            'stone', 'crystal', 'mineral', 'root', 'growth',
            'light', 'shadow', 'void', 'aether', 'quintessence'
        ]
        
        # Practical terms
        practical_terms = [
            'work', 'practice', 'method', 'technique', 'approach',
            'study', 'research', 'investigation', 'exploration',
            'relationship', 'communication', 'interaction', 'influence',
            'guidance', 'teaching', 'learning', 'wisdom', 'knowledge'
        ]
        
        all_terms = magical_terms + elemental_terms + practical_terms
        
        for term in all_terms:
            if term in text_lower:
                keywords.add(term)
        
        # Also extract significant words (longer than 4 chars, not common words)
        common_words = {'that', 'with', 'have', 'this', 'will', 'your', 'from', 'they', 'know', 'want', 'been', 'good', 'much', 'some', 'time', 'very', 'when', 'come', 'here', 'just', 'like', 'long', 'make', 'many', 'over', 'such', 'take', 'than', 'them', 'well', 'were'}
        
        words = re.findall(r'\b[a-zA-Z]{5,}\b', text_lower)
        for word in words:
            if word not in common_words:
                keywords.add(word)
        
        return keywords
    
    def _determine_priority(self, block_name: str, keywords: Set[str]) -> int:
        """Determine priority based on block name and keywords"""
        block_lower = block_name.lower()
        
        # High priority blocks (1-2)
        if any(term in block_lower for term in ['foundation', 'core', 'essential', 'primary', 'basic']):
            return 1
        if any(term in block_lower for term in ['practical', 'application', 'method', 'technique']):
            return 2
        
        # Medium priority blocks (3)
        if any(term in block_lower for term in ['relationship', 'interaction', 'communication']):
            return 3
        
        # Lower priority blocks (4-5)
        if any(term in block_lower for term in ['advanced', 'specialized', 'specific']):
            return 4
        
        # Default medium priority
        return 3
    
    def get_questions_for_governor(self, profile: GovernorProfile) -> List[QuestionSet]:
        """Return prioritized questions relevant to this governor's domains/traits"""
        relevant_sets = []
        
        # Gather all governor-related terms
        governor_terms = set()
        
        # Add domains
        if profile.domains:
            for domain in profile.domains:
                governor_terms.update(self._extract_keywords(domain))
        
        # Add personality traits
        if profile.personality_traits:
            for trait in profile.personality_traits:
                governor_terms.update(self._extract_keywords(trait))
        
        # Add element
        if profile.element:
            governor_terms.add(profile.element.lower())
        
        # Add essence keywords
        if profile.essence:
            governor_terms.update(self._extract_keywords(profile.essence))
        
        # Add themes keywords
        if profile.themes:
            governor_terms.update(self._extract_keywords(profile.themes))
        
        logger.debug(f"🔍 Governor {profile.name} terms: {sorted(list(governor_terms))[:10]}...")
        
        # Score each question set by relevance
        for question_set in self.question_sets:
            relevance_score = len(governor_terms.intersection(question_set.keywords))
            
            if relevance_score > 0:
                # Adjust priority based on relevance
                adjusted_priority = max(1, question_set.priority - (relevance_score // 3))
                
                relevant_set = QuestionSet(
                    thematic_block=question_set.thematic_block,
                    questions=question_set.questions.copy(),
                    priority=adjusted_priority,
                    keywords=question_set.keywords.copy()
                )
                relevant_sets.append(relevant_set)
                logger.debug(f"✅ {question_set.thematic_block}: relevance={relevance_score}, priority={adjusted_priority}")
        
        # Sort by priority (lower number = higher priority)
        relevant_sets.sort(key=lambda x: x.priority)
        
        logger.info(f"🎯 Found {len(relevant_sets)} relevant question sets for {profile.name}")
        return relevant_sets
    
    def get_thematic_blocks(self) -> List[str]:
        """Return all available thematic question blocks"""
        return [qs.thematic_block for qs in self.question_sets]
    
    def get_all_questions_count(self) -> int:
        """Return total number of questions across all sets"""
        return sum(len(qs.questions) for qs in self.question_sets) 