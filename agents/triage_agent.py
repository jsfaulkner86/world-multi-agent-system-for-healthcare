"""triage_agent.py — Intake and severity scoring agent."""

from crewai import Agent
from loguru import logger


class TriageAgent:
    """Handles patient intake, symptom assessment, and ESI severity scoring."""

    def __init__(self, llm):
        self.agent = Agent(
            role="Clinical Triage Specialist",
            goal="Assess patient symptoms, assign an Emergency Severity Index (ESI) score (1-5), and determine appropriate care pathway.",
            backstory=(
                "You are a highly experienced emergency triage nurse with 20+ years in Level 1 trauma centers. "
                "You rapidly assess acuity, flag life-threatening conditions, and route patients to the right care level. "
                "You follow ESI v4 protocols and AHA/ACC guidelines for chest pain and cardiac events."
            ),
            llm=llm,
            verbose=True,
        )
        logger.debug("TriageAgent initialized")

    def assess(self, complaint: str, age: int, gender: str) -> str:
        """Direct triage assessment (used outside CrewAI flow)."""
        prompt = (
            f"Patient: {age}y/o {gender}. Chief complaint: {complaint}. "
            "Assign ESI score, identify red flags, and recommend care pathway."
        )
        return self.agent.llm.predict(prompt)
