import streamlit as st
from agents import MasterAgent




st.title("Multi-Agent ChatBot")
weather_api_key=st.sidebar.text_input("Weather API Key", type="password")
huggingface_api_key=st.sidebar.text_input("HuggingFace API Key", type="password")
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Let's start chatting! 👇"}]
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
if prompt := st.chat_input("Ask me question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    master_agent = MasterAgent(weather_api_key=weather_api_key, huggingface_api_key=huggingface_api_key)
    response = master_agent.perform_task(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
st.button("Clear Chat", on_click=lambda: st.session_state.messages.clear())