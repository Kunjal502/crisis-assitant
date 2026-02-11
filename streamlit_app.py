import streamlit as st
from schemas.agent_state_schema import AgentState
from nodes.reasoning_node import reasoning_node
from nodes.response_node import response_node
import json
import time

# Page configuration
st.set_page_config(
    page_title="💸 Financial Crisis Support Assistant",
    page_icon="💸",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown(
    """
    <h1 style="text-align:center;">💸 Financial Crisis Support Assistant</h1>
    <p style="text-align:center; color:gray;">
    Calm guidance during financial stress - Chat with me!
    </p>
    """,
    unsafe_allow_html=True
)
st.divider()

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add welcome message
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I'm your Financial Crisis Assistant. Tell me about your financial situation.",
        "emergency": False
    })

# Initialize step tracking
if "current_step_index" not in st.session_state:
    st.session_state.current_step_index = 0
    
if "all_steps" not in st.session_state:
    st.session_state.all_steps = []
    
if "calming_completed" not in st.session_state:
    st.session_state.calming_completed = False
    
if "user_situation" not in st.session_state:
    st.session_state.user_situation = None

if "timer_running" not in st.session_state:
    st.session_state.timer_running = False

if "timer_remaining" not in st.session_state:
    st.session_state.timer_remaining = 0

if "timer_step_id" not in st.session_state:
    st.session_state.timer_step_id = None

if "timer_last_tick" not in st.session_state:
    st.session_state.timer_last_tick = None

# Sidebar with settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    st.markdown("### Steps Configuration")
    max_steps = st.slider("Max reasoning steps", 3, 7, 5, help="Maximum number of action steps (optimal is 5)")
    
    st.markdown("### Mode")
    emergency_mode = st.checkbox("🚨 Emergency mode", value=False, help="Enables up to 7 steps and priority support")
    
    st.markdown("### Display")
    show_details = st.checkbox("📊 Show detailed analysis", value=True, help="Show JSON details in expandable section")
    
    st.divider()
    
    if st.button("🗑️ Clear Chat History", use_container_width=True, type="secondary"):
        st.session_state.messages = [{
            "role": "assistant",
            "content": "Chat cleared. What financial challenge are you facing?",
            "emergency": False
        }]
        st.session_state.current_step_index = 0
        st.session_state.all_steps = []
        st.session_state.calming_completed = False
        st.session_state.user_situation = None
        st.rerun()
    
    st.divider()
    st.markdown("### 📋 About")
    st.info("**Financial Crisis Assistant**\n\nStep-by-step guidance for financial problems with calming exercises and actionable solutions.")
    
    st.markdown("### 💡 I can help with:")
    st.markdown("""
    - 🚗 Lost/stolen valuables (car, phone)
    - 💸 Salary delays, income loss
    - 💳 Debt, loan, EMI issues
    - 🏥 Medical bills & expenses
    - ⚠️ Financial fraud & scams
    - 📉 Budget management
    """)
    
    st.divider()
    st.caption("⚠️ Guidance only, not professional advice")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Show emergency badge
        if message.get("emergency"):
            st.error("🚨 EMERGENCY SUPPORT RECOMMENDED")
        
        # Show detailed analysis if available
        if show_details and message.get("details"):
            with st.expander("📊 View detailed analysis"):
                details = message["details"]
                
                if isinstance(details, dict):
                    # Show structured output
                    if "crisis_type" in details:
                        st.markdown(f"**Crisis Type:** {details.get('crisis_type', 'N/A')}")
                    
                    if "severity" in details:
                        severity = details.get("severity", "low")
                        if severity == "high":
                            st.error(f"**Severity:** {severity.upper()}")
                        elif severity == "medium":
                            st.warning(f"**Severity:** {severity.capitalize()}")
                        else:
                            st.success(f"**Severity:** {severity.capitalize()}")

                    if "mood" in details:
                        st.markdown(f"**Detected Mood:** {details.get('mood', 'overwhelmed')}")
                    
                    if "calming_steps" in details:
                        st.markdown("**Calming Steps:**")
                        for i, step in enumerate(details.get("calming_steps", []), 1):
                            instruction = step.get("instruction", "")
                            duration = step.get("duration_seconds", "")
                            st.markdown(f"{i}. {instruction} ({duration}s)")

                    if "action_steps" in details:
                        st.markdown("**Action Steps:**")
                        for i, step in enumerate(details.get("action_steps", []), 1):
                            st.markdown(f"{i}. {step.get('step', '')}")
                    
                    if "final_advice" in details:
                        st.markdown(f"**Final Advice:** {details['final_advice']}")
                    
                    # Show raw JSON
                    st.json(details)
                else:
                    st.write(details)

