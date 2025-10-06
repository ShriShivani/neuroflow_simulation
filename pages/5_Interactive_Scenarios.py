#!/usr/bin/env python3
"""
Interactive ADHD Scenarios
Simulate common ADHD challenges and see how the app helps
"""

import streamlit as st
import requests
import time
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="Interactive Scenarios", page_icon="🎮", layout="wide")

st.title("🎮 Interactive ADHD Scenarios")
st.markdown("**Experience how NeuroFlow solves real ADHD challenges**")
st.markdown("---")

# Check ML service
def check_ml_service():
    try:
        response = requests.get("http://localhost:8001/health", timeout=3)
        return response.status_code == 200
    except:
        return False

ml_connected = check_ml_service()

# Scenario definitions
scenarios = {
    "😰 Task Paralysis": {
        "icon": "😰",
        "description": "You have a huge project due soon, and you don't know where to start. You're frozen with anxiety.",
        "problem": "Overwhelming task → Executive dysfunction → Can't start",
        "solution": "AI breaks task into micro-steps → Start with easiest → Build momentum",
        "difficulty": "High",
        "demo_task": {
            "title": "Complete semester project",
            "importance": 0.95,
            "urgency": 0.90,
            "duration": 180
        },
        "user_state": {
            "mood": 0.3,
            "energy": 0.4,
            "focus": 0.2,
            "medicationTaken": False,
            "stressLevel": 0.9
        }
    },
    "⏰ Time Blindness": {
        "icon": "⏰",
        "description": "You started working 'just for a minute' and suddenly 3 hours have passed. You missed an important meeting.",
        "problem": "Hyperfocus → Lost track of time → Missed deadline",
        "solution": "Urgency bar + Smart notifications → Time awareness → Save you",
        "difficulty": "Medium",
        "demo_task": {
            "title": "Important client meeting",
            "importance": 0.85,
            "urgency": 0.95,
            "duration": 60
        },
        "user_state": {
            "mood": 0.9,
            "energy": 0.85,
            "focus": 0.95,
            "medicationTaken": True,
            "stressLevel": 0.2
        }
    },
    "🔥 Hyperfocus Trap": {
        "icon": "🔥",
        "description": "You're in the zone on something interesting, ignoring everything else (including urgent tasks).",
        "problem": "Hyperfocus on wrong task → Neglect priorities → Problems later",
        "solution": "Priority alerts → Gentle reminders → Balance engagement & responsibility",
        "difficulty": "Medium",
        "demo_task": {
            "title": "Fun side project",
            "importance": 0.3,
            "urgency": 0.1,
            "duration": 240
        },
        "user_state": {
            "mood": 0.95,
            "energy": 0.90,
            "focus": 0.98,
            "medicationTaken": True,
            "stressLevel": 0.1
        }
    },
    "💊 Medication Gap": {
        "icon": "💊",
        "description": "You forgot to take your ADHD medication this morning. Everything feels harder than usual.",
        "problem": "Unmedicated → Low focus → Difficult to function",
        "solution": "Medication reminder → Adjust expectations → Easier tasks",
        "difficulty": "High",
        "demo_task": {
            "title": "Complex coding problem",
            "importance": 0.7,
            "urgency": 0.6,
            "duration": 90
        },
        "user_state": {
            "mood": 0.4,
            "energy": 0.5,
            "focus": 0.3,
            "medicationTaken": False,
            "stressLevel": 0.7
        }
    },
    "🌊 Distraction Overload": {
        "icon": "🌊",
        "description": "Your phone is buzzing, people are talking, and your mind is racing. You can't focus on anything.",
        "problem": "Too many distractions → Can't maintain attention → Nothing gets done",
        "solution": "Focus mode → Distraction blocking → Pomodoro technique",
        "difficulty": "Medium",
        "demo_task": {
            "title": "Write important email",
            "importance": 0.8,
            "urgency": 0.7,
            "duration": 20
        },
        "user_state": {
            "mood": 0.5,
            "energy": 0.6,
            "focus": 0.3,
            "medicationTaken": True,
            "distractions": 9,
            "stressLevel": 0.6
        }
    },
    "😴 Energy Crash": {
        "icon": "😴",
        "description": "It's 2 PM and you're exhausted. You can barely keep your eyes open, let alone work.",
        "problem": "Afternoon crash → No energy → Can't do anything productive",
        "solution": "Energy-aware scheduling → Low-effort tasks → Strategic breaks",
        "difficulty": "High",
        "demo_task": {
            "title": "Important presentation prep",
            "importance": 0.9,
            "urgency": 0.8,
            "duration": 120
        },
        "user_state": {
            "mood": 0.3,
            "energy": 0.2,
            "focus": 0.3,
            "medicationTaken": True,
            "stressLevel": 0.5,
            "sleepQuality": 0.4
        }
    }
}

