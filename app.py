from google import genai
import streamlit as st

# Configure page
st.set_page_config(page_title="AI Compliance Assistant", layout="centered")
st.title("AI Compliance Assistant")

# Sidebar for API key configuration
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

# Input area for batch or compliance text
user_prompt = st.text_area(
    "Enter batch record details, deviations, or compliance query:", 
    height=150
)

if st.button("Analyze"):
    if not api_key:
        st.warning("Please enter your Gemini API Key in the sidebar.")
    elif not user_prompt.strip():
        st.warning("Please enter some text to analyze.")
    else:
        try:
            # Initialize the modern GenAI client
            client = genai.Client(api_key=api_key)

            system_instruction = (
                "You are an expert QA and IT compliance specialist in the pharmaceutical industry. "
                "Evaluate deviations, batch records, and compliance inquiries against GLP, GMP, "
                "GAMP 5, and 21 CFR Part 11 standards. Provide concise, structured, and actionable findings.\n\n"
            )

            with st.spinner("Analyzing compliance data..."):
                full_query = f"{system_instruction}Query:\n{user_prompt}"
                
                # Updated to gemini-3.6-flash
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=full_query,
                )

                st.subheader("Analysis Result")
                st.markdown(response.text)

        except Exception as e:
            st.error(f"Error: {e}")