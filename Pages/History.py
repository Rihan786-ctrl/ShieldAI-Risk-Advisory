import streamlit as st
import pandas as pd
from scripts.database import clear_db, get_history

st.title("📜 Analysis History")

history_data = get_history()

if not history_data:
    st.write("No history found. Start analyzing messages to see them here!")
else:
    df = pd.DataFrame(history_data, columns=["Timestamp", "Content Snippet", "Score", "Level"])
    st.table(df)

   # Functional Clear Button
    if st.button("🗑️ Clear All History"):
        clear_db()
        st.success("History deleted successfully!")
        st.rerun()