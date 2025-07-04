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


# loading json file
with open('/workspaces/mcqgenAI/response.json', 'r') as file:
    response_json = json.load(file)

# creating a title for the app
st.title("MCQ Generator App")

# Create a form using st.form
with st.form("user_inputs"):
    # file upload
    uploaded_file = st.file_uploader("Upload a pdf or text file")

    # input fields
    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=20)

    # subject
    subject = st.text_input("Insert subject", max_chars=20)

    # quiz tone
    tone = st.text_input("complexity levle of question", max_chars=20, placeholder="Simple")

    # Add button:
    button = st.form_submit_button("Generate MCQs")

    # check if the button is clicked and all fields have input
    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Generating MCQs..."):
            try:
                text = read_file(uploaded_file)
                # count tokens and the cost if API call
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
                # st.write(response)

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("error)")

            else:
                print(f"Total Tokens: {cb.total_tokens}")
                print(f"Total Cost: ${cb.total_cost:.4f}")
                print(f"completion Tokens:{cb.completion_tokens}")
                print(f"Prompt Tokens:{cb.prompt_tokens}")
                if isinstance(response, dict):
                    # Extract the quiz data from the response
                    quiz = response.get("quiz", None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if get_table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)
                            # display the review in a text box as well
                            st.text_area(label="Review", value=response["review"])
                        else:
                            st.error("No quiz data found in the response.")
                else:
                    st.write(response)
