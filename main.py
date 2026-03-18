"""main.py — Entry point for the World Multi-Agent System for Healthcare."""

from loguru import logger
from agents.coordinator_agent import CoordinatorAgent
from config.settings import settings


def main():
    logger.info("Starting World Multi-Agent System for Healthcare")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"LLM Model: {settings.openai_model}")

    coordinator = CoordinatorAgent()

    # Example task — replace with real intake payload
    sample_task = {
        "patient_id": "PATIENT-001",
        "chief_complaint": "Chest pain with shortness of breath, onset 2 hours ago",
        "age": 67,
        "gender": "male",
        "context": "ED intake at regional health system",
    }

    logger.info(f"Processing task for patient: {sample_task['patient_id']}")
    result = coordinator.run(sample_task)
    logger.info(f"Coordinator result:\n{result}")


if __name__ == "__main__":
    main()
