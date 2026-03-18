# ============================================================
# World Multi-Agent System for Healthcare — Makefile
# ============================================================

.PHONY: help install run test lint clean pull setup

PYTHON := python3
VENV := venv
ACTIVATE := source $(VENV)/bin/activate

## help: Show available commands
help:
	@echo ""
	@echo "World Multi-Agent System for Healthcare"
	@echo "========================================"
	@grep -E '^## ' Makefile | sed 's/## //g'
	@echo ""

## setup: Full first-time setup (pull, venv, install, .env)
setup: pull venv install env
	@echo ""
	@echo "✅ Setup complete. Edit .env with your API keys, then run: make run"
	@echo ""

## pull: Pull latest from remote and rebase
pull:
	@echo "→ Pulling latest from origin/main..."
	git pull origin main --rebase

## venv: Create Python virtual environment
venv:
	@echo "→ Creating virtual environment..."
	$(PYTHON) -m venv $(VENV)
	@echo "✅ venv created. It will be activated automatically by other make commands."

## install: Install all Python dependencies into venv
install:
	@echo "→ Installing dependencies..."
	$(ACTIVATE) && pip install --upgrade pip && pip install -r requirements.txt
	@echo "✅ Dependencies installed."

## env: Copy .env.example to .env if .env doesn't exist
env:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✅ .env created from .env.example — add your API keys."; \
	else \
		echo "ℹ️  .env already exists — skipping."; \
	fi

## run: Run the multi-agent system
run:
	@echo "→ Starting World Multi-Agent System for Healthcare..."
	$(ACTIVATE) && python main.py

## test: Run all unit tests
test:
	@echo "→ Running tests..."
	$(ACTIVATE) && pytest tests/ -v

## test-oauth: Run only OAuth tests
test-oauth:
	@echo "→ Running OAuth tests..."
	$(ACTIVATE) && pytest tests/test_oauth.py -v

## test-agents: Run only agent tests
test-agents:
	@echo "→ Running agent tests..."
	$(ACTIVATE) && pytest tests/test_agents.py -v

## lint: Run linter (ruff)
lint:
	@echo "→ Running linter..."
	$(ACTIVATE) && ruff check .

## clean: Remove venv, cache, and compiled files
clean:
	@echo "→ Cleaning up..."
	rm -rf $(VENV) __pycache__ .pytest_cache .coverage htmlcov
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -delete
	@echo "✅ Clean complete."

## freeze: Save current installed packages to requirements.txt
freeze:
	$(ACTIVATE) && pip freeze > requirements.txt
	@echo "✅ requirements.txt updated."
