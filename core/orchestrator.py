import asyncio
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from config import GROQ_API_KEY, LLM_MODEL
from agents.market_research import run_market_research
from agents.competitor_analysis import run_competitor_analysis
from agents.brand_identity import run_brand_identity
from agents.legal_compliance import run_legal_compliance
from agents.content_generation import run_content_generation
from agents.financial_modeling import run_financial_modeling

llm = ChatGroq(api_key=GROQ_API_KEY, model=LLM_MODEL, temperature=0.1)

def detect_language(text: str) -> str:
    prompt = PromptTemplate(
        input_variables=["text"],
        template="""
Detect the language of this text: "{text}"

Reply with ONLY one word:
- "english" if it's written in English
- "roman_urdu" if it's written in Roman Urdu (Urdu words in English letters)

Just one word, nothing else.
"""
    )
    chain = prompt | llm
    result = chain.invoke({"text": text})
    lang = result.content.strip().lower()
    if "roman" in lang or "urdu" in lang:
        return "roman_urdu"
    return "english"

async def run_agent_async(func, business_idea, location, language):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, func, business_idea, location, language)
    return result

async def run_all_agents(business_idea: str, location: str, language: str) -> dict:
    
    print("\n🚀 AutoFounder Agent Starting...")
    print(f"📋 Business: {business_idea}")
    print(f"📍 Location: {location}")
    print(f"🌐 Language: {language}")
    print("\n⚡ Running all 6 agents in parallel...\n")

    tasks = await asyncio.gather(
        run_agent_async(run_market_research, business_idea, location, language),
        run_agent_async(run_competitor_analysis, business_idea, location, language),
        run_agent_async(run_brand_identity, business_idea, location, language),
        run_agent_async(run_legal_compliance, business_idea, location, language),
        run_agent_async(run_content_generation, business_idea, location, language),
        run_agent_async(run_financial_modeling, business_idea, location, language),
    )

    print("✅ All agents completed!\n")

    return {
        "market_research": tasks[0],
        "competitor_analysis": tasks[1],
        "brand_identity": tasks[2],
        "legal_compliance": tasks[3],
        "content_generation": tasks[4],
        "financial_modeling": tasks[5],
        "language": language
    }

def run_orchestrator(business_idea: str, location: str) -> dict:
    language = detect_language(business_idea + " " + location)
    return asyncio.run(run_all_agents(business_idea, location, language))