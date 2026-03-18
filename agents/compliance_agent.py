"""compliance_agent.py — Regulatory and compliance agent."""

from crewai import Agent
from loguru import logger


class ComplianceAgent:
    """Monitors regulatory compliance including HIPAA, CMS, and Joint Commission requirements."""

    def __init__(self, llm):
        self.agent = Agent(
            role="Healthcare Compliance Officer",
            goal="Ensure all patient encounters, data handling, and clinical actions comply with HIPAA, CMS, Joint Commission, and applicable state regulations.",
            backstory=(
                "You are a senior healthcare compliance officer with expertise in HIPAA Privacy and Security Rules, "
                "CMS Conditions of Participation, and Joint Commission standards. "
                "You review clinical workflows for regulatory risk, flag potential violations, "
                "and recommend corrective actions before documentation is finalized."
            ),
            llm=llm,
            verbose=True,
        )
        logger.debug("ComplianceAgent initialized")

    def check(self, workflow_context: dict) -> str:
        """Run compliance check on a workflow (used outside CrewAI flow)."""
        prompt = (
            f"Workflow context: {workflow_context}. "
            "Identify any HIPAA, CMS, or Joint Commission compliance risks and recommend mitigations."
        )
        return self.agent.llm.predict(prompt)
