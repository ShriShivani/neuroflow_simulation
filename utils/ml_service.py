"""
ML Service integration for NeuroFlow simulation
Handles communication with trained Random Forest models
"""

import requests
import time
import json
from typing import Dict, Any, Optional

class MLService:
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.timeout = 10
        self.last_check = 0
        self.cached_status = None
    
    def check_connection(self) -> Dict[str, Any]:
        """Check if ML service is connected and return status"""
        current_time = time.time()
        
        # Cache status for 30 seconds to avoid spam requests
        if current_time - self.last_check < 30 and self.cached_status:
            return self.cached_status
        
        try:
            response = requests.get(f"{self.base_url}/health", timeout=3)
            if response.status_code == 200:
                data = response.json()
                self.cached_status = {
                    'connected': True,
                    'models_loaded': data.get('models_loaded', False),
                    'service': data.get('service', 'Unknown'),
                    'features_available': data.get('features_available', 0),
                    'timestamp': data.get('timestamp', 'Unknown')
                }
            else:
                self.cached_status = {'connected': False, 'error': f'HTTP {response.status_code}'}
        except Exception as e:
            self.cached_status = {'connected': False, 'error': str(e)}
        
        self.last_check = current_time
        return self.cached_status
    
    def get_model_info(self) -> Optional[Dict[str, Any]]:
        """Get detailed model information"""
        try:
            response = requests.get(f"{self.base_url}/model-info", timeout=5)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Failed to get model info: {e}")
            return None
    
    def predict(self, task: Dict[str, Any], user_state: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get ML prediction for task prioritization"""
        try:
            payload = {
                "task": task,
                "userState": user_state
            }
            
            response = requests.post(
                f"{self.base_url}/predict",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"ML service error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"ML prediction failed: {e}")
            return None
    
    def predict_batch(self, tasks: list, user_state: Dict[str, Any]) -> list:
        """Get ML predictions for multiple tasks"""
        results = []
        
        for task in tasks:
            prediction = self.predict(task, user_state)
            if prediction:
                results.append({
                    'task': task,
                    'prediction': prediction
                })
            else:
                # Fallback calculation
                results.append({
                    'task': task,
                    'prediction': self.fallback_prediction(task, user_state)
                })
        
        # Sort by priority score
        results.sort(key=lambda x: x['prediction'].get('priorityScore', 0), reverse=True)
        return results
    
    def fallback_prediction(self, task: Dict[str, Any], user_state: Dict[str, Any]) -> Dict[str, Any]:
        """Simple algorithmic fallback when ML service is unavailable"""
        importance = task.get('importance', 0.5)
        urgency = task.get('urgency', 0.5)
        duration = task.get('estimatedDurationMin', 30)
        
        energy = user_state.get('energy', 0.5)
        mood = user_state.get('mood', 0.5)
        medication = user_state.get('medicationTaken', False)
        
        # Simple priority calculation
        medication_boost = 0.1 if medication else 0
        duration_factor = 1.0 if duration <= 30 else 0.8 if duration <= 60 else 0.6
        
        priority = min(1.0, (importance * 0.5 + urgency * 0.3 + energy * 0.2 + medication_boost) * duration_factor)
        completion = min(1.0, (energy * 0.4 + mood * 0.3 + (0.1 if medication else 0) + 0.2) * duration_factor)
        
        return {
            'priorityScore': priority,
            'completionLikelihood': completion,
            'predictionSource': 'algorithmic_fallback',
            'confidence': 'medium',
            'reasoning': {
                'method': 'Simple algorithmic calculation',
                'adhd_recommendations': [
                    "💊 Consider taking ADHD medication if prescribed" if not medication else "✅ Great! Medication can help with focus",
                    "⚡ Try to match task energy requirements with your current energy level",
                    "🍅 Consider using Pomodoro technique for longer tasks" if duration > 60 else "⏱️ This task should be manageable in one session"
                ]
            }
        }
    
    def simulate_daily_progress(self, num_tasks: int = 5) -> Dict[str, Any]:
        """Simulate a day of ADHD task management"""
        # Generate sample tasks
        tasks = [
            {"title": "Morning email check", "duration": 15, "importance": 0.4, "energy": "low"},
            {"title": "Important project work", "duration": 90, "importance": 0.9, "energy": "high"},
            {"title": "Team meeting", "duration": 60, "importance": 0.7, "energy": "medium"},
            {"title": "Quick admin tasks", "duration": 20, "importance": 0.3, "energy": "low"},
            {"title": "Creative brainstorming", "duration": 45, "importance": 0.8, "energy": "high"}
        ]
        
        # Simulate different times of day
        morning_state = {"energy": 0.8, "mood": 0.7, "medicationTaken": True, "focus": 0.8}
        afternoon_state = {"energy": 0.6, "mood": 0.8, "medicationTaken": True, "focus": 0.9}
        evening_state = {"energy": 0.4, "mood": 0.6, "medicationTaken": False, "focus": 0.5}
        
        results = {
            'morning': self.predict_batch(tasks[:2], morning_state),
            'afternoon': self.predict_batch(tasks[2:4], afternoon_state),
            'evening': self.predict_batch(tasks[4:], evening_state)
        }
        
        return results
