#!/usr/bin/env python3
"""
Create visualizations for the prompt injection defense research paper.
Updated with refinements for clarity, accuracy, and aesthetics.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path

# Set global style for professional look
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'

def create_architecture_diagram():
    """Create the architecture diagram showing the multi-layer defense system."""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Set up the plot
    ax.set_xlim(0, 12)  # Expanded width for side annotations
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Define layer positions
    layer_y_positions = [6.5, 5.5, 4.5, 3.5, 2.5]  # y positions for each layer
    layer_names = [
        "Layer 1: Boundary Layer",
        "Layer 2: Semantic Layer", 
        "Layer 3: Context Isolation",
        "Layer 4: LLM Interaction",
        "Layer 5: Output Validation"
    ]
    
    # Professional color palette (pastel/soft)
    colors = ['#FFCBCB', '#CCE5FF', '#D5F5E3', '#FDEBD0', '#E8DAEF']
    border_color = '#333333'
    
    # Draw each layer as a rectangle
    for i, (y_pos, name, color) in enumerate(zip(layer_y_positions, layer_names, colors)):
        rect = plt.Rectangle((1.5, y_pos-0.35), 8, 0.7, 
                           facecolor=color, edgecolor=border_color, linewidth=1.5, zorder=2)
        ax.add_patch(rect)
        
        # Add layer name
        ax.text(5.5, y_pos, name, ha='center', va='center', 
                fontsize=11, fontweight='bold', color='#1a1a1a', zorder=3)
        
        # Add description
        descriptions = [
            "Input validation and normalization",
            "Attack pattern detection via similarity", 
            "Secure prompt isolation & role separation",
            "Enhanced LLM safety controls",
            "Content filtering & verification"
        ]
        ax.text(5.5, y_pos-0.2, descriptions[i], ha='center', va='top', 
                fontsize=8, style='italic', color='#444444', zorder=3)
    
    # Draw input arrow
    ax.annotate('User Requests', xy=(0.5, 7), xytext=(0.5, 7.5),
                fontsize=10, ha='center', va='center', fontweight='bold')
    ax.annotate('', xy=(5.5, 7.0), xytext=(0.5, 7.2),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='#444444', connectionstyle="angle,angleA=0,angleB=90,rad=10"))

    # Connecting arrows between layers (straight down)
    for i in range(len(layer_y_positions) - 1):
        y1 = layer_y_positions[i] - 0.35
        y2 = layer_y_positions[i+1] + 0.35
        # Main flow
        ax.annotate('', xy=(5.5, y2), xytext=(5.5, y1),
                    arrowprops=dict(arrowstyle='->', lw=1.2, color='#555555'))
    
    # Draw Output Arrow
    ax.annotate('', xy=(10.5, 2.5), xytext=(9.5, 2.5),
                 arrowprops=dict(arrowstyle='->', lw=1.5, color='#444444'))
    ax.text(10.6, 2.5, 'Processed\nResponse', ha='left', va='center', fontsize=10, fontweight='bold')

    # Draw Layer 6: Coordination
    coord_rect = plt.Rectangle((1, 0.8), 9, 0.8, 
                              facecolor='#FFF59D', edgecolor=border_color, linewidth=1.5, linestyle='--', zorder=2)
    ax.add_patch(coord_rect)
    ax.text(5.5, 1.3, 'Layer 6: Feedback Coordination', 
            ha='center', va='center', fontsize=11, fontweight='bold', zorder=3)
    ax.text(5.5, 1.05, 'Inter-layer communication & offline adaptation', 
            ha='center', va='center', fontsize=9, style='italic', zorder=3)
    
    # Feedback arrows (side arrows)
    # Reducing noise: just show abstract flow
    for y_pos in layer_y_positions:
        # From layers to coordination (left side)
        ax.annotate('', xy=(1.0, 1.2), xytext=(1.5, y_pos),
                    arrowprops=dict(arrowstyle='->', lw=0.8, color='#AAAAAA', linestyle=':', connectionstyle="arc3,rad=-0.2"))

    # Adaptive Elements Box (Right side, spanning L2-L6)
    # Covering roughly y=1.0 to y=5.8
    bbox_props = dict(boxstyle="round,pad=0.5", facecolor="#E9F7EF", edgecolor="#2ECC71", alpha=0.9, linewidth=1.5)
    ax.text(10.2, 3.8, 'Adaptive Elements\n(L2-L4, L6)', 
            ha='center', va='center', fontsize=10, fontweight='bold', color='#145A32', bbox=bbox_props, zorder=4)
    ax.text(10.2, 3.4, 'Dynamic thresholds\nRisk assessment', 
            ha='center', va='top', fontsize=8, color='#145A32', zorder=5)

    # Dashed lines connecting adaptive box to relevant layers (2, 3, 4, 6)
    relevant_layers_y = [5.5, 4.5, 3.5] # Layers 2, 3, 4
    for y in relevant_layers_y:
         ax.annotate('', xy=(9.5, y), xytext=(9.7, 3.8),
                    arrowprops=dict(arrowstyle='-', lw=1, color='#2ECC71', linestyle=':', alpha=0.6))

    # Title
    ax.text(6, 7.8, 'System-Level Workflow Model for Prompt Injection Mitigation', 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#222222')
    
    plt.tight_layout()
    plt.savefig('data/visualizations/architecture_diagram.png')
    print("Architecture diagram created: data/visualizations/architecture_diagram.png")
    plt.close()

def create_asr_comparison_chart():
    """Create the attack success rate comparison chart."""
    # Precise data from paper
    configurations = ['Baseline\n(No Defense)', 'Isolated\n(L1-L5)', 'Adaptive\nL3 Only', 'Adaptive\nL4 Only', 'Full\nAdaptive']
    asr_values = [80.77, 21.83, 20.12, 18.52, 18.67] 
    
    # 95% Confidence Intervals (margin of error)
    # Derived from Wilson score interval width for ~11k samples
    # Approximate width for 20% is ~0.7-0.8%, for 80% is ~0.7%
    # Using reasonably representative values for visual accuracy
    errors = [0.73, 0.76, 0.74, 0.72, 0.72] 
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.set_style("whitegrid")
    
    # Create bar plot
    colors = ['#CB4335', '#5DADE2', '#58D68D', '#F5B041', '#AF7AC5']
    bars = ax.bar(configurations, asr_values, 
                  yerr=errors, capsize=4, 
                  color=colors, width=0.65,
                  edgecolor='#333333', linewidth=1, zorder=3)
    
    # Add labels
    for bar, value in zip(bars, asr_values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1.2,
                f'{value:.2f}%', ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    # Styling
    ax.set_ylabel('Attack Success Rate (%)', fontsize=11, fontweight='bold')
    ax.set_xlabel('Configuration', fontsize=11, fontweight='bold')
    ax.set_title('Attack Success Rate Comparison Across Configurations\n(Lower is Better)', 
                 fontsize=14, fontweight='bold', pad=15)
    
    ax.grid(axis='y', alpha=0.3, zorder=0)
    ax.set_ylim(0, 90) # Give space for baseline
    
    # Remove top and right spines
    sns.despine()
    
    plt.tight_layout()
    plt.savefig('data/visualizations/asr_comparison_chart.png')
    print("ASR comparison chart created: data/visualizations/asr_comparison_chart.png")
    plt.close()

def create_bypass_mechanisms_viz():
    """Create the bypass mechanism analysis visualization (Pie + Bar)."""
    # Data
    mechanisms = ['Output Leakage', 'Semantic Detection\nBypass', 'LLM Constraint\nViolation']
    counts = [959, 400, 114]
    total_bypass = sum(counts)
    
    # Calculate percentages
    percentages = [c/total_bypass*100 for c in counts]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Distribution of 1,473 Bypass Mechanisms Detected Across 11,490 Traces', fontsize=14, fontweight='bold')
    
    # Pie Chart
    colors = ['#F1948A', '#85C1E9', '#F7DC6F']
    wedges, texts, autotexts = ax1.pie(counts, labels=None, 
                                        autopct='%1.1f%%', startangle=90,
                                        colors=colors, pctdistance=0.85,
                                        wedgeprops=dict(width=0.5, edgecolor='white'))
    
    # Improve pie labels
    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = f"angle,angleA=0,angleB={ang}"
        ax1.annotate(mechanisms[i], xy=(x, y), xytext=(1.2*np.sign(x), 1.2*y),
                    horizontalalignment=horizontalalignment,
                    arrowprops=dict(arrowstyle="-", color="gray"), fontsize=10, fontweight='bold')
                    
    ax1.set_title('Proportional Distribution', fontsize=12)

    # Bar Chart
    bars = ax2.bar([m.replace('\n', ' ') for m in mechanisms], counts, 
                   color=colors, edgecolor='black', linewidth=1, width=0.6)
    
    for bar, count, pct in zip(bars, counts, percentages):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 20,
                 f'{count}', ha='center', va='bottom', fontweight='bold', fontsize=11)
        ax2.text(bar.get_x() + bar.get_width()/2., height - 60,
                 f'({pct:.1f}%)', ha='center', va='top', fontsize=9, color='white', fontweight='bold')

    ax2.set_ylabel('Number of Occurrences', fontsize=11)
    ax2.set_title('Frequency Count', fontsize=12)
    ax2.grid(axis='y', alpha=0.3)
    sns.despine(ax=ax2)
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('data/visualizations/bypass_mechanisms.png')
    print("Bypass mechanisms viz created: data/visualizations/bypass_mechanisms.png")
    plt.close()

def create_layer_effectiveness_flow_qualitative():
    """Create a qualitative layer effectiveness flow (No numbers)."""
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_ylim(0, 5)
    ax.set_xlim(0, 11)
    ax.axis('off')
    
    layers = ['Request\nBoundary', 'Semantic\nAnalysis', 'Context\nIsolation', 'LLM\nInteraction', 'Output\nValidation']
    descs = ['Sanitization', 'Pattern Checks', 'Separation', 'Enforcement', 'Leakage Check']
    qualities = ['High\nEfficiency', 'Med/High\nPrecision', 'Systemic\nSafety', 'Semantic\nControls', 'Final\nSafeguard']
    
    # Colors matching architecture
    colors = ['#FFCBCB', '#CCE5FF', '#D5F5E3', '#FDEBD0', '#E8DAEF']
    
    # Draw blocks
    x_positions = np.linspace(1, 9, 5)
    
    for i, (x, name, desc, qual, color) in enumerate(zip(x_positions, layers, descs, qualities, colors)):
        # Box
        rect = mpatches.FancyBboxPatch((x-0.8, 2), 1.6, 1.2, 
                           facecolor=color, edgecolor='#444444', linewidth=1.5, boxstyle="round,pad=0.1")
        ax.add_patch(rect)
        
        # Text
        ax.text(x, 2.7, name, ha='center', va='center', fontsize=10, fontweight='bold')
        ax.text(x, 2.3, desc, ha='center', va='center', fontsize=8, style='italic')
        ax.text(x, 1.6, qual, ha='center', va='top', fontsize=9, fontweight='bold', color='#444444')

    # Arrows
    for i in range(len(x_positions)-1):
        x1 = x_positions[i] + 0.8
        x2 = x_positions[i+1] - 0.8
        ax.annotate('', xy=(x2, 2.6), xytext=(x1, 2.6),
                    arrowprops=dict(arrowstyle='->', lw=2, color='#555555'))
    
    # Input/Output
    ax.text(0, 2.6, 'User\nInput', ha='center', va='center', fontweight='bold')
    ax.annotate('', xy=(x_positions[0]-0.8, 2.6), xytext=(0.5, 2.6), arrowprops=dict(arrowstyle='->', lw=2))
    
    ax.text(10.8, 2.6, 'Safe\nOutput', ha='center', va='center', fontweight='bold')
    ax.annotate('', xy=(10.4, 2.6), xytext=(x_positions[-1]+0.8, 2.6), arrowprops=dict(arrowstyle='->', lw=2))

    # Title
    ax.text(5.5, 4.5, 'Qualitative Defense Effectiveness Flow', ha='center', va='center', fontsize=14, fontweight='bold')
    ax.text(5.5, 4.2, 'Risk reduction profile across defense layers', ha='center', va='center', fontsize=10, style='italic')
    
    plt.tight_layout()
    plt.savefig('data/visualizations/layer_effectiveness_flow.png')
    print("Layer effectiveness qualitative flow created: data/visualizations/layer_effectiveness_flow.png")
    plt.close()

def create_statistical_significance_forest():
    """Create the statistical significance visualization (Forest Plot)."""
    # Updated text to match strict paper numbers
    configs = ['Isolated', 'Adaptive L3', 'Adaptive L4', 'Full Adaptive']
    asr_values = [21.83, 20.12, 18.52, 18.67] # Precise
    
    # Calculate improvements relative to Isolated (21.83)
    baseline = 21.83
    improvements_abs = [baseline - val for val in asr_values[1:]]
    improvements_rel = [(baseline - val) / baseline * 100 for val in asr_values[1:]]
    
    # CIs (approximate symmetric for display)
    ci_err = 0.75 
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    y_pos = np.arange(len(configs))
    
    # Forest plot points
    ax.errorbar(asr_values, y_pos, xerr=ci_err, fmt='o', 
                markersize=8, capsize=5, color='#2874A6', ecolor='#2874A6', elinewidth=2)
    
    # Reference Line (Isolated Baseline)
    ax.axvline(x=21.83, color='#E74C3C', linestyle='--', alpha=0.6, label='Isolated Baseline (21.83%)')
    
    # Labels
    ax.set_yticks(y_pos)
    ax.set_yticklabels(configs, fontweight='bold', fontsize=11)
    ax.set_xlabel('Attack Success Rate (%)', fontweight='bold')
    ax.set_title('ASR Distribution with 95% Confidence Intervals', fontweight='bold', fontsize=14)
    ax.invert_yaxis() # Top-down
    
    # Add value annotations
    for i, (val, imp_rel) in enumerate(zip(asr_values, [0] + improvements_rel)):
        if i == 0:
            ax.text(val + 1, i, f'{val:.2f}%', va='center', fontweight='bold')
        else:
            ax.text(val + 1, i, f'{val:.2f}% (↓{imp_rel:.1f}%)', va='center', fontweight='bold', color='#196F3D')

    ax.set_xlim(16, 24)
    ax.grid(axis='x', alpha=0.3)
    ax.legend(loc='lower left')
    
    plt.tight_layout()
    plt.savefig('data/visualizations/statistical_significance_analysis.png')
    print("Statistical significance forest plot created: data/visualizations/statistical_significance_analysis.png")
    plt.close()

def create_attack_mitigated_flow():
    """Create the Attack Flow vs Mitigated Flow comparison diagram."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), height_ratios=[1, 1.2])
    
    # Common settings
    for ax in [ax1, ax2]:
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 4)
        ax.axis('off')
    
    # --- Top: Vulnerable Process ---
    ax1.set_title('Top: Vulnerable process susceptible to prompt injection', 
                 fontsize=14, fontweight='bold', pad=20, loc='left')
    
    # Nodes for vulnerable flow
    vuln_nodes = [
        (1.5, 'Malicious\nUser Input', '#E74C3C'), # Red
        (5.0, 'Application\n(No Validation)', '#F5B041'), # Orange
        (8.5, 'LLM\n(Direct Access)', '#E74C3C'), 
        (11.0, 'Executed\nAttack', '#922B21') # Dark Red
    ]
    
    # Draw nodes
    for x, text, color in vuln_nodes:
        # Use simple box for top flow
        box = mpatches.FancyBboxPatch((x-1.0, 1.5), 2.0, 1.0,
                                    facecolor=color, edgecolor='#333333',
                                    boxstyle="round,pad=0.1", alpha=0.3)
        ax1.add_patch(box)
        ax1.text(x, 2.0, text, ha='center', va='center', fontweight='bold', fontsize=10)

    # Arrows (Red)
    ax1.annotate('', xy=(3.8, 2.0), xytext=(2.7, 2.0), arrowprops=dict(arrowstyle='->', lw=2, color='#C0392B'))
    ax1.annotate('', xy=(7.3, 2.0), xytext=(6.2, 2.0), arrowprops=dict(arrowstyle='->', lw=2, color='#C0392B'))
    ax1.annotate('', xy=(10.8, 2.0), xytext=(9.7, 2.0), arrowprops=dict(arrowstyle='->', lw=2, color='#C0392B'))
    ax1.text(6, 3.2, "UNPROTECTED FLOW", ha='center', va='center', fontsize=12, fontweight='bold', color='#C0392B')


    # --- Bottom: Mitigated Flow ---
    ax2.set_title('Bottom: Mitigated flow with multi-layer defense', 
                 fontsize=14, fontweight='bold', pad=20, loc='left')
    
    # Defense Layers (Simplified horizontal view)
    layers = [
        (1.5, 'Layer 1:\nBoundary', '#CCE5FF'),
        (3.5, 'Layer 2:\nSemantic', '#D5F5E3'),
        (5.5, 'Layer 3:\nContext', '#FDEBD0'),
        (7.5, 'Layer 4:\nLLM', '#E8DAEF'),
        (9.5, 'Layer 5:\nOutput Validation', '#FFCBCB') # Combined label as requested
    ]
    
    # Draw logic
    
    # 1. User Input
    ax2.text(0.0, 2.0, 'User\nInput', ha='center', va='center', fontweight='bold')
    ax2.annotate('', xy=(0.8, 2.0), xytext=(0.2, 2.0), arrowprops=dict(arrowstyle='->', lw=1.5))

    # 2. Layers
    for x, text, color in layers:
        box = mpatches.FancyBboxPatch((x-0.8, 1.5), 1.6, 1.0,
                                    facecolor=color, edgecolor='#444444',
                                    boxstyle="round,pad=0.1", alpha=0.9)
        ax2.add_patch(box)
        ax2.text(x, 2.0, text, ha='center', va='center', fontsize=9, fontweight='bold')
        
        # Connectors
        if x < 9.5:
            ax2.annotate('', xy=(x+1.0, 2.0), xytext=(x+0.8, 2.0), arrowprops=dict(arrowstyle='->', lw=1.5, color='#444444'))

    # 3. Safe Output
    ax2.annotate('', xy=(11.5, 2.0), xytext=(10.5, 2.0), arrowprops=dict(arrowstyle='->', lw=1.5, color='#2ECC71'))
    ax2.text(11.8, 2.0, 'Safe\nOutput', ha='center', va='center', fontweight='bold', color='#145A32')
    
    # Layer 6 Coordination context (Background box)
    coord_box = mpatches.FancyBboxPatch((0.5, 0.5), 10.0, 3.0,
                                      facecolor='#FEF9E7', edgecolor='#F1C40F',
                                      boxstyle="round,pad=0.2", alpha=0.3, zorder=-1, linestyle='--')
    ax2.add_patch(coord_box)
    ax2.text(5.5, 0.3, 'Layer 6: Continuous Feedback & Coordination', ha='center', va='center', 
             fontsize=10, style='italic', color='#B7950B')

    plt.tight_layout()
    plt.savefig('data/visualizations/Attack Flow vs Mitigated Flow_generated.png')
    print("Attack vs Mitigated Flow diagram created: data/visualizations/Attack Flow vs Mitigated Flow_generated.png")
    plt.close()

def main():
    """Main function to create all visualizations."""
    viz_dir = Path('data/visualizations')
    viz_dir.mkdir(parents=True, exist_ok=True)
    
    print("Creating refined visualizations...")
    create_architecture_diagram()
    create_asr_comparison_chart()
    create_bypass_mechanisms_viz()
    create_layer_effectiveness_flow_qualitative()
    create_statistical_significance_forest()
    create_attack_mitigated_flow()
    print("All visualizations created.")

if __name__ == "__main__":
    main()
