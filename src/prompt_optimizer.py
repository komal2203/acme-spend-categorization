# src/prompt_optimizer.py

from collections import defaultdict
from typing import Dict, List
import json
from datetime import datetime, timedelta
from src.feedback_store import FeedbackStore

class PromptOptimizer:
    def __init__(self):
        self.feedback_store = FeedbackStore()
        
    def analyze_successful_classifications(self, days: int = 30) -> Dict:
        """
        Analyze successful classifications to identify patterns and improve prompts.
        """
        try:
            recent_classifications = self.feedback_store.get_recent_successful_classifications(days)
            
            if not recent_classifications:
                return {
                    'supplier_patterns': {},
                    'common_phrases': {},
                    'confidence_patterns': {},
                    'recommended_prompts': []
                }
            
            # Group by supplier
            supplier_patterns = defaultdict(list)
            for classification in recent_classifications:
                supplier_patterns[classification['supplier']].append(classification)
            
            # Analyze patterns
            analysis = {
                'supplier_patterns': {},
                'common_phrases': defaultdict(int),
                'confidence_patterns': defaultdict(list),
                'recommended_prompts': []
            }
            
            # Analyze each supplier's patterns
            for supplier, classifications in supplier_patterns.items():
                supplier_analysis = {
                    'total_classifications': len(classifications),
                    'avg_confidence': sum(c['confidence'] for c in classifications) / len(classifications),
                    'common_codes': defaultdict(int),
                    'successful_descriptions': []
                }
                
                # Collect successful descriptions
                for classification in classifications:
                    supplier_analysis['successful_descriptions'].append({
                        'description': classification['description'],
                        'code': classification['code'],
                        'confidence': classification['confidence']
                    })
                    supplier_analysis['common_codes'][classification['code']] += 1
                
                analysis['supplier_patterns'][supplier] = supplier_analysis
                
                # Generate supplier-specific prompt
                if len(classifications) >= 5:  # Only generate if we have enough data
                    prompt = self._generate_supplier_prompt(supplier, classifications)
                    analysis['recommended_prompts'].append(prompt)
            
            return analysis
        
        except Exception as e:
            print(f"Error analyzing classifications: {e}")
            return {
                'supplier_patterns': {},
                'common_phrases': {},
                'confidence_patterns': {},
                'recommended_prompts': []
            }
    
    def _generate_supplier_prompt(self, supplier: str, classifications: List[Dict]) -> Dict:
        """
        Generate a supplier-specific prompt based on successful classifications.
        """
        # Get most common codes for this supplier
        code_counts = defaultdict(int)
        for classification in classifications:
            code_counts[classification['code']] += 1
        
        most_common_codes = sorted(
            code_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]  # Top 3 codes
        
        # Get example descriptions for each common code
        examples = []
        for code, _ in most_common_codes:
            code_examples = [
                c['description'] for c in classifications
                if c['code'] == code
            ][:2]  # Get 2 examples per code
            examples.extend(code_examples)
        
        return {
            'supplier': supplier,
            'common_codes': [code for code, _ in most_common_codes],
            'examples': examples,
            'prompt_template': self._create_prompt_template(supplier, examples)
        }
    
    def _create_prompt_template(self, supplier: str, examples: List[str]) -> str:
        """
        Create a prompt template with examples.
        """
        examples_text = "\n".join([
            f"Example {i+1}: '{example}'"
            for i, example in enumerate(examples)
        ])
        
        return f"""When classifying invoices from {supplier}, consider these successful examples:
{examples_text}

For new invoices from {supplier}, pay special attention to:
1. Similar product/service descriptions
2. Common patterns in the examples above
3. Supplier-specific terminology

Classify the following invoice:"""
    
    def get_optimized_prompt(self, supplier: str, description: str) -> str:
        """
        Get an optimized prompt for a specific supplier and description.
        """
        analysis = self.analyze_successful_classifications()
        
        # Check if we have supplier-specific data
        if supplier in analysis['supplier_patterns']:
            supplier_data = analysis['supplier_patterns'][supplier]
            
            # Get most relevant examples
            relevant_examples = [
                ex for ex in supplier_data['successful_descriptions']
                if any(word in description.lower() 
                      for word in ex['description'].lower().split())
            ][:3]  # Get up to 3 relevant examples
            
            if relevant_examples:
                examples_text = "\n".join([
                    f"Similar example: '{ex['description']}' -> Code: {ex['code']}"
                    for ex in relevant_examples
                ])
                
                return f"""Consider these similar successful classifications:
{examples_text}

Classify this invoice:
Description: '{description}'
Supplier: '{supplier}'

Respond with the most appropriate UNSPSC code."""
        
        # If no supplier-specific data, use default prompt
        return f"""Classify this invoice:
Description: '{description}'
Supplier: '{supplier}'

Respond with the most appropriate UNSPSC code."""