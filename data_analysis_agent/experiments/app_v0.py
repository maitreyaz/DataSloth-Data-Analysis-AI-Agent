# import streamlit as st
# import pandas as pd
# from langchain_experimental.agents import create_pandas_dataframe_agent
#
# from chains import summarization_chain
# from utils import check_image_file_exists, read_image_file
#
# import os
#
# #----------------------ChatOpenAI-------------------
# from langchain_openai import ChatOpenAI
#
# # Secure retrieval of the API key from environment variables
# OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
#
# # Initializing the LLM
# llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY, temperature=0.0)
#
#
# #----------------------GROQ-------------------
# # from langchain_groq import ChatGroq
#
# # # Initialize the LLM
# # groq_api_key = os.environ['GROQ_API_KEY'] # Setup your API Key
# # llm = ChatGroq(groq_api_key=groq_api_key, model_name='mixtral-8x7b-32768', temperature=0.0)
#
# # Session Variables
#
# if 'additional_info_dataset' not in st.session_state:
#     st.session_state.additional_info_dataset = ""
#
# if 'summarized_dataset_info' not in st.session_state:
#     st.session_state.summarized_dataset_info = ""
#
# if 'img_list' not in st.session_state:
#     st.session_state.img_list = []
#
# if 'img_flag' not in st.session_state:
#     st.session_state.img_flag = 0
#
# if 'chat_history' not in st.session_state:
#     st.session_state.chat_history = []
#
#
# # 2 Columns, one with the sidebar+chat area and other with features
# main_col, right_col = st.columns([4, 1])
#
# # with right_col:
# #
# #     # st.write(st.session_state.img_list)
# #     # st.write("Archives")
# #     st.write("Features")
# #
# #     page = st.radio("Select", ["None", "View Charts", "Generate Report (Coming Soon)"])
# #
# #     if page == "View Charts":
# #         # Charts Page
# #         st.write("Generated Charts")
# #         if st.session_state.img_list:
# #             for img_path in st.session_state.img_list:
# #                 st.image(img_path)
# #                 # Download button for the image
# #                 image_data = read_image_file(img_path)
# #                 st.download_button(label="Download Image",
# #                                    data=image_data,
# #                                    file_name=os.path.basename(img_path),
# #                                    mime="image/png")
# #         else:
# #             st.write("No images to display.")
#
#
# with main_col:
#     # Display chat messages from history on app rerun
#     for message in st.session_state.chat_history:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])
#
#         # Displaying previous images
#         im = check_image_file_exists(message["content"])
#         if im not in {0, -1}:
#             with st.chat_message('assistant'):
#                 # st.markdown(st.image(im))
#                 st.image(im)
#
#                 # Download button for the image
#                 image_data = read_image_file(im)
#                 st.download_button(label="Download image",
#                                    data=image_data,
#                                    file_name=os.path.basename(im),
#                                    mime="image/png")
#
#     with st.sidebar:
#         st.title("DataGenie : Your Data Analysis Agent")
#
#         st.write("Upload your CSV File and pose your question!")
#         file = st.file_uploader("Select File", type=["csv"])
#
#     # # Display chat messages from history on app rerun
#     # for message in st.session_state.chat_history:
#     #     with st.chat_message(message["role"]):
#     #         st.markdown(message["content"])
#     #
#     #     # Displaying previous images
#     #     im = check_image_file_exists(message["content"])
#     #     if im not in {0, -1}:
#     #         with st.chat_message('assistant'):
#     #             # st.markdown(st.image(im))
#     #             st.image(im)
#     #
#     #             # Download button for the image
#     #             image_data = read_image_file(im)
#     #             st.download_button(label="Download image",
#     #                                data=image_data,
#     #                                file_name=os.path.basename(im),
#     #                                mime="image/png")
#
#
#     if file is not None:
#         df = pd.read_csv(file)
#
#         from prompts import PREFIX
#
#         # with st.sidebar:
#         #     additional_info_input = st.text_area("Additional Information About Dataset (Optional)", key='additional_info_input')
#         #
#         #     if st.button("Update Additional Information"):
#         #         whitespace = " "
#         #         st.session_state.additional_info_dataset += (whitespace + additional_info_input)
#         #         summarization_chain_res = summarization_chain.run(additional_info_input)
#         #         print("***Summarized Dataset Additional Info***\n\n")
#         #         print(summarization_chain_res)
#         #         st.session_state.summarized_dataset_info = st.session_state.summarized_dataset_info + " " + summarization_chain_res
#
#         agent_executor = create_pandas_dataframe_agent(
#             llm,
#             df,
#             agent_type="tool-calling",
#             prefix=PREFIX.format(chat_history="\n".join([f"{entry['role'].capitalize()}: {entry['content']}" for entry in st.session_state.chat_history[-6:]]), additional_info_dataset = st.session_state.summarized_dataset_info),
#             verbose=True
#         )
#
#         user_input = st.chat_input("Ask your question here...")
#
#         if user_input:
#             st.chat_message("user").markdown(user_input)
#
#             res = agent_executor.invoke(user_input)
#
#             with st.chat_message("assistant"):
#                 st.markdown(res['output'])
#                 # st.markdown(st.image(r"charts/correlation_matrix.png"))
#
#             img_file = check_image_file_exists(res['output'])
#             print("****************imgfile*****************")
#             print(img_file)
#
#             # If image path was detected in agent response and the image file exists in 'charts'
#             if img_file not in {0, -1}:
#                 with st.chat_message('assistant'):
#                     # st.markdown(st.image(img_file))
#                     st.image(img_file)
#
#                     # Download button for the image
#                     image_data = read_image_file(img_file)
#                     st.download_button(label="Download image",
#                                        data=image_data,
#                                        file_name=os.path.basename(img_file),
#                                        mime="image/png")
#                 st.session_state.img_list.append(img_file)
#
#             # if img_file==0:
#
#
#             # Update image files list
#
#             # Update chat history
#             # st.session_state.chat_history.append(f"User: {user_input}")
#             # st.session_state.chat_history.append(f"AI: {res['output']}")
#             st.session_state.chat_history.append({"role": "user", "content": user_input})
#             st.session_state.chat_history.append({"role": "assistant", "content": res['output']})
#             # st.session_state.chat_history.append({"role": "assistant", "content": r"charts/correlation_matrix.png"})
#
#             print(agent_executor)
#
#             # # Display chat messages from history on app rerun
#             # for message in st.session_state.chat_history:
#             #     with st.chat_message(message["role"]):
#             #         st.markdown(message["content"])
#             #
#             #     # Displaying previous images
#             #     im = check_image_file_exists(message["content"])
#             #     if im not in {0, -1}:
#             #         with st.chat_message('assistant'):
#             #             # st.markdown(st.image(im))
#             #             st.image(im)
#             #
#             #             # Download button for the image
#             #             image_data = read_image_file(im)
#             #             st.download_button(label="Download image",
#             #                                data=image_data,
#             #                                file_name=os.path.basename(im),
#             #                                mime="image/png")
#
# with right_col:
#
#     # st.write(st.session_state.img_list)
#     # st.write("Archives")
#     st.write("Features")
#
#     page = st.radio("Select", ["None", "View Charts", "Generate Report (Coming Soon)"])
#
#     if page == "View Charts":
#         # Charts Page
#         st.write("Generated Charts")
#         if st.session_state.img_list:
#             for img_path in st.session_state.img_list:
#                 st.image(img_path)
#                 # Download button for the image
#                 image_data = read_image_file(img_path)
#                 st.download_button(label="Download Image",
#                                    data=image_data,
#                                    file_name=os.path.basename(img_path),
#                                    mime="image/png")
#         else:
#             st.write("No images to display.")
#
#
#     st.write("")
#     additional_info_input = st.text_area("Additional Information About Dataset (Optional)", key='additional_info_input')
#
#     if additional_info_input:
#         if st.button("Update Info"):
#             whitespace = " "
#             st.session_state.additional_info_dataset += (whitespace + additional_info_input)
#             summarization_chain_res = summarization_chain.run(additional_info_input)
#             print("***Summarized Dataset Additional Info***\n\n")
#             print(summarization_chain_res)
#             st.session_state.summarized_dataset_info = st.session_state.summarized_dataset_info + " " + summarization_chain_res



#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++