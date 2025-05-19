import streamlit as st
from transformers import pipeline
import language_tool_python

# Initialize grammar tool
tool = language_tool_python.LanguageTool('en-US')

# Page configuration
st.set_page_config(page_title="Cover Letter Generator", layout="centered")

st.title("📄 AI Cover Letter Generator")

# User inputs
your_name = st.text_input("Your Name")
job_title = st.text_input("Job Title")
company_name = st.text_input("Company Name")
skills = st.text_area("Your Skills (comma-separated)", placeholder="Python, SQL, Data Analysis...")
experience = st.text_area("Your Experience", placeholder="Describe your past work or projects...")

# Generate button
if st.button("Generate Cover Letter"):
    if not all([your_name, job_title, company_name, skills, experience]):
        st.warning("Please fill in all fields.")
    else:
        with st.spinner("Generating..."):

            # Load model once
            if 'generator' not in st.session_state:
                st.session_state.generator = pipeline("text-generation", model="gpt2")

            # Build prompt
            prompt = f"""
Write a professional and concise cover letter for a job application.
Job Title: {job_title}
Company: {company_name}
Name: {your_name}
Skills: {skills}
Experience: {experience}
Make it formal and well-structured.
"""

            # Helper functions
            def clean_text(text, prompt):
                return text[len(prompt):].strip().replace('\n\n', '\n')

            def correct_grammar(text):
                matches = tool.check(text)
                return language_tool_python.utils.correct(text, matches)

            def is_valid(text):
                return len(text.split()) > 80 and "job-shopping" not in text.lower()

            # Generate multiple results
            results = st.session_state.generator(prompt, max_length=400, num_return_sequences=3)

            # Process outputs
            filtered_outputs = []
            for r in results:
                raw = clean_text(r['generated_text'], prompt)
                if is_valid(raw):
                    corrected = correct_grammar(raw)
                    filtered_outputs.append(corrected)

            # Display results
            if not filtered_outputs:
                st.error("No good quality outputs. Please try again.")
            else:
                st.success("Here are your generated cover letter options:")
                for i, output in enumerate(filtered_outputs):
                    st.text_area(f"✉️ Option {i+1}", output, height=300, key=f"option_{i}")


