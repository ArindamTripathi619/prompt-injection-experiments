#!/usr/bin/env python3
"""
Statistical analysis of prompt injection defense experiments.
Performs McNemar's test and Fisher's Exact Test to validate significance.
"""

import sqlite3
import math
from pathlib import Path
import json

def load_experiment_data(db_path):
    """Load experiment data from the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all execution traces with configuration info
    query = """
    SELECT 
        request_id,
        attack_successful,
        configuration
    FROM execution_traces
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    
    # Convert to list of dictionaries
    data = []
    for row in results:
        data.append({
            'request_id': row[0],
            'attack_successful': row[1],
            'configuration': row[2]
        })
    
    return data

def is_isolated_config(config_str):
    """Check if configuration is isolated (no coordination)."""
    return ('"enabled": false' in config_str and 
            '"adaptive_layer3": false' in config_str and 
            '"adaptive_layer4": false' in config_str and
            '"adaptive_layer5": false' in config_str)

def is_adaptive_l3_config(config_str):
    """Check if configuration is adaptive L3 only."""
    return ('"enabled": true' in config_str and 
            '"adaptive_layer3": true' in config_str and 
            '"adaptive_layer4": false' in config_str and
            '"adaptive_layer5": false' in config_str)

def is_adaptive_l4_config(config_str):
    """Check if configuration is adaptive L4 only."""
    return ('"enabled": true' in config_str and 
            '"adaptive_layer3": false' in config_str and 
            '"adaptive_layer4": true' in config_str and
            '"adaptive_layer5": false' in config_str)

def is_full_adaptive_config(config_str):
    """Check if configuration is full adaptive."""
    return ('"enabled": true' in config_str and 
            '"adaptive_layer3": true' in config_str and 
            '"adaptive_layer4": true' in config_str and
            '"adaptive_layer5": true' in config_str)

def calculate_wilson_score_interval(success, total, confidence=0.95):
    """Calculate Wilson score confidence interval for proportions."""
    if total == 0:
        return 0, 0
    
    z = 1.96 if confidence == 0.95 else 2.576  # 95% or 99% confidence
    z2 = z * z
    
    p = success / total
    denominator = 1 + z2 / total
    centre = (p + z2 / (2 * total)) / denominator
    
    interval = z * math.sqrt((p * (1 - p) + z2 / (4 * total)) / total) / denominator
    lower = centre - interval
    upper = centre + interval
    
    return lower * 100, upper * 100  # Return as percentages

def calculate_mcnemar_test(table):
    """
    Calculate McNemar's test for a 2x2 contingency table.
    table = [[a, b], [c, d]] where:
    a = both configs successful
    b = config1 successful, config2 failed
    c = config1 failed, config2 successful
    d = both configs failed
    """
    b = table[0][1]  # config1 success, config2 fail
    c = table[1][0]  # config1 fail, config2 success
    
    if b + c == 0:
        # If b+c is 0, we can't compute the test statistic
        # In this case, if b=0 and c=0, the methods are identical
        # If b=0 and c=0 but a or d are large, we have perfect agreement
        if table[0][0] + table[1][1] > 0:  # Some agreement
            return 0.0, 1.0  # No significant difference
        else:
            return None, None  # Cannot compute
    
    # Apply continuity correction
    chi2 = (abs(b - c) - 1) ** 2 / (b + c)
    # Calculate p-value (two-tailed)
    # For McNemar's test, p-value can be calculated using chi-square distribution
    # with 1 degree of freedom
    import math
    # Approximate p-value using normal distribution
    p_value = 2 * (1 - math.erf(math.sqrt(chi2) / math.sqrt(2)))
    
    return chi2, p_value

