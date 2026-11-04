.PHONY: install run test lint format clean publish

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

# Add the remote (first run) and push the main branch.
# Usage: make publish REMOTE=git@github.com:user/repo.git
publish:
	@test -n "$(REMOTE)" || (echo "Usage: make publish REMOTE=<git-url>"; exit 1)
	@git remote get-url origin >/dev/null 2>&1 && git remote set-url origin "$(REMOTE)" || git remote add origin "$(REMOTE)"
	git push -u origin main
