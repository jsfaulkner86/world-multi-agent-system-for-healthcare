"""coordinator_agent.py — Master orchestrator agent using CrewAI."""

from crewai import Agent, Crew, Task, Process
from langchain_openai import ChatOpenAI
from loguru import logger
from config.settings import settings
from agents.triage_agent import TriageAgent
from agents.clinical_agent import ClinicalAgent
from agents.compliance_agent import ComplianceAgent
from agents.ehr_agent import EHRAgent
from memory.shared_memory import SharedMemory


class CoordinatorAgent:
    """Orchestrates all sub-agents and manages the end-to-end healthcare workflow."""

    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
        )
        self.memory = SharedMemory()
        self.triage = TriageAgent(llm=self.llm)
        self.clinical = ClinicalAgent(llm=self.llm)
        self.compliance = ComplianceAgent(llm=self.llm)
        self.ehr = EHRAgent(llm=self.llm)

    def run(self, task_payload: dict) -> str:
        logger.info("Coordinator: Building CrewAI crew for task")

        coordinator = Agent(
            role="Healthcare Workflow Coordinator",
            goal="Orchestrate triage, clinical, compliance, and EHR agents to deliver a safe, compliant, and actionable healthcare response.",
            backstory=(
                "You are the master coordinator of a world-class healthcare AI system. "
                "You route tasks intelligently, synthesize agent outputs, and ensure "
                "every patient encounter is handled with clinical precision and regulatory compliance."
            ),
            llm=self.llm,
            verbose=True,
        )

        task_description = (
            f"Patient ID: {task_payload.get('patient_id')}\n"
            f"Chief Complaint: {task_payload.get('chief_complaint')}\n"
            f"Age: {task_payload.get('age')}, Gender: {task_payload.get('gender')}\n"
            f"Context: {task_payload.get('context')}\n\n"
            "Steps:\n"
            "1. Run triage assessment and assign severity score\n"
            "2. Perform clinical decision support\n"
            "3. Check compliance and regulatory requirements\n"
            "4. Retrieve relevant EHR data and document findings\n"
            "5. Synthesize a final care recommendation"
        )

        crew_task = Task(
            description=task_description,
            agent=coordinator,
            expected_output="A structured care plan with triage level, clinical recommendations, compliance notes, and EHR actions.",
        )

        crew = Crew(
            agents=[
                coordinator,
                self.triage.agent,
                self.clinical.agent,
                self.compliance.agent,
                self.ehr.agent,
            ],
            tasks=[crew_task],
            process=Process.sequential,
            verbose=True,
        )

        result = crew.kickoff()
        self.memory.store(task_payload.get("patient_id"), result)
        return result
