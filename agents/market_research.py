from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from config import GROQ_API_KEY, TAVILY_API_KEY, LLM_MODEL, LANGUAGE_INSTRUCTION
from tavily import TavilyClient

llm = ChatGroq(api_key=GROQ_API_KEY, model=LLM_MODEL, temperature=0.3)
tavily = TavilyClient(api_key=TAVILY_API_KEY)

def run_market_research(business_idea: str, location: str, language: str = "english") -> str:
    
    search_results = tavily.search(
        query=f"{business_idea} market size trends {location} 2024",
        max_results=5
    )
    
    context = "\n".join([r["content"] for r in search_results["results"]])
    
    lang_instruction = LANGUAGE_INSTRUCTION.get(language, LANGUAGE_INSTRUCTION["english"])
    
    prompt = PromptTemplate(
        input_variables=["business_idea", "location", "context", "lang_instruction"],
        template="""
You are an expert market research analyst.
IMPORTANT: {lang_instruction}

Business Idea: {business_idea}
Location: {location}

Based on this live data:
{context}

Provide a detailed market research report covering:
1. Market Size & Opportunity
2. Target Audience & Demographics
3. Market Trends (2024-2025)
4. Pricing Analysis
5. Growth Potential

Be specific with numbers and data. Format clearly with headings.
"""
    )
    
    chain = prompt | llm
    result = chain.invoke({
        "business_idea": business_idea,
        "location": location,
        "context": context,
        "lang_instruction": lang_instruction
    })
    
    return result.content