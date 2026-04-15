import streamlit as st
import os
import pandas as pd
from scripts.processor import extract_text_from_pdf, extract_text_from_image
from scripts.rules import analyze_image_metadata, analyze_pdf_structure
from scripts.model_inference import get_detailed_ai_metrics
from scripts.aggregator import calculate_final_risk 
from scripts.database import save_result, init_db

# Initialize DB on load
init_db()

# --- THEME MATCHING SETUP ---
st.set_page_config(page_title="Analyze - ShieldAI", page_icon="🔍", layout="wide")

# Apply custom theme colors through CSS
st.markdown("""
<style>
    .main { background-color: #f0f2f6; }
    .risk-container {
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        color: white;
        text-align: center;
    }
    .level-low { background-color: #28a745; border-left: 10px solid #1e7e34; }
    .level-medium { background-color: #ffc107; color: black !important; border-left: 10px solid #d39e00; }
    .level-high { background-color: #fd7e14; border-left: 10px solid #ca6510; }
    .level-critical { background-color: #dc3545; border-left: 10px solid #bd2130; animation: pulse 1s infinite; }

    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(220, 53, 69, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(220, 53, 69, 0); }
        100% { box-shadow: 0 0 0 0 rgba(220, 53, 69, 0); }
    }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ Advanced Digital Risk Analysis")
st.write("Evaluate the security posture of an image, PDF, or message using our multi-vector engine.")

# Initialize session state for analysis results
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'last_content' not in st.session_state:
    st.session_state.last_content = ""

# Input area (Tabs)
tab1, tab2, tab3 = st.tabs(["💬 Raw Text", "📄 Secure PDF Scan", "🖼️ Forensic Image Check"])
user_content = ""
meta_flags = []
meta_score = 0

with tab1:
    user_content = st.text_area("Input text:", height=150)

with tab2:
    uploaded_pdf = st.file_uploader("Upload PDF:", type=["pdf"])
    if uploaded_pdf:
        with st.spinner("Analyzing PDF structure and content..."):
            with open("temp.pdf", "wb") as f: f.write(uploaded_pdf.getbuffer())
            user_content = extract_text_from_pdf("temp.pdf")
            
            # --- QUALITY ADDITION ---
            meta_score, meta_flags = analyze_pdf_structure("temp.pdf")

with tab3:
    uploaded_img = st.file_uploader("Upload Image:", type=["png", "jpg", "jpeg"])
    if uploaded_img:
        with st.spinner("Running forensic OCR and metadata analysis..."):
            # Save temporary file for metadata access
            with open("temp.img", "wb") as f: f.write(uploaded_img.getbuffer())
            user_content = extract_text_from_image("temp.img")
            
            # --- QUALITY ADDITION ---
            meta_score, meta_flags = analyze_image_metadata("temp.img")

# Verification Area
if user_content:
    with st.expander("👁️ View Input/Extracted Content (Verify OCR Accuracy)"):
        st.write(user_content)

# --- EXECUTION & THEME DISPLAY ---
col1, col2 = st.columns([1, 1])
with col1:
    run_analysis = st.button("🚀 Run Deep Analysis", type="primary")
with col2:
    clear_analysis = False
    if st.session_state.analysis_results:
        clear_analysis = st.button("🗑️ Clear Results")

if clear_analysis:
    st.session_state.analysis_results = None
    st.session_state.last_content = ""
    st.rerun()

# Check if we need to run analysis
should_run_analysis = (
    run_analysis and user_content.strip() and
    (st.session_state.analysis_results is None or st.session_state.last_content != user_content)
)

if should_run_analysis:
    if not user_content.strip():
        st.warning("No valid content identified for analysis.")
    else:
        with st.spinner("Processing through Hybrid AI and Heuristic engines..."):
            # 1. Base Hybrid Result (Model + Keywords)
            base_result = calculate_final_risk(user_content)
            
            # 2. Add Meta Score for Best Accuracy
            final_score = min(base_result['score'] + meta_score, 100)
            
            # Recalculate Level based on new final score
            if final_score < 30: level = "Low"
            elif final_score < 60: level = "Medium"
            elif final_score < 85: level = "High"
            else: level = "Critical"
            
            # 3. Get Detailed AI Metrics for the chart
            ai_metrics = get_detailed_ai_metrics(user_content)
            
            # 4. Save to DB
            save_result(user_content, final_score, level)
            
            # Store results in session state
            st.session_state.analysis_results = {
                'final_score': final_score,
                'level': level,
                'ai_metrics': ai_metrics,
                'base_result': base_result,
                'combined_flags': base_result['flags'] + meta_flags,
                'user_content': user_content
            }
            st.session_state.last_content = user_content

# Display results from session state if available
if st.session_state.analysis_results:
    results = st.session_state.analysis_results
    final_score = results['final_score']
    level = results['level']
    ai_metrics = results['ai_metrics']
    combined_flags = results['combined_flags']
    
    st.success(f"✅ Analysis completed for current content (cached in session)")
    st.divider()

    # --- THEME MATCHING CONTAINER ---
    level_class = f"level-{level.lower()}"
    st.markdown(f"""
        <div class="risk-container {level_class}">
            <h2>Overall Risk Assessment: {level.upper()}</h2>
            <h1 style='color: white; font-size: 60px;'>{final_score}%</h1>
        </div>
    """, unsafe_allow_html=True)

    # --- DETAILED MATRIX BELOW ---
    st.subheader("📊 Analysis Matrix Breakdown")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.write("**AI Model Metrics**")
        st.caption(f"Scam Model Probability: {ai_metrics['scam_prob']:.2f}")
        
        # Show Logits as an Area Chart (Advanced visualization)
        logit_df = pd.DataFrame({
            'Metric': ['Safe Logit', 'Scam Logit'],
            'Value': [float(ai_metrics['raw_logits'][0]), float(ai_metrics['raw_logits'][1])]
        })
        st.area_chart(logit_df.set_index('Metric'))

    with c2:
        st.write("**Heuristic Flags**")
        if not combined_flags:
            st.success("✅ No red-flag patterns or metadata anomalies detected.")
        else:
            for flag in combined_flags: st.write(f"🚩 {flag}")

    with c3:
        st.write("**System Recommendation**")
        if level in ["High", "Critical"]:
            st.error("🚨 HIGH ALERT: Do not interact with links or attachments. Block sender immediately.")
        elif level == "Medium":
            st.warning("⚠️ CAUTION: Message displays suspicious patterns. Verify sender identity via official channels.")
        else:
            st.success("✅ SAFE: No significant risk vectors identified. Proceed with normal caution.")

# CLEANUP
if os.path.exists("temp.pdf"): os.remove("temp.pdf")
if os.path.exists("temp.img"): os.remove("temp.img")