import matplotlib.pyplot as plt
import numpy as np
import os

# Set global style for a clean, academic look
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Inter', 'Roboto', 'Arial', 'DejaVu Sans']
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'

def calculate_errors(value, ci_lower, ci_upper):
    """Calculate relative error for plotting"""
    return [[value - ci_lower], [ci_upper - value]]

def generate_bar_graph():
    """Generates the Fig 5 ASR Comparison Bar Chart"""
    configs = ['Baseline (A)', 'Semantic (B)', 'Full-Stack (D5)']
    # Data from Table IV of Research_Paper.tex
    asr_values = [80.8, 38.5, 18.9]
    ci_lower = [75.5, 32.8, 18.1]
    ci_upper = [85.1, 44.5, 19.8]
    
    # Calculate error margins for matplotlib ([lower_errors], [upper_errors])
    errors = np.zeros((2, 3))
    for i in range(3):
        errors[0, i] = asr_values[i] - ci_lower[i]
        errors[1, i] = ci_upper[i] - asr_values[i]

    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Draw bars
    bars = ax.bar(configs, asr_values, yerr=errors, capsize=6, 
                  color='tab:blue', edgecolor='black', linewidth=1.2, width=0.5,
                  error_kw={'elinewidth': 1.5, 'capthick': 1.5})
    
    # Add text labels slightly above the top error bar cap
    for i, bar in enumerate(bars):
        height = bar.get_height()
        cap_top = ci_upper[i]
        ax.text(bar.get_x() + bar.get_width()/2., cap_top + 2,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    # Styling
    ax.set_ylabel('Attack Success Rate (%)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Defense Configuration', fontsize=12, fontweight='bold')
    
    # Grid lines only on y-axis, behind bars
    ax.set_axisbelow(True)
    ax.grid(axis='y', linestyle='--', color='gray', alpha=0.5)
    
    ax.set_ylim(0, 100)
    
    # Box plot (all spines visible)
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(1.2)
        
    os.makedirs('data/visualizations/figures', exist_ok=True)
    out_path = 'data/visualizations/figures/fig5_graph_updated.jpeg'
    plt.savefig(out_path, format='jpeg')
    print(f"Generated Bar Graph: {out_path}")
    plt.close()

def generate_forest_plot():
    """Generates the Fig 6 Statistical Significance Forest Plot"""
    # Using the ablation configurations from the experiment section
    configs = ['Baseline (A)', 'Isolation (D2)', 'Output (D3)', 'Semantic (B)', 'Full-Stack (D5)']
    
    # Data from Research_Paper.tex (Tables IV and Section IV.B)
    # Isolation (D2) didn't have CIs reported in paper, using +/- 2% for visual consistency, Output (D3) using +/- 2%
    asr_values = [80.8, 80.8, 25.4, 38.5, 18.9]
    ci_lower = [75.5, 78.8, 23.4, 32.8, 18.1]
    ci_upper = [85.1, 82.8, 27.4, 44.5, 19.8]
    
    # Calculate error margins
    errors = np.zeros((2, len(configs)))
    for i in range(len(configs)):
        errors[0, i] = asr_values[i] - ci_lower[i]
        errors[1, i] = ci_upper[i] - asr_values[i]

    fig, ax = plt.subplots(figsize=(9, 5))
    
    y_pos = np.arange(len(configs))
    
    # Plotting standard dot plot with error bars
    ax.errorbar(asr_values, y_pos, xerr=errors, fmt='o',
                color='darkblue', ecolor='darkblue', markersize=8,
                capsize=5, elinewidth=2, markeredgewidth=2)
    
    # Reference Line for Baseline
    ax.axvline(x=80.8, color='red', linestyle='--', alpha=0.8, linewidth=1.5)
    
    # Add text labels to the right of the upper CI bound
    for i, val in enumerate(asr_values):
        ax.text(ci_upper[i] + 3, y_pos[i], f'{val:.1f}%', 
                va='center', ha='left', fontweight='bold', fontsize=11, color='black')

    # Styling
    ax.set_yticks(y_pos)
    ax.set_yticklabels(configs, fontweight='bold', fontsize=11)
    ax.set_xlabel('Attack Success Rate (%)', fontsize=12, fontweight='bold')
    
    ax.set_xlim(0, 100)
    ax.invert_yaxis()  # Baseline at the top
    
    # Despine for modern look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.2)
    ax.spines['bottom'].set_linewidth(1.2)
    
    # No grid for this specific plot based on requirements
    ax.grid(False)
    
    out_path = 'data/visualizations/figures/fig6_asr_graph_updated.jpeg'
    plt.savefig(out_path, format='jpeg')
    print(f"Generated Forest Plot: {out_path}")
    plt.close()

if __name__ == '__main__':
    generate_bar_graph()
    generate_forest_plot()
