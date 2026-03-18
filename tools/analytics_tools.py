"""analytics_tools.py — Risk stratification and analytics tools."""

from langchain.tools import tool
from loguru import logger


@tool
def analyze_patient_risk(patient_data: dict) -> dict:
    """
    Analyze patient data and return a risk stratification score.
    Evaluates cardiovascular, sepsis, and readmission risk.
    """
    logger.info("Running patient risk analysis")

    age = patient_data.get("age", 0)
    complaint = patient_data.get("chief_complaint", "").lower()

    risk_flags = []
    risk_score = 0

    if age >= 65:
        risk_score += 2
        risk_flags.append("Age >= 65 (elevated risk)")

    cardiac_keywords = ["chest pain", "shortness of breath", "palpitation", "syncope", "diaphoresis"]
    for kw in cardiac_keywords:
        if kw in complaint:
            risk_score += 3
            risk_flags.append(f"Cardiac keyword detected: '{kw}'")
            break

    sepsis_keywords = ["fever", "chills", "hypotension", "altered mental status", "tachycardia"]
    for kw in sepsis_keywords:
        if kw in complaint:
            risk_score += 3
            risk_flags.append(f"Sepsis keyword detected: '{kw}'")
            break

    risk_level = "LOW"
    if risk_score >= 5:
        risk_level = "HIGH"
    elif risk_score >= 3:
        risk_level = "MODERATE"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_flags": risk_flags,
    }
