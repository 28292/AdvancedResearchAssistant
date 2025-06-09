import streamlit as st
import os
from dotenv import load_dotenv
from utils.DocumentSearch import build_vector_store_from_docs, build_qa_chain, ask_question
from utils.FileLoader import load_uploaded_file
from utils.WebAPISearch import search_regulations
from utils.REALTIMEINTERNETSEARCH import search_serpapi

# Load environment variables
load_dotenv()

# Verify SerpAPI key
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
if not SERPAPI_API_KEY:
    st.error("❌ Missing SERPAPI_API_KEY in your environment. Please set it in your .env file.")

st.set_page_config(page_title="Agentic AI Search")
st.header("🤖 AI - Powered Search System")

# Sidebar Mode Selector
search_mode = st.sidebar.radio("Choose Search Mode", ["📄 Document Search", "🌐 Specific Web API", "🌎 Internet Search"])

query = st.text_input("🔍 Enter your query")

if search_mode == "📄 Document Search":
    uploaded_file = st.file_uploader("Upload a file", type=["pdf", "txt", "docx", "csv", "xlsx"])
    if uploaded_file:
        docs = load_uploaded_file(uploaded_file)
        db = build_vector_store_from_docs(docs)
        qa_chain = build_qa_chain(db)

        if query:
            answer, sources = ask_question(qa_chain, query)
            st.subheader("💡 Answer")
            st.write(answer)

            st.subheader("📄 Source Excerpts")
            for s in sources:
                st.markdown(f"**Source:** {s.metadata.get('source', 'uploaded')}")
                st.text(s.page_content[:300])

elif search_mode == "🌐 Specific Web API":
    topic = st.text_input("Enter the topic (e.g. 'climate change')")
    agency = st.text_input("Optional agency (e.g. 'EPA')")

    if query or topic:
        search_topic = query or topic
        result = search_regulations(search_topic, agency_id=agency if agency else None)
        st.subheader("📡 API Results")
        st.markdown(result)

elif search_mode == "🌎 Internet Search":
    if SERPAPI_API_KEY:
        if query:
            web_result = search_serpapi(query)
            st.subheader("🌍 Web Search Result")
            st.markdown(web_result)
    else:
        st.warning("Please provide a valid SERPAPI_API_KEY in your environment to use web search.")
