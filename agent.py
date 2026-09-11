import os
import operator
from typing import List, Annotated, Dict
from typing_extensions import TypedDict

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
    BaseMessage
)
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END


# =========================
# LOAD ENVIRONMENT
# =========================

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env file")


# =========================
# LLM
# =========================

llm = ChatOpenAI(
    model="openai/gpt-oss-20b",
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)


# =========================
# STATE
# =========================

class State(TypedDict):
    idea: str
    messages: Annotated[List[BaseMessage], add_messages]
    advisor_reports: Annotated[Dict[str, str], operator.or_]
    final_report: str


# =========================
# CONTROLLER
# =========================

controller_prompt = SystemMessage(
    content="""
You are the decision-making controller for a Business Evaluator AI Agent.

Analyze the user's business idea and the information already provided.

Your job is to decide whether:

1. More information is needed
OR
2. Enough information is available to evaluate the business idea.

If enough information is available, your response MUST begin with:

DONE

If more information is needed, ask ONE clear and specific question.

Do not ask unnecessary questions.
Be concise and practical.
"""
)


def decide_node(state: State):

    response = llm.invoke(
        [controller_prompt] + state["messages"]
    )

    return {
        "messages": [response]
    }


# =========================
# MARKET ADVISOR
# =========================

def market_analyst_advisor(state: State):

    prompt = f"""
You are the Market Analyst Advisor.

Analyze this business idea:

{state["idea"]}

Evaluate:

- Target customers
- Market opportunity
- Customer segments
- Competitors
- Market trends
- Demand
- Possible differentiation

Give practical recommendations.
"""

    response = llm.invoke(prompt)

    return {
        "advisor_reports": {
            "Market Analyst": response.content
        }
    }


# =========================
# LEGAL ADVISOR
# =========================

def legal_advisor(state: State):

    prompt = f"""
You are the Legal Advisor.

Analyze this business idea:

{state["idea"]}

Evaluate:

- Intellectual property
- Licensing
- Copyright
- Trademarks
- Compliance
- Contracts
- Legal risks

Give practical recommendations.
"""

    response = llm.invoke(prompt)

    return {
        "advisor_reports": {
            "Legal Advisor": response.content
        }
    }


# =========================
# TECHNICAL ADVISOR
# =========================

def technical_advisor(state: State):

    prompt = f"""
You are the Technical Advisor.

Analyze this business idea:

{state["idea"]}

Evaluate:

- Development complexity
- Recommended technology stack
- Infrastructure
- Scalability
- Development time
- Technical costs
- Possible technical risks

Give practical recommendations.
"""

    response = llm.invoke(prompt)

    return {
        "advisor_reports": {
            "Technical Advisor": response.content
        }
    }


# =========================
# STRATEGY ADVISOR
# =========================

def strategist_advisor(state: State):

    prompt = f"""
You are the Strategy Advisor.

Analyze this business idea:

{state["idea"]}

Evaluate:

- Launch strategy
- Distribution channels
- Positioning
- Marketing
- Early customers
- Community building
- Growth opportunities
- Initial milestones

Give practical recommendations.
"""

    response = llm.invoke(prompt)

    return {
        "advisor_reports": {
            "Strategist Advisor": response.content
        }
    }


# =========================
# FINAL REPORT
# =========================

def collect_and_report(state: State):

    reports = state["advisor_reports"]

    report_prompt = f"""
You are a senior business consultant.

Create a clear and structured Business Idea Evaluation Report.

Business Idea:
{state["idea"]}

Advisor Reports:

{reports}

Your final report must contain:

1. Executive Summary
2. Market Analysis
3. Legal Considerations
4. Technical Feasibility
5. Business Strategy
6. Key Risks
7. Strengths
8. Weaknesses
9. Recommendations
10. Final Verdict

Give practical and realistic recommendations.
"""

    response = llm.invoke(report_prompt)

    return {
        "final_report": response.content
    }


# =========================
# ADVISOR GRAPH
# =========================

def build_advisor_graph():

    builder = StateGraph(State)

    builder.add_node(
        "market_analyst_advisor",
        market_analyst_advisor
    )

    builder.add_node(
        "legal_advisor",
        legal_advisor
    )

    builder.add_node(
        "technical_advisor",
        technical_advisor
    )

    builder.add_node(
        "strategist_advisor",
        strategist_advisor
    )

    builder.add_node(
        "collect_and_report",
        collect_and_report
    )

    builder.set_entry_point("market_analyst_advisor")

    builder.add_edge(
        "market_analyst_advisor",
        "legal_advisor"
    )

    builder.add_edge(
        "legal_advisor",
        "technical_advisor"
    )

    builder.add_edge(
        "technical_advisor",
        "strategist_advisor"
    )

    builder.add_edge(
        "strategist_advisor",
        "collect_and_report"
    )

    builder.add_edge(
        "collect_and_report",
        END
    )

    return builder.compile()


advisor_graph = build_advisor_graph()


# =========================
# CHECK WHETHER MORE INFO
# IS NEEDED
# =========================

def check_business_idea(idea: str, conversation: List[BaseMessage]):

    state: State = {
        "idea": idea,
        "messages": conversation,
        "advisor_reports": {},
        "final_report": ""
    }

    result = decide_node(state)

    ai_message = result["messages"][0]

    if ai_message.content.strip().lower().startswith("done"):
        return {
            "status": "ready",
            "message": ai_message.content
        }

    return {
        "status": "needs_info",
        "message": ai_message.content
    }


# =========================
# RUN ADVISORS
# =========================

def evaluate_business(idea: str, conversation: List[BaseMessage]):

    state: State = {
        "idea": idea,
        "messages": conversation,
        "advisor_reports": {},
        "final_report": ""
    }

    result = advisor_graph.invoke(state)

    return result["final_report"]