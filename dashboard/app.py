#!/usr/bin/env python3
"""
Interactive Dashboard for DRL Cooperative Missile Guidance Tracker
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="DRL Missile Guidance Tracker",
    page_icon="🚀",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    """Load scored papers data"""
    scored_file = 'data/processed/scored_papers.csv'
    
    if not os.path.exists(scored_file):
        return None
    
    df = pd.read_csv(scored_file)
    
    # Parse publication dates
    df['published'] = pd.to_datetime(df['published'], errors='coerce')
    df['year'] = df['published'].dt.year
    
    return df

# Main dashboard
def main():
    # Title and header
    st.title("🚀 DRL Cooperative Missile Guidance Tracker")
    st.markdown("### Tracking Chinese Research on Deep Reinforcement Learning for Cooperative Guidance")
    
    # Load data
    df = load_data()
    
    if df is None or len(df) == 0:
        st.error("No data found. Run the paper scorer first!")
        st.code("python analysis/paper_scorer.py")
        return
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Relevance filter
    min_relevance = st.sidebar.slider(
        "Minimum Relevance Score",
        min_value=0,
        max_value=10,
        value=0,
        help="Filter papers by relevance score"
    )
    
    # Maturity filter
    maturity_options = sorted(df['maturity_level'].dropna().unique())
    selected_maturity = st.sidebar.multiselect(
        "Technology Maturity Level",
        options=maturity_options,
        default=maturity_options,
        help="TRL 1=Theory, 5=Operational"
    )
    
    # Apply filters
    filtered_df = df[
        (df['relevance_score'] >= min_relevance) &
        (df['maturity_level'].isin(selected_maturity))
    ]
    
    # Executive Summary
    st.header("📊 Executive Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Papers Tracked",
            len(filtered_df),
            delta=f"{len(filtered_df) - len(df)}" if len(filtered_df) != len(df) else None
        )
    
    with col2:
        avg_relevance = filtered_df['relevance_score'].mean()
        st.metric(
            "Avg Relevance",
            f"{avg_relevance:.1f}/10",
            help="Average relevance score"
        )
    
    with col3:
        avg_maturity = filtered_df['maturity_level'].mean()
        st.metric(
            "Avg Maturity",
            f"{avg_maturity:.1f}/5",
            help="Average TRL maturity level"
        )
    
    with col4:
        chinese_defense_count = filtered_df['chinese_defense'].sum()
        chinese_defense_pct = (chinese_defense_count / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
        st.metric(
            "Defense Connection",
            f"{chinese_defense_pct:.0f}%",
            help="Papers with Chinese defense institution connection"
        )
    
    # Key insights
    st.markdown("---")
    
    # Charts row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Relevance Distribution")
        
        fig = px.histogram(
            filtered_df,
            x='relevance_score',
            nbins=10,
            title="Distribution of Relevance Scores",
            labels={'relevance_score': 'Relevance Score', 'count': 'Number of Papers'},
            color_discrete_sequence=['#1f77b4']
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Technology Maturity Levels")
        
        maturity_counts = filtered_df['maturity_level'].value_counts().sort_index()
        
        fig = px.bar(
            x=maturity_counts.index,
            y=maturity_counts.values,
            title="Papers by TRL Maturity Level",
            labels={'x': 'TRL Level', 'y': 'Number of Papers'},
            color=maturity_counts.values,
            color_continuous_scale='Viridis'
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Charts row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📅 Publication Timeline")
        
        if 'year' in filtered_df.columns:
            year_counts = filtered_df['year'].value_counts().sort_index()
            
            fig = px.line(
                x=year_counts.index,
                y=year_counts.values,
                title="Papers Published by Year",
                labels={'x': 'Year', 'y': 'Number of Papers'},
                markers=True
            )
            fig.update_traces(line_color='#ff7f0e', marker=dict(size=10))
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🔬 Integration Readiness")
        
        fig = px.scatter(
            filtered_df,
            x='relevance_score',
            y='integration_score',
            size='maturity_level',
            color='maturity_level',
            hover_data=['title'],
            title="Relevance vs Integration Readiness",
            labels={
                'relevance_score': 'Relevance Score',
                'integration_score': 'Integration Score',
                'maturity_level': 'TRL'
            },
            color_continuous_scale='Turbo'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Top Papers Section
    st.markdown("---")
    st.header("🏆 Top Papers by Relevance")
    
    top_n = st.slider("Number of papers to display", 3, 10, 5)
    
    top_papers = filtered_df.nlargest(top_n, 'relevance_score')
    
    for idx, row in top_papers.iterrows():
        with st.expander(f"**{row['title']}** (Relevance: {row['relevance_score']}/10)"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Relevance", f"{row['relevance_score']}/10")
            with col2:
                st.metric("Maturity", f"{row['maturity_level']}/5")
            with col3:
                st.metric("Integration", f"{row['integration_score']}/10")
            
            st.markdown(f"**Authors:** {row['authors']}")
            st.markdown(f"**Published:** {row['published']}")
            
            if pd.notna(row.get('achievements')):
                st.markdown(f"**Key Achievements:** {row['achievements']}")
            
            if pd.notna(row.get('limitations')):
                st.markdown(f"**Limitations:** {row['limitations']}")
            
            if pd.notna(row.get('reasoning')):
                st.markdown(f"**Analysis:** {row['reasoning']}")
            
            if pd.notna(row.get('url')):
                st.markdown(f"[📄 View Paper]({row['url']})")
    
    # All Papers Table
    st.markdown("---")
    st.header("📚 All Papers")
    
    # Select columns to display
    display_columns = [
        'title', 
        'authors', 
        'relevance_score', 
        'maturity_level',
        'credibility_score',
        'integration_score',
        'published'
    ]
    
    # Create display dataframe
    display_df = filtered_df[display_columns].copy()
    display_df = display_df.sort_values('relevance_score', ascending=False)
    
    # Rename columns for display
    display_df.columns = [
        'Title',
        'Authors',
        'Relevance',
        'Maturity',
        'Credibility',
        'Integration',
        'Published'
    ]
    
    st.dataframe(
        display_df,
        use_container_width=True,
        height=400
    )
    
    # Download option
    st.markdown("---")
    st.subheader("💾 Download Data")
    
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download Filtered Papers as CSV",
        data=csv,
        file_name=f"filtered_papers_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
    
    # Footer
    st.markdown("---")
    st.caption(f"Dashboard generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.caption(f"Total papers in database: {len(df)} | Displayed: {len(filtered_df)}")

if __name__ == '__main__':
    main()