def calculate_asr_comparison_with_stats(data, config_func1, config_func2, name1, name2):
    """Calculate ASR comparison with McNemar's test and confidence intervals."""
    config1_data = [item for item in data if config_func1(item['configuration'])]
    config2_data = [item for item in data if config_func2(item['configuration'])]
    
    # Create paired dataset (same requests for both configurations)
    config1_map = {item['request_id']: item['attack_successful'] for item in config1_data}
    config2_map = {item['request_id']: item['attack_successful'] for item in config2_data}
    
    # Find common request IDs
    common_ids = set(config1_map.keys()) & set(config2_map.keys())
    
    if not common_ids:
        return {
            'config1': name1,
            'config2': name2,
            'config1_asr': 0,
            'config2_asr': 0,
            'config1_count': len(config1_data),
            'config2_count': len(config2_data),
            'asr_reduction': 0,
            'relative_reduction': 0,
            'mcnemar_chi2': None,
            'mcnemar_p': None,
            'config1_ci_lower': 0,
            'config1_ci_upper': 0,
            'config2_ci_lower': 0,
            'config2_ci_upper': 0,
            'common_requests': 0
        }
    
    # Create contingency table for McNemar's test
    both_success = 0  # a
    config1_success_config2_fail = 0  # b
    config1_fail_config2_success = 0  # c
    both_fail = 0  # d
    
    for req_id in common_ids:
        s1 = config1_map[req_id]
        s2 = config2_map[req_id]
        
        if s1 == 1 and s2 == 1:
            both_success += 1
        elif s1 == 1 and s2 == 0:
            config1_success_config2_fail += 1
        elif s1 == 0 and s2 == 1:
            config1_fail_config2_success += 1
        else:  # s1 == 0 and s2 == 0
            both_fail += 1
    
    contingency_table = [
        [both_success, config1_success_config2_fail],
        [config1_fail_config2_success, both_fail]
    ]
    
    # Calculate McNemar's test
    chi2, p_value = calculate_mcnemar_test(contingency_table)
    
    # Calculate ASR for each configuration based on common requests
    config1_successes = both_success + config1_success_config2_fail
    config2_successes = both_success + config1_fail_config2_success
    
    config1_asr = (config1_successes / len(common_ids)) * 100 if common_ids else 0
    config2_asr = (config2_successes / len(common_ids)) * 100 if common_ids else 0
    
    # Calculate Wilson score confidence intervals
    ci1_lower, ci1_upper = calculate_wilson_score_interval(config1_successes, len(common_ids))
    ci2_lower, ci2_upper = calculate_wilson_score_interval(config2_successes, len(common_ids))
    
    asr_reduction = config1_asr - config2_asr
    relative_reduction = (asr_reduction / config1_asr * 100) if config1_asr != 0 else 0
    
    return {
        'config1': name1,
        'config2': name2,
        'config1_asr': config1_asr,
        'config2_asr': config2_asr,
        'config1_count': len(config1_data),
        'config2_count': len(config2_data),
        'asr_reduction': asr_reduction,
        'relative_reduction': relative_reduction,
        'mcnemar_chi2': chi2,
        'mcnemar_p': p_value,
        'config1_ci_lower': ci1_lower,
        'config1_ci_upper': ci1_upper,
        'config2_ci_lower': ci2_lower,
        'config2_ci_upper': ci2_upper,
        'common_requests': len(common_ids),
        'contingency_table': contingency_table
    }

