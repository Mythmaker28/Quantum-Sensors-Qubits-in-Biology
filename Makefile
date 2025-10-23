# Makefile for Biological Qubits Atlas
# Quick commands for common tasks

.PHONY: help setup lint validate qc figures clean

# Default target
help:
	@echo "Biological Qubits Atlas - Available Commands:"
	@echo ""
	@echo "  make setup      Install dependencies and setup environment"
	@echo "  make lint       Run linter and validate CSV"
	@echo "  make validate   Validate CSV schema and data quality"
	@echo "  make qc         Generate QC_REPORT.md"
	@echo "  make figures    Generate figures (T2 vs Temp, Timeline)"
	@echo "  make clean      Remove generated files"
	@echo ""

# Setup: Install dependencies
setup:
	@echo "Setting up Biological Qubits Atlas..."
	@python --version
	@pip install -r requirements.txt 2>/dev/null || echo "No requirements.txt found"
	@echo "Setup complete!"

# Lint: Validate CSV with linter
lint:
	@echo "Running linter..."
	@python qubits_linter.py
	@echo "Lint complete!"

# Validate: Alias for lint
validate: lint

# QC: Generate quality control report
qc:
	@echo "Generating QC report..."
	@python qubits_linter.py
	@echo "QC report generated: QC_REPORT.md"

# Figures: Generate visualization figures
figures:
	@echo "Generating figures..."
	@python generate_figures.py
	@echo "Figures generated in figures/"

# Clean: Remove generated files
clean:
	@echo "Cleaning generated files..."
	@rm -f QC_REPORT.md.tmp
	@rm -f *.pyc
	@rm -rf __pycache__
	@echo "Clean complete!"

# Quick validation workflow
check: lint
	@echo ""
	@echo "Quick check complete!"
	@echo "Status: CSV validated successfully"

# Full workflow: validate + generate QC + figures
all: lint qc figures
	@echo ""
	@echo "Full workflow complete!"
	@echo "- CSV validated"
	@echo "- QC report updated"
	@echo "- Figures generated"

