"""
AI Opportunity Explorer Scoring Engine for Odisha AI Nexus.
Provides a transparent, explainable, and reproducible decision-support algorithm.
Evaluates AI product/solution proposals on a 0-100 scale across 6 configurable dimensions.
"""

from typing import Dict, List, Any, Tuple
from config import DEFAULT_SCORING_WEIGHTS

DISCLAIMER_TEXT = (
    "Prototype Decision-Support Tool: This assessment is an automated heuristic score "
    "designed to highlight structured strengths, risks, and gaps. It is NOT a scientifically "
    "validated prediction of commercial success or investment viability."
)

# Domain relevance mappings for Odisha
ODISHA_HIGH_IMPACT_KEYWORDS = {
    "Agriculture & Food Security": [
        "paddy", "rice", "cyclone", "flood", "irrigation", "soil", "pest", "crop",
        "millet", "mandis", "sambalpur", "bargarh", "farmer", "yield", "storage", "cold storage"
    ],
    "Disaster Management & Climate Resilience": [
        "cyclone", "surge", "flood", "inundation", "evacuation", "osdma", "shelter",
        "coastal", "monsoon", "rainfall", "embankment", "early warning", "satellite", "radar"
    ],
    "Steel & Heavy Metallurgy": [
        "steel", "iron ore", "blast furnace", "slag", "refractory", "pellet", "kalinganagar",
        "jajpur", "sponge iron", "metallurgy", "impurity", "rolling mill", "energy efficiency"
    ],
    "Mining & Mineral Exploration": [
        "coal", "bauxite", "chromite", "talcher", "haulage", "dumper", "blasting", "quarry",
        "pit", "vibration", "slope stability", "safety", "conveyor", "grade"
    ],
    "Logistics, Ports & Marine Economy": [
        "dhamra", "paradip", "gopalpur", "berthing", "vessel", "cargo", "anchorage",
        "freight", "turnaround", "port", "bay of bengal", "supply chain", "customs"
    ],
    "Healthcare & Rural MedTech": [
        "malnutrition", "tribal", "anganwadi", "asha", "koraput", "vaccine", "maternal",
        "diagnostic", "telemedicine", "ultrasound", "screening", "phc", "rural health"
    ],
    "Tourism, Temple Tech & Heritage Preservation": [
        "puri", "konark", "jagannath", "heritage", "palm-leaf", "odia", "manuscript",
        "chilika", "temple", "tourism", "handicraft", "crowd management", "pilgrimage"
    ],
    "Handlooms, Handicrafts & MSME Artisans": [
        "sambalpuri", "ikat", "handloom", "weaver", "bargarh", "silk", "filigree",
        "pipili", "patachitra", "artisan", "motif", "counterfeit", "thread count"
    ],
}

