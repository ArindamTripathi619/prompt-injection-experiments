"""
Bypass Analysis Engine
Identifies common patterns in injection attempts that bypass defenses.
"""

from typing import List, Dict, Any, Optional
import json
import logging

from models.layer_result import LayerResult
from models.request import RequestEnvelope

logger = logging.getLogger(__name__)

class BypassAnalyzer:
    """Analyzes execution traces to identify defense bypass patterns."""
    
    def __init__(self):
        self.common_bypass_patterns = [
            "instruction_override",
            "character_encoding",
            "few_shot_distraction",
            "jailbreak_prefix"
        ]
        
    def analyze_failure(self, request: RequestEnvelope, layer_results: List[LayerResult]) -> Dict[str, Any]:
        """Analyze why an attack successfully bypassed layers."""
        passed_layers = [r.layer_name for r in layer_results if r.passed]
        
        # Simple heuristic analysis
        patterns_detected = []
        user_input = request.user_input.lower()
        
        if "ignore all previous instructions" in user_input:
            patterns_detected.append("instruction_override")
        if "\\u" in user_input or "0x" in user_input:
            patterns_detected.append("character_encoding")
        
        return {
            "request_id": request.request_id,
            "bypassed_layers": passed_layers,
            "patterns_detected": patterns_detected,
            "input_length": len(user_input)
        }
