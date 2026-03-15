# Pattern 4: Lists of dictionaries - how ChromaDB returns results

# This is exactly what ChromaDB query results look like
search_results = [
    {'text': 'CICS is a transaction server', 'score': 0.95, 'source': 'doc1.txt'},
    {'text': 'JCL controls job execution', 'score': 0.87, 'source': 'doc2.txt'},
    {'text': 'VSAM is a file access method', 'score': 0.82, 'source': 'doc3.txt'},
]

# Loop through results - exactly what your RAG pipeline will do
for i, result in enumerate(search_results, 1):
    print(f"Result {i} (score: {result['score']}): {result['text']}")

# Filter results above a threshold
good_results = [r for r in search_results if r['score'] > 0.85]
print(f"\nHigh quality results: {len(good_results)}")

