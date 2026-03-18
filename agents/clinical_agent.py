"""clinical_agent.py — Clinical decision support agent."""

from crewai import Agent
from loguru import logger


class ClinicalAgent:
    """Provides evidence-based clinical decision support and protocol recommendations."""

    def __init__(self, llm):
        self.agent = Agent(
            role="Clinical Decision Support Specialist",
            goal="Provide evidence-based clinical recommendations, differential diagnoses, and treatment protocols aligned with AHA, ACC, and CMS guidelines.",
            backstory=(
                "You are a board-certified internal medicine physician with subspecialty training in "
                "cardiovascular medicine. You synthesize patient data, apply clinical guidelines, "
                "generate differential diagnoses, and recommend diagnostic workups and treatment plans. "
                "You always cite the guideline source for your recommendations."
            ),
            llm=llm,
            verbose=True,
        )
        logger.debug("ClinicalAgent initialized")

    def recommend(self, patient_context: dict) -> str:
        """Generate clinical recommendations (used outside CrewAI flow)."""
        prompt = (
            f"Clinical context: {patient_context}. "
            "Provide differential diagnosis, recommended workup, and treatment plan with guideline citations."
        )
        return self.agent.llm.predict(prompt)