# Chat input
user_input = st.chat_input("Describe your financial situation... (e.g., 'Salary delayed, EMI pending')")

if user_input:
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Process with assistant
    with st.chat_message("assistant"):
        with st.spinner("🤔 Analyzing..."):
            try:
                # Create state
                step_limit = 7 if emergency_mode else 5
                state = AgentState(
                    user_input=user_input,
                    steps=min(max_steps, step_limit),
                    emergency=emergency_mode
                )
                
                # Run reasoning node
                final_state = reasoning_node(state)
                output = final_state.output
                
                # Check if not financial issue
                if output.get("not_financial"):
                    st.info("Main financial crisis situations me help karta hu. Apni financial problem batao.")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "Main financial crisis situations me help karta hu. Apni financial problem batao.",
                        "emergency": False
                    })
                
                # Check for error
                elif "error" in output:
                    st.error("Kuch issue aa raha hai. Phir se try karo.")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "Kuch issue aa raha hai. Phir se try karo.",
                        "emergency": False
                    })
                
                else:
                    # Store situation and steps
                    st.session_state.user_situation = output
                    st.session_state.all_steps = output.get("action_steps", [])
                    st.session_state.current_step_index = 0
                    st.session_state.calming_completed = False
                    
                    crisis = output.get('crisis_type', 'Financial situation')
                    severity = output.get('severity', 'medium')
                    is_emergency = severity == "high" or final_state.emergency_triggered
                    
                    # Show situation
                    if is_emergency:
                        st.error(f"🚨 **Urgent:** {crisis}")
                        if "emergency_contacts" in output:
                            st.warning("**Emergency Contacts:**")
                            for ct, ci in output["emergency_contacts"].items():
                                st.write(f"📞 {ct}: {ci}")
                    else:
                        st.info(f"**Situation:** {crisis}")
                    
                    # Show mood and FIRST calming step only
                    mood = output.get("mood", "overwhelmed")
                    mood_heading = {
                        "panic": "🧘 Panic me ho? Pehle breathing karo",
                        "anxious": "🧘 Anxiety kam karte hain",
                        "depressed": "🧘 Thoda stable feel karne ke steps",
                        "angry": "🧘 Anger settle karte hain",
                        "calm": "🧘 Calm ho, bas ek steady step",
                        "overwhelmed": "🧘 Overwhelmed feel ho raha hai? Pehle calm ho jao"
                    }.get(mood, "🧘 Pehle thoda calm ho jao")

                    st.caption(f"Mood detected: {mood}")

                    # Show FIRST calming step only
                    calming_steps = output.get("calming_steps", [])
                    if calming_steps and len(calming_steps) > 0:
                        first_calm = calming_steps[0]
                        instruction = first_calm.get("instruction", "")
                        duration = first_calm.get("duration_seconds", 20)
                        
                        st.markdown(f"### {mood_heading}")
                        st.write(instruction)
                        st.write(f"**Duration:** {duration} seconds")
                        
                        # Timer
                        if st.button(f"▶️ Start {duration}s Timer", key="calm_timer_initial"):
                            timer_placeholder = st.empty()
                            progress_bar = st.progress(0)
                            
                            for remaining in range(duration, 0, -1):
                                timer_placeholder.markdown(f"### ⏱️ {remaining}s")
                                progress_bar.progress((duration - remaining) / duration)
                                time.sleep(1)
                            
                            timer_placeholder.markdown("### ✅ Done!")
                            progress_bar.progress(1.0)
                            st.session_state.calming_completed = True
                            st.success("Great! Ab aage badhte hain.")
                    
                    # Save to history
                    msg = f"Situation: {crisis}\n\nPehle calm down karo, phir steps follow karenge."
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": msg,
                        "emergency": is_emergency,
                        "details": output if show_details else None
                    })
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Technical issue hai. Phir se try karo.",
                    "emergency": False
                })

