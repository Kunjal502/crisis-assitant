from schemas.agent_state_schema import AgentState
from llm.groq_client import call_groq
from utils.json_formatter import safe_json_parse
from emergency.financial_resources import get_emergency_contacts

def reasoning_node(state: AgentState) -> AgentState:
    # Optimal 5 steps, max 7 for emergency
    optimal_steps = 5
    max_steps = 7 if state.emergency else 5
    
    steps = min(state.steps, max_steps)

    prompt = f"""
You are a FINANCIAL CRISIS support assistant. You ONLY help with FINANCIAL and MONEY-RELATED problems.

User message:
{state.user_input}

IMPORTANT RULES:
1. These are FINANCIAL problems - ALWAYS ACCEPT and provide help:
   - Lost/stolen car, vehicle, bike → insurance claims, loan EMI, transportation costs, police report
   - Lost/stolen phone, laptop, jewelry → replacement costs, insurance, financial recovery
   - Salary delayed, not paid → EMI issues, bill payments, budget crisis
   - Loan, debt, EMI problems → payment difficulties, restructuring
   - Medical bills, hospital expenses → payment plans, insurance
   - Lost job, unemployment → income loss, expense management
   - Fraud, scam, money stolen → recovery, police report, financial restoration
   - Rent payment issues → eviction concerns, negotiation
   - Business loss, bankruptcy → debt management, recovery

2. ONLY reject if problem is purely personal with NO financial aspect:
   - Pure relationship issues (no money involved)
   - General health complaints (no medical bills)
   - Emotional/mental health (unless causing job/income loss)
   
   For non-financial, respond:
   {{
       "not_financial": true,
       "redirect_message": "Main financial crisis situations me help karta hu. Apni financial problem batao."
   }}

3. For ALL FINANCIAL problems, provide this JSON with EXACTLY {steps} action steps:
{{
    "crisis_type": "specific financial issue (e.g., 'Vehicle theft impacting insurance and transportation costs')",
    "severity": "low/medium/high",
    "mood": "calm/panic/anxious/depressed/angry/overwhelmed",
    "calming_steps": [
        {{
            "instruction": "Take 5 deep breaths - we will solve this step by step",
            "type": "breathing",
            "duration_seconds": 20
        }}
    ],
    "action_steps": [
        {{
            "step": "Short, basic, calming action step (one sentence)",
            "priority": "high/medium",
            "estimated_time_minutes": 20
        }}
    ],
    "needs_emergency_support": false,
    "final_advice": "Supportive message"
}}

CRITICAL: 
- Lost car/vehicle = FINANCIAL CRISIS (insurance, loan, transport costs)
- Lost valuables = FINANCIAL CRISIS (replacement, insurance)
- Detect the user's mood from their message and provide calming steps that match it.
- Keep steps short, gentle, and basic. Avoid harsh or overwhelming language.
- Provide ONLY 1-2 calming steps and EXACTLY {steps} action steps.
"""

    try:
        raw = call_groq(prompt)
        parsed = safe_json_parse(raw)
        
        # Check if it's a non-financial issue
        if isinstance(parsed, dict) and parsed.get("not_financial"):
            state.output = parsed
            return state
        
        # Validate and add defaults for financial issues
        if not isinstance(parsed, dict) or "error" in parsed:
            parsed = create_default_response()
        else:
            # Ensure required fields
            if "crisis_type" not in parsed:
                parsed["crisis_type"] = "Financial crisis requiring attention"
            if "severity" not in parsed:
                parsed["severity"] = "medium"
            if "mood" not in parsed:
                parsed["mood"] = "overwhelmed"
            if "calming_steps" not in parsed:
                parsed["calming_steps"] = get_default_calming_steps()
            if "action_steps" not in parsed:
                parsed["action_steps"] = get_default_action_steps()
            if "final_advice" not in parsed:
                parsed["final_advice"] = "Take it one step at a time."
            if "needs_emergency_support" not in parsed:
                parsed["needs_emergency_support"] = False
            
            # Check for emergency and add resources
            emergency_contacts = get_emergency_contacts(state.user_input)
            if parsed.get("needs_emergency_support") or emergency_contacts:
                state.emergency_triggered = True
                if emergency_contacts:
                    parsed["emergency_contacts"] = emergency_contacts
        
        state.output = parsed
        
    except Exception as e:
        state.output = create_default_response()
    
    return state

def get_default_calming_steps():
    return [
        {
            "instruction": "Take 5 deep breaths - financial stress is temporary",
            "type": "breathing",
            "duration_seconds": 20
        }
    ]

def get_default_action_steps():
    return [
        {
            "step": "List all your monthly income sources and their amounts",
            "priority": "high",
            "estimated_time_minutes": 15
        },
        {
            "step": "Calculate your total monthly expenses and prioritize essential ones",
            "priority": "high",
            "estimated_time_minutes": 20
        },
        {
            "step": "Identify immediate financial obligations (bills due this week)",
            "priority": "high",
            "estimated_time_minutes": 10
        },
        {
            "step": "Contact your creditors or service providers to discuss payment options",
            "priority": "medium",
            "estimated_time_minutes": 30
        },
        {
            "step": "Explore emergency funding options or financial assistance programs",
            "priority": "medium",
            "estimated_time_minutes": 25
        }
    ]

def create_default_response():
    return {
        "crisis_type": "Financial stress requiring budget review",
        "severity": "medium",
        "mood": "overwhelmed",
        "calming_steps": get_default_calming_steps(),
        "action_steps": get_default_action_steps(),
        "needs_emergency_support": False,
        "final_advice": "Financial challenges are temporary. Let's create a plan to work through this step by step."
    }
