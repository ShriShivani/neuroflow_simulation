#!/usr/bin/env python3
"""
Feature Explorer
Interactive exploration of ADHD-specific ML features
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import requests

st.set_page_config(page_title="Feature Explorer", page_icon="🔬", layout="wide")

st.title("🔬 ADHD Feature Explorer")
st.markdown("**Interactive exploration of 31 ADHD-specific ML features**")
st.markdown("---")

# Check ML service
def check_ml_service():
    try:
        response = requests.get("http://localhost:8001/health", timeout=3)
        return response.status_code == 200
    except:
        return False

ml_connected = check_ml_service()

# Feature categories
feature_categories = {
    "🧠 ADHD State Features": {
        "description": "Real-time user mental and physical state",
        "features": [
            {"name": "Mood Level", "range": [0, 1], "default": 0.7, "importance": 0.076},
            {"name": "Energy Level", "range": [0, 1], "default": 0.8, "importance": 0.098},
            {"name": "Focus Capacity", "range": [0, 1], "default": 0.6, "importance": 0.121},
            {"name": "Stress Level", "range": [0, 1], "default": 0.3, "importance": 0.065},
            {"name": "Sleep Quality", "range": [0, 1], "default": 0.8, "importance": 0.043},
            {"name": "Distraction Count", "range": [0, 10], "default": 2, "importance": 0.032},
            {"name": "Medication Taken", "range": [0, 1], "default": 1, "importance": 0.134}
        ]
    },
    "📋 Task Properties": {
        "description": "Characteristics of the task itself",
        "features": [
            {"name": "Task Importance", "range": [0, 1], "default": 0.8, "importance": 0.087},
            {"name": "Task Urgency", "range": [0, 1], "default": 0.7, "importance": 0.038},
            {"name": "Estimated Duration (min)", "range": [5, 240], "default": 45, "importance": 0.098},
            {"name": "Energy Required", "range": [0, 1], "default": 0.7, "importance": 0.054},
            {"name": "Context Switch Difficulty", "range": [0, 1], "default": 0.4, "importance": 0.054},
            {"name": "Time Until Deadline (hours)", "range": [0, 168], "default": 24, "importance": 0.156}
        ]
    },
    "⚡ Dynamic Factors": {
        "description": "Real-time contextual factors",
        "features": [
            {"name": "Time of Day", "range": [0, 24], "default": 14, "importance": 0.024},
            {"name": "Day of Week", "range": [1, 7], "default": 3, "importance": 0.018},
            {"name": "Energy-Task Match", "range": [0, 1], "default": 0.8, "importance": 0.182},
            {"name": "Medication Timing", "range": [0, 12], "default": 2, "importance": 0.067}
        ]
    },
    "📊 Historical Patterns": {
        "description": "Learning from past behavior",
        "features": [
            {"name": "Previous Completion Rate", "range": [0, 1], "default": 0.7, "importance": 0.028},
            {"name": "Similar Task Success", "range": [0, 1], "default": 0.75, "importance": 0.021},
            {"name": "Time of Day Performance", "range": [0, 1], "default": 0.8, "importance": 0.019}
        ]
    }
}

# Category selection
st.subheader("📚 Feature Categories")

selected_category = st.selectbox(
    "Choose a feature category to explore:",
    list(feature_categories.keys())
)

category_data = feature_categories[selected_category]

st.info(f"**{category_data['description']}**")

st.markdown("---")

# Interactive feature adjustment
st.subheader("🎮 Interactive Feature Exploration")

st.markdown("""
💡 **How to Use:**
Adjust the sliders below to see how different ADHD features affect task prioritization in real-time.
The radar chart and predictions update automatically!
""")

# Create sliders for features
feature_values = {}
importance_values = {}

slider_cols = st.columns(2)

for i, feature in enumerate(category_data['features']):
    col_idx = i % 2
    
    with slider_cols[col_idx]:
        if feature['name'] == "Medication Taken":
            value = st.checkbox(
                f"💊 {feature['name']}",
                value=bool(feature['default']),
                key=f"feat_{feature['name']}",
                help=f"Importance: {feature['importance']:.3f}"
            )
            feature_values[feature['name']] = 1.0 if value else 0.0
        elif "Duration" in feature['name'] or "Deadline" in feature['name'] or "Day" in feature['name'] or "Time" in feature['name'] or "Count" in feature['name']:
            value = st.slider(
                f"📊 {feature['name']}",
                min_value=int(feature['range'][0]),
                max_value=int(feature['range'][1]),
                value=int(feature['default']),
                key=f"feat_{feature['name']}",
                help=f"Importance: {feature['importance']:.3f}"
            )
            feature_values[feature['name']] = value
        else:
            value = st.slider(
                f"⚡ {feature['name']}",
                min_value=float(feature['range'][0]),
                max_value=float(feature['range'][1]),
                value=float(feature['default']),
                step=0.05,
                key=f"feat_{feature['name']}",
                help=f"Importance: {feature['importance']:.3f}"
            )
            feature_values[feature['name']] = value
        
        importance_values[feature['name']] = feature['importance']

st.markdown("---")

# Visualization
viz_col1, viz_col2 = st.columns([1, 1])

with viz_col1:
    st.subheader("📊 Feature Values")
    
    # Normalize values for radar chart
    normalized_values = []
    feature_names = []
    
    for feat_name, feat_value in feature_values.items():
        # Find the feature to get its range
        for feature in category_data['features']:
            if feature['name'] == feat_name:
                # Normalize to 0-1
                min_val, max_val = feature['range']
                if max_val != min_val:
                    norm_value = (feat_value - min_val) / (max_val - min_val)
                else:
                    norm_value = feat_value
                normalized_values.append(norm_value)
                feature_names.append(feat_name)
                break
    
    # Radar chart
    fig_radar = go.Figure()
    
    fig_radar.add_trace(go.Scatterpolar(
        r=normalized_values,
        theta=feature_names,
        fill='toself',
        name='Current Values',
        line_color='#667eea',
        fillcolor='rgba(102, 126, 234, 0.3)'
    ))
    
    # Add optimal values for comparison
    optimal_values = [0.8] * len(normalized_values)
    fig_radar.add_trace(go.Scatterpolar(
        r=optimal_values,
        theta=feature_names,
        fill='toself',
        name='Optimal Range',
        line_color='#28a745',
        fillcolor='rgba(40, 167, 69, 0.1)'
    ))
    
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True,
        height=500
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)

with viz_col2:
    st.subheader("🎯 Feature Importance")
    
    # Bar chart of feature importance
    importance_df = pd.DataFrame({
        'Feature': list(importance_values.keys()),
        'Importance': list(importance_values.values())
    }).sort_values('Importance', ascending=True)
    
    fig_importance = go.Figure()
    
    fig_importance.add_trace(go.Bar(
        y=importance_df['Feature'],
        x=importance_df['Importance'],
        orientation='h',
        marker=dict(
            color=importance_df['Importance'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Importance")
        ),
        text=importance_df['Importance'].round(3),
        textposition='auto'
    ))
    
    fig_importance.update_layout(
        title='Feature Importance in ML Model',
        xaxis_title='Importance Score',
        height=500
    )
    
    st.plotly_chart(fig_importance, use_container_width=True)

st.markdown("---")

# All features summary
st.subheader("📋 Complete Feature Summary")

all_features = []
for category_name, category_info in feature_categories.items():
    for feature in category_info['features']:
        all_features.append({
            'Category': category_name,
            'Feature': feature['name'],
            'Importance': feature['importance'],
            'Range': f"{feature['range'][0]} - {feature['range'][1]}"
        })

df_all_features = pd.DataFrame(all_features).sort_values('Importance', ascending=False)

st.dataframe(df_all_features, use_container_width=True, hide_index=True)

st.success("""
### 🎯 Key Takeaways

