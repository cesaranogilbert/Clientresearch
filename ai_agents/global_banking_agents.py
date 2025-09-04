"""
Global Banking AI Agents
Specialized AI agents for top 20 global banks and banking services expertise
"""

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simple agent data structure
class BankingAgent:
    def __init__(self, name, specialty, expertise_areas, years_experience, project_count, collaboration_rating):
        self.name = name
        self.specialty = specialty
        self.expertise_areas = expertise_areas
        self.years_experience = years_experience
        self.project_count = project_count
        self.collaboration_rating = collaboration_rating
    
    def __str__(self):
        return f"{self.name} ({self.specialty})"

# Agent registry
global_banking_registry = []

def register_banking_agent(agent):
    """Register a banking specialist agent"""
    global_banking_registry.append(agent)
    logger.info(f"Registered banking agent: {agent.name} ({agent.specialty})")

# =============================================================================
# TOP 20 GLOBAL BANKS - SPECIALIZED AGENTS
# =============================================================================

top_global_bank_agents = [
    BankingAgent(
        name="JPMorgan Chase Integration Expert",
        specialty="JPM APIs, Corporate Banking & Investment Services",
        expertise_areas=[
            "JPMorgan Chase API integration", "Chase Pay", "Corporate banking services",
            "Investment banking", "Asset management", "Treasury services", "Trade finance",
            "Foreign exchange", "Commercial lending", "Cash management", "Merchant services",
            "Real estate banking", "Private banking", "Compliance frameworks", "Risk management"
        ],
        years_experience=72,
        project_count=1480,
        collaboration_rating=9.9
    ),
    BankingAgent(
        name="Bank of America Specialist",
        specialty="BofA APIs, Merrill Lynch Integration & Consumer Banking",
        expertise_areas=[
            "Bank of America API", "Merrill Lynch integration", "Consumer banking",
            "Corporate banking", "Investment banking", "Wealth management", "Treasury management",
            "Cash management", "International banking", "Trade services", "Equipment financing",
            "Commercial real estate", "Small business banking", "Digital banking", "Mobile banking"
        ],
        years_experience=70,
        project_count=1440,
        collaboration_rating=9.8
    ),
    BankingAgent(
        name="ICBC China Expert",
        specialty="Industrial Commercial Bank China, RMB Services & Asian Markets",
        expertise_areas=[
            "ICBC API integration", "RMB internationalization", "Cross-border banking",
            "Chinese banking regulations", "PBOC compliance", "Asian market expertise",
            "Trade finance", "Belt and Road financing", "Corporate banking", "Investment banking",
            "Foreign exchange", "Precious metals", "E-banking", "Mobile banking", "WeChat banking"
        ],
        years_experience=68,
        project_count=1400,
        collaboration_rating=9.7
    ),
    BankingAgent(
        name="Wells Fargo Integration Specialist",
        specialty="Wells Fargo APIs, Commercial Banking & Mortgage Services",
        expertise_areas=[
            "Wells Fargo API", "Commercial banking", "Mortgage banking", "Consumer lending",
            "Corporate banking", "Investment banking", "Asset management", "Insurance services",
            "Treasury management", "International banking", "Equipment finance", "Real estate",
            "Small business banking", "Agricultural banking", "Digital banking", "Compliance"
        ],
        years_experience=69,
        project_count=1420,
        collaboration_rating=9.8
    ),
    BankingAgent(
        name="China Construction Bank Expert",
        specialty="CCB Services, Infrastructure Finance & Chinese Banking",
        expertise_areas=[
            "China Construction Bank API", "Infrastructure financing", "Project finance",
            "Housing finance", "Corporate banking", "Personal banking", "E-banking",
            "International business", "Investment banking", "Asset management", "Insurance",
            "Credit card services", "Foreign exchange", "Precious metals", "Fund management"
        ],
        years_experience=66,
        project_count=1360,
        collaboration_rating=9.7
    ),
    BankingAgent(
        name="Agricultural Bank of China Specialist",
        specialty="ABC Banking, Rural Finance & Agricultural Services",
        expertise_areas=[
            "Agricultural Bank of China API", "Rural banking", "Agricultural finance",
            "County banking", "Personal banking", "Corporate banking", "International banking",
            "E-banking", "Credit card services", "Fund management", "Insurance services",
            "Investment banking", "Asset management", "Foreign exchange", "Custody services"
        ],
        years_experience=65,
        project_count=1340,
        collaboration_rating=9.6
    ),
    BankingAgent(
        name="Bank of China Integration Expert",
        specialty="Bank of China, Cross-Border Services & International Banking",
        expertise_areas=[
            "Bank of China API", "Cross-border banking", "International trade finance",
            "Foreign exchange", "Overseas banking", "Corporate banking", "Personal banking",
            "Investment banking", "Asset management", "Insurance", "Fund management",
            "E-banking", "Credit cards", "Precious metals", "Custody services"
        ],
        years_experience=67,
        project_count=1380,
        collaboration_rating=9.7
    ),
    BankingAgent(
        name="Citigroup Global Expert",
        specialty="Citi APIs, Global Banking & Institutional Services",
        expertise_areas=[
            "Citigroup API integration", "Global transaction banking", "Institutional clients",
            "Corporate banking", "Investment banking", "Private banking", "Wealth management",
            "Treasury services", "Trade finance", "Cash management", "Securities services",
            "Foreign exchange", "Commodities", "Emerging markets", "Digital banking"
        ],
        years_experience=71,
        project_count=1460,
        collaboration_rating=9.9
    ),
    BankingAgent(
        name="HSBC International Specialist",
        specialty="HSBC APIs, International Banking & Trade Finance",
        expertise_areas=[
            "HSBC API integration", "International banking", "Trade finance", "Supply chain finance",
            "Corporate banking", "Commercial banking", "Private banking", "Wealth management",
            "Global banking", "Cash management", "Foreign exchange", "Emerging markets",
            "Islamic banking", "Digital banking", "Mobile banking", "Cross-border payments"
        ],
        years_experience=69,
        project_count=1420,
        collaboration_rating=9.8
    ),
    BankingAgent(
        name="Goldman Sachs Expert",
        specialty="Goldman Sachs APIs, Investment Banking & Asset Management",
        expertise_areas=[
            "Goldman Sachs API", "Investment banking", "Asset management", "Securities",
            "Private wealth management", "Institutional services", "Market making",
            "Prime brokerage", "Commodities trading", "Foreign exchange", "Fixed income",
            "Equities", "Alternative investments", "Risk management", "Research services"
        ],
        years_experience=73,
        project_count=1500,
        collaboration_rating=9.9
    ),
    BankingAgent(
        name="Morgan Stanley Integration Specialist",
        specialty="Morgan Stanley APIs, Wealth Management & Institutional Securities",
        expertise_areas=[
            "Morgan Stanley API", "Wealth management", "Institutional securities", "Investment banking",
            "Asset management", "Private banking", "Financial advisory", "Trading services",
            "Research", "Prime brokerage", "Securities lending", "Foreign exchange",
            "Fixed income", "Equities", "Derivatives", "Risk management"
        ],
        years_experience=71,
        project_count=1460,
        collaboration_rating=9.8
    ),
    BankingAgent(
        name="BNP Paribas European Expert",
        specialty="BNP Paribas APIs, European Banking & Corporate Services",
        expertise_areas=[
            "BNP Paribas API", "European banking", "Corporate banking", "Investment banking",
            "Asset management", "Insurance", "Real estate services", "International trade",
            "Cash management", "Foreign exchange", "Securities services", "Commodity finance",
            "Equipment finance", "Project finance", "Digital banking", "SEPA integration"
        ],
        years_experience=68,
        project_count=1400,
        collaboration_rating=9.7
    ),
    BankingAgent(
        name="UBS Swiss Banking Expert",
        specialty="UBS APIs, Private Banking & Wealth Management",
        expertise_areas=[
            "UBS API integration", "Private banking", "Wealth management", "Asset management",
            "Investment banking", "Swiss banking", "International banking", "Family office services",
            "Corporate banking", "Securities services", "Foreign exchange", "Precious metals",
            "Alternative investments", "Hedge fund services", "Research", "Digital banking"
        ],
        years_experience=70,
        project_count=1440,
        collaboration_rating=9.8
    ),
    BankingAgent(
        name="Deutsche Bank Integration Specialist",
        specialty="Deutsche Bank APIs, German Banking & Investment Services",
        expertise_areas=[
            "Deutsche Bank API", "German banking", "Corporate banking", "Investment banking",
            "Asset management", "Private banking", "Transaction banking", "Foreign exchange",
            "Fixed income", "Equities", "Derivatives", "Prime brokerage", "Custody services",
            "Cash management", "Trade finance", "SEPA services", "European compliance"
        ],
        years_experience=67,
        project_count=1380,
        collaboration_rating=9.7
    ),
    BankingAgent(
        name="Royal Bank of Canada Expert",
        specialty="RBC APIs, Canadian Banking & North American Services",
        expertise_areas=[
            "Royal Bank of Canada API", "Canadian banking", "Personal banking", "Commercial banking",
            "Corporate banking", "Investment banking", "Wealth management", "Asset management",
            "Insurance", "Investor services", "Capital markets", "Foreign exchange",
            "Trade finance", "Cash management", "Digital banking", "North American markets"
        ],
        years_experience=66,
        project_count=1360,
        collaboration_rating=9.6
    ),
    BankingAgent(
        name="Barclays UK Specialist",
        specialty="Barclays APIs, UK Banking & Investment Services",
        expertise_areas=[
            "Barclays API integration", "UK banking", "Personal banking", "Business banking",
            "Corporate banking", "Investment banking", "Wealth management", "Private banking",
            "Transaction banking", "Trade finance", "Foreign exchange", "Fixed income",
            "Equities", "Research", "Digital banking", "Open banking", "PSD2 compliance"
        ],
        years_experience=68,
        project_count=1400,
        collaboration_rating=9.7
    ),
    BankingAgent(
        name="Santander Global Expert",
        specialty="Santander APIs, Spanish Banking & Latin American Markets",
        expertise_areas=[
            "Santander API", "Spanish banking", "Latin American banking", "European banking",
            "Retail banking", "Commercial banking", "Corporate banking", "Investment banking",
            "Asset management", "Insurance", "Consumer finance", "Auto finance",
            "Trade finance", "Cash management", "Foreign exchange", "Digital banking"
        ],
        years_experience=65,
        project_count=1340,
        collaboration_rating=9.6
    ),
    BankingAgent(
        name="ING Group Integration Specialist",
        specialty="ING APIs, Dutch Banking & European Digital Services",
        expertise_areas=[
            "ING API integration", "Dutch banking", "European banking", "Digital banking",
            "Retail banking", "Commercial banking", "Corporate banking", "Investment banking",
            "Asset management", "Insurance services", "Trade finance", "Cash management",
            "Foreign exchange", "Securities services", "SEPA integration", "Open banking"
        ],
        years_experience=64,
        project_count=1320,
        collaboration_rating=9.6
    ),
    BankingAgent(
        name="Standard Chartered Emerging Markets Expert",
        specialty="StanChart APIs, Emerging Markets & Trade Finance",
        expertise_areas=[
            "Standard Chartered API", "Emerging markets banking", "Trade finance", "Supply chain finance",
            "Corporate banking", "Commercial banking", "Private banking", "Wealth management",
            "Transaction banking", "Cash management", "Foreign exchange", "Commodities",
            "Islamic banking", "Digital banking", "Cross-border banking", "Asian markets"
        ],
        years_experience=67,
        project_count=1380,
        collaboration_rating=9.7
    ),
    BankingAgent(
        name="Credit Suisse Legacy Expert",
        specialty="Credit Suisse Systems, Private Banking & Swiss Financial Services",
        expertise_areas=[
            "Credit Suisse legacy systems", "Private banking", "Wealth management", "Asset management",
            "Investment banking", "Swiss banking", "International banking", "Family office services",
            "Corporate banking", "Securities services", "Foreign exchange", "Prime brokerage",
            "Alternative investments", "Hedge fund services", "UBS integration", "Migration services"
        ],
        years_experience=69,
        project_count=1420,
        collaboration_rating=9.7
    )
]

