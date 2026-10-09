"""
Seed data module for Odisha AI Nexus.
Populates realistic, culturally grounded demonstration records representing
Odisha's key economic sectors, universities, research centers, and districts.
All records are explicitly tagged with is_demo = 1.
"""

from database import (
    add_project,
    add_talent,
    add_challenge,
    add_assessment,
    has_demo_data
)

DEMO_PROJECTS = [
    {
        "title": "CycloneEye: Coastal Inundation & Micro-Evacuation AI",
        "tagline": "Physics-informed neural networks for storm surge routing along Odisha's 480 km coast",
        "description": "An AI-powered hydrological modeling engine combining satellite SAR imagery, tidal gauges, and drone terrain data to forecast localized water ingress 18 hours in advance for Ganjam, Puri, and Balasore coastal villages. Built as an academic research prototype in collaboration with earth sciences faculty.",
        "sector": "Disaster Management & Climate Resilience",
        "stage": "Field-Tested / Pilot",
        "lead_name": "Dr. Soumya Ranjan Nayak",
        "organization": "IIT Bhubaneswar Coastal AI Lab",
        "district": "Khordha (Bhubaneswar)",
        "target_beneficiaries": "Coastal Gram Panchayats, District Disaster Management Authorities, coastal fishermen",
        "tech_stack": "PyTorch, Sentinel-1 SAR API, UNet, GDAL, FastAPI, Streamlit",
        "github_or_demo_url": "https://github.com/odisha-ai-nexus-demo/cyclone-eye",
        "status": "Seeking Pilot Partners",
        "readiness_score": 78.5,
        "is_demo": 1,
    },
    {
        "title": "PaddyShield: Deep Vision Pest & Blast Fungus Early Warning",
        "tagline": "Offline edge computer vision model for Brown Plant Hopper detection in Sambalpur paddy belts",
        "description": "Lightweight quantized mobile vision model that runs without internet connectivity on sub-₹8,000 Android phones. Farmers photograph rice leaf sheaths to detect early nymph infestations of Brown Plant Hopper (BPH) and leaf blast fungus, receiving localized audio advisories in colloquial Odia (Sambalpuri dialect).",
        "sector": "Agriculture & Food Security",
        "stage": "Field-Tested / Pilot",
        "lead_name": "Chinmayee Pradhan",
        "organization": "VSSUT Burla Agritech Guild",
        "district": "Sambalpur",
        "target_beneficiaries": "Smallholder paddy farmers across Sambalpur, Bargarh, and Subarnapur",
        "tech_stack": "TensorFlow Lite, MobileNetV3, EdgeTPU, Odia TTS, Flutter",
        "github_or_demo_url": "https://github.com/odisha-ai-nexus-demo/paddyshield",
        "status": "Seeking Collaborators",
        "readiness_score": 72.0,
        "is_demo": 1,
    },
    {
        "title": "IronOre-GradeSense: Conveyor Hyperspectral Mineral Classifier",
        "tagline": "Real-time automated grade analysis and silica impurity estimation for Kalinganagar steel hubs",
        "description": "Industrial vision and near-infrared (NIR) spectral classifier that evaluates raw iron ore lump grade and alumina/silica ratios directly on moving 4 m/s belt conveyors. Replaces manual 4-hour wet chemical assays with sub-second optical categorization, reducing sintering furnace energy wastage by up to 8%.",
        "sector": "Steel & Heavy Metallurgy",
        "stage": "Proof of Concept (PoC)",
        "lead_name": "Rohan Mohapatra & Team",
        "organization": "NIT Rourkela Metallurgy AI Cohort",
        "district": "Jajpur",
        "target_beneficiaries": "Sponge iron plants, pelletization units, and integrated steel manufacturers",
        "tech_stack": "OpenCV, Scikit-learn, NIR Spectrometry SDK, TensorRT, C++ Engine",
        "github_or_demo_url": "https://github.com/odisha-ai-nexus-demo/ore-gradesense",
        "status": "Seeking Mentorship",
        "readiness_score": 58.0,
        "is_demo": 1,
    },
    {
        "title": "KalingaLipi: Ancient Palm-Leaf OCR & Archaic Odia Translator",
        "tagline": "Vision transformer preserving vulnerable palm-leaf manuscripts (Tala Patra) into machine-readable text",
        "description": "Transformer-based sequence-to-sequence optical character recognition system specifically fine-tuned on degraded, scratched stylus incisions on 14th–18th century Odia palm-leaf manuscripts housed in state archives and Mathas. Normalizes archaic scribal orthography into contemporary Unicode Odia.",
        "sector": "Tourism, Temple Tech & Heritage Preservation",
        "stage": "Working Prototype",
        "lead_name": "Debabrata Mishra",
        "organization": "IIIT Bhubaneswar Language Tech Group",
        "district": "Puri",
        "target_beneficiaries": "State archives, epigraphers, cultural researchers, international Odia diaspora",
        "tech_stack": "HuggingFace Transformers, TrOCR, PyTorch, OpenCV, SQLite",
        "github_or_demo_url": "https://github.com/odisha-ai-nexus-demo/kalinga-lipi",
        "status": "Active",
        "readiness_score": 64.0,
        "is_demo": 1,
    },
    {
        "title": "BandhaAI: Sambalpuri Handloom Motif Synthesizer & Authenticator",
        "tagline": "Generative design synthesis and cryptographic weave density authenticity verification for master weavers",
        "description": "Diffusion model trained on sacred geometric motifs of western Odisha Ikat (Bandha), assisting master weavers in generating intricate grid tie-dye graphs in seconds rather than weeks. Features a macro-camera verification model to detect authentic handloom weave thread counts vs powerloom knockoffs.",
        "sector": "Handlooms, Handicrafts & MSME Artisans",
        "stage": "Commercial MVP / Scaled",
        "lead_name": "Priyanka Meher",
        "organization": "Bargarh Weavers Creative Collective",
        "district": "Bargarh",
        "target_beneficiaries": "Over 45,000 traditional handloom artisan households across western Odisha",
        "tech_stack": "Stable Diffusion LoRA, ControlNet, ResNet-50, React Native, Python FastAPI",
        "github_or_demo_url": "https://github.com/odisha-ai-nexus-demo/bandha-ai",
        "status": "Active",
        "readiness_score": 81.0,
        "is_demo": 1,
    },
    {
        "title": "SmartHaulage: Heavy Open-Cast Dumper Fleet & Fuel Optimizer",
        "tagline": "Reinforcement learning for dispatch scheduling and pit vibration monitoring in Talcher coalfields",
        "description": "Dynamic multi-agent dispatch optimizer that coordinates 100-ton haul dumpers across complex open-cast benches in Angul and Jharsuguda. Minimizes empty haul time, monitors geophone vibrations during blasting, and curtails diesel burn by 11% using predictive queuing.",
        "sector": "Mining & Mineral Exploration",
        "stage": "Working Prototype",
        "lead_name": "Siddharth Patnaik",
        "organization": "Odisha Geospatial & Heavy Industry Labs",
        "district": "Angul",
        "target_beneficiaries": "Mining leaseholders, heavy earthmoving fleet contractors, safety directors",
        "tech_stack": "Ray RLlib, Python, GeoPandas, Kepler.gl, MQTT, TimescaleDB",
        "github_or_demo_url": "https://github.com/odisha-ai-nexus-demo/smarthaulage",
        "status": "Seeking Pilot Partners",
        "readiness_score": 67.5,
        "is_demo": 1,
    },
    {
        "title": "SishuSeva: Computer Vision Pediatric Malnutrition Triager",
        "tagline": "3D photogrammetric anthropometry assessing severe acute malnutrition in tribal Anganwadi centers",
        "description": "A low-cost smartphone camera solution that captures 360-degree point clouds of infants to accurately compute Mid-Upper Arm Circumference (MUAC), height, and stunting indices within 3mm tolerance. Designed specifically for community health workers (ASHA/Anganwadi) in remote Koraput and Rayagada blocks.",
        "sector": "Healthcare & Rural MedTech",
        "stage": "Proof of Concept (PoC)",
        "lead_name": "Dr. Ananya Dash & Tapas Das",
        "organization": "Koraput Tribal Health Initiative",
        "district": "Koraput",
        "target_beneficiaries": "Over 120,000 rural mothers and infants across Southern Odisha districts",
        "tech_stack": "MediaPipe, PyTorch Mobile, ArUco Marker Calibration, SQLite, Android SDK",
        "github_or_demo_url": "https://github.com/odisha-ai-nexus-demo/sishuseva",
        "status": "Seeking Collaborators",
        "readiness_score": 53.0,
        "is_demo": 1,
    },
    {
        "title": "DhamraVessel: AIS Marine Traffic Trajectory & Berthing Predictor",
        "tagline": "Deep spatio-temporal modeling for cape-size vessel turnaround optimization at Dhamra Port",
        "description": "Transformer-based sequence architecture modeling coastal vessel arrivals, channel dredging conditions, and tidal windows to forecast bulk carrier queue times and reduce anchorage demurrage costs for port terminal operators along the Bay of Bengal.",
        "sector": "Logistics, Ports & Marine Economy",
        "stage": "Ideation / Concept",
        "lead_name": "Kavita Senapati",
        "organization": "KIIT School of Computer Engineering",
        "district": "Bhadrak",
        "target_beneficiaries": "Private port operators, shipping agents, coastal cargo logistics firms",
        "tech_stack": "Python, Polars, Scikit-learn, XGBoost, Streamlit",
        "github_or_demo_url": "https://github.com/odisha-ai-nexus-demo/dhamra-vessel",
        "status": "Seeking Mentorship",
        "readiness_score": 42.0,
        "is_demo": 1,
    }
]

