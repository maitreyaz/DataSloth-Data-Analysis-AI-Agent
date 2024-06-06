# DataSloth : Data Analysis AI Agent

DataSloth is a personal Data Analysis AI Agent capable of processing and analyzing CSV files uploaded by the user, and generating insights and visualizations.

This is an interactive Streamlit App with an Autonomous AI Agent at the backend that :
  - Answer your queries.
  - Generate Matplotlib Charts and tables.

### App Features
  - Upload your CSV File in the file uploader located on the sidebar of the Streamlit app.
  - Once you upload the file, the Chat Area gets activated.
  - You can then post your dataset related queries, to which the agent will respond.
  - You can also view and download all the generated charts.
  - If you have dataset related info, you can also post that info to give the agent more context.

### How to Setup App Locally
  - Clone this repo.
  - Open this project in your favourite IDE.
  - In the terminal, make sure you have poetry installed by running `poetry --version`. Run `pip install poetry` if you don't have poetry installed.
  - Now, in the ``app.py`` file, select the LLM you want to pass to the model (Comment/ Uncomment the desired code blocks at the beginning of the file).
  - Set you API Key for the chosen LLM by running `$env:OPENAI_API_KEY="Your API Key Here"` or `$env:GROQ_API_KEY="<Your API Key Here>"`.
  - Now, run the following poetry commands :
    - `poetry env use "<Path to python.exe in your system>"`
    - `poetry install`
    - `poetry shell`
    - `poetry env list`
  - Finally, run the Streamlit app : `streamlit run app.py` 