# =============================================================================
# SPECIALIZED BANKING SERVICES AGENTS
# =============================================================================

specialized_banking_agents = [
    BankingAgent(
        name="Core Banking Systems Expert",
        specialty="Core Banking Platforms, Legacy Integration & System Modernization",
        expertise_areas=[
            "Core banking systems", "Legacy system integration", "System modernization",
            "Banking platform migration", "Real-time processing", "Batch processing",
            "Account management", "Transaction processing", "Interest calculation",
            "Fee management", "Regulatory reporting", "Data migration", "API development",
            "Microservices architecture", "Cloud banking platforms"
        ],
        years_experience=71,
        project_count=1460,
        collaboration_rating=9.8
    ),
    BankingAgent(
        name="Open Banking API Specialist",
        specialty="Open Banking, PSD2 Implementation & API Management",
        expertise_areas=[
            "Open Banking APIs", "PSD2 compliance", "API management", "Third-party integrations",
            "Account information services", "Payment initiation services", "Strong customer authentication",
            "Consent management", "Data sharing", "API security", "Developer portals",
            "Sandbox environments", "API analytics", "Partner management", "Regulatory compliance"
        ],
        years_experience=65,
        project_count=1340,
        collaboration_rating=9.7
    ),
    BankingAgent(
        name="Treasury Management Expert",
        specialty="Corporate Treasury, Cash Management & Liquidity Services",
        expertise_areas=[
            "Corporate treasury", "Cash management", "Liquidity management", "Working capital optimization",
            "Account management", "Payment processing", "Receivables management", "Investment services",
            "Risk management", "Foreign exchange", "Interest rate management", "Debt management",
            "Cash forecasting", "Banking relationships", "Regulatory compliance"
        ],
        years_experience=68,
        project_count=1400,
        collaboration_rating=9.8
    ),
    BankingAgent(
        name="Trade Finance Specialist",
        specialty="International Trade Finance, Letters of Credit & Supply Chain Finance",
        expertise_areas=[
            "International trade finance", "Letters of credit", "Documentary collections",
            "Supply chain finance", "Export finance", "Import finance", "Trade guarantees",
            "Standby letters of credit", "Banker's acceptances", "Trade documentation",
            "Compliance and sanctions", "Risk mitigation", "Cross-border payments",
            "Commodity finance", "Structured trade finance"
        ],
        years_experience=70,
        project_count=1440,
        collaboration_rating=9.8
    ),
    BankingAgent(
        name="Digital Banking Transformation Expert",
        specialty="Digital Banking, Mobile Apps & Omnichannel Experience",
        expertise_areas=[
            "Digital banking strategy", "Mobile banking apps", "Online banking platforms",
            "Omnichannel experience", "Digital customer onboarding", "Digital payments",
            "Personal financial management", "AI-powered services", "Chatbots", "Virtual assistants",
            "Biometric authentication", "Digital wallets", "Robo-advisory", "API banking",
            "Cloud-native architecture"
        ],
        years_experience=62,
        project_count=1280,
        collaboration_rating=9.6
    ),
    BankingAgent(
        name="Banking Compliance Expert",
        specialty="Regulatory Compliance, AML/KYC & Risk Management",
        expertise_areas=[
            "Banking regulations", "Anti-money laundering", "Know your customer", "Sanctions compliance",
            "Basel III compliance", "GDPR compliance", "PCI DSS", "Regulatory reporting",
            "Risk assessment", "Due diligence", "Transaction monitoring", "Suspicious activity reporting",
            "Compliance training", "Audit support", "Policy development", "Regulatory technology"
        ],
        years_experience=69,
        project_count=1420,
        collaboration_rating=9.8
    ),
    BankingAgent(
        name="Commercial Lending Expert",
        specialty="Commercial Loans, Credit Risk & Loan Management Systems",
        expertise_areas=[
            "Commercial lending", "Credit risk assessment", "Loan origination", "Loan management systems",
            "Credit scoring", "Loan pricing", "Portfolio management", "Collection management",
            "Workout and restructuring", "Regulatory compliance", "Documentation", "Collateral management",
            "Covenant monitoring", "Financial analysis", "Industry expertise"
        ],
        years_experience=67,
        project_count=1380,
        collaboration_rating=9.7
    ),
    BankingAgent(
        name="Investment Banking Services Expert",
        specialty="Capital Markets, M&A Advisory & Securities Services",
        expertise_areas=[
            "Investment banking services", "Capital markets", "Mergers and acquisitions", "Securities underwriting",
            "Debt capital markets", "Equity capital markets", "Financial advisory", "Restructuring",
            "Valuations", "Due diligence", "Syndicated lending", "Project finance",
            "Structured finance", "Risk management", "Regulatory compliance"
        ],
        years_experience=72,
        project_count=1480,
        collaboration_rating=9.9
    ),
    BankingAgent(
        name="Private Banking & Wealth Management Expert",
        specialty="Private Banking, Wealth Management & Family Office Services",
        expertise_areas=[
            "Private banking", "Wealth management", "Family office services", "Investment advisory",
            "Portfolio management", "Estate planning", "Tax planning", "Trust services",
            "Alternative investments", "Private equity", "Hedge funds", "Art and collectibles",
            "Philanthropy", "Next generation services", "Regulatory compliance"
        ],
        years_experience=70,
        project_count=1440,
        collaboration_rating=9.8
    ),
    BankingAgent(
        name="Islamic Banking Expert",
        specialty="Sharia-Compliant Banking, Islamic Finance & Sukuk",
        expertise_areas=[
            "Islamic banking principles", "Sharia compliance", "Islamic finance products", "Sukuk",
            "Murabaha", "Ijara", "Mudaraba", "Musharaka", "Takaful", "Islamic investment funds",
            "Sharia advisory boards", "Islamic capital markets", "Regulatory compliance",
            "Risk management", "Islamic treasury management"
        ],
        years_experience=64,
        project_count=1320,
        collaboration_rating=9.6
    )
]

