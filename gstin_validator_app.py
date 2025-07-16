import streamlit as st
import pandas as pd
import re
import io

# GSTIN format validator
def is_valid_gstin(gstin):
    pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
    return re.match(pattern, gstin) is not None

# App config
st.set_page_config(page_title="GSTIN Validator", page_icon="🧾")
st.title("GSTIN Format Validator 🔍")
st.markdown("Validate GSTIN format manually or in bulk with Excel upload.")

# Manual input
st.subheader("🔹 Validate Single GSTIN")
gstin_input = st.text_input("Enter GSTIN:")
if gstin_input:
    cleaned_gstin = gstin_input.strip().upper()
    if is_valid_gstin(cleaned_gstin):
        st.success("✅ Valid GSTIN format")
    else:
        st.error("❌ Invalid GSTIN format")

# Excel upload
st.subheader("🔸 Validate Multiple GSTINs from Excel")
uploaded_file = st.file_uploader("Upload Excel file with column 'GSTIN'", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        if 'GSTIN' not in df.columns:
            st.warning("Column 'GSTIN' not found in the uploaded file.")
        else:
            df['GSTIN'] = df['GSTIN'].astype(str).str.strip().str.upper()
            df['Validation Result'] = df['GSTIN'].apply(
                lambda x: "✅ Valid" if is_valid_gstin(x) else "❌ Invalid"
            )
            st.success("✅ GSTINs validated successfully!")
            st.dataframe(df)

            # ✅ Write Excel to memory using openpyxl
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Results')
            buffer.seek(0)

            # 📥 Download button
            st.download_button(
                label="📥 Download Validated Results",
                data=buffer.getvalue(),
                file_name="gstin_validation_results.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")