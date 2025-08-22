import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

st.set_page_config(page_title="AI Dataset Creator", page_icon="🤖", layout="wide")

# Header
st.title("🤖 AI Dataset Creator")
st.write("Paste your messy data, I will clean, structure, and let you edit before downloading.")

# Input messy data
raw_text = st.text_area("📥 Paste your messy data here:")

data = None
if raw_text:
    try:
        rows = [list(filter(None, r.strip().split())) for r in raw_text.replace(",", " ").split(";")]
        max_len = max(len(r) for r in rows)
        columns = [f"Column {i+1}" for i in range(max_len)]
        padded_rows = [r + [""]*(max_len - len(r)) for r in rows]
        data = pd.DataFrame(padded_rows, columns=columns)
    except Exception as e:
        st.error(f"Error parsing text: {e}")

# Editable table
if data is not None:
    st.subheader("✅ Preview & Edit Your Dataset")
    edited_data = st.experimental_data_editor(data, num_rows="dynamic")

    # Export options
    st.subheader("💾 Choose Export Options")
    export_format = st.selectbox("Which file do you want to create?", ["csv", "json", "excel", "pdf"])
    filename = st.text_input("File name (without extension):", "my_dataset")

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
                ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
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
