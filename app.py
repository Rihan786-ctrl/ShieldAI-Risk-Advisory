import streamlit as st

st.set_page_config(
    page_title="ShieldAI | Digital Risk Advisor",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS for a modern look
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ ShieldAI Digital Risk Advisor")
st.markdown("### Your personal AI assistant against phishing, scams, and fraud.")

st.divider()

# Top Row Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Global Scam Detection Rate", value="98.2%", delta="0.4%")
with col2:
    st.metric(label="System Status", value="Protected", delta_color="normal")
with col3:
    st.metric(label="Model Version", value="DistilBERT 2.0")

st.info("💡 **Quick Tip:** Use the sidebar to navigate to the **Analyze** page and check a suspicious message.")

# A simple "How it works" section
st.subheader("How ShieldAI Protects You")
c1, c2, c3 = st.columns(3)
with c1:
    st.write("🔍 **Scan**")
    st.caption("Paste text, upload PDFs, or snap a photo of a message.")
with c2:
    st.write("🧠 **Analyze**")
    st.caption("Our hybrid AI & Rule-based engine checks for fraud patterns.")
with c3:
    st.write("✅ **Act**")
    st.caption("Receive a risk score and clear steps to stay safe.")