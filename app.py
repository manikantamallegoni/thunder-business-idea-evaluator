import streamlit as st
from langchain_core.messages import HumanMessage

from agent import check_business_idea, evaluate_business


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="THUNDER // BUSINESS EVALUATOR",
    page_icon="🀤",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS — THUNDER / SMOKE UI
# ============================================================

st.markdown("""
<style>

/* ---------- MAIN BACKGROUND ---------- */

.stApp {
    background:
        radial-gradient(
            circle at 50% 15%,
            rgba(120, 120, 140, 0.20) 0%,
            transparent 28%
        ),
        radial-gradient(
            circle at 20% 70%,
            rgba(80, 80, 100, 0.18) 0%,
            transparent 30%
        ),
        radial-gradient(
            circle at 80% 75%,
            rgba(90, 90, 110, 0.15) 0%,
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #050507 0%,
            #0b0b10 35%,
            #111118 60%,
            #050507 100%
        );

    color: #f5f5f5;
}


/* ---------- SMOKE LAYERS ---------- */

.stApp::before {
    content: "";
    position: fixed;
    width: 700px;
    height: 700px;

    top: -250px;
    left: -180px;

    background:
        radial-gradient(
            ellipse,
            rgba(180,180,190,0.13) 0%,
            rgba(120,120,130,0.07) 30%,
            transparent 70%
        );

    filter: blur(55px);

    animation: smokeMove 12s ease-in-out infinite alternate;

    pointer-events: none;
    z-index: 0;
}


.stApp::after {
    content: "";
    position: fixed;
    width: 800px;
    height: 600px;

    right: -300px;
    bottom: -250px;

    background:
        radial-gradient(
            ellipse,
            rgba(150,150,170,0.12) 0%,
            rgba(90,90,110,0.06) 35%,
            transparent 70%
        );

    filter: blur(60px);

    animation: smokeMove2 15s ease-in-out infinite alternate;

    pointer-events: none;
    z-index: 0;
}


@keyframes smokeMove {

    0% {
        transform: translate(0px, 0px) scale(1);
    }

    50% {
        transform: translate(100px, 70px) scale(1.2);
    }

    100% {
        transform: translate(180px, -20px) scale(1.1);
    }
}


@keyframes smokeMove2 {

    0% {
        transform: translate(0px, 0px) scale(1);
    }

    50% {
        transform: translate(-100px, -60px) scale(1.25);
    }

    100% {
        transform: translate(-160px, 20px) scale(1.1);
    }
}


/* ---------- REMOVE STREAMLIT HEADER ---------- */

header {
    background: transparent !important;
}


/* ---------- MAIN CONTENT ---------- */

.block-container {
    max-width: 1150px;
    padding-top: 3rem;
    position: relative;
    z-index: 2;
}


/* ---------- TITLE ---------- */

.thunder-title {

    font-family: "Arial Black", sans-serif;

    font-size: 4.5rem;

    font-weight: 900;

    letter-spacing: 8px;

    text-align: center;

    color: #f5f5f5;

    text-shadow:
        0 0 5px #ffffff,
        0 0 15px rgba(220,220,255,0.8),
        0 0 35px rgba(150,150,255,0.45);

    animation: titlePulse 3s infinite;

}


@keyframes titlePulse {

    0%, 90%, 100% {
        text-shadow:
            0 0 5px #ffffff,
            0 0 15px rgba(220,220,255,0.7),
            0 0 30px rgba(150,150,255,0.4);
    }

    95% {
        text-shadow:
            0 0 15px white,
            0 0 40px white,
            0 0 80px rgba(190,190,255,0.9);
    }

}


/* ---------- SUBTITLE ---------- */

.thunder-subtitle {

    text-align: center;

    color: #9999a8;

    font-size: 1.05rem;

    letter-spacing: 4px;

    margin-bottom: 40px;

}


/* ---------- THUNDER LINE ---------- */

.thunder-line {

    height: 2px;

    width: 80%;

    margin: 0 auto 40px auto;

    background: linear-gradient(
        90deg,
        transparent,
        #ffffff,
        #9999ff,
        #ffffff,
        transparent
    );

    box-shadow:
        0 0 10px rgba(180,180,255,0.8),
        0 0 25px rgba(120,120,255,0.5);

}


/* ---------- CARD ---------- */

.thunder-card {

    background:
        linear-gradient(
            145deg,
            rgba(35,35,45,0.80),
            rgba(10,10,15,0.88)
        );

    border: 1px solid rgba(190,190,210,0.20);

    border-radius: 24px;

    padding: 35px;

    box-shadow:
        0 15px 60px rgba(0,0,0,0.65),
        inset 0 0 30px rgba(255,255,255,0.02);

    backdrop-filter: blur(18px);

}


/* ---------- INPUT ---------- */

.stTextArea textarea {

    background: rgba(8,8,12,0.85) !important;

    color: #eeeeee !important;

    border: 1px solid #363644 !important;

    border-radius: 15px !important;

    font-size: 1rem !important;

}


.stTextArea textarea:focus {

    border: 1px solid #aaaaff !important;

    box-shadow:
        0 0 10px rgba(150,150,255,0.5),
        0 0 25px rgba(100,100,255,0.15) !important;

}


/* ---------- BUTTON ---------- */

.stButton > button {

    width: 100%;

    background:
        linear-gradient(
            135deg,
            #eeeeff,
            #aaaadd
        );

    color: #08080b;

    border: none;

    border-radius: 14px;

    padding: 14px 25px;

    font-weight: 900;

    letter-spacing: 2px;

    transition: all 0.2s ease;

    box-shadow:
        0 0 10px rgba(200,200,255,0.35);

}


.stButton > button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 0 15px rgba(220,220,255,0.8),
        0 0 40px rgba(150,150,255,0.35);

}


/* ---------- SECTION HEADERS ---------- */

h1, h2, h3 {

    color: #eeeeff !important;

}


/* ---------- INFO BOX ---------- */

.stAlert {

    background: rgba(25,25,35,0.85) !important;

    border: 1px solid rgba(170,170,200,0.25) !important;

    border-radius: 15px !important;

}


/* ---------- REPORT ---------- */

.report-box {

    background:
        linear-gradient(
            145deg,
            rgba(25,25,35,0.95),
            rgba(8,8,12,0.98)
        );

    border:

        1px solid rgba(180,180,210,0.25);

    border-radius: 22px;

    padding: 35px;

    margin-top: 30px;

    box-shadow:

        0 20px 70px rgba(0,0,0,0.7),

        0 0 30px rgba(130,130,180,0.08);

}


/* ---------- STATUS ---------- */

.status {

    text-align: center;

    color: #a8a8ba;

    letter-spacing: 3px;

    font-size: 0.8rem;

    margin-top: 20px;

}


/* ---------- MOBILE ---------- */

@media (max-width: 700px) {

    .thunder-title {
        font-size: 2.5rem;
        letter-spacing: 4px;
    }

    .thunder-subtitle {
        font-size: 0.8rem;
        letter-spacing: 2px;
    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="thunder-title">➴ THUNDER</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="thunder-subtitle">'
    'AI BUSINESS IDEA EVALUATION ENGINE'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="thunder-line"></div>',
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "idea" not in st.session_state:
    st.session_state.idea = ""

if "question" not in st.session_state:
    st.session_state.question = None

if "report" not in st.session_state:
    st.session_state.report = None


# ============================================================
# START SCREEN
# ============================================================

if not st.session_state.idea:

    st.markdown(
        '<div class="thunder-card">',
        unsafe_allow_html=True
    )

    st.markdown("## જ⁀➴ENTER YOUR BUSINESS IDEA")

    st.write(
        "Give the AI enough detail to understand what you want to build."
    )

    idea = st.text_area(
        "Business Idea",
        placeholder=(
            "Example:\n\n"
            "I want to build an online platform that sells "
            "practical AI-agent courses to college students."
        ),
        height=180,
        label_visibility="collapsed"
    )

    if st.button("⚡ INITIALIZE EVALUATION"):

        if not idea.strip():

            st.warning("Enter a business idea first.")

        else:

            st.session_state.idea = idea

            st.session_state.conversation = [
                HumanMessage(content=idea)
            ]

            with st.spinner("⚡ THUNDER ENGINE ANALYZING..."):

                result = check_business_idea(
                    idea,
                    st.session_state.conversation
                )

            if result["status"] == "needs_info":

                st.session_state.question = result["message"]

            else:

                with st.spinner(
                        "⚡ FOUR AI ADVISORS ARE EVALUATING..."
                ):

                    report = evaluate_business(
                        idea,
                        st.session_state.conversation
                    )

                st.session_state.report = report

            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# FOLLOW-UP QUESTION
# ============================================================

if (
        st.session_state.idea
        and st.session_state.question
        and not st.session_state.report
):

    st.markdown(
        '<div class="thunder-card">',
        unsafe_allow_html=True
    )

    st.markdown("## ⚡ CONTROLLER REQUEST")

    st.info(st.session_state.question)

    answer = st.text_area(
        "Your Answer",
        placeholder="Provide the requested information...",
        height=150,
        label_visibility="collapsed"
    )

    if st.button("⚡ SEND TO CONTROLLER"):

        if not answer.strip():

            st.warning("Please provide an answer.")

        else:

            st.session_state.conversation.append(
                HumanMessage(content=answer)
            )

            with st.spinner(
                    "⚡ CONTROLLER RE-EVALUATING..."
            ):

                result = check_business_idea(
                    st.session_state.idea,
                    st.session_state.conversation
                )

            if result["status"] == "needs_info":

                st.session_state.question = result["message"]

            else:

                st.session_state.question = None

                with st.spinner(
                        "⚡ MARKET • LEGAL • TECHNICAL • STRATEGY"
                ):

                    report = evaluate_business(
                        st.session_state.idea,
                        st.session_state.conversation
                    )

                st.session_state.report = report

            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# FINAL REPORT
# ============================================================

if st.session_state.report:

    st.markdown(
        '<div class="thunder-card">',
        unsafe_allow_html=True
    )

    st.markdown("## ⚡ BUSINESS INTELLIGENCE REPORT")

    st.markdown(
        '<div class="report-box">',
        unsafe_allow_html=True
    )

    st.markdown(st.session_state.report)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="status">'
        '⚡ ANALYSIS COMPLETE // THUNDER ENGINE ONLINE'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    if st.button("↻ EVALUATE ANOTHER BUSINESS"):

        st.session_state.conversation = []
        st.session_state.idea = ""
        st.session_state.question = None
        st.session_state.report = None

        st.rerun()