# src/feedback_store.py
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List
from pathlib import Path

class FeedbackStore:
    def __init__(self, store_path: str = "data/feedback"):
        try:
            self.store_path = Path(store_path)
            self.feedback_file = self.store_path / "feedback_data.json"
            
            # Create directory if it doesn't exist
            self.store_path.mkdir(parents=True, exist_ok=True)
            
            # Initialize feedback data
            self.feedback_data = self._load_feedback_data()
        except Exception as e:
            print(f"Error initializing FeedbackStore: {e}")
            self.feedback_data = {
                "successful_classifications": [],
                "failed_classifications": [],
                "last_updated": datetime.now().isoformat()
            }
    
    def _load_feedback_data(self) -> Dict:
        """Load existing feedback data or create new if doesn't exist."""
        try:
            if self.feedback_file.exists():
                with open(self.feedback_file, 'r') as f:
                    data = json.load(f)
                    # Ensure all required keys exist
                    if not all(key in data for key in ["successful_classifications", "failed_classifications", "last_updated"]):
                        raise ValueError("Invalid feedback data structure")
                    return data
            return {
                "successful_classifications": [],
                "failed_classifications": [],
                "last_updated": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error loading feedback data: {e}")
            return {
                "successful_classifications": [],
                "failed_classifications": [],
                "last_updated": datetime.now().isoformat()
            }
    
    def get_recent_successful_classifications(self, days: int = 30) -> List[Dict]:
        """Get successful classifications from the last N days."""
        try:
            if not isinstance(days, (int, float)) or days <= 0:
                days = 30  # Default to 30 days if invalid input
            
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Ensure we have the required data structure
            if "successful_classifications" not in self.feedback_data:
                self.feedback_data["successful_classifications"] = []
            
            # Filter and validate each classification
            recent = []
            for c in self.feedback_data["successful_classifications"]:
                try:
                    if not isinstance(c, dict):
                        continue
                    if "timestamp" not in c:
                        continue
                    timestamp = datetime.fromisoformat(c["timestamp"])
                    if timestamp > cutoff_date:
                        recent.append(c)
                except (ValueError, TypeError) as e:
                    print(f"Error processing classification: {e}")
                    continue
            
            return recent
        except Exception as e:
            print(f"Error getting recent classifications: {e}")
            return []