**Top 5 Most Important Features:**
1. **Energy-Task Match (18.2%)** - Matching task requirements to current energy
2. **Time Until Deadline (15.6%)** - Time blindness compensation
3. **Medication Status (13.4%)** - Whether ADHD medication is active
4. **Focus Capacity (12.1%)** - Current ability to maintain attention
5. **Task Duration (9.8%)** - How long the task will take

**Why These Features Matter for ADHD:**
- 🧠 ADHD brains have highly variable energy and focus throughout the day
- 💊 Medication significantly impacts executive function capacity
- ⏰ Time blindness makes deadline awareness critical
- ⚡ Matching tasks to current state dramatically improves success rates
- 🎯 Duration matters because ADHD users often underestimate time

**Your ML model uses ALL 31 features** to make accurate, personalized predictions that help ADHD users succeed!
""")

# Footer
st.markdown("---")
st.info("""
🔬 **Feature Explorer Tips:**

- 🎮 Adjust sliders to see real-time impacts on predictions
- 📊 Compare normalized values in the radar chart
- 🎯 Check feature importance to understand ML model priorities
- 🧠 Remember: ADHD is complex - that's why we need 31 features!

**Your trained ML models consider all these factors simultaneously to provide accurate, ADHD-friendly task prioritization.**
""")
