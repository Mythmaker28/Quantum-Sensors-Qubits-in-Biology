#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Biological Qubits Atlas - Data Validation Script

Validates biological_qubits.csv against physical constraints and schema rules.

Author: SOFTWARE-ENGINEER-QA / CLAUDE-MAINTAINER
Date: 2025-11-15
Updated: 2025-11-15 (Windows encoding fix)
"""

import csv
import re
import sys
import io
from pathlib import Path
from typing import List, Dict, Tuple
from dataclasses import dataclass

# Force UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


@dataclass
class ValidationError:
    """Represents a validation error"""
    row: int
    column: str
    value: str
    message: str
    severity: str  # 'error' or 'warning'


class BiologicalQubitsValidator:
    """Validator for biological qubits atlas data"""
    
    def __init__(self, csv_path: str):
        self.csv_path = Path(csv_path)
        self.errors: List[ValidationError] = []
        self.warnings: List[ValidationError] = []
        self.data: List[Dict] = []
        
    def load_data(self) -> bool:
        """Load CSV data"""
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.data = list(reader)
            print(f"✅ Loaded {len(self.data)} systems from {self.csv_path}")
            return True
        except Exception as e:
            print(f"❌ Error loading {self.csv_path}: {e}")
            return False
    
    def validate_all(self):
        """Run all validation checks"""
        print("\n" + "="*70)
        print("🔍 VALIDATION BIOLOGICAL QUBITS ATLAS")
        print("="*70 + "\n")
        
        for idx, row in enumerate(self.data, start=2):  # Start at 2 (row 1 = header)
            self._validate_row(idx, row)
        
        self._print_report()
    
    def _validate_row(self, row_num: int, row: Dict):
        """Validate a single row"""
        # 1. Required fields
        self._check_required_fields(row_num, row)
        
        # 2. Physical constraints
        self._check_physical_constraints(row_num, row)
        
        # 3. Temperature consistency
        self._check_temperature_consistency(row_num, row)
        
        # 4. Class consistency
        self._check_class_consistency(row_num, row)
        
        # 5. DOI format
        self._check_doi_format(row_num, row)
        
        # 6. Numeric ranges
        self._check_numeric_ranges(row_num, row)
    
    def _check_required_fields(self, row_num: int, row: Dict):
        """Check required fields are present"""
        required = ['Systeme', 'Classe', 'Hote_contexte', 'Methode_lecture',
                   'Spin_type', 'Temperature_K', 'DOI', 'Annee', 'Qualite',
                   'Verification_statut']
        
        for field in required:
            value = row.get(field, '').strip()
            if not value or value == 'NA':
                self._add_error(row_num, field, value,
                              f"Required field '{field}' is missing or NA",
                              'error')
    
    def _check_physical_constraints(self, row_num: int, row: Dict):
        """Check T₂ ≤ 2*T₁ constraint"""
        t1_str = row.get('T1_s', '').strip()
        t2_str = row.get('T2_us', '').strip()
        
        if not t1_str or not t2_str or t1_str == 'NA' or t2_str == 'NA':
            return  # Skip if either is missing
        
        try:
            t1_s = float(t1_str)
            t2_us = float(t2_str)
            
            # Convert T1 to microseconds for comparison
            t1_us = t1_s * 1e6
            
            # Check T₂ ≤ 2*T₁
            if t2_us > 2 * t1_us:
                self._add_error(
                    row_num, 'T2_us', t2_str,
                    f"T₂ ({t2_us:.2f} µs) > 2*T₁ ({2*t1_us:.2f} µs). Violates physical constraint T₂ ≤ 2*T₁",
                    'error'
                )
        except ValueError:
            self._add_warning(row_num, 'T1_s/T2_us', f"{t1_str}/{t2_str}",
                            "Cannot parse T₁ or T₂ as float", 'warning')
    
    def _check_temperature_consistency(self, row_num: int, row: Dict):
        """Check temperature ranges for biological contexts"""
        temp_str = row.get('Temperature_K', '').strip()
        context = row.get('Hote_contexte', '').lower()
        
        if not temp_str or temp_str == 'NA':
            return
        
        try:
            temp = float(temp_str)
            
            # Check for biological contexts (in_cellulo, in_vivo)
            if 'in_cellulo' in context or 'in_vivo' in context:
                if temp < 273 or temp > 310:
                    self._add_warning(
                        row_num, 'Temperature_K', temp_str,
                        f"Temperature {temp} K outside physiological range (273-310 K) for {context}",
                        'warning'
                    )
            
            # Check for unrealistic temperatures
            # Lower bound relaxed to 1 K to accommodate cryogenic benchmarks
            # (e.g. 31P donors in Si at 2 K, SiV/GeV centers at 4 K)
            if temp < 1 or temp > 400:
                self._add_error(
                    row_num, 'Temperature_K', temp_str,
                    f"Temperature {temp} K is unrealistic (expected 1-400 K)",
                    'error'
                )
        except ValueError:
            self._add_warning(row_num, 'Temperature_K', temp_str,
                            "Cannot parse temperature as float", 'warning')
    
    def _check_class_consistency(self, row_num: int, row: Dict):
        """Check class consistency (e.g., hyperpolarization = class C)"""
        classe = row.get('Classe', '').strip()
        hyperpol = row.get('Hyperpol_flag', '').strip()
        
        # Valid classes (A_prime added in v3.0 for FP-qubits with direct ODMR)
        if classe and classe not in ['A', 'A_prime', 'B', 'C', 'D']:
            self._add_error(
                row_num, 'Classe', classe,
                f"Invalid class '{classe}'. Expected A, A_prime, B, C, or D",
                'error'
            )
        
        # Hyperpolarization should be class C
        if hyperpol == '1' and classe != 'C':
            self._add_warning(
                row_num, 'Classe', classe,
                f"Hyperpol_flag=1 but Classe={classe} (expected C for hyperpolarized)",
                'warning'
            )
    
    def _check_doi_format(self, row_num: int, row: Dict):
        """Check DOI format (should start with 10.)"""
        doi = row.get('DOI', '').strip()
        
        if not doi or doi == 'NA':
            self._add_warning(row_num, 'DOI', doi,
                            "DOI is missing (strongly recommended)", 'warning')
            return
        
        # DOI should start with "10."
        if not doi.startswith('10.'):
            self._add_error(
                row_num, 'DOI', doi,
                f"DOI '{doi}' does not start with '10.' (invalid format)",
                'error'
            )
    
    def _check_numeric_ranges(self, row_num: int, row: Dict):
        """Check numeric values are in reasonable ranges"""
        checks = [
            ('Contraste_%', 0, 100, "Contrast should be between 0 and 100%"),
            ('B0_Tesla', 0, 20, "Magnetic field should be between 0 and 20 T"),
            ('Qualite', 1, 3, "Quality should be 1, 2, or 3"),
            ('Annee', 1980, 2027, "Year should be between 1980 and 2027"),
        ]
        
        for field, min_val, max_val, msg in checks:
            value_str = row.get(field, '').strip()
            if not value_str or value_str == 'NA':
                continue
            
            try:
                value = float(value_str)
                if value < min_val or value > max_val:
                    self._add_warning(
                        row_num, field, value_str,
                        f"{msg} (got {value})",
                        'warning'
                    )
            except ValueError:
                self._add_warning(row_num, field, value_str,
                                f"Cannot parse {field} as number", 'warning')
    
    def _add_error(self, row: int, column: str, value: str, message: str, severity: str):
        """Add a validation error"""
        error = ValidationError(row, column, value, message, severity)
        if severity == 'error':
            self.errors.append(error)
        else:
            self.warnings.append(error)
    
    def _add_warning(self, row: int, column: str, value: str, message: str, severity: str):
        """Add a validation warning"""
        self._add_error(row, column, value, message, severity)
    
    def _print_report(self):
        """Print validation report"""
        print("\n" + "="*70)
        print("[VALIDATION REPORT]")
        print("="*70 + "\n")
        
        # Summary
        print(f"Total systems validated: {len(self.data)}")
        print(f"[ERROR] Errors (critical): {len(self.errors)}")
        print(f"[WARN] Warnings: {len(self.warnings)}")
        
        # Errors
        if self.errors:
            print("\n" + "-"*70)
            print("[ERRORS] Critical - must fix")
            print("-"*70)
            for error in self.errors:
                print(f"\nRow {error.row} | Column: {error.column}")
                print(f"  Value: '{error.value}'")
                print(f"  Error: {error.message}")
        
        # Warnings
        if self.warnings:
            print("\n" + "-"*70)
            print("[WARNINGS] Recommended fixes")
            print("-"*70)
            for warning in self.warnings[:20]:  # Limit to 20 warnings
                print(f"\nRow {warning.row} | Column: {warning.column}")
                print(f"  Value: '{warning.value}'")
                print(f"  Warning: {warning.message}")
            
            if len(self.warnings) > 20:
                print(f"\n... and {len(self.warnings) - 20} more warnings")
        
        # Final verdict
        print("\n" + "="*70)
        if len(self.errors) == 0:
            print("[OK] VALIDATION PASSED (no critical errors)")
            if len(self.warnings) > 0:
                print(f"[WARN] {len(self.warnings)} warnings should be reviewed")
        else:
            print(f"[FAIL] VALIDATION FAILED ({len(self.errors)} critical errors)")
        print("="*70 + "\n")
        
        return len(self.errors) == 0


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Validate Biological Qubits Atlas data'
    )
    parser.add_argument(
        '--input',
        default='data/qubits/biological_qubits.csv',
        help='Path to CSV file (default: data/qubits/biological_qubits.csv)'
    )
    
    args = parser.parse_args()
    
    # Validate
    validator = BiologicalQubitsValidator(args.input)
    
    if not validator.load_data():
        sys.exit(1)
    
    validator.validate_all()
    
    # Exit code: 0 if passed, 1 if errors
    sys.exit(0 if len(validator.errors) == 0 else 1)


if __name__ == '__main__':
    main()