# Show current step if available
if st.session_state.all_steps and st.session_state.current_step_index < len(st.session_state.all_steps):
    st.markdown("---")
    st.markdown("### 📋 One Small Step")
    
    current = st.session_state.all_steps[st.session_state.current_step_index]
    step_num = st.session_state.current_step_index + 1
    total_steps = min(len(st.session_state.all_steps), 7)
    
    st.markdown(f"**Step {step_num} of {total_steps}**")
    st.caption("Take it slowly. Focus on just this one step.")
    st.info(current.get("step", ""))
    
    priority = current.get("priority", "medium")
    est_time = current.get("estimated_time_minutes", 0)
    
    priority_emoji = "🔴" if priority == "high" else "🟡"
    st.caption(f"{priority_emoji} Priority: {priority} | Estimated: {est_time} min")

    if est_time and est_time > 0:
        total_seconds = int(est_time * 60)
        step_timer_id = f"step_{step_num}"

        timer_cols = st.columns(3)
        with timer_cols[0]:
            if st.button(f"▶️ Start {est_time} min", key=f"start_{step_num}", use_container_width=True):
                st.session_state.timer_running = True
                st.session_state.timer_remaining = total_seconds
                st.session_state.timer_step_id = step_timer_id
                st.session_state.timer_last_tick = time.time()
                st.rerun()

        with timer_cols[1]:
            if st.button("⏸️ Pause", key=f"pause_{step_num}", use_container_width=True):
                if st.session_state.timer_step_id == step_timer_id:
                    st.session_state.timer_running = False
                    st.session_state.timer_last_tick = None
                    st.rerun()

        with timer_cols[2]:
            if st.button("🔄 Reset", key=f"reset_{step_num}", use_container_width=True):
                if st.session_state.timer_step_id == step_timer_id:
                    st.session_state.timer_running = False
                    st.session_state.timer_remaining = 0
                    st.session_state.timer_step_id = None
                    st.session_state.timer_last_tick = None
                    st.rerun()

        if st.session_state.timer_step_id == step_timer_id:
            timer_placeholder = st.empty()
            progress_bar = st.progress(0)

            if st.session_state.timer_running and st.session_state.timer_last_tick:
                elapsed = int(time.time() - st.session_state.timer_last_tick)
                if elapsed > 0:
                    st.session_state.timer_remaining = max(0, st.session_state.timer_remaining - elapsed)
                    st.session_state.timer_last_tick = time.time()

            remaining = st.session_state.timer_remaining
            minutes = remaining // 60
            seconds = remaining % 60
            timer_placeholder.markdown(f"### ⏱️ {minutes:02d}:{seconds:02d}")
            progress_bar.progress((total_seconds - remaining) / total_seconds if total_seconds else 0)

            if remaining == 0 and st.session_state.timer_step_id == step_timer_id:
                st.session_state.timer_running = False
                st.session_state.timer_step_id = None
                st.session_state.timer_last_tick = None
                timer_placeholder.markdown("### ✅ Time complete!")
                progress_bar.progress(1.0)
                st.success("Timer finished. Take a breath and move to the next step when ready.")
            elif st.session_state.timer_running:
                time.sleep(1)
                st.rerun()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Step Complete", key=f"complete_{step_num}", use_container_width=True):
            st.session_state.current_step_index += 1
            
            # Check if more steps
            if st.session_state.current_step_index < len(st.session_state.all_steps):
                st.success("Great! Next step loading...")
                st.rerun()
            else:
                st.success("🎉 All steps complete! Bahut acche!")
                st.balloons()
                if st.session_state.user_situation:
                    advice = st.session_state.user_situation.get("final_advice", "")
                    st.info(f"💡 {advice}")
    
    with col2:
        if st.button("🔄 Need Help", key=f"help_{step_num}", use_container_width=True):
            # Re-evaluate
            with st.spinner("Re-evaluating..."):
                reevaluation_prompt = f"""
User is stuck on this step: {current.get("step", "")}

Original situation: {st.session_state.user_situation.get("crisis_type", "")}

Provide ONE alternative step or break this down into smaller actions. Respond with JSON:
{{
    "alternative_step": "simpler alternative action",
    "priority": "high/medium",
    "estimated_time_minutes": 10
}}
"""
                try:
                    from llm.groq_client import call_groq
                    from utils.json_formatter import safe_json_parse
                    
                    raw = call_groq(reevaluation_prompt)
                    parsed = safe_json_parse(raw)
                    
                    if "alternative_step" in parsed:
                        st.info(f"**Alternative:** {parsed['alternative_step']}")
                        st.caption(f"Estimated: {parsed.get('estimated_time_minutes', 10)} min")
                except:
                    st.info("Is step ko chhote parts me break karo aur ek ek karke karo.")

# Footer
st.divider()
st.caption("💡 This tool provides guidance only and is not professional financial advice. Always consult verified financial experts for critical decisions.")
