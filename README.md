# Financial Crisis Assistant

A Streamlit-based financial crisis assistant that provides calm, step-by-step guidance with timers and re-evaluation. The assistant focuses on financial situations only (job loss, delayed salary, debt, fraud, medical bills, lost valuables with financial impact) and avoids non-financial counseling.

## Features

- **Financial-only guidance** with clear scope enforcement - rejects non-financial problems
- **Mood-aware calming steps** - detects panic, anxiety, depression, overwhelm and provides customized calming exercises
- **One-step-at-a-time action flow** - shows a progress counter (Step X of Y) and reveals one actionable step at a time
- **Smart timers** for calming steps (20-60 seconds) and action steps (5-30 minutes) with pause/resume controls
- **Re-evaluation option** - when users are stuck, they can click "Need Help" to get simpler alternative steps
- **Emergency contacts** shown intelligently only for truly urgent cases (theft, fraud, medical, accidents)
- **Optional detailed analysis** panel for reviewing full reasoning and suggestions
- **Sidebar settings** - adjust max steps (3-7), toggle emergency mode, enable detailed analysis

## Tech Stack

- **Python 3.x** - Core language
- **Streamlit** - Interactive web UI with real-time updates
- **FastAPI** - REST API endpoint for programmatic access
- **LangGraph & LangChain** - Agent orchestration and workflow management
- **Groq API** - LLM (llama-3.3-70b-versatile) for financial analysis and mood detection
- **Pydantic** - Data validation for all schemas

## Streamlit App

The main user interface provides an intuitive experience for financial crisis support:

![Streamlit Home Screen - Initial Chat Interface](stream-images/Screenshot%202026-02-12%20010258.png)  
*Initial chat interface where users describe their financial crisis. The assistant analyzes the situation and detects mood.*

![Streamlit Step Progression - Timer and Action Steps](stream-images/Screenshot%202026-02-12%20010442.png)  
*Step-by-step flow showing calming exercise first, then one action step at a time with timer controls (Start/Pause/Reset). Progress counter shows "Step X of Y".*

### Key Streamlit Features

- **Chat History** - Displays conversation with assistant for continuity
- **One Small Step Section** - "Take it slowly" - shows current action step with priority level
- **Timer Controls** - Start/Pause/Reset buttons with live countdown display
- **Step Navigation** - "Step Complete" button to progress, "Need Help" for re-evaluation
- **Mood Detection** - Shows detected emotional state (panic, anxious, depressed, etc.)
- **Emergency Contacts** - Intelligent display of relevant contacts only when needed
- **Detailed Analysis** - Optional expandable section showing full LLM reasoning (via sidebar toggle)
- **Sidebar Controls** - Max steps slider (3-7), emergency mode toggle, detailed analysis checkbox

## Project Structure

```
assitant/
├── app.py                          # FastAPI application (optional REST API at /docs)
├── streamlit_app.py                # Main Streamlit UI application
├── requirements.txt                # Python dependencies
├── run_streamlit.bat               # Windows batch script to launch Streamlit
├── .env                            # Environment variables (GROQ_API_KEY)
├── README.md                       # This file
│
├── agent/                          # Agent orchestration
│   ├── __init__.py
│   ├── agent_runner.py             # Runs the complete agent workflow
│   ├── state.py                    # Agent state management
│   └── __pycache__/
│
├── nodes/                          # Processing nodes for the agent
│   ├── __init__.py
│   ├── reasoning_node.py           # LLM-powered financial analysis and mood detection
│   ├── response_node.py            # Response formatting and styling
│   ├── guard_node.py               # Optional input validation
│   └── __pycache__/
│
├── schemas/                        # Data models and validation
│   ├── __init__.py
│   ├── agent_state_schema.py       # Pydantic model for agent state (steps, mood, severity)
│   ├── request_schema.py           # Request validation schema
│   └── __pycache__/
│
├── emergency/                      # Emergency contact management
│   ├── __init__.py
│   ├── financial_resources.py      # Strict keyword matching for relevant emergency contacts
│   └── __pycache__/
│
├── evaluators/                     # Re-evaluation logic
│   ├── __init__.py
│   ├── reevaluator.py              # Generates simpler alternative steps on request
│   ├── escalation_evaluator.py     # Determines if situation needs escalation
│   ├── timer_evaluator.py          # Tracks and manages timer states
│   └── __pycache__/
│
├── llm/                            # LLM integration
│   ├── __init__.py
│   ├── groq_client.py              # Groq API wrapper with retry logic
│   ├── output_schema.json          # Expected JSON output schema from LLM
│   ├── prompt_template.txt         # System prompt for the reasoning node
│   └── __pycache__/
│
├── config/                         # Configuration management
│   ├── __init__.py
│   ├── settings.py                 # Model name, step limits, API settings
│   └── __pycache__/
│
├── utils/                          # Utility functions
│   ├── __init__.py
│   ├── json_formatter.py           # JSON parsing and validation utilities
│   └── __pycache__/
│
├── stream-images/                  # Screenshots for documentation
│   ├── Screenshot 2026-02-12 010258.png
│   └── Screenshot 2026-02-12 010442.png
│
└── __pycache__/
```

