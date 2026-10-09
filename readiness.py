"""
Global Market Readiness Assessment Module for Odisha AI Nexus.
Assesses an AI initiative's export maturity across 10 critical operational dimensions.
Maps projects to prospective international market corridors with explicit hypothesis disclaimers.
"""

from typing import Dict, List, Any

READINESS_CHECKLIST = [
    {
        "id": "prototype",
        "title": "1. Benchmarked Working Prototype",
        "description": "Functional solution tested on real-world representative data with documented accuracy, F1-score, and latency metrics.",
        "category": "Technology & Architecture",
        "weight": 10,
    },
    {
        "id": "measurable_roi",
        "title": "2. Quantifiable Customer ROI",
        "description": "Defined financial or operational cost-saving proposition (e.g., reduces downtime by 15%, saves 40 man-hours/month).",
        "category": "Value Proposition",
        "weight": 10,
    },
    {
        "id": "reliability_testing",
        "title": "3. Reliability, Latency & Load Testing",
        "description": "Stress-tested against packet loss, burst requests, and edge failover conditions with monitored uptime SLAs.",
        "category": "Technology & Architecture",
        "weight": 10,
    },
    {
        "id": "data_protection",
        "title": "4. Data Privacy & Encryption Standards",
        "description": "End-to-end TLS encryption, data residency adherence, anonymization protocols, and alignment with India DPDP Act / EU GDPR.",
        "category": "Governance & Compliance",
        "weight": 10,
    },
    {
        "id": "documentation",
        "title": "5. Technical Specs & API Documentation",
        "description": "Comprehensive OpenAPI/Swagger documentation, deployment runbooks, schema definitions, and developer quick-starts.",
        "category": "Operations & Support",
        "weight": 10,
    },
    {
        "id": "localization",
        "title": "6. Language & Cultural Localization",
        "description": "Support for international date/currency formats, UTF-8 multilingual characters, and localized interface paradigms.",
        "category": "Market Adaptation",
        "weight": 10,
    },
    {
        "id": "support_sla",
        "title": "7. Support Coverage & SLA Framework",
        "description": "Clear issue escalation tiers, response time commitments across target timezones, and ticketing workflows.",
        "category": "Operations & Support",
        "weight": 10,
    },
    {
        "id": "pricing_model",
        "title": "8. Transparent International Pricing",
        "description": "Clear multi-currency pricing tiers (USD/EUR/INR), automated recurring billing (e.g., Stripe), and refund policies.",
        "category": "Business Model",
        "weight": 10,
    },
    {
        "id": "ip_licensing",
        "title": "9. IP Protection & OSS License Compliance",
        "description": "Audit of all third-party libraries (MIT/Apache vs copyleft GPL), proprietary algorithms, and trademark/patent clearing.",
        "category": "Governance & Compliance",
        "weight": 10,
    },
    {
        "id": "regulatory_compliance",
        "title": "10. Regulatory Risk & AI Governance (EU AI Act)",
        "description": "Classification under high-risk AI frameworks (EU AI Act, US NIST AI RMF), model bias audits, and explainability controls.",
        "category": "Governance & Compliance",
        "weight": 10,
    },
]

