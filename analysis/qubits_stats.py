#!/usr/bin/env python3
"""
Biological Qubits Atlas - Qubit Statistics Analysis

Computes descriptive statistics for the qubits dataset:
- Overall statistics
- Statistics by class (A, B, C, D)
- Temperature vs T₂ analysis
- Spin type distribution

Outputs: JSON and Markdown reports in analysis/output/

Author: CLAUDE-MAINTAINER
Date: 2025-11-15
"""

import argparse
import pandas as pd
import numpy as np
import json
from pathlib import Path
from datetime import datetime


def load_qubits_data(csv_path='data/qubits/biological_qubits_v3.csv'):
    """Load qubits dataset"""
    try:
        df = pd.read_csv(csv_path)
        print(f"[OK] Loaded {len(df)} qubits from {csv_path}")
        return df
    except FileNotFoundError:
        print(f"[ERROR] File not found: {csv_path}")
        return None


def compute_overall_stats(df):
    """Compute overall dataset statistics"""
    stats = {
        'total_systems': len(df),
        'classes': df['Classe'].value_counts().to_dict(),
        'spin_types': df['Spin_type'].value_counts().to_dict(),
        'methods': df['Methode_lecture'].value_counts().to_dict(),
        'contexts': {
            'in_cellulo': len(df[df['Hote_contexte'].str.contains('in_cellulo', na=False)]),
            'in_vivo': len(df[df['Hote_contexte'].str.contains('in_vivo', na=False)]),
            'in_vitro': len(df[df['Hote_contexte'].str.contains('in_vitro', na=False)])
        }
    }
    
    # T₂ statistics (convert to numeric, handle errors)
    df['T2_us_numeric'] = pd.to_numeric(df['T2_us'], errors='coerce')
    t2_valid = df['T2_us_numeric'].dropna()
    
    if len(t2_valid) > 0:
        stats['T2_us'] = {
            'count': int(len(t2_valid)),
            'mean': float(t2_valid.mean()),
            'median': float(t2_valid.median()),
            'std': float(t2_valid.std()),
            'min': float(t2_valid.min()),
            'max': float(t2_valid.max()),
            'q25': float(t2_valid.quantile(0.25)),
            'q75': float(t2_valid.quantile(0.75))
        }
    
    # Temperature statistics
    df['Temperature_K_numeric'] = pd.to_numeric(df['Temperature_K'], errors='coerce')
    temp_valid = df['Temperature_K_numeric'].dropna()
    
    if len(temp_valid) > 0:
        stats['Temperature_K'] = {
            'count': int(len(temp_valid)),
            'mean': float(temp_valid.mean()),
            'median': float(temp_valid.median()),
            'std': float(temp_valid.std()),
            'min': float(temp_valid.min()),
            'max': float(temp_valid.max()),
            'physiological_range_273_310': int(len(temp_valid[(temp_valid >= 273) & (temp_valid <= 310)]))
        }
    
    # Contrast statistics
    df['Contraste_numeric'] = pd.to_numeric(df['Contraste_%'], errors='coerce')
    contraste_valid = df['Contraste_numeric'].dropna()
    
    if len(contraste_valid) > 0:
        stats['Contraste_%'] = {
            'count': int(len(contraste_valid)),
            'mean': float(contraste_valid.mean()),
            'median': float(contraste_valid.median()),
            'std': float(contraste_valid.std()),
            'min': float(contraste_valid.min()),
            'max': float(contraste_valid.max())
        }
    
    return stats


def compute_class_stats(df):
    """Compute statistics by class (A, B, C, D)"""
    classes = df['Classe'].unique()
    class_stats = {}
    
    for classe in sorted(classes):
        df_class = df[df['Classe'] == classe]
        
        # T₂ stats for this class
        t2_valid = pd.to_numeric(df_class['T2_us'], errors='coerce').dropna()
        
        class_stats[classe] = {
            'count': len(df_class),
            'spin_types': df_class['Spin_type'].value_counts().to_dict(),
            'methods': df_class['Methode_lecture'].value_counts().to_dict()
        }
        
        if len(t2_valid) > 0:
            class_stats[classe]['T2_us'] = {
                'mean': float(t2_valid.mean()),
                'median': float(t2_valid.median()),
                'min': float(t2_valid.min()),
                'max': float(t2_valid.max())
            }
    
    return class_stats


def analyze_temperature_vs_t2(df):
    """Analyze T₂ vs Temperature correlation"""
    df['T2_us_numeric'] = pd.to_numeric(df['T2_us'], errors='coerce')
    df['Temperature_K_numeric'] = pd.to_numeric(df['Temperature_K'], errors='coerce')
    
    df_valid = df[['T2_us_numeric', 'Temperature_K_numeric', 'Classe']].dropna()
    
    if len(df_valid) < 2:
        return {'note': 'Insufficient data for correlation analysis'}
    
    correlation = df_valid['T2_us_numeric'].corr(df_valid['Temperature_K_numeric'])
    
    # Group by temperature ranges
    temp_ranges = {
        'cryogenic_<100K': df_valid[df_valid['Temperature_K_numeric'] < 100],
        '100-273K': df_valid[(df_valid['Temperature_K_numeric'] >= 100) & (df_valid['Temperature_K_numeric'] < 273)],
        'physiological_273-310K': df_valid[(df_valid['Temperature_K_numeric'] >= 273) & (df_valid['Temperature_K_numeric'] <= 310)],
        '>310K': df_valid[df_valid['Temperature_K_numeric'] > 310]
    }
    
    range_stats = {}
    for range_name, df_range in temp_ranges.items():
        if len(df_range) > 0:
            range_stats[range_name] = {
                'count': len(df_range),
                'T2_mean_us': float(df_range['T2_us_numeric'].mean()),
                'T2_median_us': float(df_range['T2_us_numeric'].median())
            }
    
    return {
        'correlation_T2_vs_Temp': float(correlation) if not np.isnan(correlation) else None,
        'temperature_ranges': range_stats
    }


