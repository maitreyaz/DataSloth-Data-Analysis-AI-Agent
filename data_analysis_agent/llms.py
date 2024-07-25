import streamlit as st

#------------------OPENAI------------
from langchain_openai import ChatOpenAI
import os

# OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
OPENAI_API_KEY = st.secrets['OPENAI_API_KEY'] # Setup your API Key
chatopenai_llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY, temperature=0.0)


# -------------------GROQ--------------
from langchain_groq import ChatGroq

# Initialize the LLM
# groq_api_key = os.environ['GROQ_API_KEY'] # Setup your API Key
groq_api_key = st.secrets['GROQ_API_KEY'] # Setup your API Key
# groq_llm = ChatGroq(groq_api_key=groq_api_key, model_name='mixtral-8x7b-32768', temperature=0.0)
groq_llm = ChatGroq(groq_api_key=groq_api_key, model_name='llama3-8b-8192', temperature=0.0)
