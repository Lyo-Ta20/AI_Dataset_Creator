# save as ai_dataset_creator.py
import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

# Import the parser from utils
from utils.parser import clean_messy_text

# ------------------------
# Page config & styling
# ------------------------
st.set_page_config(page_title="AI Dataset Creator", page_icon="🤖", layout="wide")
st.markdown("""
    <style>
    body {
        background-color: #ffffff;
    }
    .stButton>button {
        background-color: #1E90FF;
        color: white;
        font-weight: bold;
    }
    .stTextArea>div>textarea {
        border: 2px solid #1E90FF;
        border-radius: 5px;
    }
    .stDataFrame {
        border: 2px solid #1E90FF;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------
# Header
# ------------------------
st.title("🤖 AI Dataset Creator")
st.write("Paste your messy data, I will clean, structure, and let you edit before downloading.")

# ------------------------
# Step 1: Input messy data
# ------------------------
raw_text = st.text_area("📥 Paste your messy data here:")

data = None
if raw_text:
    # Use parser from utils
    data = clean_messy_text(raw_text)

# ------------------------
# Step 2: Editable table
# ------------------------
if data is not None and not data.empty:
    st.subheader("✅ Preview & Edit Your Dataset")
    edited_data = st.experimental_data_editor(data, num_rows="dynamic")

    # ------------------------
    # Step 3: Export options
    # ------------------------
    st.subheader("💾 Choose Export Options")
    export_format = st.selectbox("Which file do you want to create?", ["csv", "json", "excel", "pdf"])
    filename = st.text_input("File name (without extension):", "my_dataset")

    # ------------------------
    # Step 4: Download button
    # ------------------------
    if st.button("⬇️ Download File"):
        if export_format == "csv":
            st.download_button("Download CSV",
                               data=edited_data.to_csv(index=False).encode('utf-8'),
                               file_name=f"{filename}.csv",
                               mime="text/csv")
        elif export_format == "json":
            st.download_button("Download JSON",
                               data=edited_data.to_json(orient="records", indent=4),
                               file_name=f"{filename}.json",
                               mime="application/json")
        elif export_format == "excel":
            output = BytesIO()
            edited_data.to_excel(output, index=False, engine="openpyxl")
            st.download_button("Download Excel",
                               data=output.getvalue(),
                               file_name=f"{filename}.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        elif export_format == "pdf":
            output = BytesIO()
            doc = SimpleDocTemplate(output)
            table_data = [edited_data.columns.tolist()] + edited_data.values.tolist()
            table = Table(table_data)
            style = TableStyle([
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ])
            table.setStyle(style)
            doc.build([table])
            st.download_button("Download PDF",
                               data=output.getvalue(),
                               file_name=f"{filename}.pdf",
                               mime="application/pdf")
else:
    st.info("Paste your messy data above to start.")
