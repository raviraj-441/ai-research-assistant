# Agent functions for research system
from typing import List
from langchain_groq import ChatGroq
from tavily import TavilyClient
import streamlit as st
from config import *

# Initialize clients
tavily = TavilyClient(api_key=TAVILY_API_KEY)
groq_llm = ChatGroq(
    temperature=GROQ_TEMPERATURE,
    model_name=GROQ_MODEL_NAME,
    api_key=GROQ_API_KEY
)

def update_conversation(agent: str, message: str, icon: str = "ℹ️") -> None:
    """Update the conversation history in the Streamlit session state."""
    st.session_state.messages.append({"role": agent, "content": message, "icon": icon})

def query_generator_agent(state: dict) -> str:
    """Generate focused search queries based on current research state."""
    selected_titles = [doc['title'] for doc in state["research_data"]]
    if len(selected_titles) > MAX_SOURCES_IN_PROMPT:
        selected_titles = selected_titles[-MAX_SOURCES_IN_PROMPT:]
    titles = ", ".join(selected_titles) or "none"
    
    prompt = (
        f"Based on the research query '{state['query']}' and the current source titles ({titles}), "
        f"generate a new, more focused search query for deeper exploration. Provide a single query."
    )
    response = groq_llm.invoke(prompt)
    new_query = response.content.strip()
    update_conversation("QueryGenerator", f"Generated exploration query: '{new_query}'", "🔄")
    return new_query

def research_agent(state: dict) -> dict:
    """Conduct research using Tavily search API."""
    if state["current_iteration"] >= state["max_iterations"]:
        update_conversation("System", "⚠️ Maximum iterations reached - stopping research", "⏹️")
        return state

    state["current_iteration"] += 1
    update_conversation(
        "Researcher",
        f"**Iteration {state['current_iteration']}/{state['max_iterations']}**",
        "🔍"
    )

    exploration_query = query_generator_agent(state)

    try:
        search_params = {
            "query": exploration_query,
            "search_depth": "advanced" if state["research_depth"] != "Overview" else "basic",
            "max_results": 15 if state["research_depth"] == "Deep Dive" else 10,
            "include_answer": False
        }
        search_result = tavily.search(**search_params)
        new_results = [res for res in search_result["results"] if res not in state["research_data"]]
        state["research_data"].extend(new_results)
        update_conversation(
            "Researcher",
            f"Found {len(new_results)} new sources using query: '{exploration_query}'\nTotal sources: {len(state['research_data'])}",
            "📚"
        )
    except Exception as e:
        update_conversation("Error", f"Research failed: {str(e)}", "❌")
    return state

def answer_drafter_agent(state: dict) -> dict:
    """Draft initial answer based on research data."""
    update_conversation("Drafter", "Creating final draft...", "📝")
    selected_sources = state["research_data"][-MAX_SOURCES_IN_PROMPT:] if len(state["research_data"]) > MAX_SOURCES_IN_PROMPT else state["research_data"]
    
    context = "\n".join(
        f"### Source {i+1}\n**{doc['title']}**\nURL: {doc.get('url', 'N/A')}\n{doc['content'][:SOURCE_CHAR_LIMIT_DRAFT]}"
        for i, doc in enumerate(selected_sources)
    )
    
    prompt = f"""
    **Strict Requirements:**
    1. Only include facts with direct source citations.
    2. Mark uncertain claims with [Needs Verification].
    3. Remove any unsupported statements.
    4. Use exact source numbers from provided materials.
    
    **Research Question:** {state['query']}
    **Previous Issues:** {state.get('fact_checks', [])}
    
    **Sources:**
    {context}
    
    Create a comprehensive report with:
    - Clear section headers.
    - In-text citations [Source X].
    - Technical specifications.
    - Historical timeline.
    """
    
    response = groq_llm.invoke(prompt)
    state["answer"] = response.content
    state["answer"] = "\n".join(
        line for line in state["answer"].split("\n")
        if "[Source" in line or "Needs Verification" in line
        or not any(keyword in line for keyword in ["claim", "state", "report"])
    )
    update_conversation("Drafter", "Final draft with strict citations", "✅")
    return state

