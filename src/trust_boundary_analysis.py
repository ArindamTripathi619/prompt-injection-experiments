#!/usr/bin/env python3
"""
Analysis of trust boundary violations and bypass mechanisms in prompt injection experiments.
"""

import sqlite3
import json
from pathlib import Path
import re

def analyze_trust_boundary_violations(db_path):
    """Analyze trust boundary violations in the experiment data."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all traces with detailed information
    query = """
    SELECT 
        request_id,
        attack_successful,
        configuration,
        trust_boundary_violations,
        bypass_mechanisms,
        propagation_path,
        blocked_at_layer,
        user_input,
        final_output
    FROM execution_traces
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    
    print("="*80)
    print("TRUST BOUNDARY VIOLATIONS AND BYPASS MECHANISMS ANALYSIS")
    print("="*80)
    
    total_traces = len(results)
    print(f"Total traces analyzed: {total_traces}")
    
    # Parse the data
    parsed_data = []
    for row in results:
        parsed_row = {
            'request_id': row[0],
            'attack_successful': row[1],
            'configuration': row[2],
            'trust_boundary_violations': json.loads(row[3]) if row[3] and row[3] != 'null' else [],
            'bypass_mechanisms': json.loads(row[4]) if row[4] and row[4] != 'null' else [],
            'propagation_path': json.loads(row[5]) if row[5] and row[5] != 'null' else [],
            'blocked_at_layer': row[6],
            'user_input': row[7],
            'final_output': row[8]
        }
        parsed_data.append(parsed_row)
    
    # Count trust boundary violations
    trust_violations_count = 0
    for trace in parsed_data:
        if trace['trust_boundary_violations'] and trace['trust_boundary_violations'] != []:
            trust_violations_count += 1
    
    print(f"\nTrust Boundary Violations:")
    print(f"  Traces with trust boundary violations: {trust_violations_count}")
    print(f"  Percentage: {trust_violations_count/total_traces*100:.2f}%")
    
    # Count bypass mechanisms
    bypass_mechanisms_count = 0
    bypass_mechanisms_types = {}
    
    for trace in parsed_data:
        if trace['bypass_mechanisms'] and trace['bypass_mechanisms'] != []:
            bypass_mechanisms_count += 1
            for mechanism in trace['bypass_mechanisms']:
                if mechanism not in bypass_mechanisms_types:
                    bypass_mechanisms_types[mechanism] = 0
                bypass_mechanisms_types[mechanism] += 1
    
    print(f"\nBypass Mechanisms:")
    print(f"  Traces with bypass mechanisms: {bypass_mechanisms_count}")
    print(f"  Percentage: {bypass_mechanisms_count/total_traces*100:.2f}%")
    print(f"  Types of bypass mechanisms:")
    for mechanism, count in sorted(bypass_mechanisms_types.items(), key=lambda x: x[1], reverse=True):
        print(f"    {mechanism}: {count} ({count/bypass_mechanisms_count*100:.2f}%)")
    
    # Analyze by configuration
    print(f"\nBypass Mechanisms by Configuration:")
    config_bypass = {}
    for trace in parsed_data:
        config_type = extract_configuration_type(trace['configuration'])
        if config_type not in config_bypass:
            config_bypass[config_type] = {'total': 0, 'with_bypass': 0, 'bypass_types': {}}
        
        config_bypass[config_type]['total'] += 1
        
        if trace['bypass_mechanisms'] and trace['bypass_mechanisms'] != []:
            config_bypass[config_type]['with_bypass'] += 1
            for mechanism in trace['bypass_mechanisms']:
                if mechanism not in config_bypass[config_type]['bypass_types']:
                    config_bypass[config_type]['bypass_types'][mechanism] = 0
                config_bypass[config_type]['bypass_types'][mechanism] += 1
    
    for config_type, stats in config_bypass.items():
        if stats['total'] > 0:
            bypass_rate = stats['with_bypass'] / stats['total'] * 100
            print(f"  {config_type}: {bypass_rate:.2f}% bypass rate ({stats['with_bypass']}/{stats['total']})")
            if stats['bypass_types']:
                print(f"    Top bypass mechanisms:")
                for mech, count in sorted(stats['bypass_types'].items(), key=lambda x: x[1], reverse=True)[:3]:
                    print(f"      {mech}: {count}")
    
    # Analyze propagation paths to understand bypass patterns
    print(f"\nPropagation Path Analysis:")
    
    # Count how many traces were blocked at each layer
    layer_blocks = {}
    for trace in parsed_data:
        if trace['blocked_at_layer']:
            if trace['blocked_at_layer'] not in layer_blocks:
                layer_blocks[trace['blocked_at_layer']] = 0
            layer_blocks[trace['blocked_at_layer']] += 1
    
    print(f"  Blocks by layer:")
    for layer, count in sorted(layer_blocks.items(), key=lambda x: x[1], reverse=True):
        print(f"    {layer}: {count}")
    
    # Analyze successful attacks to understand bypass patterns
    successful_attacks = [trace for trace in parsed_data if trace['attack_successful'] == 1]
    print(f"\nSuccessful Attack Analysis:")
    print(f"  Total successful attacks: {len(successful_attacks)}")
    print(f"  Success rate: {len(successful_attacks)/total_traces*100:.2f}%")
    
    # Count how many successful attacks bypassed each layer
    successful_bypass_layers = {}
    for trace in successful_attacks:
        for layer_info in trace['propagation_path']:
            layer_name = layer_info.get('layer', 'Unknown')
            decision = layer_info.get('decision', 'Unknown')
            if decision == 'pass':
                if layer_name not in successful_bypass_layers:
                    successful_bypass_layers[layer_name] = 0
                successful_bypass_layers[layer_name] += 1
    
    print(f"  Layers bypassed in successful attacks:")
    for layer, count in sorted(successful_bypass_layers.items(), key=lambda x: x[1], reverse=True):
        print(f"    {layer}: {count} bypasses")
    
    # Analyze user inputs for successful attacks to identify common bypass patterns
    print(f"\nCommon Attack Patterns in Successful Attacks:")
    successful_inputs = [trace['user_input'] for trace in successful_attacks]
    
    # Look for common patterns in successful attacks
    injection_keywords = ['ignore', 'disregard', 'system', 'prompt', 'instructions', 'admin', 'override', 'debug', 'reveal', 'show', 'output', 'display']
    keyword_matches = {}
    
    for input_text in successful_inputs:
        input_lower = input_text.lower()
        for keyword in injection_keywords:
            if keyword in input_lower:
                if keyword not in keyword_matches:
                    keyword_matches[keyword] = 0
                keyword_matches[keyword] += 1
    
    print(f"  Injection keywords found in successful attacks:")
    for keyword, count in sorted(keyword_matches.items(), key=lambda x: x[1], reverse=True):
        print(f"    {keyword}: {count} occurrences")
    
    # Identify most common user inputs that resulted in successful attacks
    input_frequency = {}
    for input_text in successful_inputs:
        if input_text not in input_frequency:
            input_frequency[input_text] = 0
        input_frequency[input_text] += 1
    
    print(f"  Most common successful attack inputs:")
    for input_text, count in sorted(input_frequency.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"    [{count}] {input_text[:80]}{'...' if len(input_text) > 80 else ''}")
    
    # Summary statistics
    print(f"\nSUMMARY:")
    print(f"  - Total traces: {total_traces}")
    print(f"  - Successful attacks: {len(successful_attacks)} ({len(successful_attacks)/total_traces*100:.2f}%)")
    print(f"  - Traces with bypass mechanisms: {bypass_mechanisms_count} ({bypass_mechanisms_count/total_traces*100:.2f}%)")
    print(f"  - Main bypass mechanisms: {', '.join([f'{k}({v})' for k, v in list(bypass_mechanisms_types.items())[:5]])}")
    
    # Save detailed analysis to file
    analysis_results = {
        'total_traces': total_traces,
        'successful_attacks': len(successful_attacks),
        'successful_attack_rate': len(successful_attacks)/total_traces*100,
        'traces_with_bypass': bypass_mechanisms_count,
        'bypass_rate': bypass_mechanisms_count/total_traces*100,
        'bypass_mechanisms': bypass_mechanisms_types,
        'config_bypass_analysis': config_bypass,
        'layer_blocks': layer_blocks,
        'successful_bypass_layers': successful_bypass_layers,
        'injection_keywords': keyword_matches,
        'common_successful_inputs': dict(sorted(input_frequency.items(), key=lambda x: x[1], reverse=True)[:20])
    }
    
    with open('data/trust_boundary_analysis.json', 'w') as f:
        json.dump(analysis_results, f, indent=2)
    
    print(f"\nDetailed analysis saved to data/trust_boundary_analysis.json")
    
    return analysis_results

def extract_configuration_type(config_str):
    """Extract configuration type from the configuration string."""
    if 'coordination' in config_str:
        if '"enabled": true' in config_str and '"adaptive_layer3": true' in config_str and '"adaptive_layer4": true' in config_str:
            return 'full_adaptive'
        elif '"enabled": true' and '"adaptive_layer4": true' in config_str:
            return 'adaptive_l4'
        elif '"enabled": true' and '"adaptive_layer3": true' in config_str:
            return 'adaptive_l3'
        elif '"enabled": false' in config_str:
            return 'isolated'
    elif 'isolation' in config_str and 'coordination' not in config_str:
        return 'baseline'
    
    return 'other'

def main():
    db_path = "experiments.db"
    if not Path(db_path).exists():
        print(f"Database {db_path} not found!")
        return
    
    results = analyze_trust_boundary_violations(db_path)
    
    print("="*80)
    print("TRUST BOUNDARY ANALYSIS COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()