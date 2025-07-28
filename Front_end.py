import streamlit as st
import requests
import uuid

BACKEND_URL = "http://127.0.0.1:8000/api/chat"

if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}
if "current_chat_id" not in st.session_state:
    new_chat_id = str(uuid.uuid4())
    st.session_state.all_chats[new_chat_id] = []
    st.session_state.current_chat_id = new_chat_id

st.sidebar.title("Chat Histories")

if st.sidebar.button("➕ New Chat"):
    new_chat_id = str(uuid.uuid4())
    st.session_state.all_chats[new_chat_id] = []
    st.session_state.current_chat_id = new_chat_id
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("Select Chat")
for chat_id in st.session_state.all_chats.keys():
    chat_name = f"Chat {chat_id[:8]}..."
    if st.session_state.all_chats[chat_id]:
        first_message_content = st.session_state.all_chats[chat_id][0].get("content", "")
        if first_message_content:
            chat_name = first_message_content.split(' ')[0:3]
            chat_name = " ".join(chat_name) + "..." if len(first_message_content.split(' ')) > 3 else first_message_content
            if len(chat_name) > 25:
                chat_name = chat_name[:22] + "..."
        else:
            chat_name = f"Chat {chat_id[:8]} (Empty)"

    if st.sidebar.button(chat_name, key=f"select_{chat_id}"):
        st.session_state.current_chat_id = chat_id
        st.rerun()

current_messages = st.session_state.all_chats[st.session_state.current_chat_id]

st.title("Abdulrahman Hamada Chat")

for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your message..."):
    current_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking..."):
        payload = {
            "messages": current_messages,
            "user_id": "current_user"
        }
        
        response = requests.post(BACKEND_URL, json=payload)
        if response.status_code == 200:
            ai_response = response.json().get("answer", "No response from LLM.")
        else:
            ai_response = f"Error from backend: {response.status_code} - {response.text}"
        
        current_messages.append({"role": "assistant", "content": ai_response})
        with st.chat_message("assistant"):
            st.markdown(ai_response)

    st.session_state.all_chats[st.session_state.current_chat_id] = current_messages
    st.rerun()