from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from config import GROQ_API_KEY, LLM_MODEL, LANGUAGE_INSTRUCTION

llm = ChatGroq(api_key=GROQ_API_KEY, model=LLM_MODEL, temperature=0.7)

def run_content_generation(business_idea: str, location: str, language: str = "english") -> str:
    
    lang_instruction = LANGUAGE_INSTRUCTION.get(language, LANGUAGE_INSTRUCTION["english"])
    
    prompt = PromptTemplate(
        input_variables=["business_idea", "location", "lang_instruction"],
        template="""
You are an expert content strategist and copywriter.
IMPORTANT: {lang_instruction}

Business Idea: {business_idea}
Location: {location}

Create a complete content package covering:

1. Landing Page Copy
   - Hero headline & subheadline
   - Value proposition (3 key benefits)
   - Call to action (CTA) text
   - About us section
   - Testimonial placeholders (3)

2. 30-Day Social Media Calendar
   - Week 1: Brand awareness posts (7 post ideas)
   - Week 2: Educational content (7 post ideas)
   - Week 3: Engagement posts (7 post ideas)
   - Week 4: Promotional posts (7 post ideas)

3. Email Welcome Sequence (3 emails)
   - Email 1: Welcome email (subject + body)
   - Email 2: Value email - Day 3 (subject + body)
   - Email 3: Offer email - Day 7 (subject + body)

4. Bio for Social Media Platforms
   - Instagram bio
   - LinkedIn bio
   - Twitter/X bio

Be creative, engaging and specific to {location} market. Format clearly with headings.
"""
    )
    
    chain = prompt | llm
    result = chain.invoke({
        "business_idea": business_idea,
        "location": location,
        "lang_instruction": lang_instruction
    })
    
    return result.content