## How It Works - Workflow

### Step-by-Step Flow

1. **User Submission**
   - User types their financial crisis message in the Streamlit chat interface
   - Example: "I just lost my job" or "I was scammed out of ₹50,000"

2. **Financial Classification & Mood Detection**
   - `reasoning_node.py` processes the input using Groq LLM (llama-3.3-70b-versatile)
   - LLM analyzes and returns:
     - `is_financial`: Boolean flag (financial vs non-financial)
     - `mood`: Detected emotional state (panic, anxious, depressed, overwhelmed, calm, angry)
     - `severity`: Crisis level (low, medium, high)
     - `why_emotional`: Explanation of mood detection
     - `steps`: List of action steps with durations
     - `emergency_triggered`: Whether emergency contacts apply

3. **Calming Exercise Phase**
   - First step is always a calming exercise (breathing, grounding technique, etc.)
   - Duration: 20-60 seconds based on detected mood
   - Timer appears with Pause/Reset controls
   - Message has warm, empathetic tone: "Take it slowly"
   - User must complete calming step before proceeding

4. **Action Steps Phase (One at a Time)**
   - After calming, action steps reveal progressively
   - Display format: **"Step X of Y: [Title]"** with priority level
   - Each step includes:
     - Short, basic description (calming language)
     - Estimated time in minutes
     - Priority level (high, medium, low)
   - User clicks "Step Complete" to progress to next step
   - Countdown timer shows for each action step

5. **Re-evaluation (Need Help)**
   - If user is stuck or overwhelmed, they click "Need Help"
   - `reevaluator.py` generates simpler, more achievable alternatives
   - Steps broken down into smaller micro-actions
   - User can pause and resume at any time

6. **Emergency Contacts (Smart Matching)**
   - Only shown when situation matches specific keywords:
     - **Police (100)**: Theft, robbery, fraud, lost vehicle
     - **Ambulance (102)**: Medical emergency, accident, injury
     - **Consumer Helpline (1800-11-4000)**: Fraud/scams/cheated
   - NOT shown for: General job loss, delayed salary, debt stress
   - Prevents unnecessary escalation and false alarms

7. **Optional Detailed Analysis**
   - Users can enable "Detailed Analysis" in sidebar
   - Displays full LLM reasoning and thoughts
   - Shows all detected information and suggestions
   - Helps transparency and builds trust

### Data Flow Diagram