def generate_markdown_report(stats, class_stats, temp_analysis, output_path, dataset_path='data/qubits/biological_qubits_v3.csv'):
    """Generate Markdown summary report"""
    report = f"""# Qubits Statistics Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Dataset:** {dataset_path}

---

## Overall Statistics

- **Total systems:** {stats['total_systems']}
- **Classes:** {', '.join([f'{k}: {v}' for k, v in stats['classes'].items()])}
- **Spin types:** {len(stats['spin_types'])}
- **Reading methods:** {len(stats['methods'])}

### Context Distribution

- In cellulo: {stats['contexts']['in_cellulo']}
- In vivo: {stats['contexts']['in_vivo']}
- In vitro: {stats['contexts']['in_vitro']}

---

## T₂ (Coherence Time) Statistics

"""
    
    if 'T2_us' in stats:
        t2 = stats['T2_us']
        report += f"""
- **Count:** {t2['count']}
- **Mean:** {t2['mean']:.2f} µs
- **Median:** {t2['median']:.2f} µs
- **Std Dev:** {t2['std']:.2f} µs
- **Range:** {t2['min']:.2f} - {t2['max']:.2f} µs
- **Q25-Q75:** {t2['q25']:.2f} - {t2['q75']:.2f} µs
"""
    
    report += "\n---\n\n## Temperature Statistics\n"
    
    if 'Temperature_K' in stats:
        temp = stats['Temperature_K']
        report += f"""
- **Count:** {temp['count']}
- **Mean:** {temp['mean']:.1f} K
- **Median:** {temp['median']:.1f} K
- **Range:** {temp['min']:.1f} - {temp['max']:.1f} K
- **Physiological range (273-310 K):** {temp['physiological_range_273_310']} systems
"""
    
    report += "\n---\n\n## Statistics by Class\n"
    
    for classe, cstats in sorted(class_stats.items()):
        report += f"\n### Class {classe}\n"
        report += f"- **Count:** {cstats['count']}\n"
        report += f"- **Spin types:** {', '.join([f'{k}: {v}' for k, v in cstats['spin_types'].items()])}\n"
        
        if 'T2_us' in cstats:
            t2 = cstats['T2_us']
            report += f"- **T₂ mean:** {t2['mean']:.2f} µs (median: {t2['median']:.2f} µs)\n"
            report += f"- **T₂ range:** {t2['min']:.2f} - {t2['max']:.2f} µs\n"
    
    report += "\n---\n\n## Temperature vs T₂ Analysis\n"
    
    if 'correlation_T2_vs_Temp' in temp_analysis and temp_analysis['correlation_T2_vs_Temp'] is not None:
        report += f"\n**Correlation coefficient:** {temp_analysis['correlation_T2_vs_Temp']:.3f}\n"
    
    if 'temperature_ranges' in temp_analysis:
        report += "\n### T₂ by Temperature Range\n"
        for range_name, rstats in temp_analysis['temperature_ranges'].items():
            report += f"\n**{range_name}:**\n"
            report += f"- Count: {rstats['count']}\n"
            report += f"- T₂ mean: {rstats['T2_mean_us']:.2f} µs\n"
            report += f"- T₂ median: {rstats['T2_median_us']:.2f} µs\n"
    
    report += "\n---\n\n*Generated by analysis/qubits_stats.py*\n"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"[OK] Markdown report saved to {output_path}")


def main():
    """Main execution"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', default='data/qubits/biological_qubits_v3.csv',
                        help='Path to qubits CSV (default: v3)')
    parser.add_argument('--version', default='3.0', help='Dataset version string')
    args = parser.parse_args()

    print("="*70)
    print("[QUBITS STATISTICS ANALYSIS]")
    print("="*70 + "\n")

    df = load_qubits_data(args.input)
    if df is None:
        return 1

    output_dir = Path('analysis/output')
    output_dir.mkdir(parents=True, exist_ok=True)

    print("\n[Computing statistics...]")
    overall_stats = compute_overall_stats(df)
    class_stats = compute_class_stats(df)
    temp_analysis = analyze_temperature_vs_t2(df)

    results = {
        'metadata': {
            'generated': datetime.now().isoformat(),
            'dataset': args.input,
            'version': args.version,
        },
        'overall': overall_stats,
        'by_class': class_stats,
        'temperature_vs_T2': temp_analysis
    }
    
    # Save JSON
    json_path = output_dir / 'qubits_stats.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"[OK] JSON results saved to {json_path}")
    
    # Save Markdown
    md_path = output_dir / 'qubits_stats.md'
    generate_markdown_report(overall_stats, class_stats, temp_analysis, md_path, args.input)
    
    print("\n" + "="*70)
    print("[ANALYSIS COMPLETE]")
    print("="*70)
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())

