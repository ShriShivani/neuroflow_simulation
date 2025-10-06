"""
ADHD data generation and simulation utilities
Generates realistic ADHD behavioral patterns for demo purposes
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any

class ADHDDataGenerator:
    def __init__(self):
        self.task_categories = [
            'work', 'personal', 'health', 'creative', 'admin', 
            'social', 'learning', 'exercise', 'shopping', 'cleaning'
        ]
        
        self.energy_levels = ['low', 'medium', 'high']
        
        self.adhd_subtypes = ['inattentive', 'hyperactive', 'combined']
        
        # ADHD-specific task titles
        self.task_templates = {
            'work': [
                "Complete project proposal", "Review team documents", "Attend important meeting",
                "Finish quarterly report", "Respond to urgent emails", "Prepare presentation slides"
            ],
            'personal': [
                "Pay monthly bills", "Organize bedroom closet", "Call family members",
                "Schedule doctor appointment", "Plan weekend activities", "Update personal budget"
            ],
            'health': [
                "Take ADHD medication", "Go for morning walk", "Prepare healthy lunch",
                "Do evening stretches", "Practice mindfulness", "Drink enough water"
            ],
            'creative': [
                "Work on art project", "Write in journal", "Learn new skill",
                "Practice musical instrument", "Design personal website", "Edit vacation photos"
            ]
        }
        
        # ADHD challenge scenarios
        self.adhd_scenarios = [
            {
                'name': '🌅 Morning Medication Peak',
                'description': 'High focus and energy after taking ADHD medication',
                'user_state': {
                    'mood': np.random.uniform(0.7, 0.9),
                    'energy': np.random.uniform(0.8, 1.0),
                    'focus': np.random.uniform(0.8, 1.0),
                    'medicationTaken': True,
                    'distractions': np.random.randint(0, 2),
                    'stressLevel': np.random.uniform(0.1, 0.3),
                    'sleepQuality': np.random.uniform(0.7, 1.0)
                },
                'recommended_tasks': ['high energy', 'important', 'complex']
            },
            {
                'name': '😴 Afternoon Crash',
                'description': 'Energy dip and difficulty focusing in the afternoon',
                'user_state': {
                    'mood': np.random.uniform(0.3, 0.6),
                    'energy': np.random.uniform(0.2, 0.5),
                    'focus': np.random.uniform(0.2, 0.5),
                    'medicationTaken': True,
                    'distractions': np.random.randint(3, 7),
                    'stressLevel': np.random.uniform(0.4, 0.7),
                    'sleepQuality': np.random.uniform(0.4, 0.7)
                },
                'recommended_tasks': ['low energy', 'simple', 'routine']
            },
            {
                'name': '🔥 Hyperfocus Mode',
                'description': 'Intense concentration on preferred tasks',
                'user_state': {
                    'mood': np.random.uniform(0.8, 1.0),
                    'energy': np.random.uniform(0.7, 1.0),
                    'focus': np.random.uniform(0.9, 1.0),
                    'medicationTaken': True,
                    'distractions': 0,
                    'stressLevel': np.random.uniform(0.1, 0.2),
                    'sleepQuality': np.random.uniform(0.8, 1.0)
                },
                'recommended_tasks': ['creative', 'complex', 'engaging']
            },
            {
                'name': '😰 Executive Dysfunction',
                'description': 'Difficulty starting tasks and making decisions',
                'user_state': {
                    'mood': np.random.uniform(0.2, 0.4),
                    'energy': np.random.uniform(0.3, 0.6),
                    'focus': np.random.uniform(0.2, 0.4),
                    'medicationTaken': False,
                    'distractions': np.random.randint(5, 10),
                    'stressLevel': np.random.uniform(0.6, 0.9),
                    'sleepQuality': np.random.uniform(0.2, 0.5)
                },
                'recommended_tasks': ['micro-tasks', 'familiar', 'low-stakes']
            },
            {
                'name': '💊 Unmedicated Struggle',
                'description': 'Managing ADHD symptoms without medication',
                'user_state': {
                    'mood': np.random.uniform(0.3, 0.5),
                    'energy': np.random.uniform(0.4, 0.7),
                    'focus': np.random.uniform(0.2, 0.5),
                    'medicationTaken': False,
                    'distractions': np.random.randint(4, 8),
                    'stressLevel': np.random.uniform(0.5, 0.8),
                    'sleepQuality': np.random.uniform(0.4, 0.8)
                },
                'recommended_tasks': ['structured', 'shorter', 'rewarding']
            }
        ]
    
    def generate_sample_tasks(self, count: int = 10) -> List[Dict[str, Any]]:
        """Generate realistic ADHD-related tasks"""
        tasks = []
        
        for _ in range(count):
            category = random.choice(self.task_categories)
            title_options = self.task_templates.get(category, ["Generic task"])
            
            task = {
                'title': random.choice(title_options),
                'category': category,
                'estimatedDurationMin': self._generate_duration(),
                'importance': round(np.random.beta(2, 2), 2),  # Slightly biased towards middle values
                'urgency': round(np.random.beta(2, 2), 2),
                'energyRequired': random.choice(self.energy_levels),
                'contextSwitchingDifficulty': round(np.random.uniform(0.1, 0.9), 2),
                'dueDate': self._generate_due_date(),
                'tags': self._generate_task_tags(category)
            }
            
            tasks.append(task)
        
        return tasks
    
    def _generate_duration(self) -> int:
        """Generate realistic task durations with ADHD considerations"""
        # ADHD users often prefer shorter tasks or underestimate time
        duration_types = [
            (5, 15, 0.3),    # Quick tasks - preferred by ADHD
            (15, 30, 0.3),   # Short tasks - manageable
            (30, 60, 0.2),   # Medium tasks - challenging
            (60, 120, 0.15), # Long tasks - difficult
            (120, 240, 0.05) # Very long tasks - often avoided
        ]
        
        duration_type = np.random.choice(len(duration_types), p=[p for _, _, p in duration_types])
        min_dur, max_dur, _ = duration_types[duration_type]
        
        return random.randint(min_dur, max_dur)
    
    def _generate_due_date(self) -> str:
        """Generate realistic due dates"""
        # ADHD users often have urgent or overdue tasks
        days_ahead = np.random.choice(
            [-1, 0, 1, 2, 7, 14, 30],  # -1 = overdue, 0 = today
            p=[0.1, 0.2, 0.3, 0.2, 0.1, 0.05, 0.05]
        )
        
        due_date = datetime.now() + timedelta(days=days_ahead)
        return due_date.isoformat()
    
    def _generate_task_tags(self, category: str) -> List[str]:
        """Generate relevant tags for tasks"""
        all_tags = {
            'work': ['deadline', 'meeting', 'important', 'collaboration'],
            'personal': ['self-care', 'organization', 'routine'],
            'health': ['medication', 'exercise', 'wellness'],
            'creative': ['fun', 'engaging', 'flow-state']
        }
        
        category_tags = all_tags.get(category, ['general'])
        return random.sample(category_tags, min(2, len(category_tags)))
    
    def generate_user_progression(self, days: int = 30) -> pd.DataFrame:
        """Generate ADHD user progression data over time"""
        dates = pd.date_range(start=datetime.now() - timedelta(days=days), periods=days, freq='D')
        
        data = []
        base_completion_rate = 0.6  # ADHD users typically have lower completion rates
        
        for i, date in enumerate(dates):
            # Simulate medication effect and routine building
            medication_consistency = min(0.9, 0.3 + (i * 0.02))  # Improving over time
            
            # Weekend effect (often harder for ADHD)
            weekend_penalty = 0.15 if date.weekday() >= 5 else 0
            
            # Random daily variation
            daily_variation = np.random.uniform(-0.2, 0.2)
            
            completion_rate = base_completion_rate + (medication_consistency * 0.3) - weekend_penalty + daily_variation
            completion_rate = max(0.1, min(0.95, completion_rate))
            
            data.append({
                'date': date,
                'tasks_created': np.random.poisson(5) + 3,  # 3-12 tasks per day
                'tasks_completed': int(np.random.poisson(5) * completion_rate),
                'completion_rate': completion_rate,
                'medication_taken': np.random.random() < medication_consistency,
                'avg_mood': np.random.uniform(0.3, 0.8),
                'avg_energy': np.random.uniform(0.2, 0.9),
                'avg_focus': np.random.uniform(0.2, 0.8),
                'points_earned': np.random.randint(10, 50),
                'streak_days': max(0, i - np.random.randint(0, 3)) if i > 0 else 0
            })
        
        return pd.DataFrame(data)
    
    def get_adhd_scenario(self, scenario_name: str = None) -> Dict[str, Any]:
        """Get a specific ADHD scenario or random one"""
        if scenario_name:
            scenarios = [s for s in self.adhd_scenarios if scenario_name in s['name']]
            return scenarios[0] if scenarios else random.choice(self.adhd_scenarios)
        
        return random.choice(self.adhd_scenarios)
    
    def generate_ml_comparison_data(self) -> Dict[str, Any]:
        """Generate comparison data between ML models and baseline methods"""
        methods = ['Your Trained ML Models', 'Enhanced Algorithmic AI', 'Basic Priority System', 'No System']
        
        # Realistic performance data
        performance_data = {
            'Method': methods,
            'Priority Accuracy (%)': [88.5, 75.0, 60.0, 30.0],
            'Completion Prediction (%)': [87.5, 70.0, 55.0, 25.0],
            'ADHD Features': [31, 15, 5, 0],
            'Training Data': ['8,000 samples', 'Research-based', 'Simple rules', 'None'],
            'Response Time (ms)': [150, 100, 50, 0],
            'User Satisfaction': [9.2, 7.8, 6.1, 3.5]
        }
        
        return performance_data
    
    def simulate_pomodoro_session(self, duration_minutes: int = 25) -> Dict[str, Any]:
        """Simulate a Pomodoro timer session with ADHD considerations"""
        # ADHD users may have varying focus during sessions
        focus_pattern = []
        distraction_events = []
        
        for minute in range(duration_minutes):
            # Focus typically starts high, may dip, then recover
            if minute < 5:
                focus = np.random.uniform(0.7, 1.0)  # High initial focus
            elif minute < 15:
                focus = np.random.uniform(0.4, 0.8)  # Mid-session dip
            else:
                focus = np.random.uniform(0.6, 0.9)  # Recovery with deadline pressure
            
            focus_pattern.append(focus)
            
            # Random distraction events (more likely for ADHD)
            if np.random.random() < 0.1:  # 10% chance per minute
                distraction_events.append({
                    'minute': minute,
                    'type': random.choice(['phone', 'thought', 'noise', 'interruption']),
                    'severity': np.random.uniform(0.1, 0.8)
                })
        
        # Calculate session metrics
        avg_focus = np.mean(focus_pattern)
        productivity_score = avg_focus * (1 - len(distraction_events) * 0.1)
        
        return {
            'duration_minutes': duration_minutes,
            'focus_pattern': focus_pattern,
            'distraction_events': distraction_events,
            'avg_focus': avg_focus,
            'productivity_score': max(0, min(1, productivity_score)),
            'distractions_count': len(distraction_events),
            'completion_likelihood': 0.9 if avg_focus > 0.7 else 0.7 if avg_focus > 0.5 else 0.4
        }
