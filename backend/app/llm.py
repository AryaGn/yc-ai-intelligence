import random

def analyze_company(data: dict):
    return f"""
Summary:
{data['name']} operates in the domain {data['domain']}.

Investment Note:
This company shows early-stage signals with potential scalability.
"""

def score_company(data: dict):
    growth = random.randint(60, 90)
    risk = random.randint(20, 60)
    innovation = random.randint(70, 95)

    return {
        "growth_score": growth,
        "risk_score": risk,
        "innovation_score": innovation,
        "explanation": f"""
Growth potential driven by market expansion.
Risk moderate due to early-stage uncertainty.
Innovation high due to AI-driven approach.
"""
    }

def synthesize_answer(question: str, companies):
    return f"Mock answer about {', '.join([c.name for c in companies])}"