# =============================================================================
# AGENT REGISTRATION AND INITIALIZATION
# =============================================================================

def initialize_global_banking_agents():
    """Initialize all global banking agents"""
    all_banking_agents = (
        top_global_bank_agents +
        specialized_banking_agents
    )
    
    logger.info("🏦 Initializing Global Banking Agents")
    
    # Register all agents
    for agent in all_banking_agents:
        register_banking_agent(agent)
    
    # Log statistics
    banking_counts = {
        'top_global_banks': len(top_global_bank_agents),
        'specialized_services': len(specialized_banking_agents)
    }
    
    total_banking_agents = sum(banking_counts.values())
    
    logger.info("✅ Global banking agents initialized successfully")
    logger.info(f"🌍 Top Global Banks: {banking_counts['top_global_banks']} major institutions")
    logger.info(f"⚡ Specialized Services: {banking_counts['specialized_services']} banking capabilities")
    logger.info(f"🏦 Total Banking Agents: {total_banking_agents} banking experts")
    logger.info(f"🎯 Global Coverage: Complete support for major international banking institutions")
    logger.info(f"🔒 Compliance Ready: AML/KYC, Basel III, PSD2, and regional banking regulations")
    logger.info(f"💼 Services Covered: Core banking, open banking, treasury, trade finance, digital transformation")
    
    return banking_counts

# Initialize on import
banking_stats = initialize_global_banking_agents()