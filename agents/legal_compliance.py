from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from config import GROQ_API_KEY, TAVILY_API_KEY, LLM_MODEL, LANGUAGE_INSTRUCTION
from tavily import TavilyClient

llm = ChatGroq(api_key=GROQ_API_KEY, model=LLM_MODEL, temperature=0.3)
tavily = TavilyClient(api_key=TAVILY_API_KEY)

def run_legal_compliance(business_idea: str, location: str, language: str = "english") -> str:
    
    search_results = tavily.search(
        query=f"how to register online business {location} legal requirements 2024",
        max_results=5
    )
    
    context = "\n".join([r["content"] for r in search_results["results"]])
    
    lang_instruction = LANGUAGE_INSTRUCTION.get(language, LANGUAGE_INSTRUCTION["english"])
    
    prompt = PromptTemplate(
        input_variables=["business_idea", "location", "context", "lang_instruction"],
        template="""
You are an expert business legal advisor.
IMPORTANT: {lang_instruction}

Business Idea: {business_idea}
Location: {location}

Based on this live data:
{context}

Provide a complete legal compliance guide covering:

1. Business Registration Steps
   - Type of business structure (Sole proprietorship, LLC, etc)
   - Step by step registration process
   - Relevant government bodies

2. Required Licenses & Permits
   - List all necessary licenses
   - Where to get them

3. Tax Obligations
   - Tax registration (NTN, GST etc)
   - Tax rates applicable
   - Filing requirements

4. Legal Checklist (tick list format)

5. Basic Terms & Privacy Policy Requirements
   - Key clauses needed for online business

Be specific to {location}. Format clearly with headings.
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