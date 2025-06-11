import pandas as pd
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
from typing import Dict, List, Tuple

def calculate_metrics(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate basic classification metrics.
    Since we don't have actual vs predicted, we'll calculate metrics based on confidence scores.
    
    Args:
        df: DataFrame containing predictions and confidence scores
    
    Returns:
        Dictionary containing accuracy, recall, and F1 score
    """
    # High confidence (>=0.9) predictions are considered "correct"
    high_confidence_mask = df['confidence'] >= 0.9
    medium_confidence_mask = (df['confidence'] >= 0.7) & (df['confidence'] < 0.9)
    
    total_predictions = len(df)
    high_confidence_predictions = high_confidence_mask.sum()
    medium_confidence_predictions = medium_confidence_mask.sum()
    
    # Accuracy: Percentage of high confidence predictions
    accuracy = high_confidence_predictions / total_predictions
    
    # Recall: Of all predictions that should be high confidence, how many were correctly identified
    # We consider medium confidence predictions as "should be high confidence"
    should_be_high = high_confidence_predictions + medium_confidence_predictions
    recall = high_confidence_predictions / should_be_high if should_be_high > 0 else 0
    
    # F1 Score: Harmonic mean of accuracy and recall
    f1 = 2 * (accuracy * recall) / (accuracy + recall) if (accuracy + recall) > 0 else 0
    
    metrics = {
        'accuracy': accuracy,
        'recall': recall,
        'f1': f1
    }
    return metrics

def analyze_confidence_distribution(df: pd.DataFrame, confidence_column: str = 'confidence') -> Dict[str, float]:
    """
    Analyze the distribution of confidence scores.
    
    Args:
        df: DataFrame containing confidence scores
        confidence_column: Column name for confidence scores
    
    Returns:
        Dictionary containing confidence distribution statistics
    """
    confidence_stats = {
        'mean': df[confidence_column].mean(),
        'median': df[confidence_column].median(),
        'std': df[confidence_column].std(),
        'min': df[confidence_column].min(),
        'max': df[confidence_column].max()
    }
    
    # Add confidence ranges
    confidence_ranges = {
        'high_confidence': len(df[df[confidence_column] >= 0.9]) / len(df),
        'medium_confidence': len(df[(df[confidence_column] >= 0.7) & (df[confidence_column] < 0.9)]) / len(df),
        'low_confidence': len(df[df[confidence_column] < 0.7]) / len(df)
    }
    
    return {**confidence_stats, **confidence_ranges}

def analyze_source_distribution(df: pd.DataFrame, source_column: str = 'source') -> Dict[str, float]:
    """
    Analyze the distribution of prediction sources (Rule vs GenAI).
    
    Args:
        df: DataFrame containing source information
        source_column: Column name for source
    
    Returns:
        Dictionary containing source distribution statistics
    """
    total = len(df)
    source_dist = df[source_column].value_counts(normalize=True).to_dict()
    
    # Calculate confidence by source
    confidence_by_source = {}
    for source in df[source_column].unique():
        source_df = df[df[source_column] == source]
        if len(source_df) > 0:
            confidence_by_source[f'{source}_confidence'] = source_df['confidence'].mean()
    
    return {**source_dist, **confidence_by_source}

def get_category_performance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate performance metrics for each category.
    
    Args:
        df: DataFrame containing predictions and confidence scores
    
    Returns:
        DataFrame with performance metrics per category
    """
    categories = df['commodity_title'].unique()
    results = []
    
    for category in categories:
        category_df = df[df['commodity_title'] == category]
        
        # Calculate metrics based on confidence scores
        high_confidence = len(category_df[category_df['confidence'] >= 0.9])
        medium_confidence = len(category_df[(category_df['confidence'] >= 0.7) & (category_df['confidence'] < 0.9)])
        low_confidence = len(category_df[category_df['confidence'] < 0.7])
        
        total = len(category_df)
        
        results.append({
            'category': category,
            'total_samples': total,
            'high_confidence': high_confidence,
            'medium_confidence': medium_confidence,
            'low_confidence': low_confidence,
            'avg_confidence': category_df['confidence'].mean(),
            'rule_based': len(category_df[category_df['source'] == 'Rule']),
            'genai_based': len(category_df[category_df['source'] == 'GenAI'])
        })
    
    return pd.DataFrame(results).sort_values('total_samples', ascending=False)

def generate_evaluation_report(df: pd.DataFrame) -> Dict:
    """
    Generate a comprehensive evaluation report.
    
    Args:
        df: DataFrame containing predictions, confidence scores, and sources
    
    Returns:
        Dictionary containing all evaluation metrics
    """
    report = {
        'overall_metrics': calculate_metrics(df),
        'confidence_analysis': analyze_confidence_distribution(df),
        'source_analysis': analyze_source_distribution(df),
        'category_performance': get_category_performance(df).to_dict('records')
    }
    
    return report 