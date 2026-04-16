#!/usr/bin/env python3
"""
Regenerate Dashboard with Latest Data
======================================

Génère docs/index.html avec les données du CSV à jour.

Usage:
    python scripts/web/regenerate_dashboard.py
"""

import json
from pathlib import Path
import pandas as pd
import numpy as np


def generate_dashboard(csv_path: Path, output_path: Path):
    """
    Génère le fichier HTML du dashboard avec les données du CSV.
    """
    print(f"[*] Chargement des donnees depuis: {csv_path}")
    df = pd.read_csv(csv_path)
    
    # Ajouter jitter pour visualisation
    np.random.seed(42)
    df['temperature_K_jitter'] = df['temperature_K'] + np.random.uniform(-1, 1, len(df))
    df['contrast_normalized_jitter'] = df['contrast_normalized'] + np.random.uniform(-0.2, 0.2, len(df))
    
    # Calculer tailles de points proportionnelles au contraste
    df['point_size'] = 3 + (df['contrast_normalized'] / df['contrast_normalized'].max()) * 4
    df['opacity'] = 0.6
    
    # Convertir en JSON (gérer les NaN)
    data_dict = df.replace({np.nan: None}).to_dict('records')
    data_json = json.dumps(data_dict, indent=0)
    
    html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Biological Qubits Atlas — Dashboard v2.2.2</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }}
        
        header {{
            background: rgba(255,255,255,0.95);
            padding: 2rem;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            font-size: 2.5rem;
            color: #2d3748;
            margin-bottom: 0.5rem;
        }}
        
        .subtitle {{
            font-size: 1.1rem;
            color: #718096;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 2rem auto;
            padding: 0 2rem;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-bottom: 3rem;
        }}
        
        .stat-card {{
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.2s;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        
        .stat-value {{
            font-size: 2.5rem;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 0.5rem;
        }}
        
        .stat-label {{
            font-size: 0.9rem;
            color: #718096;
            text-transform: uppercase;
        }}
        
        .viz-container {{
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }}
        
        .viz-title {{
            font-size: 1.5rem;
            color: #2d3748;
            margin-bottom: 1.5rem;
        }}
        
        .tooltip {{
            position: absolute;
            background: rgba(0,0,0,0.9);
            color: white;
            padding: 0.75rem;
            border-radius: 6px;
            font-size: 0.85rem;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.2s;
            z-index: 1000;
        }}
        
        .axis text {{
            font-size: 12px;
            fill: #4a5568;
        }}
        
        .axis line, .axis path {{
            stroke: #cbd5e0;
        }}
        
        circle.data-point {{
            cursor: pointer;
            transition: all 0.2s;
        }}
        
        circle.data-point:hover {{
            stroke: #667eea;
            stroke-width: 3px;
        }}
        
        .legend-item {{
            cursor: pointer;
            opacity: 1;
            transition: opacity 0.2s;
        }}
        
        .legend-item.dimmed {{
            opacity: 0.3;
        }}
    </style>
</head>
<body>
    <header>
        <h1>⚛️ Biological Qubits Atlas</h1>
        <p class="subtitle">Interactive Dashboard v2.2.2 — {len(df)} Systems</p>
    </header>
    
    <div class="container">
        <div class="stats-grid" id="stats"></div>
        
        <div class="viz-container">
            <h2 class="viz-title">📊 Contrast vs Temperature</h2>
            <div id="scatter-contrast-temp"></div>
        </div>
        
        <div class="viz-container">
            <h2 class="viz-title">🧬 Systems by Family</h2>
            <div id="bar-families"></div>
        </div>
    </div>
    
    <div class="tooltip" id="tooltip"></div>
    
    <script>
        const rawData = {data_json};
        const data = rawData.filter(d => d.temperature_K && d.contrast_normalized);
        
        // === STATISTIQUES ===
        const stats = [
            {{ label: "Total Systems", value: rawData.length }},
            {{ label: "Biosensors", value: data.filter(d => d.is_biosensor === 1.0).length }},
            {{ label: "Families", value: new Set(rawData.map(d => d.family).filter(f => f)).size }},
            {{ label: "In Vivo", value: rawData.filter(d => d.context && d.context.includes('vivo')).length }}
        ];
        
        d3.select("#stats")
            .selectAll(".stat-card")
            .data(stats)
            .join("div")
            .attr("class", "stat-card")
            .html(d => `<div class="stat-value">${{d.value}}</div><div class="stat-label">${{d.label}}</div>`);
        
        // === SCATTER PLOT ===
        const margin = {{ top: 20, right: 150, bottom: 60, left: 70 }};
        const width = 1200;
        const height = 500;
        
        const svg = d3.select("#scatter-contrast-temp")
            .append("svg")
            .attr("width", width)
            .attr("height", height);
        
        const xScale = d3.scaleLinear()
            .domain([d3.min(data, d => d.temperature_K) - 5, d3.max(data, d => d.temperature_K) + 5])
            .range([margin.left, width - margin.right]);
        
        const yScale = d3.scaleLog()
            .domain([0.5, d3.max(data, d => d.contrast_normalized) * 1.2])
            .range([height - margin.bottom, margin.top]);
        
        const colorScale = d3.scaleOrdinal(d3.schemeCategory10)
            .domain([...new Set(data.map(d => d.family))]);
        
        svg.append("g")
            .attr("transform", `translate(0,${{height - margin.bottom}})`)
            .call(d3.axisBottom(xScale))
            .attr("class", "axis")
            .append("text")
            .attr("x", width / 2)
            .attr("y", 45)
            .attr("fill", "#2d3748")
            .style("font-size", "14px")
            .style("font-weight", "bold")
            .text("Temperature (K)");
        
        svg.append("g")
            .attr("transform", `translate(${{margin.left}},0)`)
            .call(d3.axisLeft(yScale))
            .attr("class", "axis")
            .append("text")
            .attr("transform", "rotate(-90)")
            .attr("x", -height / 2)
            .attr("y", -55)
            .attr("fill", "#2d3748")
            .style("font-size", "14px")
            .style("font-weight", "bold")
            .text("Contrast (normalized, fold)");
        
        const tooltip = d3.select("#tooltip");
        
        svg.selectAll("circle")
            .data(data)
            .join("circle")
            .attr("class", "data-point")
            .attr("cx", d => xScale(d.temperature_K_jitter || d.temperature_K))
            .attr("cy", d => yScale(d.contrast_normalized_jitter || d.contrast_normalized))
            .attr("r", d => d.point_size || 5)
            .attr("fill", d => colorScale(d.family))
            .attr("opacity", d => d.opacity || 0.6)
            .on("mouseover", function(event, d) {{
                d3.select(this)
                    .transition()
                    .duration(200)
                    .attr("r", 10)
                    .attr("opacity", 1);
                
                tooltip
                    .style("opacity", 1)
                    .style("left", (event.pageX + 10) + "px")
                    .style("top", (event.pageY - 10) + "px")
                    .html(`
                        <strong>${{d.protein_name || 'Unknown'}}</strong><br>
                        Family: ${{d.family}}<br>
                        Contrast: ${{d.contrast_normalized.toFixed(2)}} fold<br>
                        Temp: ${{d.temperature_K}} K<br>
                        DOI: ${{d.doi || 'N/A'}}
                    `);
            }})
            .on("mouseout", function() {{
                d3.select(this)
                    .transition()
                    .duration(200)
                    .attr("r", 5)
                    .attr("opacity", 0.6);
                
                tooltip.style("opacity", 0);
            }});
        
        // Légende
        const families = [...new Set(data.map(d => d.family))].sort();
        const legend = svg.append("g")
            .attr("transform", `translate(${{width - margin.right + 20}}, ${{margin.top}})`);
        
        legend.selectAll("g")
            .data(families)
            .join("g")
            .attr("class", "legend-item")
            .attr("transform", (d, i) => `translate(0, ${{i * 20}})`)
            .each(function(d) {{
                const g = d3.select(this);
                g.append("rect")
                    .attr("width", 12)
                    .attr("height", 12)
                    .attr("fill", colorScale(d));
                g.append("text")
                    .attr("x", 18)
                    .attr("y", 10)
                    .text(d)
                    .style("font-size", "11px")
                    .attr("fill", "#2d3748");
            }});
        
        // === BAR CHART ===
        const barData = d3.rollups(
            data,
            v => v.length,
            d => d.family
        ).map(([family, count]) => ({{ family, count }})).sort((a, b) => b.count - a.count);
        
        const barWidth = 1200;
        const barHeight = 400;
        const barMargin = {{ top: 20, right: 40, bottom: 80, left: 60 }};
        
        const barSvg = d3.select("#bar-families")
            .append("svg")
            .attr("width", barWidth)
            .attr("height", barHeight);
        
        const xBarScale = d3.scaleBand()
            .domain(barData.map(d => d.family))
            .range([barMargin.left, barWidth - barMargin.right])
            .padding(0.2);
        
        const yBarScale = d3.scaleLinear()
            .domain([0, d3.max(barData, d => d.count)])
            .range([barHeight - barMargin.bottom, barMargin.top]);
        
        barSvg.append("g")
            .attr("transform", `translate(0,${{barHeight - barMargin.bottom}})`)
            .call(d3.axisBottom(xBarScale))
            .selectAll("text")
            .attr("transform", "rotate(-45)")
            .style("text-anchor", "end");
        
        barSvg.append("g")
            .attr("transform", `translate(${{barMargin.left}},0)`)
            .call(d3.axisLeft(yBarScale));
        
        barSvg.selectAll("rect")
            .data(barData)
            .join("rect")
            .attr("x", d => xBarScale(d.family))
            .attr("y", d => yBarScale(d.count))
            .attr("width", xBarScale.bandwidth())
            .attr("height", d => barHeight - barMargin.bottom - yBarScale(d.count))
            .attr("fill", d => colorScale(d.family))
            .attr("opacity", 0.8);
        
        barSvg.selectAll("text.bar-label")
            .data(barData)
            .join("text")
            .attr("class", "bar-label")
            .attr("x", d => xBarScale(d.family) + xBarScale.bandwidth() / 2)
            .attr("y", d => yBarScale(d.count) - 5)
            .attr("text-anchor", "middle")
            .text(d => d.count)
            .style("font-size", "12px")
            .style("font-weight", "bold")
            .attr("fill", "#2d3748");
    </script>
</body>
</html>
"""
    
    print(f"[*] Ecriture de {len(df)} systemes dans: {output_path}")
    output_path.write_text(html_content, encoding='utf-8')
    print(f"[OK] Dashboard genere avec succes!")
    print(f"     Pour visualiser: python -m http.server 8000")
    print(f"     Puis ouvrir: http://localhost:8000/docs/index.html")


def main():
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent.parent
    csv_path = repo_root / "data" / "processed" / "atlas_fp_optical_v2_2.csv"
    output_path = repo_root / "docs" / "index.html"
    
    if not csv_path.exists():
        print(f"[ERREUR] CSV introuvable: {csv_path}")
        return 1
    
    generate_dashboard(csv_path, output_path)
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())










