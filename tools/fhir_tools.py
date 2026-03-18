"""fhir_tools.py — FHIR R4 tools for agent use via LangChain @tool decorator."""

import httpx
from langchain.tools import tool
from loguru import logger
from config.settings import settings


def _get_auth_headers() -> dict:
    """Returns Bearer token headers for Epic FHIR API."""
    # TODO: Implement Epic OAuth2 SMART on FHIR token flow
    return {
        "Authorization": "Bearer YOUR_TOKEN_HERE",
        "Accept": "application/fhir+json",
    }


@tool
def get_patient(patient_id: str) -> dict:
    """Retrieve a Patient resource from Epic FHIR R4 by patient ID."""
    url = f"{settings.epic_fhir_base_url}/Patient/{patient_id}"
    logger.info(f"FHIR GET Patient: {url}")
    try:
        response = httpx.get(url, headers=_get_auth_headers(), timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"FHIR get_patient error: {e}")
        return {"error": str(e)}


@tool
def get_observations(patient_id: str, category: str = "vital-signs") -> dict:
    """Retrieve Observation resources (vitals, labs) for a patient from Epic FHIR R4."""
    url = f"{settings.epic_fhir_base_url}/Observation?patient={patient_id}&category={category}"
    logger.info(f"FHIR GET Observations: {url}")
    try:
        response = httpx.get(url, headers=_get_auth_headers(), timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"FHIR get_observations error: {e}")
        return {"error": str(e)}


@tool
def create_note(patient_id: str, note_text: str, author: str = "AI Clinical Assistant") -> dict:
    """Create a clinical DocumentReference (note) in Epic FHIR R4 for a patient."""
    import base64
    url = f"{settings.epic_fhir_base_url}/DocumentReference"
    encoded_note = base64.b64encode(note_text.encode()).decode()
    payload = {
        "resourceType": "DocumentReference",
        "status": "current",
        "subject": {"reference": f"Patient/{patient_id}"},
        "author": [{"display": author}],
        "content": [
            {
                "attachment": {
                    "contentType": "text/plain",
                    "data": encoded_note,
                }
            }
        ],
    }
    logger.info(f"FHIR POST DocumentReference for patient: {patient_id}")
    try:
        response = httpx.post(url, json=payload, headers=_get_auth_headers(), timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"FHIR create_note error: {e}")
        return {"error": str(e)}