DEMO_TALENT = [
    {
        "full_name": "Aman Kumar Biswal",
        "institution": "IIT Bhubaneswar",
        "district": "Khordha (Bhubaneswar)",
        "role_title": "Computer Vision & Edge AI Engineer",
        "experience_level": "Student / Fresher",
        "technical_skills": "PyTorch, OpenCV, TensorRT, YOLOv8, ONNX, C++, Python, CUDA",
        "areas_of_interest": "Disaster Management & Climate Resilience, Edge AI, Autonomous Drones",
        "portfolio_url": "https://github.com/aman-biswal-demo",
        "bio": "Final-year Dual Degree researcher specializing in real-time visual perception on embedded drones. Published 2 conference papers on flood line segmentation from aerial SAR.",
        "contact_email": "aman.biswal@iitbbs-alumni.demo",
        "is_available": 1,
        "is_demo": 1,
    },
    {
        "full_name": "Swastika Mahapatra",
        "institution": "NIT Rourkela",
        "district": "Sundargarh (Rourkela)",
        "role_title": "MLOps & Industrial IoT Specialist",
        "experience_level": "Mid-Level (3-5 years)",
        "technical_skills": "Python, Docker, Kubernetes, MLflow, FastAPI, MQTT, Scikit-learn, Grafana",
        "areas_of_interest": "Steel & Heavy Metallurgy, Mining & Mineral Exploration, Predictive Maintenance",
        "portfolio_url": "https://linkedin.com/in/swastika-mahapatra-demo",
        "bio": "3.5 years experience implementing vibration and temperature anomaly detection pipelines for heavy rotary machinery in steel manufacturing plants across eastern India.",
        "contact_email": "swastika.m@metal-ai.demo",
        "is_available": 1,
        "is_demo": 1,
    },
    {
        "full_name": "Subhashree Panigrahi",
        "institution": "Utkal University / Independent",
        "district": "Cuttack",
        "role_title": "Computational Linguist & NLP Researcher",
        "experience_level": "Academic / Researcher / Faculty",
        "technical_skills": "Transformers, HuggingFace, SpaCy, Odia Corpus Linguistics, Tokenizers, PyTorch",
        "areas_of_interest": "Tourism, Temple Tech & Heritage Preservation, Indic Language Technologies, EdTech",
        "portfolio_url": "https://subhashree-nlp.demo",
        "bio": "PhD scholar working on low-resource Odia language tokenization, POS tagging, and machine translation benchmarks for tribal dialect preservation.",
        "contact_email": "subhashree.p@utkal-demo.ac.in",
        "is_available": 1,
        "is_demo": 1,
    },
    {
        "full_name": "Rakesh Jena",
        "institution": "VSSUT Burla",
        "district": "Sambalpur",
        "role_title": "Full-Stack AI & Geospatial Developer",
        "experience_level": "Junior (1-2 years)",
        "technical_skills": "Python, GeoPandas, GDAL, Streamlit, PostGIS, React, Scikit-learn, Leaflet",
        "areas_of_interest": "Agriculture & Food Security, Logistics, Ports & Marine Economy, Urban Governance",
        "portfolio_url": "https://rakeshjena-geo.demo",
        "bio": "Geospatial data engineer passionate about mapping cropping patterns, soil moisture index variation, and canal irrigation efficiency across Hirakud command areas.",
        "contact_email": "rakesh.jena@vssut-demo.in",
        "is_available": 1,
        "is_demo": 1,
    },
    {
        "full_name": "Lipika Sahoo",
        "institution": "IIIT Bhubaneswar",
        "district": "Khordha (Bhubaneswar)",
        "role_title": "Deep Learning & Medical Imaging Intern",
        "experience_level": "Student / Fresher",
        "technical_skills": "PyTorch, MONAI, TensorFlow, Torchvision, Scikit-image, Python",
        "areas_of_interest": "Healthcare & Rural MedTech, Agriculture & Food Security",
        "portfolio_url": "https://github.com/lipika-sahoo-demo",
        "bio": "Passionate about applying 3D segmentation and convolutional networks to low-cost ultrasound and X-ray screenings for primary health centers.",
        "contact_email": "lipika.s@iiit-bbs.demo",
        "is_available": 1,
        "is_demo": 1,
    },
    {
        "full_name": "Debasis Rout",
        "institution": "Silicon University / Ex-Infosys",
        "district": "Balasore (Baleswar)",
        "role_title": "Senior Data Architect & AI Consultant",
        "experience_level": "Senior (5+ years)",
        "technical_skills": "Apache Spark, Kafka, Python, AWS SageMaker, Snowflake, Scikit-learn, dbt",
        "areas_of_interest": "Steel & Heavy Metallurgy, Logistics, Ports & Marine Economy, Energy & Grid AI",
        "portfolio_url": "https://github.com/debasis-rout-demo",
        "bio": "Over 7 years architecting enterprise real-time event streaming and analytical data platforms for manufacturing and supply-chain logistics.",
        "contact_email": "debasis.rout@silicon-demo.in",
        "is_available": 1,
        "is_demo": 1,
    }
]

