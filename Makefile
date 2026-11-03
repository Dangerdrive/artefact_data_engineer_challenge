.PHONY: install run test lint format clean

# Install dependencies
install:
	python -m pip install -r requirements.txt

# Run the agent (CLI)
run:
	python -m src.cli

# Run the tests
test:
	pytest

# Check lint
lint:
	ruff check .

# Format the code
format:
	ruff format .

# Remove temporary artifacts
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .pytest_cache .ruff_cache .tmp
