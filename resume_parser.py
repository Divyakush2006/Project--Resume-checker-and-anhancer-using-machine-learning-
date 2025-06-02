import pdfplumber
import spacy
import re

# Load the English NLP model from spaCy
# Make sure you have downloaded it using: python -m spacy download en_core_web_sm
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("SpaCy model 'en_core_web_sm' not found. Please run 'python -m spacy download en_core_web_sm'")
    exit()

# --- Extensive Keyword Lists (Expanded for better coverage) ---
SKILL_KEYWORDS = [
    "Python", "C++", "Java", "Machine Learning", "ML", "Deep Learning", "UI/UX",
    "Project Management", "Teamwork", "Critical Thinking", "Figma",
    "API", "Git", "HTML", "CSS", "SQL", "Data Analysis", "Cloud", "AWS",
    "Azure", "GCP", "Docker", "Kubernetes", "Agile", "Scrum", "Frontend",
    "Backend", "Fullstack", "JavaScript", "React", "Angular", "Vue.js",
    "Node.js", "Express.js", "Django", "Flask", "Spring Boot", "C#", ".NET",
    "Go", "Rust", "TypeScript", "Data Structures", "Algorithms", "Database",
    "NoSQL", "MongoDB", "PostgreSQL", "MySQL", "CI/CD", "Testing", "DevOps",
    "Cybersecurity", "Networking", "Linux", "Windows Server", "Virtualization",
    "Big Data", "Spark", "Hadoop", "Tableau", "Power BI", "Excel", "Statistics",
    "Linear Algebra", "Calculus", "NLP", "Computer Vision", "Reinforcement Learning",
    "Time Series", "Econometrics", "Quantitative Analysis", "Risk Management",
    "Financial Modeling", "Blockchain", "Solidity", "Smart Contracts", "Unity",
    "Unreal Engine", "Game Development", "Mobile Development", "iOS", "Android",
    "Swift", "Kotlin", "RESTful APIs", "GraphQL", "Microservices", "System Design",
    "Problem Solving", "Communication", "Leadership", "Adaptability", "Creativity",
    "Attention to Detail", "Research", "Documentation", "Presentation Skills",
    "Public Speaking", "Negotiation", "Conflict Resolution", "Mentoring", "Training",
    "Budgeting", "Financial Planning", "Marketing", "Sales", "Customer Service",
    "CRM", "ERP", "SAP", "Salesforce", "Jira", "Confluence", "Asana", "Trello",
    "Microsoft Office", "Google Workspace", "Shell Scripting", "Bash", "Powershell",
    "Data Visualization", "Matplotlib", "Seaborn", "Plotly", "D3.js", "ETL",
    "Data Warehousing", "Data Governance", "Compliance", "Regulation", "Auditing",
    "Business Intelligence", "Strategy Development", "Market Research",
    "Competitive Analysis", "Product Management", "Product Development",
    "User Stories", "Wireframing", "Prototyping", "Usability Testing",
    "A/B Testing", "Analytics", "Google Analytics", "SEO", "SEM",
    "Social Media Marketing", "Content Marketing", "Email Marketing",
    "Copywriting", "Editing", "Proofreading", "Technical Writing",
    "Grantsmanship", "Fundraising", "Non-profit Management", "Event Planning",
    "Logistics", "Supply Chain Management", "Inventory Management",
    "Quality Assurance", "Quality Control", "Six Sigma", "Lean Manufacturing",
    "Robotics", "Automation", "IoT", "Embedded Systems", "Circuit Design",
    "PCB Design", "Firmware Development", "Control Systems", "Signal Processing",
    "Image Processing", "Video Processing", "Audio Processing", "Speech Recognition",
    "Bioinformatics", "Genomics", "Proteomics", "Cheminformatics", "Drug Discovery",
    "Clinical Trials", "Medical Devices", "Healthcare IT", "EHR", "HL7",
    "GIS", "Geospatial Analysis", "Remote Sensing", "Cartography",
    "Urban Planning", "Environmental Science", "Sustainability",
    "Renewable Energy", "Civil Engineering", "Structural Engineering",
    "Mechanical Engineering", "Electrical Engineering", "Chemical Engineering",
    "Biomedical Engineering", "Materials Science", "Nanotechnology",
    "Aerospace Engineering", "Automotive Engineering", "Manufacturing Engineering",
    "Industrial Engineering", "Systems Engineering", "Operations Research",
    "Quantitative Finance", "Algorithmic Trading", "Derivatives", "Fixed Income",
    "Equity Research", "Portfolio Management", "Wealth Management",
    "Financial Advisory", "Taxation", "Accounting", "Auditing", "Forensic Accounting",
    "Management Consulting", "Strategy Consulting", "IT Consulting",
    "HR Consulting", "Change Management", "Organizational Development",
    "Training and Development", "Coaching", "Mentoring", "Recruitment",
    "Talent Acquisition", "Compensation & Benefits", "Employee Relations",
    "Labor Law", "Workplace Safety", "Diversity & Inclusion", "Corporate Social Responsibility",
    "Public Relations", "Media Relations", "Crisis Management", "Internal Communications",
    "External Communications", "Stakeholder Engagement", "Government Relations",
    "Lobbying", "Policy Analysis", "Legal Research", "Contract Law",
    "Intellectual Property", "Litigation", "Compliance", "Regulatory Affairs",
    "Paralegal", "Legal Writing", "Case Management", "Client Management",
    "Customer Relationship Management", "Sales Operations", "Sales Strategy",
    "Lead Generation", "Conversion Rate Optimization", "Customer Retention",
    "Brand Management", "Market Positioning", "Product Launch",
    "Go-to-Market Strategy", "Pricing Strategy", "Channel Management",
    "Supply Chain Optimization", "Logistics Management", "Warehouse Management Systems",
    "Transportation Management", "Fleet Management", "Route Optimization",
    "Demand Planning", "Forecasting", "Procurement", "Vendor Management",
    "Contract Negotiation", "Risk Assessment", "Fraud Detection",
    "Anti-Money Laundering", "KYC", "Due Diligence", "Internal Audit",
    "External Audit", "Financial Reporting", "GAAP", "IFRS", "SOX Compliance",
    "Tax Planning", "Estate Planning", "Investment Analysis", "Securities Trading",
    "Hedge Funds", "Private Equity", "Venture Capital", "Mergers & Acquisitions",
    "Corporate Finance", "Treasury Management", "Credit Analysis",
    "Underwriting", "Claims Processing", "Actuarial Science", "Insurance",
    "Reinsurance", "P&C Insurance", "Life Insurance", "Health Insurance",
    "Employee Benefits", "Pension Funds", "Wealth Management",
    "Financial Planning & Analysis (FP&A)", "Budgeting & Forecasting",
    "Cost Accounting", "Management Accounting", "Financial Modeling",
    "Valuation", "Due Diligence", "Capital Markets", "Derivatives Trading",
    "Fixed Income Trading", "Equity Trading", "Foreign Exchange",
    "Commodities Trading", "Risk Management", "Compliance", "Regulatory Reporting",
    "Internal Controls", "Audit Management", "Tax Compliance", "Tax Advisory",
    "International Tax", "Transfer Pricing", "SAP FICO", "Oracle Financials",
    "Workday Financials", "QuickBooks", "Xero", "Sage", "ERP Implementation",
    "CRM Implementation", "Project Planning", "Project Execution",
    "Project Monitoring", "Project Control", "Risk Management (Project)",
    "Stakeholder Management", "Vendor Management (Project)", "Resource Allocation",
    "Budget Management", "Schedule Management", "Quality Management",
    "Change Management (Project)", "Scope Management", "Agile Methodologies",
    "Scrum Master", "Product Owner", "Kanban", "Lean", "Six Sigma",
    "PMP", "PRINCE2", "CSM", "CSPO", "SAFe", "DevOps Engineering",
    "Site Reliability Engineering (SRE)", "Cloud Architecture",
    "Network Architecture", "Security Architecture", "Data Architecture",
    "Enterprise Architecture", "Solution Architecture", "Technical Leadership",
    "Mentoring", "Coaching", "Team Leadership", "Cross-functional Team Leadership",
    "Strategic Planning", "Business Development", "Partnership Management",
    "Client Relationship Management", "Account Management", "Sales Management",
    "Marketing Strategy", "Digital Marketing", "SEO Strategy", "SEM Strategy",
    "Content Strategy", "Social Media Strategy", "Email Marketing Strategy",
    "Brand Strategy", "Product Strategy", "Market Entry Strategy",
    "Competitive Intelligence", "Market Analysis", "Consumer Behavior",
    "User Research", "UX Research", "UI Design", "UX Design", "Interaction Design",
    "Visual Design", "Information Architecture", "Wireframing", "Prototyping",
    "Usability Testing", "A/B Testing", "Design Thinking", "Service Design",
    "Design Systems", "Figma", "Sketch", "Adobe XD", "InVision", "Zeplin",
    "HTML5", "CSS3", "JavaScript ES6+", "TypeScript", "React.js", "Angular",
    "Vue.js", "Node.js", "Express.js", "NestJS", "Next.js", "Nuxt.js",
    "Gatsby.js", "Svelte", "jQuery", "Bootstrap", "Tailwind CSS",
    "Material-UI", "Ant Design", "Chakra UI", "Web Components",
    "Progressive Web Apps (PWAs)", "Responsive Design", "Cross-browser Compatibility",
    "Performance Optimization", "Web Security", "Accessibility (A11y)",
    "SEO Best Practices", "Version Control (Git)", "GitHub", "GitLab",
    "Bitbucket", "CI/CD Pipelines", "Jenkins", "Travis CI", "CircleCI",
    "GitHub Actions", "Docker", "Kubernetes", "AWS", "Azure", "GCP",
    "Terraform", "Ansible", "Chef", "Puppet", "Bash Scripting", "Shell Scripting",
    "Python Scripting", "Go Lang", "Rust", "Java", "Spring Boot", "Kotlin",
    "C#", ".NET Core", "ASP.NET", "PHP", "Laravel", "Symfony", "Ruby",
    "Ruby on Rails", "Node.js", "Django", "Flask", "FastAPI", "SQL",
    "PostgreSQL", "MySQL", "MongoDB", "Cassandra", "Redis", "Elasticsearch",
    "Kafka", "RabbitMQ", "RESTful APIs", "GraphQL", "gRPC", "Microservices",
    "Serverless Architectures", "AWS Lambda", "Azure Functions",
    "Google Cloud Functions", "Distributed Systems", "System Design",
    "Scalability", "Reliability", "Fault Tolerance", "Concurrency",
    "Load Balancing", "Caching", "Message Queues", "Databases (SQL/NoSQL)",
    "Data Warehousing", "ETL", "Data Lakes", "Cloud Data Platforms",
    "Snowflake", "Databricks", "Redshift", "BigQuery", "Azure Synapse",
    "Data Virtualization", "Data Federation", "Master Data Management (MDM)",
    "Data Governance Frameworks", "Data Quality", "Data Security", "Data Privacy", "GDPR", "CCPA",
    "HIPAA", "PCI DSS", "Cybersecurity", "Network Security", "Endpoint Security",
    "Cloud Security", "Application Security", "Threat Modeling",
    "Vulnerability Assessment", "Penetration Testing", "Incident Response",
    "Security Information and Event Management (SIEM)", "Firewalls",
    "Intrusion Detection/Prevention Systems (IDS/IPS)", "Encryption",
    "Identity and Access Management (IAM)", "Multi-factor Authentication (MFA)",
    "Security Audits", "Compliance Audits", "Risk Management Frameworks",
    "NIST", "ISO 27001", "SOC 2", "Machine Learning", "Deep Learning",
    "Supervised Learning", "Unsupervised Learning", "Reinforcement Learning",
    "Natural Language Processing (NLP)", "Computer Vision", "Time Series Analysis",
    "Recommendation Systems", "Fraud Detection", "Predictive Analytics",
    "Prescriptive Analytics", "Descriptive Analytics", "Feature Engineering",
    "Model Training", "Model Evaluation", "Hyperparameter Tuning",
    "Model Deployment", "MLOps", "TensorFlow", "Keras", "PyTorch",
    "Scikit-learn", "Pandas", "NumPy", "SciPy", "Matplotlib", "Seaborn",
    "Plotly", "Streamlit", "Dash", "Jupyter Notebooks", "Google Colab",
    "AWS SageMaker", "Azure Machine Learning", "Google AI Platform",
    "Data Science", "Statistical Analysis", "Hypothesis Testing",
    "Regression Analysis", "Classification", "Clustering", "Dimensionality Reduction",
    "Bayesian Statistics", "A/B Testing", "Experiment Design",
    "Data Storytelling", "Communication of Results", "Business Acumen",
    "Domain Knowledge", "Consulting Skills", "Client Management",
    "Project Management (Data Science)", "Research Skills", "Problem Solving",
    "Critical Thinking", "Analytical Thinking", "Creativity", "Innovation",
    "Adaptability", "Collaboration", "Teamwork", "Communication",
    "Presentation Skills", "Public Speaking", "Negotiation", "Conflict Resolution",
    "Time Management", "Organization", "Attention to Detail",
    "Customer Focus", "Sales Skills", "Marketing Skills", "Financial Literacy",
    "Budgeting", "Forecasting", "Risk Management", "Compliance",
    "Legal Knowledge", "Contract Management", "Vendor Management",
    "Procurement", "Supply Chain Management", "Logistics",
    "Operations Management", "Quality Assurance", "Process Improvement",
    "Lean Principles", "Six Sigma", "Agile Methodologies", "Scrum",
    "Kanban", "Design Thinking", "User-Centered Design", "Prototyping",
    "Wireframing", "Usability Testing", "A/B Testing", "User Research",
    "Market Research", "Competitive Analysis", "Product Roadmapping",
    "Product Lifecycle Management", "Go-to-Market Strategy",
    "Pricing Strategy", "Channel Sales", "Direct Sales", "B2B Sales",
    "B2C Sales", "Account Management", "Client Success",
    "Customer Support", "Technical Support", "Help Desk",
    "Troubleshooting", "System Administration", "Network Administration",
    "Database Administration", "Cloud Administration", "DevOps Practices",
    "SRE Principles", "Infrastructure as Code", "Configuration Management",
    "Monitoring", "Logging", "Alerting", "Incident Management",
    "Change Management (IT)", "Release Management", "Deployment Automation",
    "Virtualization", "Containerization", "Orchestration",
    "Cloud Computing", "Hybrid Cloud", "Multi-cloud", "Edge Computing",
    "IoT Devices", "Embedded Systems Development", "Firmware Development",
    "Hardware Design", "Circuit Design", "PCB Design", "FPGA Development",
    "VHDL", "Verilog", "Assembly Language", "C", "C++", "RTOS",
    "Signal Processing", "Control Systems", "Robotics", "Automation",
    "Mechatronics", "Mechanical Design", "CAD", "CAM", "FEA",
    "Thermodynamics", "Fluid Dynamics", "Materials Science",
    "Manufacturing Processes", "Quality Control", "Statistical Process Control",
    "Lean Manufacturing", "Six Sigma", "Project Management (Engineering)",
    "Requirements Gathering", "System Integration", "Testing & Validation",
    "Technical Documentation", "Research & Development", "Innovation Management",
    "Patent Law", "Intellectual Property Management", "Regulatory Compliance",
    "Quality Management Systems (QMS)", "ISO Standards", "GMP",
    "GLP", "GCP", "Clinical Research", "Biostatistics", "Epidemiology",
    "Public Health", "Health Informatics", "EHR Systems", "Medical Billing",
    "Coding (Medical)", "Health Policy", "Healthcare Administration",
    "Patient Care", "Nursing", "Physician Assistant", "Medical Doctor",
    "Dentistry", "Pharmacy", "Physical Therapy", "Occupational Therapy",
    "Speech Therapy", "Nutrition", "Dietetics", "Veterinary Medicine",
    "Biotechnology", "Genetics", "Molecular Biology", "Cell Biology",
    "Biochemistry", "Immunology", "Microbiology", "Pharmacology",
    "Toxicology", "Bioinformatics Tools", "Genomic Data Analysis",
    "Proteomic Data Analysis", "Drug Discovery & Development",
    "Clinical Trials Management", "Regulatory Submissions", "FDA Regulations",
    "EMA Regulations", "Medical Device Development", "IVD Development",
    "Quality Assurance (Biotech)", "Quality Control (Biotech)",
    "Manufacturing (Biotech)", "Process Development", "Scale-up",
    "Fermentation", "Cell Culture", "Protein Purification",
    "Analytical Chemistry", "Organic Chemistry", "Inorganic Chemistry",
    "Physical Chemistry", "Polymer Chemistry", "Materials Chemistry",
    "Environmental Chemistry", "Food Science", "Cosmetic Science",
    "Forensic Science", "Geology", "Geophysics", "Oceanography",
    "Meteorology", "Climatology", "Environmental Modeling",
    "GIS Software (ArcGIS, QGIS)", "Remote Sensing Data Analysis",
    "Spatial Analysis", "Cartography", "Map Production",
    "Urban Planning", "Zoning Laws", "Land Use Planning",
    "Community Development", "Sustainable Development",
    "Renewable Energy Systems", "Solar Energy", "Wind Energy",
    "Geothermal Energy", "Hydropower", "Energy Storage",
    "Energy Efficiency", "Environmental Impact Assessment",
    "Pollution Control", "Waste Management", "Water Treatment",
    "Air Quality Management", "Ecology", "Conservation",
    "Wildlife Management", "Forestry", "Agriculture", "Agronomy",
    "Horticulture", "Animal Science", "Food Production",
    "Supply Chain Optimization (Agriculture)", "Agricultural Economics",
    "Rural Development", "International Development", "Humanitarian Aid",
    "Non-profit Management", "Fundraising", "Grant Writing",
    "Volunteer Management", "Program Management", "Project Coordination",
    "Community Engagement", "Social Work", "Counseling", "Psychology",
    "Sociology", "Anthropology", "Political Science",
    "International Relations", "Public Administration", "Public Policy",
    "Economics", "Econometrics", "Financial Economics",
    "Development Economics", "Behavioral Economics", "Game Theory",
    "Operations Research", "Management Science", "Decision Science",
    "Quantitative Methods", "Statistical Modeling", "Optimization",
    "Simulation", "Supply Chain Analytics", "Logistics Analytics",
    "Marketing Analytics", "Sales Analytics", "HR Analytics",
    "Financial Analytics", "Healthcare Analytics", "Education Analytics",
    "Sports Analytics", "Web Analytics", "Social Media Analytics",
    "Customer Analytics", "Retail Analytics", "Manufacturing Analytics",
    "IoT Analytics", "Big Data Analytics", "Data Mining", "Data Warehousing",
    "ETL Processes", "Data Lakes", "Cloud Data Platforms",
    "Snowflake", "Databricks", "Redshift", "BigQuery", "Azure Synapse",
    "Data Virtualization", "Data Federation", "Master Data Management (MDM)",
    "Data Governance Frameworks", "Data Ethics", "Responsible AI",
    "Fairness in AI", "Transparency in AI", "Explainable AI (XAI)",
    "AI Governance", "AI Policy", "AI Risk Management",
    "AI Audit", "AI Compliance", "AI Legal Frameworks", "AI Regulations",
    "AI Standards", "AI Best Practices", "AI for Good", "AI for Social Impact",
    "AI in Healthcare", "AI in Finance", "AI in Retail",
    "AI in Manufacturing", "AI in Education", "AI in Government",
    "AI in Cybersecurity", "AI in Marketing", "AI in Sales",
    "AI in HR", "AI in Operations", "AI in Supply Chain",
    "AI in Customer Service", "AI in Product Development",
    "AI in Research & Development", "AI in Engineering",
    "AI in Science", "AI in Arts", "AI in Music", "AI in Gaming",
    "AI in Robotics", "AI in Automation", "AI in IoT",
    "AI in Autonomous Systems", "AI in Smart Cities",
    "AI in Environmental Monitoring", "AI in Climate Change",
    "AI in Disaster Response", "AI in Public Safety",
    "AI in National Security", "AI in Defense", "AI in Space Exploration",
    "AI in Astronomy", "AI in Physics", "AI in Chemistry",
    "AI in Biology", "AI in Medicine", "AI in Agriculture",
    "AI in Energy", "AI in Transportation", "AI in Logistics",
    "AI in Manufacturing", "AI in Construction", "AI in Real Estate",
    "AI in Hospitality", "AI in Tourism", "AI in Sports",
    "AI in Entertainment", "AI in Media", "AI in Publishing",
    "AI in Education Technology", "AI in Financial Technology",
    "AI in Health Technology", "AI in Retail Technology",
    "AI in Marketing Technology", "AI in Sales Technology",
    "AI in Human Resources Technology", "AI in Legal Technology",
    "AI in Government Technology", "AI in Cybersecurity Technology",
    "AI in Cloud Technology", "AI in Big Data Technology",
    "AI in IoT Technology", "AI in Blockchain Technology",
    "AI in Quantum Computing", "AI in Edge Computing",
    "AI in Computer Vision Technology", "AI in Natural Language Processing Technology",
    "AI in Speech Technology", "AI in Robotics Technology",
    "AI in Automation Technology", "AI in Virtual Reality",
    "AI in Augmented Reality", "AI in Mixed Reality",
    "AI in Gaming Technology", "AI in Simulation Technology",
    "AI in Digital Twins", "AI in Predictive Maintenance",
    "AI in Anomaly Detection", "AI in Optimization",
    "AI in Personalization", "AI in Recommendation Engines",
    "AI in Chatbots", "AI in Virtual Assistants",
    "AI in Content Generation", "AI in Image Generation",
    "AI in Video Generation", "AI in Audio Generation",
    "AI in Code Generation", "AI in Data Synthesis",
    "AI in Data Augmentation", "AI in Data Labeling",
    "AI in Data Annotation", "AI in Data Cleaning",
    "AI in Data Preprocessing", "AI in Feature Selection",
    "AI in Model Selection", "AI in Model Deployment",
    "AI in Model Monitoring", "AI in Model Retraining",
    "AI in Explainable AI", "AI in Responsible AI",
    "AI in AI Ethics", "AI in AI Governance",
    "AI in AI Policy", "AI in AI Regulation",
    "AI in AI Standards", "AI in AI Best Practices",
    "AI in AI for Social Good", "AI in AI for Sustainable Development",
    "AI in AI for Healthcare", "AI in AI for Education",
    "AI in AI for Environmental Protection", "AI in AI for Disaster Management",
    "AI in AI for Public Safety", "AI in AI for National Security",
    "AI in AI for Defense", "AI in AI for Space Exploration",
    "AI in AI for Scientific Discovery", "AI in AI for Arts and Culture",
    "AI in AI for Sports and Entertainment", "AI in AI for Media and Publishing",
    "AI in AI for Financial Services", "AI in AI for Retail and E-commerce",
    "AI in AI for Manufacturing and Industry 4.0", "AI in AI for Construction and Infrastructure",
    "AI in AI for Real Estate and Property Management", "AI in AI for Hospitality and Tourism",
    "AI in AI for Transportation and Logistics", "AI in AI for Energy and Utilities",
    "AI in AI for Agriculture and Food Systems", "AI in AI for Water Management",
    "AI in AI for Air Quality Management", "AI in AI for Waste Management",
    "AI in AI for Biodiversity Conservation", "AI in AI for Ecosystem Restoration",
    "AI in AI for Climate Change Mitigation", "AI in AI for Climate Change Adaptation",
    "AI in AI for Sustainable Cities", "AI in AI for Smart Homes",
    "AI in AI for Smart Grids", "AI in AI for Smart Mobility",
    "AI in AI for Smart Manufacturing", "AI in AI for Smart Healthcare",
    "AI in AI for Smart Education", "AI in AI for Smart Government",
    "AI in AI for Smart Security", "AI in AI for Smart Agriculture",
    "AI in AI for Smart Energy", "AI in AI for Smart Water",
    "AI in AI for Smart Waste", "AI in AI for Smart Environment",
    "AI in AI for Smart Buildings", "AI in AI for Smart Infrastructure",
    "AI in AI for Smart Transportation", "AI in AI for Smart Logistics",
    "AI in AI for Smart Retail", "AI in AI for Smart Hospitality",
    "AI in AI for Smart Tourism", "AI in AI for Smart Sports",
    "AI in AI for Smart Entertainment", "AI in AI for Media",
    "AI in AI for Publishing"
]

