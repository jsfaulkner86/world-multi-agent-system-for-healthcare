"""ehr_tools.py — Higher-level EHR tools that aggregate FHIR resources."""

from langchain.tools import tool
from loguru import logger
from tools.fhir_tools import get_patient, get_observations


@tool
def get_patient_summary(patient_id: str) -> dict:
    """Retrieve a full patient summary including demographics and recent vitals."""
    logger.info(f"Building patient summary for: {patient_id}")
    patient = get_patient(patient_id)
    vitals = get_observations(patient_id, category="vital-signs")
    labs = get_observations(patient_id, category="laboratory")

    return {
        "patient": patient,
        "vitals": vitals,
        "labs": labs,
    }