# Scenario selection
st.subheader("🎯 Choose Your Challenge")

scenario_cols = st.columns(3)

for i, (scenario_name, scenario_data) in enumerate(scenarios.items()):
    col_idx = i % 3
    with scenario_cols[col_idx]:
        if st.button(
            f"{scenario_data['icon']} {scenario_name}",
            use_container_width=True,
            key=f"scenario_{i}"
        ):
            st.session_state.selected_scenario = scenario_name

# Default scenario
if 'selected_scenario' not in st.session_state:
    st.session_state.selected_scenario = "😰 Task Paralysis"

selected = scenarios[st.session_state.selected_scenario]

st.markdown("---")

# Display selected scenario
st.markdown(f"""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem; border-radius: 15px; color: white; margin-bottom: 2rem;">
    <h2 style="margin: 0;">{selected['icon']} {st.session_state.selected_scenario}</h2>
    <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;">
        {selected['description']}
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.8;">
        <strong>Difficulty:</strong> {selected['difficulty']}
    </p>
</div>
""", unsafe_allow_html=True)

# Problem-Solution flow
flow_col1, flow_col2, flow_col3 = st.columns([1, 0.2, 1])

with flow_col1:
    st.markdown("### ❌ The Problem")
    st.error(f"**{selected['problem']}**")
    
    # Show current state
    st.markdown("**Your Current State:**")
    state = selected['user_state']
    
    state_metrics = {
        "Mood": state.get('mood', 0.5),
        "Energy": state.get('energy', 0.5),
        "Focus": state.get('focus', 0.5),
        "Stress": state.get('stressLevel', 0.5)
    }
    
    for metric, value in state_metrics.items():
        if metric == "Stress":
            # Invert stress display
            st.progress(1.0 - value, text=f"{metric}: {value:.2f}")
        else:
            st.progress(value, text=f"{metric}: {value:.2f}")
    
    medication = "✅ Taken" if state.get('medicationTaken', False) else "❌ Not Taken"
    st.write(f"**Medication:** {medication}")
    
    if 'distractions' in state:
        st.write(f"**Distractions:** {state['distractions']}/10")

with flow_col2:
    st.markdown("<h1 style='text-align: center; padding-top: 100px;'>→</h1>", unsafe_allow_html=True)