GLOBAL_MARKET_NICHES = {
    "Agriculture & Food Security": [
        "Southeast Asian Rice Farming Economies (Vietnam, Thailand, Indonesia, Philippines)",
        "Sub-Saharan African Smallholder AgTech Initiatives (Kenya, Nigeria, Ghana)",
        "Global Climate-Adaptive Crop Insurance & Micro-Fintech Platforms"
    ],
    "Disaster Management & Climate Resilience": [
        "Bay of Bengal & Indo-Pacific Coastal Nations (Bangladesh, Sri Lanka, Philippines)",
        "Caribbean & Gulf of Mexico Hurricane Early Warning Authorities",
        "International Red Cross & UN Disaster Risk Reduction Agencies"
    ],
    "Steel & Heavy Metallurgy": [
        "Primary Steel Producers across APAC (Japan, South Korea, India, Vietnam)",
        "European Decarbonization & Scrap Metallurgy Operators",
        "Latin American Mineral Beneficiation Complexes"
    ],
    "Mining & Mineral Exploration": [
        "Australian Open-Cast Coal & Iron Ore Leaseholders (Pilbara, Hunter Valley)",
        "South American Copper & Lithium Extraction Corridors (Chile, Peru)",
        "Southern African Mining & Mineral Operations (South Africa, Botswana)"
    ],
    "Logistics, Ports & Marine Economy": [
        "Mid-Sized Bulk Ports in Middle East & Persian Gulf (Oman, UAE)",
        "ASEAN Feeder Ports & Coastal Logistics Operators (Malaysia, Vietnam)",
        "Global Maritime Fleet Operators seeking berth demurrage reduction"
    ],
    "Healthcare & Rural MedTech": [
        "Low-and-Middle-Income Countries (LMIC) Primary Health Frameworks (WHO / UNICEF)",
        "Southeast Asian Decentralized Health Clinics",
        "Non-Governmental Global Health & Humanitarian Missions"
    ],
    "Tourism, Temple Tech & Heritage Preservation": [
        "Global Cultural Heritage & Digitization Institutions (UNESCO, National Libraries)",
        "International Museum Conservators & Archival Foundations",
        "Global Odia & Indian Diaspora Cultural Organizations"
    ],
    "Handlooms, Handicrafts & MSME Artisans": [
        "High-End Ethical Fashion & Fair-Trade Boutiques (Western Europe, Japan, US)",
        "Textile Traceability & Blockchain Authenticity Platforms",
        "Craft Preservation & Design Schools Worldwide"
    ],
}


