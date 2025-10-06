#!/usr/bin/env python3
"""
ADHD State Simulator
Interactive simulation of different ADHD states and their effects
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="ADHD State Simulator", page_icon="🧠", layout="wide")

st.title("🧠 ADHD State Simulator")
st.markdown("**Explore how different ADHD states affect task performance**")
st.markdown("---")

# ADHD State presets
adhd_scenarios = {
    "🌅 Morning Medication Peak": {
        "description": "High focus and energy after taking ADHD medication in the morning",
        "state": {
            "mood": 0.85,
            "energy": 0.90,
            "focus": 0.88,
            "medicationTaken": True,
            "distractions": 1,
            "stressLevel": 0.20,
            "sleepQuality": 0.85
        },
        "best_for": ["Complex problem-solving", "Important meetings", "Creative work", "Deep focus tasks"],
        "avoid": ["Routine busywork", "Simple admin tasks"],
        "color": "success"
    },
    "😴 Afternoon Energy Crash": {
        "description": "Energy dip and difficulty focusing in the afternoon, even with medication",
        "state": {
            "mood": 0.45,
            "energy": 0.30,
            "focus": 0.35,
            "medicationTaken": True,
            "distractions": 5,
            "stressLevel": 0.60,
            "sleepQuality": 0.60
        },
        "best_for": ["Email responses", "Filing/organizing", "Planning tomorrow", "Taking breaks"],
        "avoid": ["Complex tasks", "Important decisions", "New learning"],
        "color": "warning"
    },
    "🔥 Hyperfocus Mode": {
        "description": "Intense concentration on engaging tasks - hard to switch but highly productive",
        "state": {
            "mood": 0.92,
            "energy": 0.85,
            "focus": 0.98,
            "medicationTaken": True,
            "distractions": 0,
            "stressLevel": 0.15,
            "sleepQuality": 0.90
        },
        "best_for": ["Passion projects", "Creative flow", "Deep research", "Coding sessions"],
        "avoid": ["Time-sensitive tasks (might lose track)", "Tasks requiring switching"],
        "color": "info"
    },
    "😰 Executive Dysfunction": {
        "description": "Difficulty starting tasks, making decisions, or maintaining focus",
        "state": {
            "mood": 0.25,
            "energy": 0.35,
            "focus": 0.20,
            "medicationTaken": False,
            "distractions": 8,
            "stressLevel": 0.85,
            "sleepQuality": 0.30
        },
        "best_for": ["Micro-tasks (< 5 min)", "Self-care", "Body doubling", "Asking for help"],
        "avoid": ["New complex tasks", "High-stakes decisions", "Multitasking"],
        "color": "error"
    },
    "💊 Unmedicated Morning": {
        "description": "Managing ADHD without medication - requires extra strategies",
        "state": {
            "mood": 0.50,
            "energy": 0.55,
            "focus": 0.40,
            "medicationTaken": False,
            "distractions": 6,
            "stressLevel": 0.65,
            "sleepQuality": 0.70
        },
        "best_for": ["Structured routines", "Physical activity", "Shorter tasks", "External accountability"],
        "avoid": ["Open-ended tasks", "Long meetings", "Boring admin work"],
        "color": "warning"
    },
    "🌙 Evening Wind-Down": {
        "description": "Medication wearing off, tired but might have evening energy spike",
        "state": {
            "mood": 0.60,
            "energy": 0.50,
            "focus": 0.45,
            "medicationTaken": False,
            "distractions": 4,
            "stressLevel": 0.40,
            "sleepQuality": 0.75
        },
        "best_for": ["Reflection/journaling", "Planning", "Creative hobbies", "Relaxation"],
        "avoid": ["Critical work", "Starting new projects", "Screen-heavy tasks"],
        "color": "info"
    }
}

# Scenario selection
st.subheader("🎯 Choose ADHD Scenario")

scenario_names = list(adhd_scenarios.keys())
selected_scenario = st.selectbox(
    "Select a scenario to explore:",
    scenario_names,
    help="Each scenario represents a common ADHD state throughout the day"
)

scenario = adhd_scenarios[selected_scenario]

# Display scenario info
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 2rem; border-radius: 15px; color: white; margin-bottom: 1rem;">
        <h2 style="margin: 0;">{selected_scenario}</h2>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;">
            {scenario['description']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # State visualization
    state = scenario['state']
    
    st.subheader("📊 State Metrics")
    
    state_col1, state_col2, state_col3, state_col4 = st.columns(4)
    
    with state_col1:
        st.metric("Mood", f"{state['mood']:.2f}", 
                 delta=f"{(state['mood']-0.5)*100:.0f}%" if state['mood'] != 0.5 else None)
        st.metric("Energy", f"{state['energy']:.2f}",
                 delta=f"{(state['energy']-0.5)*100:.0f}%" if state['energy'] != 0.5 else None)
    
    with state_col2:
        st.metric("Focus", f"{state['focus']:.2f}",
                 delta=f"{(state['focus']-0.5)*100:.0f}%" if state['focus'] != 0.5 else None)
        st.metric("Sleep Quality", f"{state['sleepQuality']:.2f}",
                 delta=f"{(state['sleepQuality']-0.7)*100:.0f}%" if state['sleepQuality'] != 0.7 else None)
    
    with state_col3:
        st.metric("Stress Level", f"{state['stressLevel']:.2f}",
                 delta=f"{(0.5-state['stressLevel'])*100:.0f}%" if state['stressLevel'] != 0.5 else None,
                 delta_color="inverse")
        st.metric("Distractions", state['distractions'])
    
    with state_col4:
        medication_status = "✅ Yes" if state['medicationTaken'] else "❌ No"
        st.metric("Medication", medication_status)
        
        # Overall readiness score
        readiness = (state['mood'] + state['energy'] + state['focus'] + 
                    (1 - state['stressLevel']) + state['sleepQuality']) / 5
        st.metric("Overall Readiness", f"{readiness:.2f}")

with col2:
    # Radar chart
    st.subheader("🎯 State Radar")
    
    categories = ['Mood', 'Energy', 'Focus', 'Sleep', 'Med Effect', 'Stress (inv)']
    values = [
        state['mood'],
        state['energy'],
        state['focus'],
        state['sleepQuality'],
        1.0 if state['medicationTaken'] else 0.0,
        1.0 - state['stressLevel']
    ]
    
    fig_radar = go.Figure()
    
    fig_radar.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Current State',
        line_color='#667eea',
        fillcolor='rgba(102, 126, 234, 0.3)'
    ))
    
    # Add ideal state
    ideal_values = [0.8, 0.8, 0.8, 0.9, 1.0, 0.8]
    fig_radar.add_trace(go.Scatterpolar(
        r=ideal_values,
        theta=categories,
        fill='toself',
        name='Ideal State',
        line_color='#28a745',
        fillcolor='rgba(40, 167, 69, 0.1)'
    ))
    
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True,
        height=400
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)

st.markdown("---")

# Recommendations
rec_col1, rec_col2 = st.columns(2)

with rec_col1:
    st.subheader("✅ Best Task Types")
    for task in scenario['best_for']:
        st.success(f"✓ {task}")

with rec_col2:
    st.subheader("❌ Tasks to Avoid")
    for task in scenario['avoid']:
        st.error(f"✗ {task}")

st.markdown("---")

# Interactive state customization
st.subheader("🎨 Customize State Parameters")

st.info("💡 Adjust the sliders below to create your own custom ADHD state and see recommendations change in real-time!")

custom_col1, custom_col2, custom_col3 = st.columns(3)

with custom_col1:
    custom_mood = st.slider("Custom Mood", 0.0, 1.0, state['mood'], 0.05, key="custom_mood")
    custom_energy = st.slider("Custom Energy", 0.0, 1.0, state['energy'], 0.05, key="custom_energy")
    custom_focus = st.slider("Custom Focus", 0.0, 1.0, state['focus'], 0.05, key="custom_focus")

with custom_col2:
    custom_sleep = st.slider("Custom Sleep Quality", 0.0, 1.0, state['sleepQuality'], 0.05, key="custom_sleep")
    custom_stress = st.slider("Custom Stress", 0.0, 1.0, state['stressLevel'], 0.05, key="custom_stress")
    custom_distractions = st.slider("Custom Distractions", 0, 10, state['distractions'], key="custom_dist")

with custom_col3:
    custom_medication = st.checkbox("Custom Medication Taken", state['medicationTaken'], key="custom_med")
    
    # Calculate custom readiness
    custom_readiness = (custom_mood + custom_energy + custom_focus + 
                       (1 - custom_stress) + custom_sleep) / 5
    
    st.metric("Custom Readiness Score", f"{custom_readiness:.3f}")
    
    if custom_readiness > 0.8:
        st.success("🔥 Excellent state for challenging tasks!")
    elif custom_readiness > 0.6:
        st.info("👍 Good state for moderate tasks")
    elif custom_readiness > 0.4:
        st.warning("⚠️ Moderate state - be strategic")
    else:
        st.error("😔 Challenging state - focus on self-care")

# Generate recommendations based on custom state
if st.button("🎯 Generate Recommendations for Custom State", type="primary"):
    st.subheader("📋 Custom State Recommendations")
    
    recommendations = []
    warnings = []
    
    # Energy-based recommendations
    if custom_energy > 0.7 and custom_focus > 0.7:
        recommendations.append("✅ Perfect for high-energy, complex tasks")
        recommendations.append("✅ Tackle your most challenging work now")
    elif custom_energy < 0.4:
        recommendations.append("⚡ Low energy - focus on low-effort tasks")
        warnings.append("❌ Avoid starting new complex projects")
    
    # Medication recommendations
    if not custom_medication:
        recommendations.append("💊 Consider taking ADHD medication if prescribed")
        warnings.append("⚠️ Unmedicated - use extra structure and support")
    
    # Stress recommendations
    if custom_stress > 0.6:
        recommendations.append("🧘 High stress detected - try breathing exercises")
        warnings.append("❌ Not ideal for high-stakes decisions")
    
    # Distraction recommendations
    if custom_distractions > 5:
        recommendations.append("📵 Too many distractions - find a quieter space")
        recommendations.append("🎧 Use noise-cancelling headphones or white noise")
    
    # Sleep recommendations
    if custom_sleep < 0.5:
        recommendations.append("😴 Poor sleep - prioritize rest today")
        warnings.append("❌ Avoid complex problem-solving")
    
    # Focus recommendations
    if custom_focus > 0.8:
        recommendations.append("🎯 Excellent focus - this is hyperfocus territory!")
        recommendations.append("⏰ Set timers to avoid losing track of time")
    elif custom_focus < 0.4:
        recommendations.append("🍅 Try Pomodoro technique (25min focus blocks)")
        recommendations.append("🔄 Break tasks into 5-minute micro-tasks")
    
    # Display recommendations
    col_rec1, col_rec2 = st.columns(2)
    
    with col_rec1:
        st.markdown("**✅ Recommendations:**")
        for rec in recommendations[:5]:
            st.markdown(rec)
    
    with col_rec2:
        st.markdown("**⚠️ Cautions:**")
        for warn in warnings[:5]:
            st.markdown(warn)

# Daily state simulation
st.markdown("---")
st.subheader("📈 Daily ADHD State Simulation")

st.info("💡 This shows how a typical ADHD user's state might change throughout the day")

# Generate daily state data
hours = list(range(6, 24))  # 6 AM to 11 PM
daily_data = []

for hour in hours:
    # Morning peak (medication effect)
    if 8 <= hour <= 11:
        base_energy = 0.8
        base_focus = 0.85
        base_mood = 0.75
    # Afternoon dip
    elif 13 <= hour <= 16:
        base_energy = 0.4
        base_focus = 0.45
        base_mood = 0.55
    # Evening recovery
    elif 17 <= hour <= 20:
        base_energy = 0.6
        base_focus = 0.5
        base_mood = 0.65
    # Night
    else:
        base_energy = 0.5
        base_focus = 0.4
        base_mood = 0.6
    
    # Add some random variation
    daily_data.append({
        'Hour': f"{hour}:00",
        'Energy': base_energy + np.random.uniform(-0.1, 0.1),
        'Focus': base_focus + np.random.uniform(-0.1, 0.1),
        'Mood': base_mood + np.random.uniform(-0.1, 0.1)
    })

df_daily = pd.DataFrame(daily_data)

fig_daily = go.Figure()

fig_daily.add_trace(go.Scatter(
    x=df_daily['Hour'],
    y=df_daily['Energy'],
    mode='lines+markers',
    name='Energy',
    line=dict(color='#ff6b6b', width=3)
))

fig_daily.add_trace(go.Scatter(
    x=df_daily['Hour'],
    y=df_daily['Focus'],
    mode='lines+markers',
    name='Focus',
    line=dict(color='#4ecdc4', width=3)
))

fig_daily.add_trace(go.Scatter(
    x=df_daily['Hour'],
    y=df_daily['Mood'],
    mode='lines+markers',
    name='Mood',
    line=dict(color='#95e1d3', width=3)
))

# Add medication marker
fig_daily.add_vline(
    x=2, 
    line_dash="dash", 
    line_color="purple", 
    annotation_text="💊 Medication", 
    annotation_position="top"
)

# Add typical challenge zones - FIXED
fig_daily.add_hrect(
    y0=0, 
    y1=0.4, 
    fillcolor="rgba(255, 107, 107, 0.1)", 
    annotation_text="Low State", 
    annotation_position="top left",  # FIXED: changed from "inside topleft"
    line_width=0
)

fig_daily.add_hrect(
    y0=0.7, 
    y1=1.0, 
    fillcolor="rgba(78, 205, 196, 0.1)", 
    annotation_text="Peak State", 
    annotation_position="top left",  # FIXED: changed from "inside topleft"
    line_width=0
)

fig_daily.update_layout(
    title='Typical Daily ADHD State Progression',
    xaxis_title='Time of Day',
    yaxis_title='State Level',
    height=500,
    hovermode='x unified'
)

st.plotly_chart(fig_daily, use_container_width=True)

# Tips
st.markdown("---")
st.success("""
### 💡 Using State Awareness to Your Advantage

**Morning (6-12):** Medication peak - tackle complex, important tasks
**Afternoon (12-17):** Energy dip - handle routine tasks, take breaks
**Evening (17-22):** Variable - good for creative work or planning

**Key Strategies:**
- 📊 Track your patterns over time
- 💊 Time important tasks with medication peak
- 🔄 Have backup tasks for low-energy periods  
- 🎯 Be flexible and compassionate with yourself
- ⏰ Use external structure (timers, alarms, routines)
""")