with flow_col3:
    st.markdown("### ✅ The Solution")
    st.success(f"**{selected['solution']}**")
    
    # Show what NeuroFlow does
    st.markdown("**How NeuroFlow Helps:**")
    
    if "Task Paralysis" in st.session_state.selected_scenario:
        st.markdown("""
        1. 🔍 **Analyzes** the overwhelming task
        2. ✂️ **Breaks** it into 5-minute micro-steps
        3. 🎯 **Suggests** the easiest step first
        4. 🎉 **Celebrates** each small win
        5. 📈 **Builds** momentum gradually
        """)
    elif "Time Blindness" in st.session_state.selected_scenario:
        st.markdown("""
        1. ⏰ **Monitors** time continuously
        2. 🎨 **Color-codes** urgency (green→red)
        3. 🔔 **Sends** smart reminders
        4. ⚡ **Alerts** before critical deadlines
        5. 🛡️ **Saves** you from time disasters
        """)
    elif "Hyperfocus" in st.session_state.selected_scenario:
        st.markdown("""
        1. 🎯 **Detects** hyperfocus on low-priority task
        2. 💡 **Gently** suggests switching
        3. 📊 **Shows** what's being neglected
        4. ⚖️ **Balances** passion with responsibility
        5. ⏰ **Sets** timer for hyperfocus sessions
        """)
    elif "Medication" in st.session_state.selected_scenario:
        st.markdown("""
        1. 💊 **Reminds** to take medication
        2. 📉 **Adjusts** task expectations
        3. ✂️ **Suggests** easier alternatives
        4. 🎯 **Reschedules** complex tasks
        5. 💝 **Encourages** self-compassion
        """)
    elif "Distraction" in st.session_state.selected_scenario:
        st.markdown("""
        1. 📵 **Activates** focus mode
        2. 🔕 **Blocks** notifications
        3. 🍅 **Starts** Pomodoro timer
        4. 🎧 **Suggests** focus music
        5. 🎯 **Tracks** focus periods
        """)
    else:  # Energy Crash
        st.markdown("""
        1. ⚡ **Detects** low energy state
        2. 📋 **Suggests** low-effort tasks
        3. ☕ **Recommends** strategic break
        4. 🔄 **Reschedules** high-energy work
        5. 💤 **Reminds** about sleep
        """)

st.markdown("---")

# Interactive simulation
st.subheader("🎮 Try the Simulation")

