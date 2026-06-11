#!/usr/bin/env python3
"""
Content Generation Skill
Generates content based on NYVC pedagogy and trending topics.
HUMAN-IN-THE-LOOP GATE: Does not execute without user vector selection.
"""
import json, os
from datetime import datetime
from pathlib import Path

PEDAGOGY_DIR = Path('/home/user/workspace/pedagogy')
VAULT_DIR = Path('/home/user/workspace/vault')
TRENDS_FILE = VAULT_DIR / 'trends.json'

def load_pedagogy():
    """Load NYVC framework references."""
    framework = {}
    for f in PEDAGOGY_DIR.glob('*.md'):
        with open(f) as fh:
            framework[f.stem] = fh.read()
    return framework

def load_trends():
    """Load latest trend scan."""
    if TRENDS_FILE.exists():
        with open(TRENDS_FILE) as f:
            return json.load(f)
    return {}

def generate_content_brief(topic, target_audience='singers', content_type='blog'):
    """Generate a content brief based on topic + NYVC framework."""
    pedagogy = load_pedagogy()
    trends = load_trends()
    
    brief = {
        'topic': topic,
        'target_audience': target_audience,
        'content_type': content_type,
        'generated_at': datetime.utcnow().isoformat(),
        'nyvc_alignment': [],
        'trend_signals': [],
        'outline': [],
        'status': 'PENDING_APPROVAL',
    }
    
    # Find relevant NYVC concepts
    framework = pedagogy.get('nyvc-framework', '')
    exercises = pedagogy.get('nyvc-exercises', '')
    
    # Simple keyword matching for NYVC alignment
    topic_lower = topic.lower()
    nyvc_concepts = {
        'breath': ['breath support', 'appoggio', 'diaphragmatic'],
        'belt': ['belt coordination', 'thick folds', 'twang'],
        'mix': ['mix voice', 'registration balance', 'passaggio'],
        'resonance': ['forward placement', 'mask resonance', 'formant'],
        'onset': ['clean onset', 'vocal fold closure', 'glottal'],
        'range': ['vowel modification', 'covering', 'registration'],
        'warmup': ['daily routine', 'vocal health', 'hydration'],
    }
    
    for concept, keywords in nyvc_concepts.items():
        if any(kw in topic_lower for kw in keywords):
            brief['nyvc_alignment'].append(concept)
    
    # Find trend signals
    for proposal in trends.get('proposals', []):
        if any(kw in proposal.get('title', '').lower() for kw in topic_lower.split()):
            brief['trend_signals'].append(proposal['title'])
    
    return brief

def generate_exercise_content(exercise_name, level='beginner'):
    """Generate exercise content from NYVC library."""
    exercises_path = PEDAGOGY_DIR / 'nyvc-exercises.md'
    if not exercises_path.exists():
        return {'error': 'Exercise library not found'}
    
    with open(exercises_path) as f:
        content = f.read()
    
    # Find the exercise
    exercise_section = None
    sections = content.split('### ')
    for section in sections:
        if exercise_name.lower() in section.lower():
            exercise_section = section
            break
    
    if not exercise_section:
        return {'error': f'Exercise "{exercise_name}" not found in library'}
    
    return {
        'exercise': exercise_name,
        'level': level,
        'content': exercise_section[:1000],
        'source': 'NYVC Exercise Library',
        'generated_at': datetime.utcnow().isoformat(),
    }

def list_available_exercises():
    """List all available exercises from NYVC library."""
    exercises_path = PEDAGOGY_DIR / 'nyvc-exercises.md'
    if not exercises_path.exists():
        return []
    
    with open(exercises_path) as f:
        content = f.read()
    
    exercises = []
    for line in content.split('\n'):
        if line.startswith('**') and '**' in line[2:]:
            name = line.strip('*').strip()
            if name and not name.startswith('Source'):
                exercises.append(name)
    
    return exercises

if __name__ == '__main__':
    print("=== Content Generation Skill ===")
    print("Status: HUMAN-IN-THE-LOOP GATE")
    print()
    print("Available exercises:")
    for ex in list_available_exercises():
        print(f"  - {ex}")
    print()
    print("To generate content, call generate_content_brief() with a topic.")
    print("Execution requires user vector selection.")
