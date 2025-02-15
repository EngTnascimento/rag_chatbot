# chatbot_app.py
import streamlit as st
from services import ChatService

class StreamlitChat:
    def __init__(self, chat_service: ChatService):
        self.chat_service = chat_service

    def run(self):
        st.title("Chatbot with Streamlit + FastAPI")

        # Initialize chat history in Session State
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []

        # User text input
        user_input = st.text_input("You:", key="user_input")

        # Send button
        if st.button("Send"):
            if user_input.strip() != "":
                # Append user message to chat history
                st.session_state["chat_history"].append(("user", user_input))

                # Use ChatService to send message and get response
                bot_response = self.chat_service.send_message(user_input)
                st.session_state["chat_history"].append(("bot", bot_response))

                # Clear the user input field
                st.session_state["user_input"] = ""

        # Display the chat history
        st.markdown("---")
        for sender, msg in st.session_state["chat_history"]:
            if sender == "user":
                st.markdown(f"**You:** {msg}")
            else:
                st.markdown(f"**Bot:** {msg}")

