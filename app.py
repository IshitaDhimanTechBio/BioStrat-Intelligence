import streamlit as st
import google.generativeai as genai
import json

# Set up the visual look of the website
st.set_page_config(page_title="BioStrat Intelligence", page_icon="🧬", layout="wide")

# Sidebar for the user to type their free AI password (API Key)
st.sidebar.title("🔐 Secure Authentication")
api_key = st.sidebar.text_input("Enter Google Gemini API Key:", type="password")
st.sidebar.markdown("Get your free key from [Google AI Studio](https://google.com)")

# Main titles on the website screen
st.title("BioStrat Intelligence 🧬")
st.subheader("Enterprise AI-Driven Regulatory Compliance Auditor")
st.markdown("Automating quality assurance workflows for life sciences and food-tech industries.")

# Open and read our rules file
with open("fssai_rules.json", "r") as f:
    rules_data = json.load(f)

# Create a text area box with some sample data already typed in it
default_text = """Batch ID: LPU-BIO-2026-X9
Product: Probiotic Curd
Laboratory Results:
- Total Plate Count: 38,000 CFU/g
- E. coli: Detected (4 CFU/g)
- Salmonella: Not Detected"""

lab_report_input = st.text_area("Paste raw microbial lab logs or text reports here:", value=default_text, height=250)
run_audit_button = st.button("🚀 Run Compliance Audit")

# What happens when the user clicks the button
if run_audit_button:
    if not api_key:
        st.error("⚠️ Please enter your Gemini API Key in the sidebar first!")
    else:
        with st.spinner("AI is analyzing parameters against legal standards..."):
            try:
                # Turn on the Google AI engine using the user's key
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Instructions telling the AI how to behave
                prompt = f"Act as an expert food safety auditor. Check this data: {lab_report_input} against these rules: {json.dumps(rules_data)}. Give a clear status (PASSED/FAILED) and explain why."
                
                # Get response from AI and show it on the website
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.success("✅ Audit Completed Successfully.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