EDUCATION_KEYWORDS = [
    "Bachelor", "Master", "B.Tech", "M.Tech", "PhD", "University", "College", "Institute",
    "Degree", "Diploma", "Associate", "Undergraduate", "Graduate", "Postgraduate",
    "School", "Academy", "Polytechnic", "Faculty", "Department", "Program", "Course",
    "Major", "Minor", "Curriculum", "Thesis", "Dissertation", "Capstone", "GPA",
    "Dean's List", "Honors", "Cum Laude", "Magna Cum Laude", "Summa Cum Laude",
    "Scholarship", "Fellowship", "Certificate", "Certification", "Vocational",
    "Technical", "Apprenticeship", "Internship", "Exchange Program", "Study Abroad"
]

# --- Backend Processing Functions ---

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file using pdfplumber.
    Args:
        pdf_path (str): The path to the PDF file.
    Returns:
        str: The extracted text from the PDF. Returns None if file not found or error.
    """
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except FileNotFoundError:
        print(f"Error: PDF file not found at '{pdf_path}'")
        return None
    except Exception as e:
        print(f"Error extracting text from PDF '{pdf_path}': {e}")
        return None
    return text

def extract_skills(text):
    """
    Extracts skills from text based on a predefined list of keywords.
    Args:
        text (str): The input text (e.g., resume or job description).
    Returns:
        list: A list of unique skills found in the text.
    """
    found_skills = []
    text_lower = text.lower()
    for skill in SKILL_KEYWORDS:
        # Use regex to find whole words, case-insensitively
        if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text_lower):
            found_skills.append(skill)
    return sorted(list(set(found_skills)))

def extract_education(text):
    """
    Extracts education-related information from text based on keywords.
    It tries to capture the context around the education keywords.
    Args:
        text (str): The input text (e.g., resume).
    Returns:
        list: A list of unique education snippets found in the text.
    """
    found_education = []
    for keyword in EDUCATION_KEYWORDS:
        # Find matches with some context (50 characters before/after) around the keyword
        matches = re.findall(rf".{{0,50}}\b{re.escape(keyword)}\b.{{0,50}}", text, re.IGNORECASE)
        found_education.extend(matches)
    # Clean up whitespace and remove duplicates
    return sorted(list(set([m.strip() for m in found_education])))

def extract_organizations(text):
    """
    Extracts organization names from text using spaCy's Named Entity Recognition (NER).
    Args:
        text (str): The input text (e.g., resume).
    Returns:
        list: A list of unique organization names found in the text.
    """
    doc = nlp(text)
    orgs = set()
    for ent in doc.ents:
        # Filter for entities labeled as 'ORG' (Organization)
        if ent.label_ == "ORG":
            orgs.add(ent.text)
    return sorted(list(orgs))

def compare_skills(resume_skills, job_description_skills):
    """
    Compares skills from a resume against skills from a job description.
    Args:
        resume_skills (list): Skills extracted from the resume.
        job_description_skills (list): Skills extracted from the job description.
    Returns:
        dict: A dictionary containing:
            - 'matched_skills': Skills present in both.
            - 'missing_skills': Skills in JD but not in resume.
            - 'extra_skills': Skills in resume but not in JD.
    """
    # Convert to lowercase sets for case-insensitive comparison
    resume_set = set(s.lower() for s in resume_skills)
    jd_set = set(s.lower() for s in job_description_skills)

    matched_skills = sorted(list(resume_set.intersection(jd_set)))
    missing_skills = sorted(list(jd_set.difference(resume_set)))
    extra_skills = sorted(list(resume_set.difference(jd_set)))

    # Return original casing if desired, or keep lowercase for consistency.
    # For display, converting back to original casing (if available in a map) might be nice.
    # For now, we'll return the lowercased matches.
    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "extra_skills": extra_skills
    }

def calculate_scores(resume_data, jd_data, skill_comparison_results):
    """
    Calculates various scores based on resume and job description analysis.
    Args:
        resume_data (dict): Dictionary with resume_skills, resume_education, resume_organizations.
        jd_data (dict): Dictionary with jd_skills.
        skill_comparison_results (dict): Results from compare_skills function.
    Returns:
        dict: A dictionary containing calculated scores.
    """
    scores = {}

    # 1. Overall Skill Match Score (out of 100)
    # How many of the JD's skills are present in the resume
    total_jd_skills = len(jd_data['jd_skills'])
    matched_skills_count = len(skill_comparison_results['matched_skills'])

    if total_jd_skills > 0:
        scores['overall_skill_match_score'] = round((matched_skills_count / total_jd_skills) * 100, 2)
    else:
        scores['overall_skill_match_score'] = 0.0 # No skills in JD to match against

    # 2. Recruiter Readiness Score (Impact on Recruiter - out of 100)
    # A subjective score combining skill match with completeness of key sections
    readiness_score = scores['overall_skill_match_score'] * 0.7 # 70% from skill match directly

    # Add bonuses for presence of fundamental resume sections
    if resume_data['resume_education']:
        readiness_score += 10 # 10% bonus for education found
    if resume_data['resume_organizations']:
        readiness_score += 20 # 20% bonus for organizations (strong work history indicator)

    scores['recruiter_readiness_score'] = min(100.0, round(readiness_score, 2)) # Cap at 100

    # 3. Resume Completeness Score (out of 100)
    # Assesses if the key expected sections were successfully extracted
    completeness_score = 0.0
    if resume_data['resume_skills']: completeness_score += 33.33
    if resume_data['resume_education']: completeness_score += 33.33
    if resume_data['resume_organizations']: completeness_score += 33.33
    scores['resume_completeness_score'] = min(100.0, round(completeness_score, 2))

    return scores

def generate_feedback(skill_comparison_results, scores):
    """
    Generates actionable textual feedback for the user based on skill comparison and scores.
    Args:
        skill_comparison_results (dict): Results from compare_skills function.
        scores (dict): Calculated scores.
    Returns:
        list: A list of strings, each representing a feedback point.
    """
    feedback_messages = []

    # --- General Resume Advice ---
    feedback_messages.append("--- General Resume Advice ---")
    feedback_messages.append("To make your resume stand out, always quantify your achievements (e.g., 'Increased efficiency by 15%', 'Managed projects worth $X').")
    feedback_messages.append("Ensure consistent formatting and clear headings for easy readability by recruiters.")
    feedback_messages.append("Proofread carefully for any typos or grammatical errors.")

    # --- Skill Match Feedback ---
    feedback_messages.append("\n--- Skill Match & Alignment ---")
    if not skill_comparison_results['missing_skills']:
        feedback_messages.append("🎉 **Excellent Skill Match!** Your resume covers all the key skills mentioned in the job description. You're very well-aligned!")
    else:
        feedback_messages.append("To better align your resume with this job description, consider the following:")
        feedback_messages.append("  * **Add or Emphasize Missing Skills:**")
        for skill in skill_comparison_results['missing_skills']:
            feedback_messages.append(f"    - Look for opportunities to include '{skill.title()}' in your experience or skills section.")
            feedback_messages.append(f"      If you have experience with '{skill.title()}', make sure it's clearly stated with examples and achievements.")

    if skill_comparison_results['extra_skills']:
        feedback_messages.append("\n  * **Consider Prioritizing Relevant Skills:**")
        feedback_messages.append("    - While your 'Extra Skills' are valuable, ensure the most relevant skills for *this specific job* are prominent and easily visible to the recruiter, especially in your 'Skills' section or experience bullet points.")
        feedback_messages.append("    - You might move less relevant 'Extra Skills' to a general 'Other Skills' section if space is a concern, to keep the focus on the job requirements.")

    # --- Score-Based Feedback ---
    feedback_messages.append("\n--- Score-Based Recommendations ---")

    # Overall Skill Match Score
    if scores['overall_skill_match_score'] >= 80:
        feedback_messages.append(f"📈 **Overall Skill Match Score ({scores['overall_skill_match_score']}%)**: Fantastic! Your skills are a strong match for this role. Focus on highlighting these connections even more.")
    elif scores['overall_skill_match_score'] >= 50:
        feedback_messages.append(f"📈 **Overall Skill Match Score ({scores['overall_skill_match_score']}%)**: Good foundation. Review the 'Missing Skills' section above and try to integrate more of those keywords and related experiences.")
    else:
        feedback_messages.append(f"📈 **Overall Skill Match Score ({scores['overall_skill_match_score']}%)**: There's significant room for improvement. Carefully tailor your resume to include more of the required skills from the job description.")

    # Recruiter Readiness Score
    if scores['recruiter_readiness_score'] >= 80:
        feedback_messages.append(f"🌟 **Recruiter Readiness Score ({scores['recruiter_readiness_score']}%)**: Your resume is highly recruiter-friendly. Key information is easy to find, and your alignment is clear.")
    elif scores['recruiter_readiness_score'] >= 50:
        feedback_messages.append(f"🌟 **Recruiter Readiness Score ({scores['recruiter_readiness_score']}%)**: Your resume is generally readable. Consider refining your strongest achievements and skills to be more prominent at the top.")
    else:
        feedback_messages.append(f"🌟 **Recruiter Readiness Score ({scores['recruiter_readiness_score']}%)**: Your resume might need significant restructuring to quickly convey your value. Ensure your most relevant skills and experiences are visible within the first half-page.")

    # Resume Completeness Score
    if scores['resume_completeness_score'] >= 90:
        feedback_messages.append(f"📝 **Resume Completeness Score ({scores['resume_completeness_score']}%)**: Excellent! Your resume appears to have all the essential sections well-covered.")
    elif scores['resume_completeness_score'] >= 60:
        feedback_messages.append(f"📝 **Resume Completeness Score ({scores['resume_completeness_score']}%)**: Good. Double-check if you've included all relevant education, work experience, and projects. Sometimes, minor details can increase this score.")
    else:
        feedback_messages.append(f"📝 **Resume Completeness Score ({scores['resume_completeness_score']}%)**: Your resume might be missing key sections (e.g., detailed work experience, education, or a comprehensive skills list). Ensure all relevant sections are present and populated.")


    feedback_messages.append("\n--- Regarding Salary Expectations ---")
    feedback_messages.append("Estimating an exact job salary solely from a resume is highly challenging and often inaccurate. Salaries depend on factors like your precise years of experience, specific location, company size, industry, and current market demand for your skills, none of which are definitively quantified from a resume alone.")
    feedback_messages.append("\n**Recommendation for Salary Research:** To get an accurate expected salary range, we recommend using reputable online salary aggregators. Based on the software development role and your skills, you can research sites like:")
    feedback_messages.append("  * Glassdoor.com")
    feedback_messages.append("  * LinkedIn Salary")
    feedback_messages.append("  * Payscale.com")
    feedback_messages.append("  * Indeed.com/salaries")
    feedback_messages.append("\nFilter by 'Software Developer' roles in 'Surat, Gujarat' (or your target city) with your estimated years of experience, and look at roles that specifically mention the technologies (Python, Java, Cloud, etc.) you possess or the job requires.")

    return feedback_messages


# --- Main Backend Execution Flow (Simulating a single request) ---

def run_analysis(resume_pdf_path, job_description_pdf_path):
    """
    Executes the full backend analysis pipeline.
    This function simulates what a backend endpoint would do upon receiving a request.
    Returns a dictionary of all results suitable for a frontend.
    """
    results = {
        "resume_processed": False,
        "job_description_processed": False,
        "raw_resume_text": None,
        "raw_jd_text": None,
        "resume_extracted_data": {},
        "jd_extracted_data": {},
        "skill_comparison_results": {},
        "scores": {},
        "feedback_messages": []
    }

    # 1. Process Resume
    resume_text = extract_text_from_pdf(resume_pdf_path)
    if resume_text:
        results["resume_processed"] = True
        results["raw_resume_text"] = resume_text
        results["resume_extracted_data"] = {
            "skills": extract_skills(resume_text),
            "education": extract_education(resume_text),
            "organizations": extract_organizations(resume_text)
        }
    else:
        results["feedback_messages"].append("Error: Could not process resume PDF. Please ensure it's provided.")
        return results # Early exit if resume fails

    # 2. Process Job Description
    job_description_text = extract_text_from_pdf(job_description_pdf_path)
    if job_description_text:
        results["job_description_processed"] = True
        results["raw_jd_text"] = job_description_text
        results["jd_extracted_data"] = {
            "skills": extract_skills(job_description_text)
        }
    else:
        results["feedback_messages"].append("Error: Could not process job description PDF. Please ensure it's provided.")
        # We can still provide resume feedback if JD is missing, but skill comparison/scores will be affected
        return results # Early exit if JD fails for comparison

    # 3. Compare Skills
    skill_comp_results = compare_skills(
        results["resume_extracted_data"]["skills"],
        results["jd_extracted_data"]["skills"]
    )
    results["skill_comparison_results"] = skill_comp_results

    # 4. Calculate Scores
    scores = calculate_scores(
        {
            'resume_skills': results["resume_extracted_data"]["skills"],
            'resume_education': results["resume_extracted_data"]["education"],
            'resume_organizations': results["resume_extracted_data"]["organizations"]
        },
        {
            'jd_skills': results["jd_extracted_data"]["skills"]
        },
        skill_comp_results
    )
    results["scores"] = scores

    # 5. Generate Feedback - Pass scores to the function
    results["feedback_messages"] = generate_feedback(skill_comp_results, scores)

    return results
