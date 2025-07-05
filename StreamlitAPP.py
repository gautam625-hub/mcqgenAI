import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
import streamlit as st
from langchain_community.callbacks.manager import get_openai_callback
from src.mcqgenerator.MCQgenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

# Load .env variables
load_dotenv()

# loading JSON config file
with open('response.json', 'r') as file:
    response_json = json.load(file)

# Streamlit app title
st.title("MCQ Generator App")

# Create form
with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Upload a PDF or text file")
    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=20)
    subject = st.text_input("Insert subject", max_chars=20)
    tone = st.text_input("Complexity level of question", max_chars=20, placeholder="Simple")
    button = st.form_submit_button("Generate MCQs")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Generating MCQs..."):
            try:
                # Read uploaded file
                text = read_file(uploaded_file)

                # Count tokens and cost using OpenAI callback
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject": subject,
                            "tone": tone,
                            "response_json": json.dumps(response_json)
                        }
                    )

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("An error occurred while generating MCQs.")
            else:
                print(f"Total Tokens: {cb.total_tokens}")
                print(f"Total Cost: ${cb.total_cost:.4f}")
                print(f"Completion Tokens: {cb.completion_tokens}")
                print(f"Prompt Tokens: {cb.prompt_tokens}")

                if isinstance(response, dict):
                    quiz = response.get("quiz", None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)
                            st.text_area(label="Review", value=response.get("review", "No review provided"))
                        else:
                            st.error("No table data found in the response.")
                            st.json(response)  # For debugging
                    else:
                        st.error("No quiz data found in the response.")
                        st.json(response)  # For debugging
                else:
                    st.write(response)
