from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from config import GROQ_API_KEY, TAVILY_API_KEY, LLM_MODEL, LANGUAGE_INSTRUCTION
from tavily import TavilyClient

llm = ChatGroq(api_key=GROQ_API_KEY, model=LLM_MODEL, temperature=0.3)
tavily = TavilyClient(api_key=TAVILY_API_KEY)

def run_competitor_analysis(business_idea: str, location: str, language: str = "english") -> str:
    
    search_results = tavily.search(
        query=f"top competitors {business_idea} {location} 2024",
        max_results=5
    )
    
    context = "\n".join([r["content"] for r in search_results["results"]])
    
    lang_instruction = LANGUAGE_INSTRUCTION.get(language, LANGUAGE_INSTRUCTION["english"])
    
    prompt = PromptTemplate(
        input_variables=["business_idea", "location", "context", "lang_instruction"],
        template="""
You are an expert business competitive analyst.
IMPORTANT: {lang_instruction}

Business Idea: {business_idea}
Location: {location}

Based on this live data:
{context}

Provide a detailed competitor analysis covering:
1. Top 5 Competitors (name, website, what they offer)
2. Their Strengths & Weaknesses
3. Market Gaps & Opportunities (what they are missing)
4. Your Competitive Advantage (how to beat them)
5. Pricing Comparison

Be specific. Format clearly with headings.
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