def fact_checker_agent(state: dict) -> dict:
    """Verify claims against source materials."""
    update_conversation("FactChecker", "Verifying claims against sources...", "🔎")
    selected_sources = state["research_data"][-MAX_SOURCES_IN_PROMPT:] if len(state["research_data"]) > MAX_SOURCES_IN_PROMPT else state["research_data"]
    
    sources_str = "".join(
        f"Source {i+1}: {doc['title']}\n{doc['content'][:SOURCE_CHAR_LIMIT_FACTCHECK]}\n\n"
        for i, doc in enumerate(selected_sources)
    )
    
    verification_prompt = f"""
    **Document to Verify:**
    {state['answer']}
    
    **Available Sources:**
    {sources_str}
    
    Identify:
    1. Claims needing stronger citations.
    2. Statements conflicting with sources.
    3. Unverified technical assertions.
    4. Overly broad generalizations.
    
    For EACH issue:
    - Quote the exact text.
    - List relevant source numbers.
    - Classify as: Unsupported/Contradicted/Unclear.
    - Suggest resolution approach.
    
    Format as:
    - [❌] [Type]: [Exact Text]
      Sources: [Numbers]
      Action: [Research Needed/Remove/Clarify]
    """
    
    response = groq_llm.invoke(verification_prompt)
    state["fact_checks"] = response.content.split("\n")
    update_conversation(
        "FactChecker",
        f"Identified {len([x for x in state['fact_checks'] if '❌' in x])} resolvable issues",
        "⚠️"
    )
    return state

def corrector_agent(state: dict) -> dict:
    """Generate correction queries for identified issues."""
    update_conversation("Corrector", "Resolving identified issues...", "🔧")
    failed_checks = [check for check in state["fact_checks"] if "❌" in check]
    
    correction_plan = """
    Based on the following issues, generate specific research queries to resolve them:
    
    {issues}
    
    Format as:
    - Issue: [brief description]
      Resolution Query: [specific search query to resolve this]
    """.format(issues="\n".join(failed_checks))
    
    response = groq_llm.invoke(correction_plan)
    correction_queries = [
        line.split("Resolution Query: ")[1]
        for line in response.content.split("\n")
        if "Resolution Query:" in line
    ]
    
    original_query = state["query"]
    state["query"] += " " + " ".join([f'"{q}"' for q in correction_queries])
    update_conversation(
        "Corrector",
        f"Generated {len(correction_queries)} correction queries\nOriginal query: {original_query}\nUpdated query: {state['query']}",
        "📌"
    )
    return state

def validation_agent(state: dict) -> dict:
    """Perform final validation of the research report."""
    update_conversation("Validator", "Final verification...", "🛡️")
    selected_sources = state["research_data"][-MAX_SOURCES_IN_PROMPT:] if len(state["research_data"]) > MAX_SOURCES_IN_PROMPT else state["research_data"]
    
    sources_val_str = "".join(
        f"Source {i+1}: {doc['title']}\n{doc['content'][:SOURCE_CHAR_LIMIT_VALIDATION]}\n\n"
        for i, doc in enumerate(selected_sources)
    )
    
    final_check_prompt = f"""
    Final Report:
    {state['answer']}
    
    Sources:
    {sources_val_str}
    
    Identify ANY remaining:
    1. Uncited claims.
    2. Contradictions.
    3. Uncertain statements.
    
    For EACH issue:
    - [❌] [Exact Quote]
      Required Action: [Remove/Clarify/Add Citation]
    """
    
    response = groq_llm.invoke(final_check_prompt)
    state["final_checks"] = response.content.split("\n")
    update_conversation("Validator", "Final verification completed", "🛡️")
    return state

def report_generator_agent(state: dict) -> dict:
    """Generate the final professional report."""
    update_conversation("Reporter", "Compiling professional report...", "📑")
    selected_sources = state["research_data"][-MAX_SOURCES_IN_PROMPT:] if len(state["research_data"]) > MAX_SOURCES_IN_PROMPT else state["research_data"]
    
    sources_report_str = "".join(
        f"Source {i+1}: {doc['title']} | {doc.get('url', 'N/A')}\n{doc['content'][:SOURCE_CHAR_LIMIT_REPORT]}\n\n"
        for i, doc in enumerate(selected_sources)
    )
    
    report_prompt = f"""
    **Professional Report Requirements:**
    1. Create a very detailed 15-20 page equivalent report in academic paper format.
    2. Include sections:
       - Executive Summary
       - Introduction & Background
       - Technical Architecture
       - Key Achievements
       - Ethical Considerations
       - Extended Analysis and Future Outlook
       - Conclusion
       - References (APA format)
    3. Support all claims with [Source X] citations.
    4. Include data tables for key metrics.
    5. Add a timeline of major milestones.
    6. Present 3-5 case studies.
    7. Incorporate an expert commentary section.
    
    **Research Data:**
    {state['answer']}
    
    **Sources:**
    {sources_report_str}
    
    **Fact Checks:**
    {state['fact_checks']}
    
    Create a comprehensive and very detailed professional report using markdown formatting.
    """
    
    response = groq_llm.invoke(report_prompt)
    state["professional_report"] = response.content
    state["professional_report"] += "\n\n## Appendices\n"
    state["professional_report"] += "\n".join(
        f"### Source {i+1}\n**{doc['title']}**\n*URL: {doc.get('url', 'N/A')}*\n{doc['content'][:SOURCE_CHAR_LIMIT_REPORT]}..."
        for i, doc in enumerate(selected_sources)
    )
    update_conversation("Reporter", "Professional report generated", "✅")
    return state