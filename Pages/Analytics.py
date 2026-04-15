import streamlit as st
import pandas as pd
import plotly.express as px
from scripts.database import get_history

st.set_page_config(page_title="Analytics - ShieldAI", page_icon="📊", layout="wide")

st.title("📊 Risk Analytics Dashboard")

# Fetch data from Database
data = get_history()

if not data:
    st.warning("No data available to analyze. Please scan some messages first!")
else:
    # Convert to DataFrame
    df = pd.DataFrame(data, columns=["Timestamp", "Content", "Score", "Level"])
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # --- ROW 1: Key Metrics ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Scans", len(df))
    col2.metric("Avg Risk Score", f"{int(df['Score'].mean())}%")
    col3.metric("Highest Risk", f"{df['Score'].max()}%")

    st.divider()

    # --- ROW 2: Charts ---
    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader("Risk Level Distribution")
        # Pie Chart
        fig_pie = px.pie(df, names='Level', 
                         color='Level',
                         color_discrete_map={'Low':'#28a745', 'Medium':'#ffc107', 'High':'#fd7e14', 'Critical':'#dc3545'},
                         hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

    with right_col:
        st.subheader("Risk Score Trends")
        # Line Chart
        fig_line = px.line(df, x='Timestamp', y='Score', 
                           title="Risk Fluctuation Over Time",
                           markers=True)
        fig_line.update_traces(line_color='#007BFF')
        st.plotly_chart(fig_line, use_container_width=True)

    # --- ROW 3: Category Breakdown ---
    st.subheader("Recent Activity Summary")
    st.dataframe(df[['Timestamp', 'Level', 'Score']].head(10), use_container_width=True)