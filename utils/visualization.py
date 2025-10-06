"""
Visualization utilities for NeuroFlow ADHD simulation
Creates beautiful, informative charts for ADHD data
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import streamlit as st
from typing import Dict, List, Any

class VisualizationHelper:
    def __init__(self):
        # ADHD-friendly color palette
        self.colors = {
            'primary': '#667eea',
            'secondary': '#764ba2',
            'success': '#28a745',
            'warning': '#ffc107',
            'danger': '#dc3545',
            'info': '#17a2b8',
            'light': '#f8f9fa',
            'dark': '#343a40'
        }
        
        # Color schemes for different data types
        self.priority_colors = ['#28a745', '#ffc107', '#fd7e14', '#dc3545']  # Low to High
        self.energy_colors = ['#6f42c1', '#007bff', '#28a745']  # Low, Medium, High
        self.mood_colors = ['#dc3545', '#ffc107', '#28a745']  # Sad, Neutral, Happy
    
    def create_priority_gauge(self, priority_score: float, title: str = "Task Priority") -> go.Figure:
        """Create a gauge chart for task priority"""
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = priority_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': title, 'font': {'size': 24}},
            delta = {'reference': 0.5, 'increasing': {'color': self.colors['success']}},
            gauge = {
                'axis': {'range': [None, 1], 'tickcolor': "darkblue", 'tickwidth': 1, 'ticklen': 5},
                'bar': {'color': self.colors['primary']},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 0.3], 'color': 'lightgreen'},
                    {'range': [0.3, 0.7], 'color': 'lightyellow'},
                    {'range': [0.7, 1], 'color': 'lightcoral'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 0.8
                }
            }
        ))
        
        fig.update_layout(
            height=400,
            font={'color': self.colors['dark'], 'family': "Arial"}
        )
        
        return fig
    
    def create_adhd_radar_chart(self, user_state: Dict[str, Any]) -> go.Figure:
        """Create radar chart for ADHD user state"""
        categories = ['Mood', 'Energy', 'Focus', 'Sleep Quality', 'Medication Effect', 'Stress (Inverted)']
        
        values = [
            user_state.get('mood', 0.5),
            user_state.get('energy', 0.5),
            user_state.get('focus', 0.5),
            user_state.get('sleepQuality', 0.7),
            1.0 if user_state.get('medicationTaken', False) else 0.0,
            1.0 - user_state.get('stressLevel', 0.5)  # Invert stress so higher is better
        ]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Current State',
            line_color=self.colors['primary'],
            fillcolor=f"rgba(102, 126, 234, 0.3)"
        ))
        
        # Add ideal state for comparison
        ideal_values = [0.8, 0.8, 0.8, 0.9, 1.0, 0.8]
        fig.add_trace(go.Scatterpolar(
            r=ideal_values,
            theta=categories,
            fill='toself',
            name='Ideal State',
            line_color=self.colors['success'],
            fillcolor=f"rgba(40, 167, 69, 0.1)"
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=True,
            title="ADHD State Assessment",
            height=500
        )
        
        return fig
    
    def create_task_distribution_chart(self, tasks: List[Dict[str, Any]]) -> go.Figure:
        """Create distribution chart for tasks by priority and energy"""
        df = pd.DataFrame(tasks)
        
        # Map energy levels to numeric values
        energy_map = {'low': 1, 'medium': 2, 'high': 3}
        df['energy_numeric'] = df['energyRequired'].map(energy_map)
        
        fig = px.scatter(
            df,
            x='importance',
            y='energy_numeric',
            size='estimatedDurationMin',
            color='category',
            hover_name='title',
            hover_data={'estimatedDurationMin': True, 'urgency': True},
            title="Task Distribution: Importance vs Energy Requirements"
        )
        
        fig.update_layout(
            xaxis_title="Importance Level",
            yaxis_title="Energy Required",
            height=500
        )
        
        # Update y-axis labels
        fig.update_yaxes(
            tickmode='array',
            tickvals=[1, 2, 3],
            ticktext=['Low', 'Medium', 'High']
        )
        
        return fig
    
    def create_ml_performance_comparison(self, performance_data: Dict[str, Any]) -> go.Figure:
        """Create comparison chart for ML model performance"""
        methods = performance_data['Method']
        priority_acc = performance_data['Priority Accuracy (%)']
        completion_acc = performance_data['Completion Prediction (%)']
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Priority Accuracy',
            x=methods,
            y=priority_acc,
            marker_color=self.colors['primary'],
            text=[f'{acc}%' for acc in priority_acc],
            textposition='auto',
        ))
        
        fig.add_trace(go.Bar(
            name='Completion Prediction',
            x=methods,
            y=completion_acc,
            marker_color=self.colors['info'],
            text=[f'{acc}%' for acc in completion_acc],
            textposition='auto',
        ))
        
        fig.update_layout(
            title='ML Model Performance Comparison',
            xaxis_title='Method',
            yaxis_title='Accuracy (%)',
            barmode='group',
            height=500,
            showlegend=True
        )
        
        return fig
    
    def create_daily_progress_chart(self, progress_data: pd.DataFrame) -> go.Figure:
        """Create daily progress tracking chart"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Task Completion Rate', 'Mood & Energy Levels', 'Points Earned', 'Medication Consistency'),
            specs=[[{"secondary_y": False}, {"secondary_y": True}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Completion rate
        fig.add_trace(
            go.Scatter(
                x=progress_data['date'],
                y=progress_data['completion_rate'],
                mode='lines+markers',
                name='Completion Rate',
                line=dict(color=self.colors['success'], width=3)
            ),
            row=1, col=1
        )
        
        # Mood and Energy
        fig.add_trace(
            go.Scatter(
                x=progress_data['date'],
                y=progress_data['avg_mood'],
                mode='lines',
                name='Average Mood',
                line=dict(color=self.colors['warning'])
            ),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Scatter(
                x=progress_data['date'],
                y=progress_data['avg_energy'],
                mode='lines',
                name='Average Energy',
                line=dict(color=self.colors['info'])
            ),
            row=1, col=2
        )
        
        # Points earned
        fig.add_trace(
            go.Bar(
                x=progress_data['date'],
                y=progress_data['points_earned'],
                name='Points Earned',
                marker_color=self.colors['primary']
            ),
            row=2, col=1
        )
        
        # Medication consistency
        medication_rate = progress_data.groupby(progress_data['date'].dt.date)['medication_taken'].mean().reset_index()
        fig.add_trace(
            go.Bar(
                x=medication_rate['date'],
                y=medication_rate['medication_taken'],
                name='Medication Rate',
                marker_color=self.colors['danger']
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            title='30-Day ADHD Management Progress',
            height=600,
            showlegend=True
        )
        
        return fig
    
    def create_pomodoro_focus_chart(self, session_data: Dict[str, Any]) -> go.Figure:
        """Create focus pattern chart for Pomodoro session"""
        minutes = list(range(session_data['duration_minutes']))
        focus_pattern = session_data['focus_pattern']
        distraction_events = session_data['distraction_events']
        
        fig = go.Figure()
        
        # Focus line
        fig.add_trace(go.Scatter(
            x=minutes,
            y=focus_pattern,
            mode='lines+markers',
            name='Focus Level',
            line=dict(color=self.colors['success'], width=3),
            fill='tonexty',
            fillcolor=f"rgba(40, 167, 69, 0.2)"
        ))
        
        # Add distraction markers
        for event in distraction_events:
            fig.add_vline(
                x=event['minute'],
                line_dash="dash",
                line_color=self.colors['danger'],
                annotation_text=event['type'].title(),
                annotation_position="top"
            )
        
        # Add focus zones
        fig.add_hrect(
            y0=0.8, y1=1.0,
            fillcolor="rgba(40, 167, 69, 0.1)",
            annotation_text="High Focus", annotation_position="inside topleft",
            line_width=0
        )
        
        fig.add_hrect(
            y0=0.5, y1=0.8,
            fillcolor="rgba(255, 193, 7, 0.1)",
            annotation_text="Medium Focus", annotation_position="inside topleft",
            line_width=0
        )
        
        fig.add_hrect(
            y0=0, y1=0.5,
            fillcolor="rgba(220, 53, 69, 0.1)",
            annotation_text="Low Focus", annotation_position="inside topleft",
            line_width=0
        )
        
        fig.update_layout(
            title=f'Pomodoro Session Focus Pattern ({session_data["duration_minutes"]} minutes)',
            xaxis_title='Time (minutes)',
            yaxis_title='Focus Level',
            height=400,
            yaxis=dict(range=[0, 1])
        )
        
        return fig
    
    def create_feature_importance_chart(self, features: List[str], importance: List[float]) -> go.Figure:
        """Create horizontal bar chart for feature importance"""
        fig = go.Figure()
        
        # Create color gradient based on importance
        colors = [f'rgba(102, 126, 234, {imp})' for imp in importance]
        
        fig.add_trace(go.Bar(
            x=importance,
            y=features,
            orientation='h',
            marker=dict(
                color=colors,
                line=dict(color='rgba(102, 126, 234, 1.0)', width=1)
            ),
            text=[f'{imp:.3f}' for imp in importance],
            textposition='auto'
        ))
        
        fig.update_layout(
            title='ADHD Feature Importance in ML Model',
            xaxis_title='Importance Score',
            yaxis_title='Features',
            height=max(400, len(features) * 25),
            showlegend=False
        )
        
        return fig
    
    def create_success_prediction_scatter(self, tasks_data: List[Dict[str, Any]]) -> go.Figure:
        """Create scatter plot of priority vs success prediction"""
        priorities = [task.get('priorityScore', 0.5) for task in tasks_data]
        success_rates = [task.get('completionLikelihood', 0.5) for task in tasks_data]
        titles = [task.get('title', 'Unknown Task') for task in tasks_data]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=priorities,
            y=success_rates,
            mode='markers',
            marker=dict(
                size=15,
                color=priorities,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Priority Score")
            ),
            text=titles,
            hovertemplate='<b>%{text}</b><br>' +
                         'Priority: %{x:.3f}<br>' +
                         'Success Rate: %{y:.3f}<br>' +
                         '<extra></extra>'
        ))
        
        # Add quadrant lines
        fig.add_hline(y=0.5, line_dash="dash", line_color="gray", opacity=0.5)
        fig.add_vline(x=0.5, line_dash="dash", line_color="gray", opacity=0.5)
        
        # Add quadrant annotations
        fig.add_annotation(x=0.75, y=0.25, text="High Priority<br>Low Success", showarrow=False, opacity=0.7)
        fig.add_annotation(x=0.25, y=0.25, text="Low Priority<br>Low Success", showarrow=False, opacity=0.7)
        fig.add_annotation(x=0.25, y=0.75, text="Low Priority<br>High Success", showarrow=False, opacity=0.7)
        fig.add_annotation(x=0.75, y=0.75, text="High Priority<br>High Success", showarrow=False, opacity=0.7)
        
        fig.update_layout(
            title='Task Priority vs Success Prediction',
            xaxis_title='Priority Score',
            yaxis_title='Success Likelihood',
            height=500
        )
        
        return fig
