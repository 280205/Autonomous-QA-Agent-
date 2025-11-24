"""
Streamlit UI for the QA Agent System.
Provides interface for document upload, test case generation, and script generation.
"""

import streamlit as st
import requests
import json
import os
from pathlib import Path
import time


# Configuration
# For Streamlit Cloud, set BACKEND_URL in secrets
API_BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Page configuration
st.set_page_config(
    page_title="QA Agent - Test Generation",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Glassmorphism Theme with Animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Animated Gradient Background */
    .main {
        background: linear-gradient(-45deg, #0a0e27, #1a1f3a, #0f1123, #1e2139);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }
    
    /* Glowing Headers with Animation */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 1rem;
        animation: shimmer 3s linear infinite, float 3s ease-in-out infinite;
        text-shadow: 0 0 30px rgba(102, 126, 234, 0.5);
    }
    
    @keyframes shimmer {
        to { background-position: 200% center; }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .section-header {
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
        margin-top: 3rem;
        margin-bottom: 1.5rem;
        padding: 1rem 1.5rem;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    /* Glassmorphic Success/Error/Info Boxes */
    .success-box {
        padding: 1.5rem;
        background: rgba(76, 175, 80, 0.1);
        backdrop-filter: blur(10px);
        border-left: 4px solid #4CAF50;
        color: #a5d6a7;
        margin: 1.5rem 0;
        border-radius: 16px;
        border: 1px solid rgba(76, 175, 80, 0.2);
        box-shadow: 0 8px 32px 0 rgba(76, 175, 80, 0.2);
        animation: slideInLeft 0.5s ease-out;
    }
    
    .error-box {
        padding: 1.5rem;
        background: rgba(244, 67, 54, 0.1);
        backdrop-filter: blur(10px);
        border-left: 4px solid #f44336;
        color: #ef9a9a;
        margin: 1.5rem 0;
        border-radius: 16px;
        border: 1px solid rgba(244, 67, 54, 0.2);
        box-shadow: 0 8px 32px 0 rgba(244, 67, 54, 0.2);
        animation: shake 0.5s ease-out;
    }
    
    .info-box {
        padding: 1.5rem;
        background: rgba(33, 150, 243, 0.1);
        backdrop-filter: blur(10px);
        border-left: 4px solid #2196F3;
        color: #90caf9;
        margin: 1.5rem 0;
        border-radius: 16px;
        border: 1px solid rgba(33, 150, 243, 0.2);
        box-shadow: 0 8px 32px 0 rgba(33, 150, 243, 0.2);
        animation: slideInLeft 0.5s ease-out;
    }
    
    @keyframes slideInLeft {
        from { transform: translateX(-50px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
    
    /* Glassmorphic Test Case Cards with Hover Effects */
    .test-case-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .test-case-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 50px 0 rgba(102, 126, 234, 0.4);
        border-color: rgba(102, 126, 234, 0.5);
    }
    
    .test-case-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .test-case-card:hover::before {
        left: 100%;
    }
    
    /* Subtle Navigation Buttons */
    .stButton>button {
        width: 100%;
        background: rgba(255, 255, 255, 0.05);
        color: #b0b0c0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 50px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 4px 12px 0 rgba(102, 126, 234, 0.3);
        background: rgba(102, 126, 234, 0.15);
        border-color: rgba(102, 126, 234, 0.3);
        color: #e0e0f0;
    }
    
    .stButton>button:active {
        transform: translateY(0) scale(0.98);
    }
    
    /* Primary Button (Active Navigation) - Subtle Highlight */
    .stButton>button[kind="primary"] {
        background: rgba(102, 126, 234, 0.2);
        border-color: rgba(102, 126, 234, 0.4);
        color: #c8d0ff;
        box-shadow: 0 2px 8px 0 rgba(102, 126, 234, 0.25);
    }
    
    .stButton>button[kind="primary"]:hover {
        background: rgba(102, 126, 234, 0.25);
        border-color: rgba(102, 126, 234, 0.5);
        color: #dce3ff;
    }
    
    /* Glassmorphic Sidebar with Blur Effect */
    section[data-testid="stSidebar"] {
        background: rgba(10, 14, 39, 0.8) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem 1rem;
        box-shadow: 4px 0 24px 0 rgba(0, 0, 0, 0.3);
    }
    
    section[data-testid="stSidebar"] > div {
        background: transparent !important;
    }
    
    /* Hide all horizontal lines in sidebar */
    section[data-testid="stSidebar"] hr,
    section[data-testid="stSidebar"] .stDivider {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Hide radio label */
    section[data-testid="stSidebar"] .stRadio > label[data-baseweb="radio"] {
        display: none !important;
    }
    
    /* Futuristic Navigation Items */
    .stRadio > div {
        gap: 1rem;
    }
    
    .stRadio > label {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        padding: 1rem 1.5rem !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        cursor: pointer !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        display: flex !important;
        align-items: center !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        color: #e0e0e0 !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stRadio > label::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent) !important;
        transition: left 0.5s !important;
    }
    
    .stRadio > label:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(102, 126, 234, 0.5) !important;
        color: #ffffff !important;
        transform: translateX(5px) !important;
        box-shadow: 0 8px 16px 0 rgba(102, 126, 234, 0.3) !important;
    }
    
    .stRadio > label:hover::before {
        left: 100% !important;
    }
    
    /* Hide default radio button */
    .stRadio input[type="radio"] {
        display: none !important;
    }
    
    /* Selected state with gradient */
    .stRadio input[type="radio"]:checked + label {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border-color: transparent !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        box-shadow: 0 8px 24px 0 rgba(102, 126, 234, 0.5) !important;
        transform: scale(1.02) !important;
    }
    
    /* Sidebar Headers */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #4CAF50;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Sidebar Divider - Hidden */
    section[data-testid="stSidebar"] hr {
        display: none;
    }
    
    /* Knowledge Base Status Badge */
    section[data-testid="stSidebar"] .element-container {
        background-color: transparent;
    }
    
    /* Futuristic Input Fields */
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>select {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput>div>div>input:focus, 
    .stTextArea>div>div>textarea:focus {
        border-color: rgba(102, 126, 234, 0.8) !important;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.4) !important;
        background: rgba(255, 255, 255, 0.08) !important;
    }
    
    /* Animated File Uploader */
    .stFileUploader {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(10px) !important;
        border: 2px dashed rgba(102, 126, 234, 0.4) !important;
        border-radius: 20px !important;
        padding: 3rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader:hover {
        border-color: rgba(102, 126, 234, 0.8) !important;
        background: rgba(102, 126, 234, 0.05) !important;
        transform: scale(1.02) !important;
    }
    
    /* Glassmorphic Expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        transition: all 0.3s ease !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        border-color: rgba(102, 126, 234, 0.5) !important;
    }
    
    /* Futuristic Code Blocks */
    .stCodeBlock {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Animated Metrics Cards */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        padding: 1.5rem !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37) !important;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 12px 40px 0 rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Futuristic Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: transparent !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        color: #ffffff !important;
        border-radius: 12px 12px 0 0 !important;
        padding: 1rem 2rem !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        transform: translateY(-2px) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        box-shadow: 0 8px 24px 0 rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Animated Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb) !important;
        background-size: 200% auto !important;
        animation: shimmer 2s linear infinite !important;
    }
    
    /* Enhanced Text Colors */
    p, span, label {
        color: #e0e0e0 !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Particle Effect Container */
    .particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }
    
    /* Glow Effects */
    .glow-text {
        text-shadow: 0 0 10px rgba(102, 126, 234, 0.8),
                     0 0 20px rgba(102, 126, 234, 0.6),
                     0 0 30px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []
if 'kb_built' not in st.session_state:
    st.session_state.kb_built = False
if 'test_cases' not in st.session_state:
    st.session_state.test_cases = []
if 'selected_test_case' not in st.session_state:
    st.session_state.selected_test_case = None
if 'generated_script' not in st.session_state:
    st.session_state.generated_script = None
if 'html_content' not in st.session_state:
    st.session_state.html_content = None


# Helper functions
def check_backend_health():
    """Check if backend is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False


def upload_documents(files):
    """Upload documents to backend"""
    files_data = []
    for file in files:
        files_data.append(
            ('files', (file.name, file.getvalue(), file.type))
        )
    
    response = requests.post(
        f"{API_BASE_URL}/upload",
        files=files_data
    )
    return response.json()


def build_knowledge_base(reset=False):
    """Build knowledge base"""
    response = requests.post(
        f"{API_BASE_URL}/build-knowledge-base",
        params={"reset": reset}
    )
    return response.json()


def generate_test_cases(query, top_k=5):
    """Generate test cases"""
    response = requests.post(
        f"{API_BASE_URL}/generate-test-cases",
        json={"query": query, "top_k": top_k}
    )
    return response.json()


def generate_selenium_script(test_case, html_content=None):
    """Generate Selenium script"""
    response = requests.post(
        f"{API_BASE_URL}/generate-selenium-script",
        json={"test_case": test_case, "html_content": html_content}
    )
    return response.json()


def get_kb_stats():
    """Get knowledge base statistics"""
    response = requests.get(f"{API_BASE_URL}/knowledge-base/stats")
    return response.json()


def get_test_suggestions():
    """Get test scenario suggestions"""
    response = requests.get(f"{API_BASE_URL}/test-suggestions")
    return response.json()


# Main UI
def main():
    # Dynamic Animated Header
    st.markdown('''
    <div style="text-align: center; padding: 2rem 0 3rem 0;">
        <div class="main-header">Autonomous QA Agent</div>
        <p style="font-size: 1.3rem; color: #a0a0ff; font-weight: 300; margin-top: 1rem; letter-spacing: 2px;">
            Generate Test Cases & Selenium Scripts with AI
        </p>
        <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 1.5rem;">
            <span style="background: rgba(102, 126, 234, 0.2); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.85rem; color: #90caf9; border: 1px solid rgba(102, 126, 234, 0.4);">AI-Powered</span>
            <span style="background: rgba(118, 75, 162, 0.2); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.85rem; color: #ce93d8; border: 1px solid rgba(118, 75, 162, 0.4);">Lightning Fast</span>
            <span style="background: rgba(76, 175, 80, 0.2); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.85rem; color: #a5d6a7; border: 1px solid rgba(76, 175, 80, 0.4);">Accurate</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Check backend health
    if not check_backend_health():
        st.error("Backend API is not running. Please start the FastAPI backend first.")
        st.code("python -m backend.main", language="bash")
        st.stop()
    
    # Sidebar
    with st.sidebar:
        # Futuristic Sidebar Header
        st.markdown("""
        <div style='text-align: center; padding: 2rem 0 2.5rem 0; margin-bottom: 2rem; background: rgba(255, 255, 255, 0.03); border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.1);'>
            <h2 style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 1.6rem; margin: 0; font-weight: 700; letter-spacing: 2px;'>QA AGENT</h2>
            <p style='color: #999; font-size: 0.75rem; margin: 0.5rem 0 0 0; letter-spacing: 3px;'>VERSION 1.0.0</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        st.markdown("<div style='color: #999; font-size: 0.75rem; font-weight: 600; letter-spacing: 1px; margin-bottom: 1rem; text-transform: uppercase;'>Navigation</div>", unsafe_allow_html=True)
        
        # Initialize page state
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "Home"
        
        # Navigation buttons
        nav_options = ["Home", "Document Upload", "Test Case Generation", "Script Generation", "Dashboard"]
        
        for nav_page in nav_options:
            if st.button(
                nav_page,
                key=f"nav_{nav_page}",
                use_container_width=True,
                type="primary" if st.session_state.current_page == nav_page else "secondary"
            ):
                st.session_state.current_page = nav_page
                st.rerun()
        
        page = st.session_state.current_page
        
        # Knowledge Base Status
        st.markdown("<div style='color: #999; font-size: 0.75rem; font-weight: 600; letter-spacing: 1px; margin: 2rem 0 1rem 0; text-transform: uppercase;'>Knowledge Base</div>", unsafe_allow_html=True)
        try:
            stats = get_kb_stats()
            kb_stats = stats.get("vector_db", {})
            if kb_stats.get("exists") and kb_stats.get("count", 0) > 0:
                st.markdown(f"""
                <div style='background: rgba(76, 175, 80, 0.1); backdrop-filter: blur(10px); padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(76, 175, 80, 0.3); box-shadow: 0 8px 32px 0 rgba(76, 175, 80, 0.2); animation: slideInLeft 0.5s ease-out;'>
                    <div style='display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem;'>
                        <div style='color: #a5d6a7; font-weight: 700; font-size: 1rem; display: flex; align-items: center; gap: 0.5rem;'>
                            ACTIVE
                        </div>
                        <div style='background: linear-gradient(135deg, #4CAF50, #81c784); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 1.8rem; font-weight: 800;'>{kb_stats.get('count')}</div>
                    </div>
                    <div style='color: #81c784; font-size: 0.8rem; font-weight: 500; letter-spacing: 1px;'>CHUNKS LOADED</div>
                    <div style='margin-top: 0.8rem; height: 4px; background: rgba(76, 175, 80, 0.2); border-radius: 2px; overflow: hidden;'>
                        <div style='height: 100%; background: linear-gradient(90deg, #4CAF50, #81c784); width: 100%; animation: shimmer 2s linear infinite;'></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.session_state.kb_built = True
            else:
                st.markdown("""
                <div style='background-color: #3d2d1a; padding: 1rem; border-radius: 6px; border: 1px solid #5a4a2d;'>
                    <div style='color: #ffcc80; font-weight: 600; font-size: 0.9rem;'>Not Built</div>
                    <div style='color: #ffb74d; font-size: 0.75rem; margin-top: 0.3rem;'>Upload documents first</div>
                </div>
                """, unsafe_allow_html=True)
                st.session_state.kb_built = False
        except:
            st.markdown("""
            <div style='background-color: #3d1a1a; padding: 1rem; border-radius: 6px; border: 1px solid #5a2d2d;'>
                <div style='color: #ef9a9a; font-weight: 600; font-size: 0.9rem;'>Error</div>
                <div style='color: #e57373; font-size: 0.75rem; margin-top: 0.3rem;'>Cannot check status</div>
            </div>
            """, unsafe_allow_html=True)
        

    
    # Main content based on selected page
    if page == "Home":
        show_home_page()
    elif page == "Document Upload":
        show_document_upload_page()
    elif page == "Test Case Generation":
        show_test_case_generation_page()
    elif page == "Script Generation":
        show_script_generation_page()
    elif page == "Dashboard":
        show_dashboard_page()


def show_home_page():
    """Home page with instructions"""
    st.markdown('<div class="section-header">Welcome to QA Agent</div>', unsafe_allow_html=True)
    
    st.markdown("""
    This system helps you automatically generate comprehensive test cases and Selenium scripts from your project documentation.
    
    ### How It Works
    
    1. **Upload Documents** - Upload your product specifications, UI/UX guidelines, API documentation, and HTML files
    2. **Build Knowledge Base** - Process documents and create a searchable knowledge base
    3. **Generate Test Cases** - AI generates structured test cases based on your documentation
    4. **Generate Scripts** - Convert test cases into executable Selenium Python scripts
    
    ### Getting Started
    
    Follow these steps:
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        #### Step 1: Upload
        Go to **Document Upload** page and upload your support documents:
        - Product specifications (.md)
        - UI/UX guidelines (.txt)
        - API endpoints (.json)
        - HTML files (.html)
        """)
    
    with col2:
        st.info("""
        #### Step 2: Build KB
        Click **Build Knowledge Base** to process your documents and create vector embeddings for semantic search.
        """)
    
    with col3:
        st.info("""
        #### Step 3: Generate
        Use the AI agent to generate test cases and then convert them to Selenium scripts.
        """)
    
    st.markdown("---")
    
    # Quick stats
    try:
        stats = get_kb_stats()
        col1, col2, col3 = st.columns(3)
        
        with col1:
            uploaded_files = len(stats.get("uploaded_files", []))
            st.metric("Uploaded Files", uploaded_files)
        
        with col2:
            chunks = stats.get("vector_db", {}).get("count", 0)
            st.metric("Knowledge Chunks", chunks)
        
        with col3:
            test_cases = len(st.session_state.test_cases)
            st.metric("Generated Test Cases", test_cases)
    except:
        pass


def show_document_upload_page():
    """Document upload page"""
    st.markdown('<div class="section-header">Document Upload & Knowledge Base</div>', unsafe_allow_html=True)
    
    # Upload section
    st.subheader("1. Upload Support Documents")
    
    uploaded_files = st.file_uploader(
        "Upload your documentation files",
        type=['txt', 'md', 'json', 'pdf', 'html', 'htm'],
        accept_multiple_files=True,
        help="Upload product specifications, UI/UX guidelines, API docs, and HTML files"
    )
    
    if uploaded_files:
        st.write(f"Selected {len(uploaded_files)} file(s):")
        for file in uploaded_files:
            st.write(f"- {file.name} ({file.size} bytes)")
        
        if st.button("Upload Documents", type="primary"):
            with st.spinner("Uploading documents..."):
                try:
                    result = upload_documents(uploaded_files)
                    st.success(f"{result['message']}")
                    st.session_state.uploaded_files = result['details']['files']
                except Exception as e:
                    st.error(f"Error uploading documents: {str(e)}")
    
    st.markdown("---")
    
    # Build KB section
    st.subheader("2. Build Knowledge Base")
    
    st.info("""
    Building the knowledge base will:
    - Process all uploaded documents
    - Extract and chunk text content
    - Generate vector embeddings
    - Store in searchable database
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Build Knowledge Base", type="primary", use_container_width=True):
            with st.spinner("Building knowledge base... This may take a minute."):
                try:
                    result = build_knowledge_base(reset=False)
                    st.success(f"{result['message']}")
                    st.json(result['details'])
                    st.session_state.kb_built = True
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error building knowledge base: {str(e)}")
    
    with col2:
        if st.button("Rebuild (Reset)", use_container_width=True):
            with st.spinner("Rebuilding knowledge base..."):
                try:
                    result = build_knowledge_base(reset=True)
                    st.success(f"{result['message']}")
                    st.session_state.kb_built = True
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error rebuilding knowledge base: {str(e)}")
    
    st.markdown("---")
    
    # Current status
    st.subheader("3. Knowledge Base Status")
    
    try:
        stats = get_kb_stats()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Uploaded Files", len(stats.get("uploaded_files", [])))
            if stats.get("uploaded_files"):
                with st.expander("View uploaded files"):
                    for file in stats["uploaded_files"]:
                        st.write(f"- {file}")
        
        with col2:
            kb_info = stats.get("vector_db", {})
            chunks = kb_info.get("count", 0)
            st.metric("Knowledge Chunks", chunks)
            
            if kb_info.get("exists"):
                st.success("Knowledge base is ready")
            else:
                st.warning("Knowledge base not built")
    
    except Exception as e:
        st.error(f"Error loading stats: {str(e)}")


def show_test_case_generation_page():
    """Test case generation page"""
    st.markdown('<div class="section-header">Test Case Generation</div>', unsafe_allow_html=True)
    
    # Check if KB is built
    if not st.session_state.kb_built:
        st.warning("Please build the knowledge base first by uploading documents.")
        if st.button("Go to Document Upload"):
            st.rerun()
        return
    
    # Test suggestions
    st.subheader("Suggested Test Scenarios")
    
    try:
        suggestions_response = get_test_suggestions()
        suggestions = suggestions_response.get("suggestions", [])
        
        selected_suggestion = st.selectbox(
            "Choose a pre-defined scenario or write your own below:",
            ["Custom Query"] + suggestions
        )
    except:
        selected_suggestion = "Custom Query"
    
    # Query input
    st.subheader("Generate Test Cases")
    
    if selected_suggestion != "Custom Query":
        query = st.text_area(
            "Test Case Query",
            value=selected_suggestion,
            height=100,
            help="Describe what test cases you want to generate"
        )
    else:
        query = st.text_area(
            "Test Case Query",
            placeholder="Example: Generate all positive and negative test cases for the discount code feature",
            height=100,
            help="Describe what test cases you want to generate"
        )
    
    top_k = st.slider("Number of context chunks to retrieve", 3, 10, 5)
    
    if st.button("Generate Test Cases", type="primary"):
        if not query:
            st.error("Please enter a query")
        else:
            with st.spinner("Generating test cases... This may take 30-60 seconds."):
                try:
                    result = generate_test_cases(query, top_k)
                    st.session_state.test_cases = result.get("test_cases", [])
                    
                    if st.session_state.test_cases:
                        st.success(f"Generated {len(st.session_state.test_cases)} test case(s)")
                    else:
                        st.warning("No test cases were generated. Try modifying your query.")
                
                except Exception as e:
                    st.error(f"Error generating test cases: {str(e)}")
    
    # Display test cases
    if st.session_state.test_cases:
        st.markdown("---")
        st.subheader("Generated Test Cases")
        
        for i, tc in enumerate(st.session_state.test_cases):
            with st.expander(f"**{tc.get('test_id', f'TC-{i+1}')}**: {tc.get('feature', 'N/A')} - {tc.get('test_scenario', 'N/A')[:80]}..."):
                st.markdown(f"""
                **Feature:** {tc.get('feature', 'N/A')}
                
                **Test Scenario:** {tc.get('test_scenario', 'N/A')}
                
                **Test Type:** {tc.get('test_type', 'N/A')}
                
                **Priority:** {tc.get('priority', 'N/A')}
                
                **Preconditions:** {tc.get('preconditions', 'N/A')}
                
                **Test Steps:**
                """)
                
                steps = tc.get('test_steps', [])
                if isinstance(steps, list):
                    for j, step in enumerate(steps, 1):
                        st.write(f"{j}. {step}")
                else:
                    st.write(steps)
                
                st.markdown(f"""
                **Expected Result:** {tc.get('expected_result', 'N/A')}
                
                **Grounded In:** {tc.get('grounded_in', 'N/A')}
                """)
                
                if st.button(f"Generate Selenium Script", key=f"gen_script_{i}"):
                    st.session_state.selected_test_case = tc
                    st.info("Go to **Script Generation** page to generate the Selenium script")
        
        # Export options
        st.markdown("---")
        st.subheader("Export Test Cases")
        
        col1, col2 = st.columns(2)
        
        with col1:
            json_data = json.dumps(st.session_state.test_cases, indent=2)
            st.download_button(
                label="Download as JSON",
                data=json_data,
                file_name="test_cases.json",
                mime="application/json"
            )
        
        with col2:
            # Create markdown format
            md_content = "# Generated Test Cases\n\n"
            for tc in st.session_state.test_cases:
                md_content += f"## {tc.get('test_id', 'N/A')}: {tc.get('feature', 'N/A')}\n\n"
                md_content += f"**Scenario:** {tc.get('test_scenario', 'N/A')}\n\n"
                md_content += f"**Type:** {tc.get('test_type', 'N/A')}\n\n"
                md_content += f"**Expected Result:** {tc.get('expected_result', 'N/A')}\n\n"
                md_content += f"**Source:** {tc.get('grounded_in', 'N/A')}\n\n"
                md_content += "---\n\n"
            
            st.download_button(
                label="Download as Markdown",
                data=md_content,
                file_name="test_cases.md",
                mime="text/markdown"
            )


def show_script_generation_page():
    """Script generation page"""
    st.markdown('<div class="section-header">Selenium Script Generation</div>', unsafe_allow_html=True)
    
    # Check if KB is built
    if not st.session_state.kb_built:
        st.warning("Please build the knowledge base first.")
        return
    
    # HTML upload
    st.subheader("1. Upload HTML File (Optional)")
    st.info("Upload the HTML file to improve script accuracy. If not provided, the system will search the knowledge base.")
    
    html_file = st.file_uploader("Upload checkout.html", type=['html', 'htm'])
    
    if html_file:
        st.session_state.html_content = html_file.getvalue().decode('utf-8')
        st.success(f"HTML file loaded: {html_file.name}")
    
    st.markdown("---")
    
    # Test case selection
    st.subheader("2. Select Test Case")
    
    if not st.session_state.test_cases:
        st.warning("No test cases available. Please generate test cases first.")
        if st.button("Go to Test Case Generation"):
            st.rerun()
        return
    
    # Create dropdown options
    test_case_options = [
        f"{tc.get('test_id', f'TC-{i+1}')}: {tc.get('feature', 'N/A')} - {tc.get('test_scenario', 'N/A')[:50]}"
        for i, tc in enumerate(st.session_state.test_cases)
    ]
    
    selected_index = st.selectbox(
        "Choose a test case:",
        range(len(test_case_options)),
        format_func=lambda x: test_case_options[x]
    )
    
    selected_tc = st.session_state.test_cases[selected_index]
    
    # Display selected test case
    with st.expander("View Selected Test Case Details", expanded=True):
        st.json(selected_tc)
    
    st.markdown("---")
    
    # Generate script
    st.subheader("3. Generate Selenium Script")
    
    if st.button("Generate Selenium Script", type="primary"):
        with st.spinner("Generating Selenium script... This may take 30-60 seconds."):
            try:
                result = generate_selenium_script(
                    test_case=selected_tc,
                    html_content=st.session_state.html_content
                )
                
                st.session_state.generated_script = result.get("script", "")
                validation = result.get("validation", {})
                
                if validation.get("valid"):
                    st.success("Script generated successfully and syntax is valid!")
                else:
                    st.warning(f"Script generated but has syntax issues: {validation.get('error')}")
            
            except Exception as e:
                st.error(f"Error generating script: {str(e)}")
    
    # Display script
    if st.session_state.generated_script:
        st.markdown("---")
        st.subheader("Generated Selenium Script")
        
        st.code(st.session_state.generated_script, language="python")
        
        # Download button
        st.download_button(
            label="Download Script",
            data=st.session_state.generated_script,
            file_name=f"test_{selected_tc.get('test_id', 'script')}.py",
            mime="text/x-python"
        )
        
        # Instructions
        with st.expander("How to Run This Script"):
            st.markdown("""
            ### Prerequisites
            ```bash
            pip install selenium webdriver-manager
            ```
            
            ### Running the Script
            1. Save the script to a `.py` file
            2. Make sure `checkout.html` is in the correct location
            3. Run the script:
            ```bash
            python test_script.py
            ```
            
            ### Notes
            - The script uses Chrome WebDriver (automatically managed)
            - Make sure you have Chrome browser installed
            - The HTML file path may need to be adjusted
            """)


def show_dashboard_page():
    """Dashboard page with overall statistics"""
    st.markdown('<div class="section-header">Dashboard</div>', unsafe_allow_html=True)
    
    try:
        stats = get_kb_stats()
        
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Uploaded Files", len(stats.get("uploaded_files", [])))
        
        with col2:
            kb_chunks = stats.get("vector_db", {}).get("count", 0)
            st.metric("Knowledge Chunks", kb_chunks)
        
        with col3:
            st.metric("Test Cases Generated", len(st.session_state.test_cases))
        
        with col4:
            scripts_generated = 1 if st.session_state.generated_script else 0
            st.metric("Scripts Generated", scripts_generated)
        
        st.markdown("---")
        
        # Files list
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Uploaded Documents")
            if stats.get("uploaded_files"):
                for file in stats["uploaded_files"]:
                    st.write(f"- {file}")
            else:
                st.info("No documents uploaded yet")
        
        with col2:
            st.subheader("Test Case Summary")
            if st.session_state.test_cases:
                types = {}
                priorities = {}
                
                for tc in st.session_state.test_cases:
                    tc_type = tc.get("test_type", "unknown")
                    types[tc_type] = types.get(tc_type, 0) + 1
                    
                    priority = tc.get("priority", "unknown")
                    priorities[priority] = priorities.get(priority, 0) + 1
                
                st.write("By Type:")
                for t, count in types.items():
                    st.write(f"- {t}: {count}")
                
                st.write("By Priority:")
                for p, count in priorities.items():
                    st.write(f"- {p}: {count}")
            else:
                st.info("No test cases generated yet")
        
        st.markdown("---")
        
        # System info
        st.subheader("System Information")
        health = requests.get(f"{API_BASE_URL}/health").json()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Backend Status:**", "Healthy" if health.get("status") == "healthy" else "Unhealthy")
            st.write("**LLM Provider:**", health.get("llm_provider", "N/A"))
        
        with col2:
            st.write("**Vector DB:**", "Connected" if health.get("vector_db", {}).get("connected") else "Disconnected")
            st.write("**API URL:**", API_BASE_URL)
    
    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")


# Run the app
if __name__ == "__main__":
    main()
