from langchain.prompts import PromptTemplate
# from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI

import os

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY, temperature=0.0)
# print(llm)

#-------------------Additonal Info Summarization Chain____________________

summarization_chain_template = """

You will be provided with some dataset related information by the user.
Background : The user is a Data Analyst and has some information related to the dataset they are working on. You are a helpful summary generator. You generate summary that might help the user in performing Data Analysis.

Your task is to :
    1) Determine if the user provided info is related to a dataset and not some generic query/ statement.
        - In this case, your response should be the following token (delimited in ``) : `<USER_PROVIDED_INFO_NOT_RELATED_TO_DATASET>`.
    2) If the provided info is dataset related, return a summary of the information.
    
*Guidelines for Summary Generation*:
    1) Identify mentions of variables/ fields/ columns from the dataset if any. Make a list.
    2) Map any info/ descriptions related to these dataset columns.
    3) Generate summary by including these columns and their info (if mentioned in the info provided by user). Also, take into account any information you find useful from the point of Data Analysis.
    4) The entire summary should be generated such that it might help the Data Analyst working on the dataset.
    5) IMP : Do Not assume and make up things. Summarize the content present in the info provided by the user ONLY.
    6) If the information provided is not enough, generate the token (delimited in ``): `<INFO_NOT_SUFFICIENT>`.  
   
Begin:

*Information provided by the User:*
{additional_info_dataset}
"""

summarization_chain_prompt = PromptTemplate(
    template=summarization_chain_template,
    input_variables=['additional_info_dataset']
)

summarization_chain = LLMChain(llm=llm, prompt=summarization_chain_prompt)


#-------------------Query Enhancer Chain____________________
