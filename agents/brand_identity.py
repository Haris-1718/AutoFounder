from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from config import GROQ_API_KEY, LLM_MODEL, LANGUAGE_INSTRUCTION

llm = ChatGroq(api_key=GROQ_API_KEY, model=LLM_MODEL, temperature=0.7)

def run_brand_identity(business_idea: str, location: str, language: str = "english") -> str:
    
    lang_instruction = LANGUAGE_INSTRUCTION.get(language, LANGUAGE_INSTRUCTION["english"])
    
    prompt = PromptTemplate(
        input_variables=["business_idea", "location", "lang_instruction"],
        template="""
You are an expert brand strategist and creative director.
IMPORTANT: {lang_instruction}

Business Idea: {business_idea}
Location: {location}

Create a complete brand identity package covering:

1. Business Name Suggestions (5 unique names with domain availability check format)
   - For each name explain why it works

2. Brand Tagline (3 options)

3. Brand Voice & Personality
   - Tone (professional/friendly/energetic etc)
   - Key messaging pillars (3)

4. Color Palette Suggestions
   - Primary color (with hex code)
   - Secondary color (with hex code)
   - Accent color (with hex code)
   - Why these colors work for this business

5. Target Brand Positioning Statement
   - "For [target audience] who [need], [Brand Name] is the [category] that [benefit] because [reason]"

Be creative and specific. Format clearly with headings.
"""
    )
    
    chain = prompt | llm
    result = chain.invoke({
        "business_idea": business_idea,
        "location": location,
        "lang_instruction": lang_instruction
    })
    
    return result.content