GLOBAL_MARKET_CORRIDORS = {
    "Disaster Management & Climate Resilience": [
        {"region": "Southeast Asia (ASEAN)", "countries": "Philippines, Vietnam, Indonesia", "rationale": "High monsoon and typhoon vulnerability; immense demand for community flood routing and early storm surge warnings."},
        {"region": "Bay of Bengal Rim", "countries": "Bangladesh, Sri Lanka", "rationale": "Shared coastal climate dynamics; high receptivity to cost-effective satellite SAR hydrologic predictive models."},
        {"region": "Caribbean Basin", "countries": "Jamaica, Dominican Republic, Barbados", "rationale": "Island economies requiring hurricane inundation early warning without expensive sensor infrastructure."}
    ],
    "Agriculture & Food Security": [
        {"region": "Southeast Asian Rice Belt", "countries": "Thailand, Vietnam, Cambodia", "rationale": "Intensive smallholder paddy farming with severe exposure to Brown Plant Hopper (BPH) and leaf blast pathogens."},
        {"region": "East & West Africa", "countries": "Kenya, Nigeria, Tanzania", "rationale": "Offline edge mobile vision models for localized smallholder pest diagnosis where cellular data is scarce."},
        {"region": "Latin America", "countries": "Brazil, Colombia", "rationale": "Expanding specialty crop and grain sectors with rapid adoption of smartphone-based agricultural diagnostics."}
    ],
    "Steel & Heavy Metallurgy": [
        {"region": "Asia-Pacific Heavy Industry", "countries": "Japan, South Korea, Taiwan", "rationale": "High-tech primary steelmakers seeking conveyor computer vision and furnace thermal optimization to lower carbon footprints."},
        {"region": "Central & Eastern Europe", "countries": "Germany, Poland, Austria", "rationale": "Tight emission caps driving demand for AI slag reduction and raw ore impurity sorting."},
        {"region": "Latin American Mining/Steel", "countries": "Brazil, Chile, Mexico", "rationale": "Vast mineral beneficiation complexes needing real-time automated grade classification."}
    ],
    "Mining & Mineral Exploration": [
        {"region": "Australia & Oceania", "countries": "Australia (Western Australia, Queensland)", "rationale": "World's most automated open-cast mining sector; high willingness to pay for haulage fleet optimization and vibration telemetry."},
        {"region": "Southern Africa", "countries": "South Africa, Botswana, Namibia", "rationale": "Extensive open-pit and deep shaft operations needing low-cost predictive equipment health."},
        {"region": "South America", "countries": "Chile, Peru", "rationale": "World leaders in copper and mineral extraction seeking predictive ore transport scheduling."}
    ],
    "Logistics, Ports & Marine Economy": [
        {"region": "Middle East / GCC", "countries": "UAE (Jebel Ali, Fujairah), Oman (Sohar, Salalah)", "rationale": "Critical maritime transit hubs requiring AI vessel queuing to eliminate costly berth demurrage."},
        {"region": "Southeast Asia", "countries": "Singapore, Malaysia (Port Klang, Tanjung Pelepas)", "rationale": "World's densest maritime choke points seeking predictive marine traffic coordination."}
    ],
    "Tourism, Temple Tech & Heritage Preservation": [
        {"region": "Global Cultural Institutions", "countries": "UK (British Library), France (BNF), US (Library of Congress)", "rationale": "Institutions digitizing rare South Asian manuscript collections requiring archaic script OCR."},
        {"region": "Global Heritage Conservators", "countries": "UNESCO Partner Institutes, Europe", "rationale": "Preservation of non-Latin low-resource language inscriptions on organic media."}
    ],
    "Handlooms, Handicrafts & MSME Artisans": [
        {"region": "Western Europe & Scandinavia", "countries": "UK, Germany, France, Sweden", "rationale": "Surging consumer demand for certified ethical luxury fashion, slow textiles, and authenticated craft provenance."},
        {"region": "North America & Japan", "countries": "United States, Canada, Japan", "rationale": "High-value markets for artisanal textiles valuing verified weave density and anti-counterfeiting authenticity."}
    ],
    "Healthcare & Rural MedTech": [
        {"region": "Global Health & Multilateral Bodies", "countries": "Sub-Saharan Africa, South Asia (UNICEF, WHO pilots)", "rationale": "Deployable smartphone camera anthropometry for severe acute malnutrition screening in remote settlements."}
    ]
}


def evaluate_readiness(completed_items: List[str], sector: str) -> Dict[str, Any]:
    """
    Compute readiness score, identify missing gaps, formulate tailored next steps,
    and generate prospective international market hypotheses.
    """
    total_weight = sum(item["weight"] for item in READINESS_CHECKLIST)
    earned_weight = sum(
        item["weight"] for item in READINESS_CHECKLIST if item["id"] in completed_items
    )
    score = round((earned_weight / total_weight) * 100.0, 1) if total_weight > 0 else 0.0

    completed_ids = set(completed_items)
    missing_items = [item for item in READINESS_CHECKLIST if item["id"] not in completed_ids]

    # Category breakdown
    categories: Dict[str, Dict[str, int]] = {}
    for item in READINESS_CHECKLIST:
        cat = item["category"]
        if cat not in categories:
            categories[cat] = {"total": 0, "completed": 0}
        categories[cat]["total"] += 1
        if item["id"] in completed_ids:
            categories[cat]["completed"] += 1

    # Specific actionable gaps
    actionable_remedies = []
    for item in missing_items:
        if item["id"] == "regulatory_compliance":
            actionable_remedies.append("Conduct an EU AI Act Risk Tiering review (determine whether solution falls under High-Risk Annex III).")
        elif item["id"] == "data_protection":
            actionable_remedies.append("Implement standard TLS 1.3 transport encryption and publish a transparent Privacy Policy aligning with GDPR Articles 13 & 14.")
        elif item["id"] == "documentation":
            actionable_remedies.append("Generate OpenAPI 3.0 specs and publish interactive documentation via Swagger or Postman.")
        elif item["id"] == "support_sla":
            actionable_remedies.append("Define a 99.5% uptime SLA and establish 8x5 or 24x7 escalation runbooks for international pilot partners.")
        elif item["id"] == "ip_licensing":
            actionable_remedies.append("Perform an open-source license audit using tools like FOSSA or pip-licenses to prevent GPL contamination.")

    # Retrieve prospective international markets
    target_corridors = GLOBAL_MARKET_CORRIDORS.get(sector, [
        {"region": "South & Southeast Asia", "countries": "Bangladesh, Sri Lanka, Vietnam", "rationale": "Similar emerging market conditions and operating constraints."},
        {"region": "Middle East / GCC", "countries": "UAE, Saudi Arabia", "rationale": "Rapidly adopting enterprise AI solutions with strong cross-border tech investment."}
    ])

    return {
        "score": score,
        "completed_count": len(completed_items),
        "total_count": len(READINESS_CHECKLIST),
        "missing_items": missing_items,
        "category_summary": categories,
        "actionable_remedies": actionable_remedies,
        "target_corridors": target_corridors,
        "disclaimer": (
            "Hypothesis & Advisory Notice: The readiness score and target market suggestions "
            "are educational self-assessment benchmarks. They do not constitute formal legal "
            "counsel, official compliance certification (CE mark, FDA, HIPAA), or guaranteed "
            "commercial viability in foreign jurisdictions."
        )
    }
