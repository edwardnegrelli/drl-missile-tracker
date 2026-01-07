#!/usr/bin/env python3
"""Inspect collected and scored papers"""

import pandas as pd
import glob
import os

def inspect_raw_papers():
    """Look at raw collected papers"""
    csv_files = glob.glob('data/raw/arxiv_papers_*.csv')
    
    if not csv_files:
        print("No papers found")
        return
    
    latest = max(csv_files, key=os.path.getctime)
    df = pd.read_csv(latest)
    
    print("="*70)
    print(f"RAW COLLECTED PAPERS ({len(df)} total)")
    print("="*70)
    
    print("\nFirst 10 paper titles:")
    for idx, row in df.head(10).iterrows():
        print(f"\n{idx+1}. {row['title']}")
        print(f"   Categories: {row['categories']}")
        print(f"   Abstract preview: {row['abstract'][:150]}...")

def inspect_scored_papers():
    """Look at scored papers"""
    scored_file = 'data/processed/scored_papers.csv'
    
    if not os.path.exists(scored_file):
        print("No scored papers found")
        return
    
    df = pd.read_csv(scored_file)
    
    print("\n" + "="*70)
    print(f"SCORED PAPERS ({len(df)} total)")
    print("="*70)
    
    print("\nScore Distribution:")
    print(f"Relevance: min={df['relevance_score'].min()}, max={df['relevance_score'].max()}, avg={df['relevance_score'].mean():.1f}")
    print(f"Maturity: min={df['maturity_level'].min()}, max={df['maturity_level'].max()}, avg={df['maturity_level'].mean():.1f}")
    
    print("\n" + "="*70)
    print("SAMPLE SCORED PAPERS:")
    print("="*70)
    
    for idx, row in df.head(5).iterrows():
        print(f"\n{idx+1}. {row['title'][:70]}...")
        print(f"   Relevance: {row['relevance_score']}/10")
        print(f"   Maturity: {row['maturity_level']}/5")
        print(f"   Chinese Defense: {row.get('chinese_defense', 'N/A')}")
        print(f"   Reasoning: {row.get('reasoning', 'N/A')[:200]}...")

if __name__ == '__main__':
    inspect_raw_papers()
    print("\n")
    inspect_scored_papers()