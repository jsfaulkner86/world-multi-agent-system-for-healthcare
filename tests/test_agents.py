"""test_agents.py — Unit tests for all agents."""

import pytest
from unittest.mock import MagicMock, patch
from agents.triage_agent import TriageAgent
from agents.clinical_agent import ClinicalAgent
from agents.compliance_agent import ComplianceAgent
from memory.shared_memory import SharedMemory
from tools.analytics_tools import analyze_patient_risk


@pytest.fixture
def mock_llm():
    llm = MagicMock()
    llm.predict.return_value = "Mocked LLM response"
    return llm


def test_triage_agent_initializes(mock_llm):
    agent = TriageAgent(llm=mock_llm)
    assert agent.agent is not None
    assert agent.agent.role == "Clinical Triage Specialist"


def test_clinical_agent_initializes(mock_llm):
    agent = ClinicalAgent(llm=mock_llm)
    assert agent.agent is not None
    assert agent.agent.role == "Clinical Decision Support Specialist"


def test_compliance_agent_initializes(mock_llm):
    agent = ComplianceAgent(llm=mock_llm)
    assert agent.agent is not None
    assert agent.agent.role == "Healthcare Compliance Officer"


def test_shared_memory_store_retrieve():
    mem = SharedMemory()
    mem.store("PATIENT-001", {"result": "test"})
    result = mem.retrieve("PATIENT-001")
    assert result == {"result": "test"}


def test_shared_memory_delete():
    mem = SharedMemory()
    mem.store("KEY", "value")
    mem.delete("KEY")
    assert mem.retrieve("KEY") is None


def test_analyze_patient_risk_high():
    data = {"age": 67, "chief_complaint": "chest pain with shortness of breath"}
    result = analyze_patient_risk(data)
    assert result["risk_level"] == "HIGH"
    assert result["risk_score"] >= 5


def test_analyze_patient_risk_low():
    data = {"age": 25, "chief_complaint": "mild headache"}
    result = analyze_patient_risk(data)
    assert result["risk_level"] == "LOW"
