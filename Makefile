.PHONY: install run test lint format clean

# Instala as dependências
install:
	python -m pip install -r requirements.txt

# Executa o agente (CLI)
run:
	python -m src.cli

# Executa os testes
test:
	pytest

# Verifica lint
lint:
	ruff check .

# Formata o código
format:
	ruff format .

# Remove artefatos temporários
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .pytest_cache .ruff_cache .tmp