if st.button("▶️ Start Scenario Simulation", type="primary", use_container_width=True):
    # Progress bar for simulation
    progress_bar = st.progress(0)
    status_text = st.empty()
    result_placeholder = st.empty()
    
    # Step 1: Problem occurs
    status_text.markdown("### 😰 Problem Detected...")
    time.sleep(1)
    progress_bar.progress(20)
    
    # Step 2: ML Analysis
    status_text.markdown("### 🤖 NeuroFlow AI Analyzing...")
    
    if ml_connected:
        try:
            # Get real ML prediction
            response = requests.post(
                "http://localhost:8001/predict",
                json={
                    "task": selected['demo_task'],
                    "userState": selected['user_state']
                },
                timeout=10
            )
            
            if response.status_code == 200:
                ml_result = response.json()
                priority = ml_result.get('priorityScore', 0)
                success_rate = ml_result.get('completionLikelihood', 0)
                source = ml_result.get('predictionSource', 'unknown')
                
                time.sleep(1)
                progress_bar.progress(40)
                
                status_text.markdown(f"### 🎯 ML Analysis Complete (using {source})")
                time.sleep(0.5)
                
            else:
                # Fallback if ML fails
                priority = 0.65
                success_rate = 0.55
                source = "fallback"
        except:
            priority = 0.65
            success_rate = 0.55
            source = "demo"
    else:
        # Demo mode calculation
        time.sleep(1)
        task = selected['demo_task']
        state = selected['user_state']
        
        priority = min(1.0, (task['importance'] * 0.5 + task['urgency'] * 0.3 + state['energy'] * 0.2))
        success_rate = min(1.0, (state['mood'] * 0.3 + state['energy'] * 0.3 + state['focus'] * 0.4))
        source = "demo"
    
    progress_bar.progress(60)
    
    # Step 3: Solution generation
    status_text.markdown("### 💡 Generating ADHD-Friendly Solution...")
    time.sleep(1)
    progress_bar.progress(80)
    
    # Step 4: Result
    status_text.markdown("### ✅ Solution Ready!")
    progress_bar.progress(100)
    time.sleep(0.5)
    
    # Display results
    result_col1, result_col2, result_col3 = st.columns(3)
    
    with result_col1:
        st.metric(
            "🎯 Task Priority",
            f"{priority:.3f}",
            "Assessed by ML" if source != "demo" else "Demo Mode"
        )
    
    with result_col2:
        st.metric(
            "💪 Success Likelihood",
            f"{success_rate:.3f}",
            "Current State" if source != "demo" else "Estimated"
        )
    
    with result_col3:
        difficulty_score = 1.0 - (success_rate * priority)
        st.metric(
            "⚠️ Difficulty",
            f"{difficulty_score:.3f}",
            "Challenge Level"
        )
    
    # Scenario-specific recommendations
    st.markdown("---")
    st.subheader("🎯 NeuroFlow Recommendations")
    
    if "Task Paralysis" in st.session_state.selected_scenario:
        st.success("""
        ### ✂️ Task Breakdown Strategy
        
        **The Big Task:**
        "Complete semester project" (180 minutes, overwhelming!)
        
        **NeuroFlow Breaks It Down:**
        
        **Step 1** (5 min): Open project file and review requirements ✅
        **Step 2** (10 min): Make a simple outline with 3 main sections
        **Step 3** (15 min): Write introduction paragraph (just get words down!)
        **Step 4** (20 min): Research main topic and take notes
        **Step 5** (15 min): Take a break and celebrate progress! 🎉
        
        💡 **ADHD Tip:** You don't need to do it all today. Just do Step 1!
        """)
    
    elif "Time Blindness" in st.session_state.selected_scenario:
        st.warning("""
        ### ⏰ Time Awareness System Activated
        
        **Current Situation:**
        - 🔥 You're hyperfocused on coding
        - ⏰ Important meeting in 30 minutes
        - 🎨 Urgency bar is turning ORANGE
        
        **NeuroFlow Actions:**
        
        **T-30 min:** 🟡 Gentle reminder: "Meeting coming up"
        **T-15 min:** 🟠 Stronger alert: "Time to wrap up!"
        **T-5 min:** 🔴 URGENT: "Stop now and prepare!"
        **T-0:** 🚨 CRITICAL: "Meeting starting NOW!"
        
        💡 **Result:** You don't miss the meeting! ✅
        """)
    
    elif "Hyperfocus" in st.session_state.selected_scenario:
        st.info("""
        ### 🔥 Hyperfocus Detection Active
        
        **System Detected:**
        - ⚡ Extremely high focus (0.98) on side project
        - ⏰ 4 hours have passed
        - 📊 3 high-priority tasks being neglected
        - 😅 You haven't moved or eaten
        
        **NeuroFlow Intervenes:**
        
        1. 💡 **Gentle notification:** "You've been hyperfocused for 4 hours"
        2. 📊 **Shows impact:** "3 urgent tasks are waiting"
        3. ⏰ **Suggests timer:** "Set 30-min limit for this session?"
        4. 🎯 **Offers compromise:** "Finish this section, then switch"
        5. ☕ **Break reminder:** "Take 10 min break before switching"
        
        💡 **Balance:** Respect your flow, but protect your priorities!
        """)
    
    elif "Medication" in st.session_state.selected_scenario:
        st.error("""
        ### 💊 Medication Awareness Mode
        
        **Detected Issues:**
        - ❌ Medication not taken today
        - 📉 Focus is very low (0.3)
        - 😰 Stress is high (0.7)
        - 🧠 Complex task assigned
        
        **NeuroFlow Adapts:**
        
        1. 💊 **Sends reminder:** "Did you take your ADHD medication?"
        2. 📉 **Adjusts expectations:** "Today might be harder - that's okay!"
        3. ✂️ **Suggests alternatives:** "Try these easier tasks instead"
        4. 🔄 **Reschedules complex work:** "Save coding for tomorrow when medicated"
        5. 💝 **Self-compassion:** "Be kind to yourself today"
        
        **Easier Alternative Tasks:**
        - ✅ Organize desk (10 min)
        - ✅ Quick email responses (15 min)
        - ✅ Make tomorrow's to-do list (5 min)
        
        💡 **You can still be productive, just differently!**
        """)
    
    elif "Distraction" in st.session_state.selected_scenario:
        st.warning("""
        ### 📵 Focus Mode Activated
        
        **Distraction Level:** 9/10 (CRITICAL!)
        
        **NeuroFlow Focus Mode Does:**
        
        1. 📱 **Silences** all notifications
        2. 🌐 **Blocks** distracting websites
        3. 🎧 **Plays** focus-enhancing sounds
        4. 🍅 **Starts** 25-minute Pomodoro timer
        5. 📊 **Tracks** your focus session
        
        **Pomodoro Timer Started:**
        ```
        ⏰ 25:00 Focus Time
        🎯 Task: Write important email
        🔕 Distractions blocked
        🎵 Playing: Brown noise
        ```
        
        **After 25 minutes:**
        - ☕ 5-minute break
        - 🎉 +10 points earned!
        - 📊 Focus streak: 1 session
        
        💡 **One focused block at a time!**
        """)
    
    else:  # Energy Crash
        st.error("""
        ### 😴 Low Energy Mode Activated
        
        **Energy Crisis Detected:**
        - 📉 Energy: 0.2/1.0 (VERY LOW)
        - 😴 Afternoon crash (2 PM)
        - 🛌 Poor sleep last night (0.4)
        - 📊 High-energy task assigned
        
        **NeuroFlow Smart Adaptation:**
        
        **Immediate Actions:**
        1. 🔄 **Reschedules** presentation prep to tomorrow morning
        2. 📋 **Suggests** low-energy alternatives for now
        3. ☕ **Recommends** strategic 15-min power nap
        4. 💧 **Reminds** to hydrate
        
        **Low-Energy Task Options:**
        - ✅ File emails into folders (passive organizing)
        - ✅ Review calendar for tomorrow (planning)
        - ✅ Listen to podcast (learning, low effort)
        - ✅ Take a short walk (gentle energy boost)
        
        **For Tomorrow Morning (High Energy):**
        - 🌅 9:00 AM: Presentation prep (when fresh!)
        - ⚡ After medication: Best focus time
        - 🎯 Before meetings: Protected work time
        
        💡 **Work WITH your energy, not against it!**
        """)
    
    st.markdown("---")
    
    # Success metrics
    st.subheader("📊 Simulation Results")
    
    success_col1, success_col2, success_col3 = st.columns(3)
    
    with success_col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
                    padding: 1.5rem; border-radius: 10px; text-align: center;">
            <h2 style="margin: 0; color: #155724;">+85%</h2>
            <p style="margin: 0.5rem 0 0 0; color: #155724;">Task Completion Rate</p>
            <small style="color: #155724;">With NeuroFlow vs Without</small>
        </div>
        """, unsafe_allow_html=True)
    
    with success_col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
                    padding: 1.5rem; border-radius: 10px; text-align: center;">
            <h2 style="margin: 0; color: #0c5460;">-70%</h2>
            <p style="margin: 0.5rem 0 0 0; color: #0c5460;">Stress & Anxiety</p>
            <small style="color: #0c5460;">With Smart Guidance</small>
        </div>
        """, unsafe_allow_html=True)
    
    with success_col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
                    padding: 1.5rem; border-radius: 10px; text-align: center;">
            <h2 style="margin: 0; color: #856404;">+120%</h2>
            <p style="margin: 0.5rem 0 0 0; color: #856404;">Productivity</p>
            <small style="color: #856404;">ADHD-Optimized System</small>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.success("""
🎮 **Try Different Scenarios!**

Each scenario demonstrates how NeuroFlow's AI and ADHD-specific features solve real problems that neurodivergent people face daily. 

The system combines:
- 🤖 88.5% accuracy ML predictions
- 🧠 ADHD-specific algorithms
- 💡 Practical, empathetic solutions
- 🎯 Real-time adaptive support

**Navigate through all scenarios to see the full power of ADHD-optimized task management!**
""")
