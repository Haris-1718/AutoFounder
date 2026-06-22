from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from config import GROQ_API_KEY, TAVILY_API_KEY, LLM_MODEL, LANGUAGE_INSTRUCTION
from tavily import TavilyClient

llm = ChatGroq(api_key=GROQ_API_KEY, model=LLM_MODEL, temperature=0.3)
tavily = TavilyClient(api_key=TAVILY_API_KEY)

def run_financial_modeling(business_idea: str, location: str, language: str = "english") -> str:
    
    search_results = tavily.search(
        query=f"{business_idea} startup costs revenue model {location} 2024",
        max_results=5
    )
    
    context = "\n".join([r["content"] for r in search_results["results"]])
    
    lang_instruction = LANGUAGE_INSTRUCTION.get(language, LANGUAGE_INSTRUCTION["english"])
    
    prompt = PromptTemplate(
        input_variables=["business_idea", "location", "context", "lang_instruction"],
        template="""
You are an expert financial analyst and startup advisor.
IMPORTANT: {lang_instruction}

Business Idea: {business_idea}
Location: {location}

Based on this live data:
{context}

Create a complete financial model covering:

1. Revenue Model Options (3 options)
   - Model name
   - How it works
   - Pros & cons
   - Recommended pricing in PKR

2. Startup Costs Breakdown
   - One-time costs (tools, setup etc)
   - Monthly recurring costs
   - Total initial investment needed

3. Month 1-6 Revenue Projection
   - Realistic client acquisition numbers
   - Expected monthly revenue
   - Running total

4. Break-Even Analysis
   - Fixed costs per month
   - Revenue needed to break even
   - Expected month to break even

5. 90-Day Action Plan with Financial Milestones
   - Month 1 goals & targets
   - Month 2 goals & targets
   - Month 3 goals & targets

Use PKR for all amounts. Be realistic and specific. Format clearly with headings.
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