# knowledge_base.py
# A simple knowledge base - preview of what ChromaDB does in Phase 5

import json
import os

# Our knowledge base is a list of dictionaries
# This mirrors how ChromaDB stores documents internally
knowledge_base = []
KB_FILE = 'knowledge_base.json'
def save_kb():
    """Save knowledge base to disk - like a VSAM CLOSE with DISP=KEEP"""
    with open(KB_FILE, 'w') as f:
        json.dump(knowledge_base, f, indent=2)
    print(f'Saved {len(knowledge_base)} entries to {KB_FILE}')

def load_kb():
    """Load knowledge base from disk - like a VSAM OPEN"""
    global knowledge_base
    if os.path.exists(KB_FILE):
        with open(KB_FILE, 'r') as f:
            knowledge_base = json.load(f)
        print(f'Loaded {len(knowledge_base)} entries from {KB_FILE}')
    else:
        print('No existing knowledge base found. Starting fresh.')

def add_entry(topic, content, source='manual'):
    """Add an entry to the knowledge base"""
    # Check for duplicates first
    for entry in knowledge_base:
        if entry['topic'].lower() == topic.lower():
            print(f'Entry already exists: {topic} - skipping')
            return None
    entry = {
        'id': len(knowledge_base) + 1,
        'topic': topic,
        'content': content,
        'source': source
    }
    knowledge_base.append(entry)
    print(f'Added entry {entry["id"]}: {topic}')
    return entry

def search(query):
    """Search entries by keyword - simple version of what ChromaDB does semantically"""
    query_lower = query.lower()
    results = []
    for entry in knowledge_base:
        if (query_lower in entry['topic'].lower() or
                query_lower in entry['content'].lower()):
            results.append(entry)
    return results
def display_results(results, query):
    """Display search results - like a formatted report"""
    print(f'\nSearch results for: "{query}"')
    print('-' * 50)
    if not results:
        print('No results found.')
        return
    for i, entry in enumerate(results, 1):
        print(f'{i}. [{entry["topic"]}] {entry["content"][:80]}...')
        print(f'   Source: {entry["source"]} | ID: {entry["id"]}')


# Main program - runs when you execute the script
if __name__ == '__main__':
    # Load any existing data
    load_kb()

    # Add some mainframe knowledge entries
    add_entry('CICS', 'CICS is a transaction server that receives requests and routes them to programs. It manages regions, tasks, and resources.', 'mainframe_manual')
    add_entry('JCL', 'Job Control Language defines batch jobs with steps, datasets, and programs. EXEC PGM= runs a program, DD defines datasets.', 'mainframe_manual')
    add_entry('VSAM', 'VSAM is a file access method supporting KSDS keyed, ESDS sequential, and RRDS relative organizations.', 'mainframe_manual')
    add_entry('DB2', 'DB2 is the IBM relational database for z/OS. It uses SQL for queries and BIND for program access packages.', 'mainframe_manual')
    add_entry('Ollama', 'Ollama is the local LLM server for macOS. It is the CICS equivalent for AI - receives requests and routes to models.', 'ai_notes')
    add_entry('ChromaDB', 'ChromaDB is a vector database. It stores embeddings and enables semantic search - like VSAM but searches by meaning not exact key.', 'ai_notes')

    # Save to disk
    save_kb()

    # Test searches
    display_results(search('CICS'), 'CICS')
    display_results(search('database'), 'database')
    display_results(search('semantic'), 'semantic')
    display_results(search('python'), 'python')