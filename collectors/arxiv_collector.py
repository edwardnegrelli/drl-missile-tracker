#!/usr/bin/env python3
"""Collect papers from arXiv"""

import arxiv
import pandas as pd
from datetime import datetime
import os

def search_arxiv(query, max_results=20):
    print(f"Searching: {query}")
    
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    
    papers = []
    for result in search.results():
        paper = {
            'title': result.title,
            'authors': ', '.join([a.name for a in result.authors]),
            'abstract': result.summary,
            'published': result.published.strftime('%Y-%m-%d'),
            'url': result.entry_id,
            'categories': ', '.join(result.categories)
        }
        papers.append(paper)
        print(f"  ✓ {paper['title'][:50]}...")
    
    return papers

def main():
    queries = [
        'cooperative guidance reinforcement learning',
        'multi-agent missile guidance',
        'distributed UAV swarm control'
    ]
    
    all_papers = []
    print("\nCollecting papers...\n")
    
    for query in queries:
        papers = search_arxiv(query, max_results=15)
        all_papers.extend(papers)
        print(f"  Found {len(papers)} papers\n")
    
    df = pd.DataFrame(all_papers)
    df = df.drop_duplicates(subset=['url'])
    
    print(f"Total unique papers: {len(df)}")
    
    os.makedirs('data/raw', exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output = f'data/raw/arxiv_papers_{timestamp}.csv'
    
    df.to_csv(output, index=False)
    print(f"✅ Saved to: {output}")
    
    print("\nSample papers:")
    for idx, row in df.head(5).iterrows():
        print(f"{idx+1}. {row['title']}")

if __name__ == '__main__':
    print("="*70)
    print("arXiv Paper Collector")
    print("="*70)
    main()