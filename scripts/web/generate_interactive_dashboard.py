#!/usr/bin/env python3
"""
Génère dashboard HTML/D3.js avec visualisations interactives
Licence: MIT
"""

import pandas as pd
import json
import os
import numpy as np

def generate_dashboard_html(atlas_csv: str, output_html: str = "index_v2_interactive.html"):
    """
    Génère dashboard interactif avec D3.js
    
    Visualisations incluses:
    1. Scatter plot T2 vs Température (interactif)
    2. Barplot familles (trié par médiane T2)
    3. Timeline publications
    4. Statistiques en temps réel
    """
    
    df = pd.read_csv(atlas_csv)
    
    # PATCH 1 : Filtrage données aberrantes (avant génération JSON)
    df_clean = df[
        (df['temperature_K'] > 270) & (df['temperature_K'] < 320) &  # Biologique uniquement
        (df['contrast_normalized'].notna()) &
        (df['contrast_normalized'] > 0)
    ].copy()
    
    print(f"[FILTER] {len(df)} -> {len(df_clean)} systemes (aberrants exclus)")
    
    # PATCH 2 : Jitter coordonnées (éviter superposition exacte)
    np.random.seed(42)
    df_clean['temperature_K_jitter'] = df_clean['temperature_K'] + np.random.uniform(-1, 1, len(df_clean))
    df_clean['contrast_normalized_jitter'] = df_clean['contrast_normalized'] * (1 + np.random.uniform(-0.02, 0.02, len(df_clean)))
    
    # PATCH 3 : Taille conditionnelle (importance = contraste élevé)
    df_clean['point_size'] = df_clean['contrast_normalized'].clip(0.01, 100).apply(lambda x: 4 + np.log10(max(x, 0.01)) * 1.5)
    
    # PATCH 4 : Opacité adaptative (simple version)
    df_clean['opacity'] = 0.6  # Base opacity
    
    # PATCH 5 : Sauvegarder JSON propre
    os.makedirs('docs/data', exist_ok=True)
    df_clean.to_json('docs/data/plot_v2_clean.json', orient='records', indent=2)
    
    # Utiliser données filtrées pour le dashboard
    data_json = df_clean.to_json(orient='records')
    
    html_template = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Biological Qubits Atlas — Dashboard v2.0</title>
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
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }}
        
        .stat-value {{
            font-size: 2.5rem;
            font-weight: bold;
            color: #667eea;
        }}
        
        .stat-label {{
            font-size: 0.9rem;
            color: #718096;
            margin-top: 0.5rem;
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
            margin-bottom: 1rem;
            border-left: 4px solid #667eea;
            padding-left: 1rem;
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
        <p class="subtitle">Interactive Dashboard v2.0 — Quantum Systems Visualization</p>
    </header>
    
    <div class="container">
        <div class="stats-grid" id="stats"></div>
        
        <div class="viz-container">
            <h2 class="viz-title">📊 T2 Coherence vs Temperature</h2>
            <div id="scatter-t2-temp"></div>
        </div>
        
        <div class="viz-container">
            <h2 class="viz-title">🧬 Systems by Family</h2>
            <div id="bar-families"></div>
        </div>
    </div>
    
    <div class="tooltip" id="tooltip"></div>
    
    <script>
        const rawData = {data_json};
        const data = rawData; // Tous les systèmes (pas de filtre température)
        
        // === STATISTIQUES ===
        const stats = [
            {{ label: "Total Systems", value: rawData.length }},
            {{ label: "With T2 Data", value: data.filter(d => d.t2_us).length }},
            {{ label: "Families", value: new Set(rawData.map(d => d.family)).size }},
            {{ label: "In Vivo", value: rawData.filter(d => d.context && d.context.includes('vivo')).length }}
        ];
        
        d3.select("#stats")
            .selectAll(".stat-card")
            .data(stats)
            .join("div")
            .attr("class", "stat-card")
            .html(d => `
                <div class="stat-value">${{d.value}}</div>
                <div class="stat-label">${{d.label}}</div>
            `);
        
        // === SCATTER PLOT ===
        const width = 1200;
        const height = 600;
        const margin = {{ top: 40, right: 180, bottom: 60, left: 80 }};
        
        const scatterData = data.filter(d => d.contrast_normalized);
        
        const svg = d3.select("#scatter-t2-temp")
            .append("svg")
            .attr("width", width)
            .attr("height", height);
        
        const xScale = d3.scaleLinear()
            .domain([270, d3.max(scatterData, d => d.temperature_K) + 10])
            .range([margin.left, width - margin.right]);
        
        const yScale = d3.scaleLinear()
            .domain([0, d3.max(scatterData, d => d.contrast_normalized) * 1.1])
            .range([height - margin.bottom, margin.top]);
        
        const colorScale = d3.scaleOrdinal(d3.schemeCategory10);
        
        // Axes
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
            .text("Contrast (normalized)");
        
        const tooltip = d3.select("#tooltip");
        
        // Points (avec jitter, taille et opacité personnalisées)
        svg.selectAll("circle")
            .data(scatterData)
            .join("circle")
            .attr("class", "data-point")
            .attr("cx", d => xScale(d.temperature_K_jitter || d.temperature_K))
            .attr("cy", d => yScale(d.contrast_normalized_jitter || d.contrast_normalized))
            .attr("r", d => d.point_size || 6)
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
                        Contrast: ${{(d.contrast_normalized * 100).toFixed(1)}}%<br>
                        Temp: ${{d.temperature_K}} K<br>
                        DOI: ${{d.doi || 'N/A'}}
                    `);
            }})
            .on("mouseout", function() {{
                d3.select(this)
                    .transition()
                    .duration(200)
                    .attr("r", 6)
                    .attr("opacity", 0.7);
                
                tooltip.style("opacity", 0);
            }});
        
        // Légende
        const families = Array.from(new Set(scatterData.map(d => d.family)));
        const legend = svg.append("g")
            .attr("transform", `translate(${{width - margin.right + 20}}, ${{margin.top}})`);
        
        const legendItems = legend.selectAll("g")
            .data(families)
            .join("g")
            .attr("class", "legend-item")
            .attr("transform", (d, i) => `translate(0, ${{i * 25}})`)
            .style("cursor", "pointer")
            .on("click", function(event, family) {{
                const isActive = !d3.select(this).classed("dimmed");
                
                svg.selectAll("circle")
                    .transition()
                    .duration(300)
                    .attr("opacity", d => {{
                        if (isActive && d.family === family) return 0.1;
                        if (!isActive && d.family === family) return 0.7;
                        return d3.select(`circle[data-family="${{d.family}}"]`).attr("opacity");
                    }});
                
                d3.select(this).classed("dimmed", isActive);
            }});
        
        legendItems.append("rect")
            .attr("width", 15)
            .attr("height", 15)
            .attr("fill", d => colorScale(d));
        
        legendItems.append("text")
            .attr("x", 20)
            .attr("y", 12)
            .text(d => d)
            .style("font-size", "12px")
            .attr("fill", "#2d3748");
        
        // === BAR CHART FAMILLES ===
        const barData = d3.rollup(
            scatterData,
            v => v.length,
            d => d.family
        );
        
        const barDataArray = Array.from(barData, ([family, count]) => ({{family, count}}))
            .sort((a, b) => b.count - a.count);
        
        const barWidth = 1200;
        const barHeight = 400;
        const barMargin = {{ top: 20, right: 40, bottom: 80, left: 60 }};
        
        const barSvg = d3.select("#bar-families")
            .append("svg")
            .attr("width", barWidth)
            .attr("height", barHeight);
        
        const xBarScale = d3.scaleBand()
            .domain(barDataArray.map(d => d.family))
            .range([barMargin.left, barWidth - barMargin.right])
            .padding(0.2);
        
        const yBarScale = d3.scaleLinear()
            .domain([0, d3.max(barDataArray, d => d.count)])
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
            .data(barDataArray)
            .join("rect")
            .attr("x", d => xBarScale(d.family))
            .attr("y", d => yBarScale(d.count))
            .attr("width", xBarScale.bandwidth())
            .attr("height", d => barHeight - barMargin.bottom - yBarScale(d.count))
            .attr("fill", d => colorScale(d.family))
            .attr("opacity", 0.8)
            .on("mouseover", function(event, d) {{
                d3.select(this).attr("opacity", 1);
                tooltip
                    .style("opacity", 1)
                    .style("left", (event.pageX + 10) + "px")
                    .style("top", (event.pageY - 10) + "px")
                    .html(`
                        <strong>${{d.family}}</strong><br>
                        Count: ${{d.count}} systems
                    `);
            }})
            .on("mouseout", function() {{
                d3.select(this).attr("opacity", 0.8);
                tooltip.style("opacity", 0);
            }});
    </script>
</body>
</html>
"""
    
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"[OK] Dashboard genere: {output_html}")
    print(f"[INFO] Ouvrir dans navigateur pour visualiser")
    print(f"[INFO] {len(df)} systemes inclus dans les visualisations")

if __name__ == "__main__":
    # Utiliser version v2.0 (mise à jour)
    atlas_path = "data/processed/atlas_fp_optical_v2_0.csv"
    
    if os.path.exists(atlas_path):
        generate_dashboard_html(atlas_path)
    else:
        print(f"[WARN] Fichier non trouve: {atlas_path}")
        print("   Utiliser le bon chemin vers votre atlas CSV")


