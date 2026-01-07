#!/usr/bin/env python3
"""Try to find missing papers using Semantic Scholar"""

import pandas as pd
import requests
import time
from tqdm import tqdm

def search_semantic_scholar(title):
    """Search Semantic Scholar for a paper by title"""
    
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    
    params = {
        'query': title,
        'fields': 'title,authors,abstract,year,url,venue,publicationTypes',
        'limit': 3
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('data') and len(data['data']) > 0:
                result = data['data'][0]  # Take first match
                
                # Extract author names
                authors = ', '.join([a.get('name', 'Unknown') for a in result.get('authors', [])])
                
                paper = {
                    'title': result.get('title', title),
                    'authors': authors,
                    'abstract': result.get('abstract', 'Abstract not available'),
                    'published': str(result.get('year', 'Unknown')),
                    'url': result.get('url', 'No URL'),
                    'categories': result.get('venue', 'Not specified'),
                    'source': 'semantic_scholar'
                }
                
                return paper
        
        return None
        
    except Exception as e:
        print(f"Error: {e}")
        return None

def fetch_missing_papers():
    """Try to fetch papers that weren't found previously"""
    
    # Load the not-found list
    not_found_file = 'data/raw/papers_not_found.csv'
    
    try:
        not_found_df = pd.read_csv(not_found_file)
    except FileNotFoundError:
        print(f"❌ File not found: {not_found_file}")
        return
    
    titles = not_found_df['title'].tolist()
    
    print("="*70)
    print(f"Searching Semantic Scholar for {len(titles)} missing papers")
    print("="*70)
    
    found_papers = []
    still_not_found = []
    
    for idx, title in enumerate(titles, 1):
        print(f"\n[{idx}/{len(titles)}] {title[:60]}...")
        
        paper = search_semantic_scholar(title)
        
        if paper:
            found_papers.append(paper)
            print(f"  ✓ Found!")
        else:
            still_not_found.append(title)
            print(f"  ✗ Not found")
        
        time.sleep(1)  # Rate limiting
    
    # Save newly found papers
    if found_papers:
        new_df = pd.DataFrame(found_papers)
        
        # Append to existing curated papers
        existing_file = 'data/raw/curated_papers.csv'
        
        try:
            existing_df = pd.read_csv(existing_file)
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        except FileNotFoundError:
            combined_df = new_df
        
        combined_df.to_csv(existing_file, index=False)
        
        print("\n" + "="*70)
        print(f"✅ Found {len(found_papers)} additional papers")
        print(f"   Added to: {existing_file}")
        print(f"   Total papers now: {len(combined_df)}")
    
    # Update not-found list
    if still_not_found:
        still_not_found_df = pd.DataFrame({'title': still_not_found})
        still_not_found_df.to_csv(not_found_file, index=False)
        
        print("\n" + "="*70)
        print(f"⚠️  Still couldn't find {len(still_not_found)} papers")
        print(f"   Updated: {not_found_file}")
    else:
        print("\n✅ All papers found!")

if __name__ == '__main__':
    fetch_missing_papers()