```
User Message (Streamlit)
        ↓
   [Guard Node] (Optional validation)
        ↓
   [Reasoning Node] 
      ↓ (LLM call)
   Groq API (Analysis & Mood Detection)
      ↓
   JSON Response (steps, mood, severity, emergency)
        ↓
   [Response Node] (Formatting)
        ↓
   Session State (Step tracking, timer state)
        ↓
   Streamlit UI (Display with timers)
        ↓
   Timer Loop (Non-blocking with pause/resume)
        ↓
   [Reevaluator] (If "Need Help" clicked)
        ↓
   Updated Steps / Emergency Contacts Display
```

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Groq API key (get from https://console.groq.com)
- pip (Python package manager)

### Installation

1. **Clone or download the project**
   ```bash
   cd assitant
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   ```
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   - Create a `.env` file in the project root
   - Add your Groq API key:
     ```
     GROQ_API_KEY=your_actual_api_key_here
     ```

## Running the Application

### Streamlit (Recommended - Full Interactive UI)

```bash
python -m streamlit run streamlit_app.py
```

Or on Windows, simply double-click:
```
run_streamlit.bat
```

Then open your browser to:
```
http://localhost:8501
```

### FastAPI (REST API)

```bash
uvicorn app:app --reload
```

Then visit the interactive API docs:
```
http://127.0.0.1:8000/docs
```

## Configuration

### Main Settings (`config/settings.py`)

```python
MODEL_NAME = "llama-3.3-70b-versatile"  # Groq model to use
MAX_STEPS = 5                           # Optimal max steps
MAX_STEPS_EMERGENCY = 7                 # Max steps in emergency mode
DEFAULT_TEMPERATURE = 0.7               # LLM temperature (creativity)
```

### Sidebar Controls (in Streamlit App)

- **Max Steps Slider**: Adjust from 3 to 7 (default: 5)
- **Emergency Mode**: Toggle for more detailed/aggressive steps
- **Detailed Analysis**: Enable to see full LLM reasoning

## Key Technical Details

### Mood Detection
The reasoning node detects six mood states:
- **Panic**: High anxiety, feels uncontrollable
- **Anxious**: Worried, nervous, some control
- **Depressed**: Hopeless, discouraged, low energy
- **Overwhelmed**: Too much to handle, scattered
- **Calm**: In control, clear-headed
- **Angry**: Frustrated, feels wronged, need justice

Each mood receives customized calming techniques (breathing, meditation, grounding, writing, etc.).

### Emergency Contact Logic
The emergency contact system uses **strict keyword matching**:
- If situation contains "theft" OR "robbery" OR "fraud" → Police
- If situation contains "injured" OR "medical" OR "accident" → Ambulance
- If situation contains "scam" OR "cheated" OR "fraud" → Consumer Helpline
- No automatic fallback (safety-first approach)

### Timer Implementation
- **Non-blocking timers** using session state + Streamlit reruns
- **Session state fields tracked**:
  - `timer_running`: Boolean pause/resume state
  - `timer_remaining`: Seconds left in countdown
  - `timer_step_id`: Which step's timer is active
  - `timer_last_tick`: Last update timestamp for delta calculation
- **Prevents UI freeze** during countdown using delta calculation instead of sleep()

### Step Progression
- **Current step index** tracked in session state
- **All steps stored** as list for navigation
- **"Step Complete"** button increments index
- **"Need Help"** triggers reevaluator without losing step history

## Notes

- ⚠️ **Not Professional Advice**: This assistant provides emotional support and practical guidance only. It is **not** a substitute for professional financial, legal, or medical advice.
- 🔒 **Emergency Contacts**: Shown intelligently based on situation. Police only appear for actual crimes/accidents, not general financial stress.
- 💾 **Session-Based**: Chat history and step progress reset per browser session (not persistent).
- 🌐 **Internet Required**: Groq API calls require active internet connection.

## Troubleshooting

### "Groq API Key not found"
- Ensure `.env` file exists in project root
- Check `GROQ_API_KEY=` line is correct
- Restart Streamlit app (`Ctrl+C`, then re-run)

### Timer not showing
- Check browser console for errors (F12)
- Toggle "Emergency Mode" or refresh page
- Ensure JavaScript is enabled

### Non-financial issues not being rejected
- Check `reasoning_node.py` prompt is loading correctly
- Verify Groq API is responding (test with `/docs` endpoint)
- Try simpler non-financial input like "What's the weather?"

## License

MIT License - See LICENSE file for details

## Contact & Support

For issues or suggestions:
- Create an issue in the repository
- Check the README troubleshooting section
- Review logs in Streamlit terminal output