DEMO_CHALLENGES = [
    {
        "title": "Slag Carry-Over & Molten Metal Ladle Level Computer Vision",
        "organization_name": "Kalinga Heavy Metallurgy Consortium",
        "org_type": "PSU / Large Enterprise",
        "sector": "Steel & Heavy Metallurgy",
        "district": "Jajpur",
        "problem_statement": "During steel tapping from Basic Oxygen Furnaces into transfer ladles, carry-over of oxidizing slag causes phosphorus reversion and refractories wear. Infrared and optical cameras face high smoke, particulate glare, and extreme temperatures (1600°C), making human visual inspection dangerous and error-prone.",
        "expected_outcome": "An automated computer vision inference pipeline resilient to thermal glare that detects slag vortex formation within 200 milliseconds and triggers pneumatic slag dart cutoff.",
        "budget_range": "Industry Scale (₹10 - ₹25 Lakhs)",
        "urgency": "High (1 - 3 months)",
        "status": "Open for Proposals",
        "contact_person": "Vice President - Digital Transformation",
        "is_demo": 1,
    },
    {
        "title": "Baitarani River Basin Flash Runoff & Embankment Breach Prediction",
        "organization_name": "State Water Resources & Embankment Cell",
        "org_type": "Government Dept / Urban Local Body",
        "sector": "Disaster Management & Climate Resilience",
        "district": "Kendujhar (Keonjhar)",
        "problem_statement": "Monsoon cloudbursts in Upper Keonjhar catchment trigger rapid river swelling down into Anandapur and Jajpur floodplains within 12 hours. Existing linear hydrodynamic models fail to account for antecedent soil moisture saturation and silt sedimentation rates.",
        "expected_outcome": "A hybrid AI hydrological forecasting tool with a 24-hour predictive horizon, predicting vulnerable embankment stress points and river peak stage with ±15 cm precision.",
        "budget_range": "Seed / Pilot (₹2 - ₹10 Lakhs)",
        "urgency": "Critical / Immediate (< 1 month)",
        "status": "Open for Proposals",
        "contact_person": "Executive Engineer (Hydrology Monitoring)",
        "is_demo": 1,
    },
    {
        "title": "Automated Grading of Cashew Nut Raw Kernels for Coastal MSMEs",
        "organization_name": "Ganjam Agro-Processors & Exporters Association",
        "org_type": "MSME / Local Industry",
        "sector": "Agriculture & Food Security",
        "district": "Ganjam",
        "problem_statement": "Manual sorting of unshelled raw cashew nuts across 80+ micro-processing units in Ganjam leads to inconsistent kernel outturn ratio (KOR) estimation and sub-optimal pricing in export auctions. High labor turnover impairs throughput during harvesting season.",
        "expected_outcome": "A low-cost optical sorting unit or mobile imaging app that estimates moisture content, nut count per kilogram, and internal defect probability with 90%+ accuracy.",
        "budget_range": "Micro-grant (Up to ₹2 Lakhs)",
        "urgency": "Medium (3 - 6 months)",
        "status": "Open for Proposals",
        "contact_person": "Secretary, MSME Cluster Development",
        "is_demo": 1,
    },
    {
        "title": "Satellite AI for Chilika Lake Weed Encroachment & Dolphin Habitat",
        "organization_name": "Chilika Coastal Ecology Research Initiative",
        "org_type": "Non-Profit / Cooperative",
        "sector": "Tourism, Temple Tech & Heritage Preservation",
        "district": "Puri",
        "problem_statement": "Proliferation of invasive macrophytes (water hyacinth) and illegal prawn gherries threatens Irrawaddy dolphin breeding channels and traditional fishing livelihoods in Chilika Lake, India's largest brackish lagoon.",
        "expected_outcome": "Automated bi-weekly satellite image segmentation classifying weed canopy coverage, salinity boundaries, and illegal gherry enclosures, delivered via a web GIS dashboard.",
        "budget_range": "Seed / Pilot (₹2 - ₹10 Lakhs)",
        "urgency": "Medium (3 - 6 months)",
        "status": "Open for Proposals",
        "contact_person": "Lead Coastal Ecologist",
        "is_demo": 1,
    },
    {
        "title": "Cold-Chain Anomaly & Power Outage Prediction for Rural Primary Health",
        "organization_name": "Mayurbhanj Community Health Development Network",
        "org_type": "Non-Profit / Cooperative",
        "sector": "Healthcare & Rural MedTech",
        "district": "Mayurbhanj",
        "problem_statement": "Deep forest Primary Health Centers in Similipal foothills face recurrent grid outages. Vaccine storage refrigerators (ILRs) experience undetectable temperature excursions above 8°C, leading to compromised potency of anti-rabies, hepatitis, and measles vaccines.",
        "expected_outcome": "An edge IoT AI logger utilizing ambient and internal thermal gradients to forecast catastrophic thermal excursions 3 hours before threshold breach, alerting via SMS alerts.",
        "budget_range": "Micro-grant (Up to ₹2 Lakhs)",
        "urgency": "High (1 - 3 months)",
        "status": "Open for Proposals",
        "contact_person": "District Health Logistics Coordinator",
        "is_demo": 1,
    }
]

