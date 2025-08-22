import streamlit as st
import pandas as pd

# --- Page config ---
st.set_page_config(page_title="DataForge Studio", page_icon="🧠", layout="centered")

# --- Custom CSS ---
st.markdown("""
    <style>
    .chat-bubble {
        padding: 10px 15px;
        border-radius: 15px;
        margin: 8px 0;
        max-width: 80%;
        font-family: 'Open Sans', sans-serif;
        font-size: 15px;
        line-height: 1.4;
    }
    .bot {
        background-color: #f1f1f1;
        color: #000;
        text-align: left;
    }
    .user {
        background-color: #007BFF;
        color: #fff;
        text-align: right;
        margin-left: auto;
    }
    </style>
""", unsafe_allow_html=True)

# --- Session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "raw_data" not in st.session_state:
    st.session_state.raw_data = ""
if "df" not in st.session_state:
    st.session_state.df = None

# --- Greeting ---
if not st.session_state.messages:
    st.session_state.messages.append(("bot", "👋 Welcome to **DataForge Studio**! Paste your data or upload a file to begin."))

# --- Display chat bubbles ---
for sender, msg in st.session_state.messages:
    css_class = "bot" if sender == "bot" else "user"
    st.markdown(f"<div class='chat-bubble {css_class}'>{msg}</div>", unsafe_allow_html=True)

# --- Tabs for modular workflow ---
tab1, tab2, tab3 = st.tabs(["📥 Input", "🧠 Preview & Edit", "📤 Export"])

# --- Tab 1: Input ---
with tab1:
    st.subheader("Paste Raw Data")
    user_input = st.text_area("Paste CSV-style data (comma-separated):", height=150)
    if st.button("Submit Text"):
        if user_input:
            st.session_state.messages.append(("user", user_input))
            st.session_state.messages.append(("bot", "✅ Got your data! Preview it in the next tab."))
            st.session_state.raw_data = user_input
            st.rerun()

    st.divider()
    st.subheader("Upload File")
    uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])
    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.session_state.df = df
            st.session_state.messages.append(("bot", f"📁 Uploaded `{uploaded_file.name}` successfully!"))
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error reading file: {e}")

# --- Tab 2: Preview & Edit ---
with tab2:
    st.subheader("Parsed Data Preview")

    def parse_raw_data(raw_text):
        lines = raw_text.strip().split('\n')
        headers = [h.strip() for h in lines[0].split(',')]
        rows = [[cell.strip() for cell in line.split(',')] for line in lines[1:] if line.strip()]
        return pd.DataFrame(rows, columns=headers)

    if st.session_state.df is None and st.session_state.raw_data:
        try:
            st.session_state.df = parse_raw_data(st.session_state.raw_data)
        except Exception as e:
            st.error(f"⚠️ Failed to parse raw data: {e}")

    if st.session_state.df is not None:
        edited_df = st.experimental_data_editor(st.session_state.df, num_rows="dynamic")
        st.session_state.df = edited_df
        st.success("✅ You can now export your edited data!")

# --- Tab 3: Export ---
with tab3:
    st.subheader("Export Your Dataset")

    if st.session_state.df is not None:
        st.download_button("Download JSON", st.session_state.df.to_json(orient="records"), file_name="data.json", mime="application/json")
        st.download_button("Download CSV", st.session_state.df.to_csv(index=False), file_name="data.csv", mime="text/csv")
        st.download_button("Download Excel", st.session_state.df.to_excel("data.xlsx", index=False), file_name="data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.info("📋 No data available yet. Paste or upload your dataset in the first tab.")
