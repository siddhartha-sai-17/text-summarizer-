import streamlit as st
import os
from dotenv import load_dotenv
import pyperclip
import PyPDF2
from docx import Document

# --- Import Core Logic ---
# Ensure these files are in the same directory
from gemini_client import call_gemini_api
from summarizer import summarize_text
from grammar_corrector import correct_grammar
from ai_detector import detect_ai_text

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Text Summarizer & Detector",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Load API Key ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- UI Styling ---
st.markdown("""
    <style>
        .stApp {
            background: #0a0a0a;
            color: #e5e7eb;
        }
        .stTextArea textarea {
            min-height: 250px;
        }
        .stButton>button {
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

# --- Main App ---
st.title("🤖 AI Text Summarizer & Detector")
st.write("Paste your text, upload a file, and get a concise summary, grammar check, or AI analysis in seconds.")

# --- Text Input Area ---
input_text = st.text_area("Original Text", placeholder="Paste your article, essay, or document here...", height=250, label_visibility="collapsed")

# --- File Uploader and Action Buttons ---
col1, col2, col3 = st.columns(3)
with col1:
    uploaded_file = st.file_uploader("Upload a file", type=['txt', 'pdf', 'docx'], label_visibility="collapsed")
with col2:
    if st.button("📋 Paste from Clipboard"):
        try:
            input_text = pyperclip.paste()
            st.rerun()
        except Exception as e:
            st.error(f"Could not paste from clipboard: {e}")
with col3:
    if st.button("🗑️ Clear Text"):
        input_text = ""
        st.rerun()

# --- File Processing Logic ---
if uploaded_file is not None:
    try:
        if uploaded_file.type == "text/plain":
            input_text = uploaded_file.getvalue().decode("utf-8")
        elif uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            input_text = text
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(uploaded_file)
            input_text = "\n".join([para.text for para in doc.paragraphs])
        st.success(f"Successfully loaded text from {uploaded_file.name}")
    except Exception as e:
        st.error(f"Error reading file: {e}")

# --- Control Panel ---
st.markdown("---")
st.subheader("Control Panel")
c1, c2, c3 = st.columns(3)
with c1:
    summary_format = st.selectbox(
        "Summary Format",
        ('Paragraph', 'Bullet Points', 'Keywords'),
        key='format'
    )
with c2:
    summary_tone = st.selectbox(
        "Summary Tone",
        ('Neutral', 'Formal', 'Casual', 'Academic'),
        key='tone'
    )
with c3:
    summary_length = st.number_input(
        "Summary Length (lines/points)",
        min_value=1,
        max_value=20,
        value=5,
        key='length'
    )

# --- Action Buttons ---
st.markdown("---")
action_col1, action_col2, action_col3 = st.columns(3)
with action_col1:
    summarize_button = st.button("✨ Summarize", use_container_width=True)
with action_col2:
    correct_button = st.button("✍️ Correct Grammar", use_container_width=True)
with action_col3:
    detect_button = st.button("🔍 Analyze for AI", use_container_width=True)

# --- Output Area ---
st.markdown("---")

if 'result' not in st.session_state:
    st.session_state.result = None
if 'result_type' not in st.session_state:
    st.session_state.result_type = None


# --- Event Handlers ---
if summarize_button:
    if not input_text:
        st.warning("Please enter some text to summarize.")
    elif not GEMINI_API_KEY:
        st.error("GEMINI_API_KEY is not set. Please add it to your .env file.")
    else:
        with st.spinner("Summarizing..."):
            try:
                result = summarize_text(GEMINI_API_KEY, input_text, summary_format.lower(), summary_tone.lower(), summary_length)
                st.session_state.result = result
                st.session_state.result_type = 'summary'
            except Exception as e:
                st.error(f"An error occurred: {e}")

if correct_button:
    if not input_text:
        st.warning("Please enter some text to correct.")
    elif not GEMINI_API_KEY:
        st.error("GEMINI_API_KEY is not set. Please add it to your .env file.")
    else:
        with st.spinner("Correcting grammar..."):
            try:
                result = correct_grammar(GEMINI_API_KEY, input_text)
                st.session_state.result = result
                st.session_state.result_type = 'correction'
                st.success("Grammar corrected! The original text has been updated.")
                # This is tricky in Streamlit, best to show the result
                st.text_area("Corrected Text", value=result, height=250)
            except Exception as e:
                st.error(f"An error occurred: {e}")

if detect_button:
    if not input_text:
        st.warning("Please enter some text to analyze.")
    elif not GEMINI_API_KEY:
        st.error("GEMINI_API_KEY is not set. Please add it to your .env file.")
    else:
        with st.spinner("Analyzing for AI..."):
            try:
                result = detect_ai_text(GEMINI_API_KEY, input_text)
                st.session_state.result = result
                st.session_state.result_type = 'detection'
            except Exception as e:
                st.error(f"An error occurred: {e}")

# --- Display Results ---
if st.session_state.result:
    st.subheader("Results")
    if st.session_state.result_type == 'summary':
        st.markdown(st.session_state.result)
    elif st.session_state.result_type == 'detection':
        data = st.session_state.result
        ai_prob = data.get('overall_probability', 0)
        human_prob = 100 - ai_prob

        res_col1, res_col2 = st.columns([1, 2])
        with res_col1:
            st.metric(label="Likely AI-Generated", value=f"{ai_prob}%")

        with res_col2:
            st.write("Breakdown:")
            st.progress(ai_prob / 100, text=f"AI: {ai_prob}%")
            st.progress(human_prob / 100, text=f"Human: {human_prob}%")
        
        with st.expander("Understanding your results"):
            st.write(data.get('explanation', ''))
            st.caption("This detector is not 100% accurate and should be used as an indicator rather than a definitive judgment.")

