import streamlit as st
import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent

from chains import summarization_chain
from utils import check_image_file_exists, read_image_file

import os

# from fastapi import FastAPI
# from langserve import add_routes
#
# fastapiapp = FastAPI(
#     title="Data Analysis Agent Monitoring - LangServe",
#     version="1.0",
#     description="Let's monitor the pandas agent running in the streamlit app..."
# )


# #----------------------ChatOpenAI-------------------
# from langchain_openai import ChatOpenAI

# OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# # Initializing the LLM
# llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY, temperature=0.0)

# #----------------------GROQ-------------------
from llms import groq_llm
llm = groq_llm

st.set_page_config(
    page_title="DataGenie",
    page_icon="🧞",
)

# Session Variables
if 'additional_info_dataset' not in st.session_state:
    st.session_state.additional_info_dataset = ""

if 'summarized_dataset_info' not in st.session_state:
    st.session_state.summarized_dataset_info = ""

if 'img_list' not in st.session_state:
    st.session_state.img_list = []

if 'img_flag' not in st.session_state:
    st.session_state.img_flag = 0

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# 2 Columns, one with the sidebar+chat area and other with features
main_col, right_col = st.columns([4, 1])

with main_col:

    st.title("Chat Area")

    with st.sidebar:
        st.title("DataGenie : Your Data Analysis Agent🧞")

        st.write("Upload your CSV File and pose your questions!")
        file = st.file_uploader("Select File", type=["csv"])
        st.divider()


    # Display chat messages from history on app rerun
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

        # Displaying previous images
        im = check_image_file_exists(message["content"])
        if im not in {0, -1}:
            with st.chat_message('assistant'):
                st.image(im)

                # Generate a unique key for each download button
                download_button_key = f"download_button_{message['content']}"

                # Download button for the image
                image_data = read_image_file(im)
                st.download_button(label="Download image",
                                   data=image_data,
                                   file_name=os.path.basename(im),
                                   mime="image/png")

    # If the user uploads a CSV file
    if file is not None:

        # Read the CSV file in a pandas dataframe 'df'
        df = pd.read_csv(file)

        from prompts import PREFIX

        # Initialize the agent executor with the pandas agent
        agent_executor = create_pandas_dataframe_agent(
            llm,
            df,
            agent_type="tool-calling",
            prefix=PREFIX.format(chat_history="\n".join([f"{entry['role'].capitalize()}: {entry['content']}" for entry in st.session_state.chat_history[-6:]]), additional_info_dataset=st.session_state.summarized_dataset_info),
            verbose=True
        )

        # import uvicorn
        # import subprocess
        # add_routes(fastapiapp, agent_executor, path="/pandas_agent")
        # subprocess.Popen(["uvicorn", "app:fastapiapp", "--host", "localhost", "--port", "8003"])

        # Get user input
        user_input = st.chat_input("Ask your question here...")

        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            # Invoke the agent executor with the user's query
            res = agent_executor.invoke(user_input)

            st.session_state.chat_history.append({"role": "assistant", "content": res['output']})

            # The `check_image_file_exists` method takes the agent's response.
            # It returns an image file path if the agent generates and saves a chart image.
            # Returns 0 if a chart image was generated but not saved.
            # Returns -1 if no chart image was generated.
            img_file = check_image_file_exists(res['output'])
            if img_file not in {0, -1}:
                st.session_state.chat_history.append({"role": "assistant", "content": img_file})
                st.session_state.img_list.append(img_file)

            # Display chat messages after new input
            st.rerun()

with right_col:
    # st.write("Features")
    st.subheader("Features", divider="blue")

    page = st.radio("Select", ["None", "View Charts", "Add Dataset Info"])
    st.divider()

    if page == "View Charts":
        # st.write("Generated Charts")
        st.subheader('Generated Charts', divider='rainbow')
        if st.session_state.img_list:
            for img_path in st.session_state.img_list:
                st.image(img_path)
                image_data = read_image_file(img_path)
                st.download_button(label="Download",
                                   data=image_data,
                                   file_name=os.path.basename(img_path),
                                   mime="image/png")
        else:
            st.write("No images to display.")


    if page == "Add Dataset Info":
        additional_info_input = st.text_area("Additional Information About Dataset (Optional)",
                                             key='additional_info_input')

        if additional_info_input:
            if st.button("Update Info"):
                whitespace = " "
                st.session_state.additional_info_dataset += (whitespace + additional_info_input)
                summarization_chain_res = summarization_chain.run(additional_info_input)
                st.session_state.summarized_dataset_info = st.session_state.summarized_dataset_info + " " + summarization_chain_res
