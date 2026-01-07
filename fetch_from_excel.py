#!/usr/bin/env python3
"""Fetch paper details from Excel list of titles"""

import pandas as pd
import arxiv
from scholarly import scholarly
import time
import os
from tqdm import tqdm

def search_paper_by_title(title):
    """
    Search for paper by title on arXiv and Google Scholar
    
    Args:
        title: Paper title string
    
    Returns:
        Dictionary with paper data or None
    """
    
    print(f"\nSearching: {title[:70]}...")
    
    # Try arXiv first (faster and more reliable)
    try:
        search = arxiv.Search(
            query=f'ti:"{title}"',
            max_results=3
        )
        
        results = list(search.results())
        
        if results:
            result = results[0]  # Take first match
            paper = {
                'title': result.title,
                'authors': ', '.join([a.name for a in result.authors]),
                'abstract': result.summary,
                'published': result.published.strftime('%Y-%m-%d'),
                'url': result.entry_id,
                'categories': ', '.join(result.categories),
                'source': 'arxiv',
                'search_title': title,
                'match_quality': 'exact' if title.lower() in result.title.lower() else 'partial'
            }
            print(f"  ✓ Found on arXiv: {result.title[:60]}...")
            return paper
    except Exception as e:
        print(f"  ⚠️  arXiv search failed: {e}")
    
    # Try Google Scholar as backup
    try:
        print(f"  Trying Google Scholar...")
        search_query = scholarly.search_pubs(title)
        result = next(search_query)
        
        paper = {
            'title': result['bib']['title'],
            'authors': ', '.join(result['bib'].get('author', ['Unknown'])),
            'abstract': result['bib'].get('abstract', 'Abstract not available from Google Scholar'),
            'published': str(result['bib'].get('pub_year', 'Unknown')),
            'url': result.get('pub_url', result.get('eprint_url', 'No URL available')),
            'categories': 'Not specified',
            'source': 'google_scholar',
            'search_title': title,
            'match_quality': 'google_scholar'
        }
        print(f"  ✓ Found on Google Scholar: {result['bib']['title'][:60]}...")
        return paper
    except Exception as e:
        print(f"  ⚠️  Google Scholar search failed: {e}")
    
    print(f"  ❌ Not found")
    return None

def fetch_papers_from_excel(excel_file):
    """
    Read Excel file with paper titles and fetch full paper data
    
    Args:
        excel_file: Path to Excel file with titles
    """
    
    print("="*70)
    print("Fetching Papers from Excel List")
    print("="*70)
    
    # Read Excel file
    print(f"\nReading: {excel_file}")
    
    try:
        df = pd.read_excel(excel_file)
    except FileNotFoundError:
        print(f"❌ File not found: {excel_file}")
        print("\nMake sure the Excel file is in your project folder:")
        print(f"   {os.getcwd()}")
        return None
    
    # Find the column with titles
    # Try common column names
    title_column = None
    for col in df.columns:
        if 'title' in col.lower():
            title_column = col
            break
    
    # If no column named 'title', use first column
    if title_column is None:
        title_column = df.columns[0]
        print(f"\nUsing first column as titles: '{title_column}'")
    
    titles = df[title_column].dropna().tolist()
    
    print(f"Found {len(titles)} paper titles")
    
    # Fetch each paper
    papers = []
    not_found = []
    
    print("\n" + "="*70)
    print("Fetching paper details...")
    print("="*70)
    
    for idx, title in enumerate(titles, 1):
        print(f"\n[{idx}/{len(titles)}]", end=" ")
        
        paper = search_paper_by_title(title)
        
        if paper:
            papers.append(paper)
        else:
            not_found.append(title)
        
        # Rate limiting to avoid being blocked
        time.sleep(3)
    
    # Save found papers
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)
    
    if papers:
        papers_df = pd.DataFrame(papers)
        
        output_file = 'data/raw/curated_papers.csv'
        os.makedirs('data/raw', exist_ok=True)
        papers_df.to_csv(output_file, index=False)
        
        print(f"\n✅ Successfully fetched {len(papers)}/{len(titles)} papers")
        print(f"   Saved to: {output_file}")
        
        # Show statistics
        print("\nSources:")
        print(papers_df['source'].value_counts().to_string())
        
        # Show sample
        print("\n" + "="*70)
        print("Sample of fetched papers:")
        print("="*70)
        for idx, row in papers_df.head(5).iterrows():
            print(f"\n{idx+1}. {row['title']}")
            print(f"   Authors: {row['authors'][:60]}...")
            print(f"   Published: {row['published']}")
    
    # Report not found
    if not_found:
        print("\n" + "="*70)
        print(f"⚠️  Could not auto-fetch {len(not_found)} papers:")
        print("="*70)
        
        # Save not found list
        not_found_df = pd.DataFrame({'title': not_found})
        not_found_file = 'data/raw/papers_not_found.csv'
        not_found_df.to_csv(not_found_file, index=False)
        
        for title in not_found[:5]:
            print(f"  • {title}")
        if len(not_found) > 5:
            print(f"  ... and {len(not_found)-5} more")
        
        print(f"\nFull list saved to: {not_found_file}")
        print("\nFor papers not found, you can:")
        print("  1. Manually add them to curated_papers.csv")
        print("  2. Search for them manually and add URLs")
        print("  3. Try different title variations")
    
    return papers_df

if __name__ == '__main__':
    import sys
    
    # Check if Excel file is provided
    if len(sys.argv) > 1:
        excel_file = sys.argv[1]
    else:
        # Default filename
        excel_file = 'curated_paper_titles.xlsx'
    
    print("\nLooking for Excel file...")
    
    if not os.path.exists(excel_file):
        print(f"\n❌ File not found: {excel_file}")
        print("\nUsage:")
        print("  1. Save your Excel file as 'curated_paper_titles.xlsx'")
        print("  2. Put it in your project folder")
        print("  3. Run: python fetch_from_excel.py")
        print("\nOr specify file path:")
        print("  python fetch_from_excel.py path/to/your/file.xlsx")
        sys.exit(1)
    
    fetch_papers_from_excel(excel_file)