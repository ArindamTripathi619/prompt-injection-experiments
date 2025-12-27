#!/usr/bin/env python3
"""
Comprehensive statistical analysis of all experiment results.
Analyzes the merged experiments.db and generates statistical reports.
"""

import sqlite3
import json
from collections import defaultdict
from src.statistical_analysis import (
    wilson_score_interval,
    mcnemar_test_from_results,
    cohen_h,
    absolute_risk_reduction,
    relative_risk_reduction,
    interpret_cohen_h,
    format_ci_string
)


def load_experiment_data(db_path="experiments.db"):
    """Load all experiment data from merged database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Load all execution traces
    cursor.execute("""
        SELECT 
            experiment_id,
            configuration,
            attack_successful,
            attack_label,
            blocked_at_layer
        FROM execution_traces
    """)
    
    traces = []
    for row in cursor.fetchall():
        exp_id, config_str, attack_success, attack_label, blocked_layer = row
        config = json.loads(config_str)
        traces.append({
            'experiment_id': exp_id,
            'config': config,
            'attack_successful': bool(attack_success),
            'attack_label': attack_label,
            'blocked_at_layer': blocked_layer
        })
    
    conn.close()
    return traces


def classify_experiment(exp_id):
    """Classify experiment by ID."""
    if 'exp1' in exp_id:
        return 'Experiment 1: Baseline'
    elif 'exp2' in exp_id:
        return 'Experiment 2: Progressive Layers'
    elif 'exp3' in exp_id:
        return 'Experiment 3: Individual Layers'
    elif 'exp4' in exp_id:
        return 'Experiment 4: Layer Ablation'
    return 'Unknown'


def extract_config_name(exp_id):
    """Extract configuration name from experiment ID."""
    parts = exp_id.split('_')
    for i, part in enumerate(parts):
        if part.startswith('Config'):
            return '_'.join(parts[i:i+2])
    return 'Unknown'


def analyze_by_experiment():
    """Analyze results grouped by experiment."""
    print("=" * 80)
    print("STATISTICAL ANALYSIS - ALL EXPERIMENTS")
    print("=" * 80)
    
    traces = load_experiment_data()
    
    # Group by experiment
    by_experiment = defaultdict(list)
    for trace in traces:
        exp_type = classify_experiment(trace['experiment_id'])
        by_experiment[exp_type].append(trace)
    
    print(f"\nTotal traces analyzed: {len(traces)}")
    print(f"Experiments: {len(by_experiment)}")
    
    # Analyze each experiment
    for exp_name in sorted(by_experiment.keys()):
        exp_traces = by_experiment[exp_name]
        print(f"\n{'=' * 80}")
        print(f"{exp_name}")
        print(f"{'=' * 80}")
        print(f"Total traces: {len(exp_traces)}")
        
        # Group by configuration
        by_config = defaultdict(list)
        for trace in exp_traces:
            config_name = extract_config_name(trace['experiment_id'])
            by_config[config_name].append(trace)
        
        # Calculate ASR for each configuration
        print(f"\nConfigurations analyzed: {len(by_config)}")
        print(f"\n{'Configuration':<30} {'ASR':<12} {'95% CI':<20} {'n':<6}")
        print("-" * 80)
        
        config_results = []
        for config_name in sorted(by_config.keys()):
            config_traces = by_config[config_name]
            successes = sum(1 for t in config_traces if t['attack_successful'])
            total = len(config_traces)
            asr = successes / total if total > 0 else 0
            ci = wilson_score_interval(successes, total)
            
            print(f"{config_name:<30} {asr:>6.1%}     {format_ci_string(ci):<20} {total:<6}")
            config_results.append({
                'name': config_name,
                'asr': asr,
                'ci': ci,
                'successes': successes,
                'total': total,
                'traces': config_traces
            })
        
        # Statistical comparisons
        if len(config_results) >= 2:
            print(f"\n{'=' * 80}")
            print("STATISTICAL COMPARISONS")
            print(f"{'=' * 80}")
            
            # Compare first config (usually no defense) with others
            baseline = config_results[0]
            print(f"\nBaseline: {baseline['name']} (ASR = {baseline['asr']:.1%})")
            print(f"\nComparisons vs Baseline:")
            print(f"{'Configuration':<30} {'McNemar p':<12} {'Cohen h':<10} {'ARR':<10} {'Effect':<15}")
            print("-" * 80)
            
            for config in config_results[1:]:
                # McNemar test - match by user_input (prompt) across configurations
                baseline_dict = {}
                for t in baseline['traces']:
                    user_input = t['config'].get('user_input', '')
                    if user_input not in baseline_dict:
                        baseline_dict[user_input] = []
                    baseline_dict[user_input].append(t['attack_successful'])
                
                config_dict = {}
                for t in config['traces']:
                    user_input = t['config'].get('user_input', '')
                    if user_input not in config_dict:
                        config_dict[user_input] = []
                    config_dict[user_input].append(t['attack_successful'])
                
                # Get common prompts and aggregate results
                common_prompts = set(baseline_dict.keys()) & set(config_dict.keys())
                if len(common_prompts) > 0:
                    # For each prompt, take majority vote or first result
                    matched_baseline = []
                    matched_config = []
                    for prompt in sorted(common_prompts):
                        # Use first trial result for each prompt
                        matched_baseline.append(baseline_dict[prompt][0])
                        matched_config.append(config_dict[prompt][0])
                    
                    if len(matched_baseline) > 1:  # Need at least 2 pairs for McNemar
                        mcnemar_result = mcnemar_test_from_results(matched_baseline, matched_config)
                        h = cohen_h(baseline['asr'], config['asr'])
                        arr = absolute_risk_reduction(baseline['asr'], config['asr'])
                        
                        sig_mark = "***" if mcnemar_result.p_value < 0.001 else "**" if mcnemar_result.p_value < 0.01 else "*" if mcnemar_result.p_value < 0.05 else ""
                        
                        print(f"{config['name']:<30} {mcnemar_result.p_value:<8.4f}{sig_mark:<4} {h:<10.2f} {arr:<10.1%} {interpret_cohen_h(h):<15}")


def analyze_overall_summary():
    """Generate overall summary statistics."""
    print(f"\n{'=' * 80}")
    print("OVERALL SUMMARY STATISTICS")
    print(f"{'=' * 80}")
    
    traces = load_experiment_data()
    
    total_traces = len(traces)
    total_successes = sum(1 for t in traces if t['attack_successful'])
    total_blocked = total_traces - total_successes
    overall_asr = total_successes / total_traces if total_traces > 0 else 0
    overall_ci = wilson_score_interval(total_successes, total_traces)
    
    print(f"\nTotal Execution Traces: {total_traces:,}")
    print(f"Attacks Successful: {total_successes:,} ({total_successes/total_traces:.1%})")
    print(f"Attacks Blocked: {total_blocked:,} ({total_blocked/total_traces:.1%})")
    print(f"Overall ASR: {overall_asr:.1%}")
    print(f"95% CI: {format_ci_string(overall_ci)}")
    
    # By experiment type
    by_experiment = defaultdict(list)
    for trace in traces:
        exp_type = classify_experiment(trace['experiment_id'])
        by_experiment[exp_type].append(trace)
    
    print(f"\n{'Experiment':<40} {'Traces':<10} {'ASR':<10} {'95% CI':<20}")
    print("-" * 80)
    
    for exp_name in sorted(by_experiment.keys()):
        exp_traces = by_experiment[exp_name]
        successes = sum(1 for t in exp_traces if t['attack_successful'])
        total = len(exp_traces)
        asr = successes / total if total > 0 else 0
        ci = wilson_score_interval(successes, total)
        print(f"{exp_name:<40} {total:<10} {asr:<10.1%} {format_ci_string(ci):<20}")


def main():
    """Run full statistical analysis."""
    print("\n" + "=" * 80)
    print(" " * 20 + "EXPERIMENT RESULTS ANALYSIS")
    print("=" * 80)
    print(f"\nAnalyzing: experiments.db")
    print(f"Date: December 26, 2025")
    
    # Overall summary
    analyze_overall_summary()
    
    # Detailed by-experiment analysis
    print("\n\n")
    analyze_by_experiment()
    
    # Analysis notes
    print(f"\n{'=' * 80}")
    print("STATISTICAL NOTES")
    print(f"{'=' * 80}")
    print("\nSignificance levels:")
    print("  *** p < 0.001 (highly significant)")
    print("  **  p < 0.01  (very significant)")
    print("  *   p < 0.05  (significant)")
    print("\nEffect size interpretation (Cohen's h):")
    print("  < 0.2  : negligible")
    print("  0.2-0.5: small")
    print("  0.5-0.8: medium")
    print("  > 0.8  : large")
    print("\nConfidence intervals: Wilson score method (recommended for proportions)")
    print("Statistical test: McNemar's test (for paired binary outcomes)")
    
    print(f"\n{'=' * 80}")
    print("ANALYSIS COMPLETE")
    print(f"{'=' * 80}\n")


if __name__ == "__main__":
    main()
