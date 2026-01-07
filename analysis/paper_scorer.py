#!/usr/bin/env python3
"""
Score papers using Claude API
"""

import os
import json
import pandas as pd
from anthropic import Anthropic
from dotenv import load_dotenv
from tqdm import tqdm
import time

from scoring_rubric import get_scoring_prompt

# Load environment
load_dotenv()

def score_paper(paper, client):
    """
    Score a single paper using Claude API
    
    Args:
        paper: Dictionary with paper metadata
        client: Anthropic client
    
    Returns:
        Dictionary with scores
    """
    
    prompt = get_scoring_prompt(paper)
    
    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = message.content[0].text
        
        # Parse JSON response
        # Remove markdown code blocks if present
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]
        
        scores = json.loads(response_text.strip())
        
        # Add usage stats
        scores['tokens_used'] = message.usage.input_tokens + message.usage.output_tokens
        
        return scores
        
    except json.JSONDecodeError as e:
        print(f"\n⚠️  JSON parsing error for: {paper.get('title', 'Unknown')[:50]}...")
        print(f"   Response: {response_text[:200]}")
        return None
        
    except Exception as e:
        print(f"\n❌ Error scoring paper: {e}")
        return None

def score_papers_batch(input_csv, output_csv, max_papers=None):
    """
    Score a batch of papers from CSV
    
    Args:
        input_csv: Path to input CSV with papers
        output_csv: Path to save scored papers
        max_papers: Maximum number to score (None = all)
    """
    
    # Load papers
    print(f"\nLoading papers from: {input_csv}")
    df = pd.read_csv(input_csv)
    
    if max_papers:
        df = df.head(max_papers)
    
    print(f"Found {len(df)} papers to score")
    
    # Initialize API client
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ No API key found. Check your .env file")
        return
    
    client = Anthropic(api_key=api_key)
    
    # Score each paper
    scored_papers = []
    total_tokens = 0
    
    print("\nScoring papers...\n")
    
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Progress"):
        paper = row.to_dict()
        
        scores = score_paper(paper, client)
        
        if scores:
            # Combine original paper data with scores
            scored_paper = {**paper, **scores}
            scored_papers.append(scored_paper)
            total_tokens += scores.get('tokens_used', 0)
        
        # Rate limiting: small delay between requests
        time.sleep(0.5)
    
    # Convert to DataFrame
    scored_df = pd.DataFrame(scored_papers)
    
    # Save results
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    scored_df.to_csv(output_csv, index=False)
    
    # Print summary
    print("\n" + "="*70)
    print("SCORING COMPLETE")
    print("="*70)
    print(f"Papers scored: {len(scored_papers)}/{len(df)}")
    print(f"Total tokens used: {total_tokens:,}")
    print(f"Estimated cost: ${(total_tokens / 1_000_000) * 3:.4f}")
    print(f"\nSaved to: {output_csv}")
    
    # Show statistics
    if len(scored_papers) > 0:
        print("\n" + "="*70)
        print("SUMMARY STATISTICS")
        print("="*70)
        
        print(f"\nAverage Relevance: {scored_df['relevance_score'].mean():.1f}/10")
        print(f"Average Maturity: {scored_df['maturity_level'].mean():.1f}/5")
        print(f"Average Credibility: {scored_df['credibility_score'].mean():.1f}/10")
        print(f"Average Integration: {scored_df['integration_score'].mean():.1f}/10")
        
        print(f"\nChinese Defense Connection: {scored_df['chinese_defense'].sum()} papers ({scored_df['chinese_defense'].sum()/len(scored_df)*100:.0f}%)")
        
        print("\nTop 5 Most Relevant Papers:")
        top_papers = scored_df.nlargest(5, 'relevance_score')[['title', 'relevance_score', 'maturity_level']]
        for idx, row in top_papers.iterrows():
            print(f"  • {row['title'][:60]}...")
            print(f"    Relevance: {row['relevance_score']}/10, Maturity: {row['maturity_level']}/5\n")
    
    return scored_df

if __name__ == '__main__':
    import sys
    
    # Use curated papers file
    input_file = 'data/raw/curated_papers.csv'
    output_file = 'data/processed/scored_papers.csv'
    
    if not os.path.exists(input_file):
        print(f"❌ Curated papers file not found: {input_file}")
        print("Run fetch_from_excel.py first to create curated papers")
        sys.exit(1)
    
    print("="*70)
    print("DRL Cooperative Missile Guidance - Paper Scorer")
    print("="*70)
    print(f"\nUsing curated papers from: {input_file}\n")
    
    # Score all papers (no limit)
    scored_df = score_papers_batch(input_file, output_file, max_papers=None)