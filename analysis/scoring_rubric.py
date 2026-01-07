#!/usr/bin/env python3
"""
Scoring rubric for DRL cooperative missile guidance papers
"""

SCORING_PROMPT = """
You are analyzing a research paper about Deep Reinforcement Learning (DRL) for cooperative missile guidance systems.

Paper Information:
Title: {title}
Authors: {authors}
Published: {published}
Abstract: {abstract}

Analyze this paper and provide scores on the following dimensions:

1. RELEVANCE (0-10): How directly related is this to DRL-based cooperative missile guidance?
   - 10: Directly about DRL for cooperative missile/UAV guidance
   - 7-9: About multi-agent RL for aerial vehicles or guidance systems
   - 4-6: About RL for control/guidance but not cooperative or not aerial
   - 1-3: Tangentially related (general RL, general guidance theory)
   - 0: Not related

2. TECHNOLOGY MATURITY (1-5): What development stage does this represent?
   - 1 = THEORY: Pure algorithms, mathematical proofs, simulation only
   - 2 = LAB DEMO: Component tests, simple scenarios, proof-of-concept
   - 3 = INTEGRATED DEMO: Multi-agent coordination, realistic scenarios, hardware-in-loop mentioned
   - 4 = FIELD TEST: Outdoor tests, actual hardware platforms mentioned, test range activities
   - 5 = OPERATIONAL: Integration with named military systems, operational deployment

3. SOURCE CREDIBILITY (0-10): How credible/important is this source?
   - 10: PLA research institute, defense contractor (AVIC, CASIC, CASC)
   - 8-9: Top defense universities (NUDT, Beihang, Harbin IT, NWPU)
   - 6-7: Other Chinese universities with aerospace programs
   - 4-5: General universities, international collaboration
   - 1-3: Preprints, unaffiliated authors

4. INTEGRATION READINESS (0-10): Does this discuss real-world implementation?
   - 10: Mentions specific missile platforms (PL-15, PL-17, etc.)
   - 7-9: Discusses hardware constraints (compute, power, size, weight)
   - 4-6: Mentions deployment considerations
   - 1-3: Pure theory, no implementation discussion
   - 0: No mention of real-world application

5. KEY TECHNICAL ACHIEVEMENTS: What significant results or capabilities are demonstrated?

6. LIMITATIONS: What limitations or challenges are mentioned?

7. CHINESE DEFENSE CONNECTION: Does this involve Chinese defense institutions?
   - Look for: NUDT, Beihang, NWPU, Harbin Institute of Technology
   - Look for: AVIC, CASIC, CASC, NORINCO
   - Look for: PLA-affiliated labs

Return your analysis as JSON in this exact format:
{{
  "relevance_score": <number 0-10>,
  "maturity_level": <number 1-5>,
  "credibility_score": <number 0-10>,
  "integration_score": <number 0-10>,
  "achievements": "<brief description>",
  "limitations": "<brief description>",
  "chinese_defense": <true/false>,
  "institution_type": "<university/defense_contractor/research_institute/other>",
  "reasoning": "<2-3 sentence explanation of scores>"
}}

Be objective and precise. Only return the JSON, no other text.
"""

def get_scoring_prompt(paper):
    """Generate scoring prompt for a paper"""
    return SCORING_PROMPT.format(
        title=paper.get('title', 'Unknown'),
        authors=paper.get('authors', 'Unknown'),
        published=paper.get('published', 'Unknown'),
        abstract=paper.get('abstract', 'No abstract available')
    )