DEMO_ASSESSMENTS = [
    {
        "idea_title": "Coastal Mangrove Carbon Sequestration Verification AI",
        "sector": "Disaster Management & Climate Resilience",
        "problem_statement": "Manual auditing of blue carbon credits in Kendrapara and Bhitarkanika mangrove estuaries is slow, expensive, and difficult to verify for voluntary carbon markets.",
        "overall_score": 83.5,
        "factor_breakdown": {
            "technical_feasibility": 82.0,
            "local_relevance": 92.0,
            "socio_economic_impact": 88.0,
            "global_market_potential": 85.0,
            "budget_resource_realism": 74.0,
            "data_regulatory_viability": 78.0,
        },
        "strengths": [
            "Bhitarkanika and Mahanadi delta offer rich, verified ground-truth mangrove datasets.",
            "High global demand for verified blue carbon credits (Gold Standard, Verra).",
            "Clear synergy with coastal community livelihood restoration."
        ],
        "weaknesses": [
            "Requires access to multi-temporal high-resolution SAR and LiDAR datasets.",
            "Complex carbon certification methodologies demand verified forestry domain experts."
        ],
        "recommendations": [
            "Partner with remote sensing departments at Utkal University or OUAT.",
            "Conduct a pilot test over a 50 sq. km test parcel in Rajnagar block.",
            "Establish baseline allometric equations with local forestry authorities."
        ],
        "risks": {
            "technical": "Cloud cover during monsoon hinders optical imagery (requires SAR radar focus).",
            "financial": "High upfront compute cost for processing petabyte-scale earth observation tiles.",
            "operational": "Ground calibration requires physical field surveys in marshy tidal terrains.",
            "adoption": "Carbon credit buyers require international accreditation body sign-off."
        },
        "target_markets": [
            "International Voluntary Carbon Offset Exchanges (Singapore, London, Zurich)",
            "ESG and Net-Zero Compliance Audits for Indian Steel & Power Conglomerates",
            "State Forest Departments & National Coastal Zone Management Authorities"
        ],
        "is_demo": 1,
    }
]


def seed_database_if_empty() -> bool:
    """Populate demonstration data only if no demo data exists."""
    if has_demo_data():
        return False

    for project in DEMO_PROJECTS:
        add_project(project)

    for talent in DEMO_TALENT:
        add_talent(talent)

    for challenge in DEMO_CHALLENGES:
        add_challenge(challenge)

    for assessment in DEMO_ASSESSMENTS:
        add_assessment(assessment)

    return True