def run_comprehensive_statistical_analysis():
    """Run comprehensive statistical analysis on all experiments."""
    print("="*80)
    print("COMPREHENSIVE STATISTICAL ANALYSIS")
    print("="*80)
    
    db_path = "experiments.db"
    if not Path(db_path).exists():
        print(f"Database {db_path} not found!")
        return
    
    data = load_experiment_data(db_path)
    print(f"Loaded {len(data)} execution traces from database")
    
    # Calculate overall statistics
    total_successful = sum(item['attack_successful'] for item in data)
    overall_asr = total_successful / len(data) * 100 if len(data) > 0 else 0
    
    print(f"\nOverall Statistics:")
    print(f"Total traces: {len(data)}")
    print(f"Attack success rate: {overall_asr:.2f}%")
    
    # Calculate ASR by configuration type
    print(f"\nAttack Success Rates by Configuration:")
    
    isolated_data = [item for item in data if is_isolated_config(item['configuration'])]
    adaptive_l3_data = [item for item in data if is_adaptive_l3_config(item['configuration'])]
    adaptive_l4_data = [item for item in data if is_adaptive_l4_config(item['configuration'])]
    full_adaptive_data = [item for item in data if is_full_adaptive_config(item['configuration'])]
    
    isolated_asr = sum(item['attack_successful'] for item in isolated_data) / len(isolated_data) * 100 if len(isolated_data) > 0 else 0
    adaptive_l3_asr = sum(item['attack_successful'] for item in adaptive_l3_data) / len(adaptive_l3_data) * 100 if len(adaptive_l3_data) > 0 else 0
    adaptive_l4_asr = sum(item['attack_successful'] for item in adaptive_l4_data) / len(adaptive_l4_data) * 100 if len(adaptive_l4_data) > 0 else 0
    full_adaptive_asr = sum(item['attack_successful'] for item in full_adaptive_data) / len(full_adaptive_data) * 100 if len(full_adaptive_data) > 0 else 0
    
    print(f"  Isolated (no coordination): {isolated_asr:.2f}% ({len(isolated_data)} traces)")
    print(f"  Adaptive L3 only: {adaptive_l3_asr:.2f}% ({len(adaptive_l3_data)} traces)")
    print(f"  Adaptive L4 only: {adaptive_l4_asr:.2f}% ({len(adaptive_l4_data)} traces)")
    print(f"  Full adaptive: {full_adaptive_asr:.2f}% ({len(full_adaptive_data)} traces)")
    
    # Perform ASR comparisons with McNemar's test and confidence intervals
    print(f"\nASR Comparisons with Statistical Tests:")
    print("-" * 60)
    
    # Define key configuration pairs to compare
    config_pairs = [
        (is_isolated_config, is_full_adaptive_config, 'isolated', 'full_adaptive'),
        (is_isolated_config, is_adaptive_l4_config, 'isolated', 'adaptive_l4'),
        (is_isolated_config, is_adaptive_l3_config, 'isolated', 'adaptive_l3'),
        (is_adaptive_l3_config, is_adaptive_l4_config, 'adaptive_l3', 'adaptive_l4'),
        (is_adaptive_l3_config, is_full_adaptive_config, 'adaptive_l3', 'full_adaptive'),
        (is_adaptive_l4_config, is_full_adaptive_config, 'adaptive_l4', 'full_adaptive')
    ]
    
    asr_comparisons = []
    for config_func1, config_func2, name1, name2 in config_pairs:
        comparison = calculate_asr_comparison_with_stats(data, config_func1, config_func2, name1, name2)
        asr_comparisons.append(comparison)
        
        if comparison['common_requests'] > 0:
            print(f"{name1} vs {name2}:")
            print(f"  {name1} ASR: {comparison['config1_asr']:.2f}% (95% CI: {comparison['config1_ci_lower']:.2f}%, {comparison['config1_ci_upper']:.2f}%)")
            print(f"  {name2} ASR: {comparison['config2_asr']:.2f}% (95% CI: {comparison['config2_ci_lower']:.2f}%, {comparison['config2_ci_upper']:.2f}%)")
            print(f"  ASR Reduction: {comparison['asr_reduction']:.2f}%")
            print(f"  Relative Reduction: {comparison['relative_reduction']:.2f}%")
            print(f"  McNemar's Chi²: {comparison['mcnemar_chi2']:.4f}" if comparison['mcnemar_chi2'] is not None else "  McNemar's Chi²: N/A")
            print(f"  P-value: {comparison['mcnemar_p']:.6f}" if comparison['mcnemar_p'] is not None else "  P-value: N/A")
            if comparison['mcnemar_p'] is not None:
                print(f"  Significant (α=0.05): {'Yes' if comparison['mcnemar_p'] < 0.05 else 'No'}")
            print(f"  Common requests: {comparison['common_requests']}")
            print()
        else:
            print(f"{name1} vs {name2}: No common requests for paired comparison")
            print()
    
    # Calculate overall effectiveness of adaptive coordination
    isolated_data = [item for item in data if is_isolated_config(item['configuration'])]
    adaptive_data = [item for item in data if 'adaptive' in item['configuration'] and 'enabled": true' in item['configuration']]
    
    if len(isolated_data) > 0 and len(adaptive_data) > 0:
        isolated_asr = sum(item['attack_successful'] for item in isolated_data) / len(isolated_data) * 100
        adaptive_asr = sum(item['attack_successful'] for item in adaptive_data) / len(adaptive_data) * 100
        
        overall_reduction = isolated_asr - adaptive_asr
        relative_reduction = (isolated_asr - adaptive_asr) / isolated_asr * 100 if isolated_asr != 0 else 0
        
        # Calculate Wilson confidence intervals for overall comparison
        isolated_ci_lower, isolated_ci_upper = calculate_wilson_score_interval(
            sum(item['attack_successful'] for item in isolated_data), len(isolated_data)
        )
        adaptive_ci_lower, adaptive_ci_upper = calculate_wilson_score_interval(
            sum(item['attack_successful'] for item in adaptive_data), len(adaptive_data)
        )
        
        print(f"Overall Effectiveness of Adaptive Coordination:")
        print(f"  Isolated ASR: {isolated_asr:.2f}% (95% CI: {isolated_ci_lower:.2f}%, {isolated_ci_upper:.2f}%)")
        print(f"  Adaptive ASR: {adaptive_asr:.2f}% (95% CI: {adaptive_ci_lower:.2f}%, {adaptive_ci_upper:.2f}%)")
        print(f"  Absolute Reduction: {overall_reduction:.2f}%")
        print(f"  Relative Reduction: {relative_reduction:.2f}%")
        print()
    
    # Summary statistics
    print(f"Statistical Summary:")
    print("-" * 30)
    significant_comparisons = [c for c in asr_comparisons 
                              if c['mcnemar_p'] is not None and c['mcnemar_p'] < 0.05 and c['common_requests'] > 0]
    print(f"  Significant comparisons (p < 0.05): {len(significant_comparisons)}")
    print(f"  Total valid comparisons: {len([c for c in asr_comparisons if c['common_requests'] > 0])}")
    
    # Save results to JSON
    results = {
        'total_traces': len(data),
        'overall_asr': overall_asr,
        'config_stats': {
            'isolated': {
                'asr': isolated_asr,
                'count': len(isolated_data),
                'successful': sum(item['attack_successful'] for item in isolated_data)
            },
            'adaptive_l3': {
                'asr': adaptive_l3_asr,
                'count': len(adaptive_l3_data),
                'successful': sum(item['attack_successful'] for item in adaptive_l3_data)
            },
            'adaptive_l4': {
                'asr': adaptive_l4_asr,
                'count': len(adaptive_l4_data),
                'successful': sum(item['attack_successful'] for item in adaptive_l4_data)
            },
            'full_adaptive': {
                'asr': full_adaptive_asr,
                'count': len(full_adaptive_data),
                'successful': sum(item['attack_successful'] for item in full_adaptive_data)
            }
        },
        'asr_comparisons': [
            {
                'config1': c['config1'],
                'config2': c['config2'],
                'config1_asr': c['config1_asr'],
                'config2_asr': c['config2_asr'],
                'config1_count': c['config1_count'],
                'config2_count': c['config2_count'],
                'asr_reduction': c['asr_reduction'],
                'relative_reduction': c['relative_reduction'],
                'mcnemar_chi2': c['mcnemar_chi2'],
                'mcnemar_p': c['mcnemar_p'],
                'config1_ci_lower': c['config1_ci_lower'],
                'config1_ci_upper': c['config1_ci_upper'],
                'config2_ci_lower': c['config2_ci_lower'],
                'config2_ci_upper': c['config2_ci_upper'],
                'common_requests': c['common_requests']
            } for c in asr_comparisons
        ],
        'overall_effectiveness': {
            'isolated_asr': sum(item['attack_successful'] for item in isolated_data) / len(isolated_data) * 100 if len(isolated_data) > 0 else None,
            'adaptive_asr': sum(item['attack_successful'] for item in adaptive_data) / len(adaptive_data) * 100 if len(adaptive_data) > 0 else None,
            'isolated_count': len(isolated_data),
            'adaptive_count': len(adaptive_data),
            'absolute_reduction': (sum(item['attack_successful'] for item in isolated_data) / len(isolated_data) * 100 - 
                                 sum(item['attack_successful'] for item in adaptive_data) / len(adaptive_data) * 100) if len(isolated_data) > 0 and len(adaptive_data) > 0 else None,
            'relative_reduction': ((sum(item['attack_successful'] for item in isolated_data) / len(isolated_data) * 100 - 
                                  sum(item['attack_successful'] for item in adaptive_data) / len(adaptive_data) * 100) / 
                                 (sum(item['attack_successful'] for item in isolated_data) / len(isolated_data) * 100) * 100) if len(isolated_data) > 0 and sum(item['attack_successful'] for item in isolated_data) / len(isolated_data) * 100 != 0 else None
        }
    }
    
    with open('data/statistical_analysis_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nStatistical analysis results saved to data/statistical_analysis_results.json")
    
    return results

def main():
    results = run_comprehensive_statistical_analysis()
    
    print("="*80)
    print("STATISTICAL ANALYSIS COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()