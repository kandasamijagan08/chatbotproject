import os
import streamlit as st
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL = "deepseek-ai/DeepSeek-V4.1-Flash"

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="TravelMind AI",
    page_icon="✈️",
    layout="wide"
)

# ============================================================
# CHECK API KEY
# ============================================================

if not HF_TOKEN:
    st.error("❌ HF_TOKEN is missing. Please add it to your .env file.")
    st.stop()

client = InferenceClient(
    provider="auto",
    api_key=HF_TOKEN
)

# ============================================================
# CUSTOM UI
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
    radial-gradient(
        circle at 10% 10%,
        rgba(0, 234, 255, 0.14),
        transparent 30%
    ),
    radial-gradient(
        circle at 90% 20%,
        rgba(130, 50, 255, 0.16),
        transparent 30%
    ),
    linear-gradient(
        135deg,
        #02030a,
        #080b20,
        #02030a
    );
}

.main-title {
    text-align: center;
    font-size: 58px;
    font-weight: 900;

    background: linear-gradient(
        90deg,
        #00eaff,
        #ffffff,
        #9b5cff,
        #ff3cac
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #aeb9d8;
    font-size: 20px;
    margin-bottom: 35px;
}

.agent-card {
    padding: 18px;
    border-radius: 18px;

    background: rgba(255,255,255,0.05);

    border: 1px solid rgba(0,234,255,0.2);

    text-align: center;

    box-shadow:
        0 0 20px rgba(0,234,255,0.07);
}

.agent-icon {
    font-size: 30px;
}

.agent-name {
    font-weight: 700;
}

.stButton > button {

    width: 100%;
    height: 55px;

    border-radius: 15px;

    border: 1px solid #00eaff;

    background:
    linear-gradient(
        90deg,
        #005eff,
        #742cff,
        #d62cff
    );

    color: white;

    font-size: 18px;
    font-weight: 800;

    box-shadow:
        0 0 25px rgba(0,234,255,0.3);
}

.result-box {
    padding: 25px;

    border-radius: 20px;

    background: rgba(255,255,255,0.04);

    border: 1px solid rgba(0,234,255,0.2);
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# AI FUNCTION
# ============================================================

def ask_ai(prompt, max_tokens=2500, temperature=0.3):

    response = client.chat_completion(
        model=MODEL,

        messages=[
            {
                "role": "system",
                "content": """
You are a professional Agentic AI travel planning assistant.

Give practical, structured and useful answers.

Do not pretend that estimated prices,
hotel availability, flight availability,
weather or opening hours are live-confirmed.
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        max_tokens=max_tokens,
        temperature=temperature
    )

    return response.choices[0].message.content


# ============================================================
# AGENT 1 — TRAVEL RESEARCHER
# ============================================================

def researcher_agent(
    destination,
    start_location,
    days,
    interests
):

    prompt = f"""
You are AGENT 1 — TRAVEL RESEARCHER.

Research the user's destination.

Destination:
{destination}

Starting location:
{start_location}

Duration:
{days} days

Interests:
{", ".join(interests)}

Provide:

1. Important attractions
2. Activities
3. Transportation options
4. Popular areas
5. Food experiences
6. Cultural experiences
7. Nature experiences
8. Practical travel information

Do not invent live prices.

Return concise structured research.
"""

    return ask_ai(
        prompt,
        max_tokens=2500,
        temperature=0.3
    )


# ============================================================
# AGENT 2 — ITINERARY PLANNER
# ============================================================

def itinerary_agent(
    destination,
    days,
    travelers,
    style,
    interests,
    research
):

    prompt = f"""
You are AGENT 2 — ITINERARY PLANNER.

Create a realistic {days}-day itinerary.

Destination:
{destination}

Travelers:
{travelers}

Travel style:
{style}

Interests:
{", ".join(interests)}

Research from Agent 1:

{research}

For every day provide:

Morning:
Afternoon:
Evening:
Places:
Activities:
Estimated local travel time:

Rules:

- Avoid unrealistic schedules.
- Group nearby places together.
- Include meal and rest time.
- Prioritize user interests.
- Do not invent reservations.
"""

    return ask_ai(
        prompt,
        max_tokens=3500,
        temperature=0.4
    )


# ============================================================
# AGENT 3 — BUDGET AGENT
# ============================================================

def budget_agent(
    destination,
    days,
    travelers,
    budget,
    style,
    itinerary
):

    prompt = f"""
You are AGENT 3 — TRAVEL BUDGET SPECIALIST.

Create an approximate INR travel budget.

Destination:
{destination}

Days:
{days}

Travelers:
{travelers}

Maximum user budget:
₹{budget}

Travel style:
{style}

Itinerary:
{itinerary}

Estimate:

Accommodation
Transportation
Food
Activities
Miscellaneous
Total

Important:

- Use INR.
- Prices are estimates.
- Do not claim live prices.
- Keep the total mathematically consistent.
- Consider the user's travel style.
"""

    return ask_ai(
        prompt,
        max_tokens=1800,
        temperature=0.2
    )


# ============================================================
# AGENT 4 — TRAVEL ADVISOR
# ============================================================

def advisor_agent(
    itinerary,
    budget
):

    prompt = f"""
You are AGENT 4 — TRAVEL ADVISOR.

Review the following itinerary:

{itinerary}

Review the following budget:

{budget}

Check:

1. Unrealistic timing
2. Excessive travel
3. Missing rest periods
4. Budget problems
5. Activities that may need advance booking
6. Weather considerations
7. Important travel planning issues

Provide practical improvements.

Do not rewrite the complete itinerary.
"""

    return ask_ai(
        prompt,
        max_tokens=2000,
        temperature=0.3
    )


# ============================================================
# AGENT 5 — FINAL REPORT AGENT
# ============================================================

def final_report_agent(
    destination,
    start_location,
    travel_date,
    days,
    travelers,
    style,
    interests,
    itinerary,
    budget,
    advice
):

    prompt = f"""
You are AGENT 5 — FINAL TRAVEL REPORT SPECIALIST.

Create the final professional travel plan.

Destination:
{destination}

Starting location:
{start_location}

Travel date:
{travel_date}

Duration:
{days} days

Travelers:
{travelers}

Travel style:
{style}

Interests:
{", ".join(interests)}

ITINERARY:
{itinerary}

BUDGET:
{budget}

ADVISOR REVIEW:
{advice}

Create the final report using:

# ✈️ TRIP OVERVIEW

# 🗓️ DAY-BY-DAY ITINERARY

# 💰 BUDGET BREAKDOWN

# 🚗 TRANSPORTATION

# 🍴 FOOD RECOMMENDATIONS

# 🎒 PACKING CHECKLIST

# 💡 AI TRAVEL TIPS

# ⚠️ THINGS TO VERIFY BEFORE TRAVEL

Keep it professional and easy to read.

Do not claim live prices,
hotel availability,
flight availability,
weather or opening hours.
"""

    return ask_ai(
        prompt,
        max_tokens=5000,
        temperature=0.4
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">✈️ TRAVELMIND AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Multi-Agent AI Travel Planner • DeepSeek-V4.1-Flash'
    '</div>',
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR INPUT
# ============================================================

with st.sidebar:

    st.header("🌍 Trip Configuration")

    destination = st.text_input(
        "📍 Destination",
        placeholder="Example: Goa"
    )

    start_location = st.text_input(
        "🚀 Starting Location",
        placeholder="Example: Chennai"
    )

    travel_date = st.date_input(
        "📅 Travel Start Date"
    )

    days = st.number_input(
        "🗓️ Number of Days",
        min_value=1,
        max_value=30,
        value=3
    )

    travelers = st.number_input(
        "👥 Number of Travelers",
        min_value=1,
        max_value=20,
        value=2
    )

    budget = st.number_input(
        "💰 Budget (₹)",
        min_value=1000,
        value=30000,
        step=1000
    )

    style = st.selectbox(
        "✨ Travel Style",
        [
            "Budget",
            "Standard",
            "Luxury"
        ]
    )

    interests = st.multiselect(
        "❤️ Interests",
        [
            "Nature",
            "Beaches",
            "Adventure",
            "Food",
            "History",
            "Shopping",
            "Photography",
            "Culture"
        ],
        default=[
            "Nature",
            "Food"
        ]
    )

    plan_button = st.button(
        "✨ PLAN MY TRIP"
    )


# ============================================================
# AGENT DASHBOARD
# ============================================================

st.subheader("🤖 Multi-Agent Workflow")

col1, col2, col3, col4, col5 = st.columns(5)

agent_data = [
    ("🔎", "Researcher"),
    ("🗺️", "Itinerary"),
    ("💰", "Budget"),
    ("🧠", "Advisor"),
    ("📝", "Final Report")
]

for col, (icon, name) in zip(
    [col1, col2, col3, col4, col5],
    agent_data
):

    with col:

        st.markdown(
            f"""
            <div class="agent-card">

            <div class="agent-icon">
            {icon}
            </div>

            <div class="agent-name">
            {name}
            </div>

            <small>
            Waiting
            </small>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# RUN WORKFLOW
# ============================================================

if plan_button:

    if not destination:

        st.error("❌ Please enter a destination.")
        st.stop()

    if not start_location:

        st.error("❌ Please enter your starting location.")
        st.stop()

    if not interests:

        st.error("❌ Please select at least one interest.")
        st.stop()

    try:

        # ====================================================
        # AGENT 1
        # ====================================================

        with st.status(
            "🔎 Travel Researcher Agent working...",
            expanded=True
        ) as status:

            research = researcher_agent(
                destination,
                start_location,
                days,
                interests
            )

            st.markdown("### 🔎 Research Results")
            st.write(research)

            status.update(
                label="🔎 Researcher Agent ✓ Completed",
                state="complete"
            )


        # ====================================================
        # AGENT 2
        # ====================================================

        with st.status(
            "🗺️ Itinerary Planner Agent working...",
            expanded=True
        ) as status:

            itinerary = itinerary_agent(
                destination,
                days,
                travelers,
                style,
                interests,
                research
            )

            st.markdown("### 🗺️ Itinerary")
            st.write(itinerary)

            status.update(
                label="🗺️ Itinerary Agent ✓ Completed",
                state="complete"
            )


        # ====================================================
        # AGENT 3
        # ====================================================

        with st.status(
            "💰 Budget Agent calculating...",
            expanded=True
        ) as status:

            budget_result = budget_agent(
                destination,
                days,
                travelers,
                budget,
                style,
                itinerary
            )

            st.markdown("### 💰 Budget")
            st.write(budget_result)

            status.update(
                label="💰 Budget Agent ✓ Completed",
                state="complete"
            )


        # ====================================================
        # AGENT 4
        # ====================================================

        with st.status(
            "🧠 Travel Advisor reviewing...",
            expanded=True
        ) as status:

            advice = advisor_agent(
                itinerary,
                budget_result
            )

            st.markdown("### 🧠 Advisor Review")
            st.write(advice)

            status.update(
                label="🧠 Travel Advisor ✓ Completed",
                state="complete"
            )


        # ====================================================
        # AGENT 5
        # ====================================================

        with st.status(
            "📝 Final Report Agent preparing...",
            expanded=True
        ) as status:

            final_report = final_report_agent(
                destination,
                start_location,
                travel_date,
                days,
                travelers,
                style,
                interests,
                itinerary,
                budget_result,
                advice
            )

            status.update(
                label="📝 Final Report Agent ✓ Completed",
                state="complete"
            )


        # ====================================================
        # FINAL RESULT
        # ====================================================

        st.success(
            "🎉 TravelMind AI has completed your travel plan!"
        )

        st.markdown("---")

        st.markdown(
            f"""
            ## ✈️ {destination}

            **📍 Starting Location:** {start_location}

            **📅 Travel Date:** {travel_date}

            **🗓️ Duration:** {days} days

            **👥 Travelers:** {travelers}

            **✨ Travel Style:** {style}
            """
        )

        st.markdown(
            '<div class="result-box">',
            unsafe_allow_html=True
        )

        st.markdown(final_report)

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

        # ====================================================
        # DOWNLOAD
        # ====================================================

        st.download_button(
            label="📥 Download Travel Plan",
            data=final_report,
            file_name="TravelMind_AI_Travel_Plan.txt",
            mime="text/plain"
        )

    except Exception as e:

        st.error(
            "❌ Something went wrong in the Agentic AI workflow."
        )

        st.exception(e)