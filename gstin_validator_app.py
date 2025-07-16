import streamlit as st
import pandas as pd
import re
import io
import matplotlib.pyplot as plt
from pathlib import Path

# 🔍 GSTIN format validator
def is_valid_gstin(gstin):
    pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
    return re.match(pattern, gstin) is not None

# 🚀 Page setup
st.set_page_config(page_title="GSTIN Validator – Vijay Khemka", page_icon="🧾")

# 🟦 Styled header
st.markdown("""
    <h1 style='text-align: center; color: #0077cc;'>GSTIN Format Validator</h1>
    <h4 style='text-align: center;'>Simplifying GST validations for smarter compliance</h4>
    <p style='text-align: center; font-size:13px;'>Developed by <strong>Vijay Khemka</strong></p>
    <br>
""", unsafe_allow_html=True)

# 🔹 Manual input section
st.subheader("🔹 Validate Single GSTIN")
gstin_input = st.text_input("Enter GSTIN:")
if gstin_input:
    cleaned_gstin = gstin_input.strip().upper()
    if is_valid_gstin(cleaned_gstin):
        st.success("✅ Valid GSTIN format")
    else:
        st.error("❌ Invalid GSTIN format")

# 📂 File upload section
st.subheader("🔸 Validate GSTINs from File (.xlsx or .csv)")
uploaded_file = st.file_uploader("Upload an Excel or CSV file with a GSTIN column", type=["xlsx", "csv"])
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)

        # Auto-detect GSTIN column
        gstin_col = next((col for col in df.columns if "gst" in col.lower()), None)

        if not gstin_col:
            st.warning("GSTIN column not found. Please make sure one column contains GSTINs.")
        else:
            df[gstin_col] = df[gstin_col].astype(str).str.strip().str.upper()
            df['Validation Result'] = df[gstin_col].apply(
                lambda x: "✅ Valid" if is_valid_gstin(x) else "❌ Invalid"
            )

            # 📊 Pie chart summary
            valid_count = (df['Validation Result'] == "✅ Valid").sum()
            invalid_count = (df['Validation Result'] == "❌ Invalid").sum()
            fig, ax = plt.subplots()
            ax.pie([valid_count, invalid_count], labels=["Valid", "Invalid"],
                   colors=["#4caf50", "#f44336"], autopct="%1.1f%%")
            st.pyplot(fig)

            # 🔴 Red highlight for invalid entries
            def highlight_invalid(val):
                return 'background-color: #ffe6e6' if val == "❌ Invalid" else ''

            st.success("✅ GSTINs validated successfully!")
            st.dataframe(df.style.applymap(highlight_invalid, subset=["Validation Result"]))

            # 📥 Excel download
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Results')
            output.seek(0)

            st.download_button(
                label="📥 Download Validated Results",
                data=output.getvalue(),
                file_name="gstin_validation_results.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    except Exception as e:
        st.error(f"❌ Error processing file: {e}")

# 🧾 Footer
st.markdown("---")
st.markdown(f"""
    <div style='text-align:center; font-size:13px;'>
    © 2025 Vijay Khemka. All rights reserved. |
    <a href='mailto:vijaykhemka95@gmail.com'>vijaykhemka95@gmail.com</a>
    </div>
""", unsafe_allow_html=True)
