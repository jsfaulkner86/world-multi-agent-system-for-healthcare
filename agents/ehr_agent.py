"""ehr_agent.py — Epic EHR read/write agent via FHIR R4."""

from crewai import Agent
from loguru import logger
from tools.fhir_tools import get_patient, get_observations, create_note


class EHRAgent:
    """Interfaces with Epic EHR via FHIR R4 for patient data retrieval and documentation."""

    def __init__(self, llm):
        self.agent = Agent(
            role="EHR Integration Specialist",
            goal="Retrieve relevant patient records from Epic EHR via FHIR R4, and document clinical findings accurately and compliantly.",
            backstory=(
                "You are a clinical informaticist and Epic-certified EHR specialist. "
                "You retrieve patient demographics, labs, vitals, medications, and history from Epic "
                "using FHIR R4 APIs, and you document clinical notes and orders with precision. "
                "You understand HL7 FHIR resource types and Epic's proprietary extensions."
            ),
            llm=llm,
            tools=[get_patient, get_observations, create_note],
            verbose=True,
        )
        logger.debug("EHRAgent initialized")
