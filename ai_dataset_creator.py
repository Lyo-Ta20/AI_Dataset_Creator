import streamlit as st
import pandas as pd
import time
from io import StringIO

# --- Page config ---
st.set_page_config(page_title="AI Dataset Creator", page_icon="🤖", layout="centered")

# --- Session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_option" not in st.session_state:
    st.session_state.selected_option = None
if "df" not in st.session_state:
    st.session_state.df = None
if "styled" not in st.session_state:
    st.session_state.styled = False

# --- Greeting ---
if not st.session_state.messages:
    st.session_state.messages.append(("bot", "👋 Hello! Welcome to **AI Dataset Creator**."))
    st.session_state.messages.append(("bot", "I can help you clean, organize, and create datasets in different formats."))
    st.session_state.messages.append(("bot", "✨ What do you want to do today? Choose an option below:"))

# --- Chat bubble UI ---
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

for sender, msg in st.session_state.messages:
    css_class = "bot" if sender == "bot" else "user"
    st.markdown(f"<div class='chat-bubble {css_class}'>{msg}</div>", unsafe_allow_html=True)

# --- Options Menu ---
options = {
    "🧹 Clean Messy Data": "Paste or upload raw text and the tool cleans & structures it.",
    "📄 Create JSON File": "Input data, arrange it, and download as JSON.",
    "📊 Create CSV File": "Input data or upload messy file → get CSV.",
    "📑 Create Excel File": "Input / upload data → download Excel (.xlsx).",
    "📕 Create PDF File": "Convert structured data to a PDF table.",
    "✏️ Edit Data": "Add/Remove Rows & Columns before downloading.",
    "🎨 Style Data": "Choose fonts, colors, header styles.",
    "📂 Upload Existing File": "Upload CSV/Excel/JSON → convert to another format.",
    "🔄 Convert Between Formats": "Select input/output formats directly.",
    "📊 Visualize Data": "Preview charts or summaries before export."
}

if st.session_state.selected_option is None:
    for label, desc in options.items():
        if st.button(label):
            st.session_state.messages.append(("user", label))
            st.session_state.messages.append(("bot", f"✅ You chose: **{label}** — {desc}"))
            st.session_state.selected_option = label
            st.rerun()

# --- Data Input ---
if st.session_state.selected_option:
    st.markdown("### 📥 Paste Data or Upload File")
    raw_text = st.text_area("Paste CSV-style data:", height=150)
    uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

    if st.button("Send ➡️", key="process"):
        with st.spinner("⏳ Creating your dataset..."):
            time.sleep(2)  # Simulate processing time
            try:
                if uploaded_file:
                    if uploaded_file.name.endswith(".csv"):
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                elif raw_text:
                    cleaned_text = "\n".join([line.strip() for line in raw_text.strip().splitlines() if line.strip()])
                    df = pd.read_csv(
                        StringIO(cleaned_text),
                        skip_blank_lines=True,
                        quotechar='"',
                        on_bad_lines='skip'
                    )
                else:
                    st.warning("⚠️ Please paste data or upload a file.")
                    st.stop()

                st.session_state.df = df
                st.success("✅ Data created successfully! Scroll down to preview and style.")
            except Exception as e:
                st.error(f"❌ Failed to parse data: {e}")
                st.stop()

# --- Preview & Edit ---
if st.session_state.df is not None:
    st.markdown("### 🧠 Preview & Edit")
    edited_df = st.data_editor(st.session_state.df, num_rows="dynamic")
    st.session_state.df = edited_df

    # --- Styling Controls ---
    st.markdown("### 🎨 Style Your Data")
    header_color = st.color_picker("Header Color", "#007BFF")
    font_choice = st.selectbox("Font", ["Arial", "Courier", "Times New Roman", "Verdana"])
    font_size = st.slider("Font Size", 10, 20, 14)

    st.session_state.styled = True

    # --- Export Options ---
    st.markdown("### 📤 Download Your Dataset")
    st.download_button("Download JSON", edited_df.to_json(orient="records"), file_name="data.json", mime="application/json")
    st.download_button("Download CSV", edited_df.to_csv(index=False), file_name="data.csv", mime="text/csv")
    st.download_button("Download Excel", edited_df.to_excel("data.xlsx", index=False), file_name="data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    st.info("📕 PDF export coming soon with full styling support.")