def calculate_opportunity_score(
    title: str,
    sector: str,
    problem_statement: str,
    tech_feasibility_input: int,  # 1-10 scale
    impact_input: int,            # 1-10 scale
    budget_input: int,            # 1-10 scale
    data_readiness_input: int,    # 1-10 scale
    global_potential_input: int,  # 1-10 scale
    custom_weights: Dict[str, float] = None
) -> Dict[str, Any]:
    """
    Calculate opportunity score and generate comprehensive, explainable breakdown.
    
    Inputs:
    - User parameters on 1-10 scale
    - Sector and problem text for automated local relevance matching
    - Optional custom weight dictionary
    """
    weights = custom_weights or DEFAULT_SCORING_WEIGHTS

    # Normalize user inputs (1-10 to 10-100)
    tech_feasibility_score = float(tech_feasibility_input * 10)
    impact_score = float(impact_input * 10)
    budget_score = float(budget_input * 10)
    data_score = float(data_readiness_input * 10)
    global_score = float(global_potential_input * 10)

    # Compute Local Relevance score heuristically based on keywords & problem specificity
    text_corpus = f"{title.lower()} {problem_statement.lower()} {sector.lower()}"
    relevant_keywords = ODISHA_HIGH_IMPACT_KEYWORDS.get(sector, ["odisha", "local", "regional"])
    keyword_matches = sum(1 for kw in relevant_keywords if kw in text_corpus)
    
    # Base local relevance on keyword density and explicit text length
    base_relevance = 60.0
    bonus = min(keyword_matches * 8.0, 35.0)
    if len(problem_statement.strip()) > 150:
        bonus += 5.0
    local_relevance_score = min(100.0, base_relevance + bonus)

    # Factors dictionary (normalized 0-100)
    factors = {
        "technical_feasibility": round(tech_feasibility_score, 1),
        "local_relevance": round(local_relevance_score, 1),
        "socio_economic_impact": round(impact_score, 1),
        "global_market_potential": round(global_score, 1),
        "budget_resource_realism": round(budget_score, 1),
        "data_regulatory_viability": round(data_score, 1),
    }

    # Calculate overall weighted score
    total_weight = sum(weights.values())
    weighted_sum = sum(factors[k] * weights.get(k, 0) for k in factors)
    overall_score = round(weighted_sum / total_weight, 1)

    # Factor point contributions
    contributions = {
        k: round((factors[k] * weights.get(k, 0)) / total_weight, 2)
        for k in factors
    }

    # Generate Strengths
    strengths = []
    if factors["local_relevance"] >= 80:
        strengths.append(
            f"High alignment with Odisha's core economic priorities in {sector} "
            f"({keyword_matches} regional domain markers identified)."
        )
    if factors["technical_feasibility"] >= 80:
        strengths.append("Strong technical clarity with realistic model architectures and delivery mechanisms.")
    if factors["socio_economic_impact"] >= 80:
        strengths.append("High societal leverage with direct potential to improve grassroots livelihoods or operational safety.")
    if factors["global_market_potential"] >= 80:
        strengths.append("Significant exportability; problem structure translates well to international geographic markets.")
    if not strengths:
        strengths.append("Broad thematic alignment with initial problem definition.")

    # Generate Weaknesses & Gaps
    weaknesses = []
    if factors["data_regulatory_viability"] < 70:
        weaknesses.append(
            "Low data readiness or unaddressed regulatory hurdles. Machine learning requires ground-truth "
            "datasets and clear data governance before model development."
        )
    if factors["budget_resource_realism"] < 60:
        weaknesses.append(
            "Budget or resource assumptions appear constrained. Advanced vision, geospatial, or edge "
            "hardware solutions typically require sustained hardware compute and field testing budgets."
        )
    if factors["technical_feasibility"] < 60:
        weaknesses.append(
            "Technical architecture requires further validation. Assess inference latency, network availability, "
            "and edge deployment constraints."
        )
    if len(problem_statement.strip()) < 80:
        weaknesses.append("Problem statement is very concise; provide more operational specifics to refine evaluation.")
    if not weaknesses:
        weaknesses.append("No immediate structural flaws detected; prioritize rapid prototyping and pilot partnerships.")

    # Actionable Recommendations
    recommendations = [
        f"Stage 1 (Local Pilot): Conduct a 30-day proof of concept in a selected district block or pilot partner facility in Odisha.",
        f"Stage 2 (Data Protocol): Formalize data capture agreements and ground-truth validation with domain practitioners.",
        f"Stage 3 (Evaluation Metric): Define a single quantifiable business/social KPI (e.g. false alarm rate < 5%, turnaround reduced by 20%).",
        f"Stage 4 (Ecosystem Engagement): Register the initiative in the Odisha AI Project Registry to discover academic collaborators or student interns."
    ]

    # Multidimensional Risk Matrix
    risks = {
        "technical": (
            "Model degradation under harsh local environmental conditions (e.g., thermal glare, intermittent connectivity, dialect variations)."
            if factors["technical_feasibility"] < 75 else
            "Moderate edge hardware compute bottlenecks and model drift over seasonal operational shifts."
        ),
        "financial": (
            "Risk of running out of development runway before reaching pilot stage without academic or incubator grant support."
            if factors["budget_resource_realism"] < 70 else
            "Manageable initial burn; ensure sufficient budget allocation for data annotation and field pilot testing."
        ),
        "operational": (
            "Difficulty obtaining ground-truth labeled datasets and field-level cooperation from end users."
            if factors["data_regulatory_viability"] < 75 else
            "Field change management and user resistance to adopting automated workflows."
        ),
        "adoption": (
            "End-user hesitation if solution lacks local language support (Odia) or intuitive voice/visual interfaces."
            if "language" in text_corpus or "rural" in text_corpus else
            "Procurement cycles and bureaucratic approvals at enterprise or institutional levels."
        )
    }

    # Target Market Recommendations
    target_markets = GLOBAL_MARKET_NICHES.get(sector, [
        "Domestic Indian Enterprise & Institutional Buyers",
        "Emerging South Asian Technology Ecosystems",
        "Global Humanitarian & Open-Science Collaborations"
    ])

    return {
        "title": title,
        "sector": sector,
        "problem_statement": problem_statement,
        "overall_score": overall_score,
        "factors": factors,
        "contributions": contributions,
        "weights": weights,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations,
        "risks": risks,
        "target_markets": target_markets,
        "disclaimer": DISCLAIMER_TEXT,
    }
