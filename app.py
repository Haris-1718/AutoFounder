import streamlit as st
from core.orchestrator import run_orchestrator
from core.synthesis import run_synthesis, save_to_docx
import os

# Page config
st.set_page_config(
    page_title="AutoFounder",
    page_icon="🚀",
    layout="wide"
)

# Header
st.title("🚀 AutoFounder")
st.subheader("AI-Powered Startup Launch Agent")
st.markdown("*English ya Roman Urdu mein likho — AutoFounder samajh jayega!*")
st.markdown("---")

# Input section
col1, col2 = st.columns(2)

with col1:
    business_idea = st.text_input(
        "💡 Business Idea",
        placeholder="e.g. online fitness coaching / online tuition ka kaam"
    )

with col2:
    location = st.text_input(
        "📍 Location",
        placeholder="e.g. Pakistan / Lahore"
    )

st.markdown("---")

# Generate button
if st.button("🚀 Generate Startup Package", use_container_width=True):
    
    if not business_idea or not location:
        st.error("⚠️ Please enter both business idea and location!")
    
    else:
        progress = st.progress(0)
        status = st.status("🤖 AutoFounder kaam kar raha hai...", expanded=True)
        
        with status:
            st.write("🌐 Language detect ho rahi hai...")
            progress.progress(10)

            st.write("⚡ 6 AI agents parallel chal rahe hain...")
            progress.progress(20)
            
            results = run_orchestrator(business_idea, location)
            progress.progress(60)

            # Show detected language
            lang = results.get("language", "english")
            if lang == "roman_urdu":
                st.write("✅ Language detect hui: **Roman Urdu**")
            else:
                st.write("✅ Language detect hui: **English**")

            st.write("✅ Sare agents complete!")
            
            st.write("📝 Executive summary ban rahi hai...")
            summary = run_synthesis(results, business_idea, location)
            progress.progress(80)
            st.write("✅ Summary ready!")
            
            st.write("💾 DOCX file save ho rahi hai...")
            filename = save_to_docx(results, summary, business_idea, location)
            progress.progress(100)
            st.write("✅ Report save ho gayi!")
        
        status.update(label="✅ Startup Package Ready!", state="complete")
        
        st.markdown("---")
        
        # Executive Summary
        st.header("📋 Executive Summary")
        st.markdown(summary)
        
        st.markdown("---")
        
        # All sections in tabs
        st.header("📊 Full Report")
        
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📈 Market Research",
            "🥊 Competitor Analysis",
            "🏷️ Brand Identity",
            "⚖️ Legal Compliance",
            "📝 Content Strategy",
            "💰 Financial Model"
        ])
        
        with tab1:
            st.markdown(results["market_research"])
        with tab2:
            st.markdown(results["competitor_analysis"])
        with tab3:
            st.markdown(results["brand_identity"])
        with tab4:
            st.markdown(results["legal_compliance"])
        with tab5:
            st.markdown(results["content_generation"])
        with tab6:
            st.markdown(results["financial_modeling"])
        
        st.markdown("---")
        
        # Download button
        with open(filename, "rb") as f:
            st.download_button(
                label="📥 Download Full Report (DOCX)",
                data=f,
                file_name=os.path.basename(filename),
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )