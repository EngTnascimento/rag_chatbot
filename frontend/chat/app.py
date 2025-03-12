import streamlit as st
import time
import uuid
from chat.services.chat_service import ChatService


class ChatApp:
    def __init__(self):
        self.chat_service = ChatService()

    def initialize_session(self):
        """Initialize session state variables"""
        if "client_ids" not in st.session_state:
            st.session_state.client_ids = {}

        if "chat_histories" not in st.session_state:
            st.session_state.chat_histories = {}

        if "last_heartbeats" not in st.session_state:
            st.session_state.last_heartbeats = {}

        if "active_chat" not in st.session_state:
            st.session_state.active_chat = "default"

        # Ensure the active chat has a client ID and history
        if st.session_state.active_chat not in st.session_state.client_ids:
            st.session_state.client_ids[st.session_state.active_chat] = str(
                uuid.uuid4()
            )

        if st.session_state.active_chat not in st.session_state.chat_histories:
            st.session_state.chat_histories[st.session_state.active_chat] = []

        if st.session_state.active_chat not in st.session_state.last_heartbeats:
            st.session_state.last_heartbeats[st.session_state.active_chat] = time.time()

    def run(self):
        # Page configuration
        st.set_page_config(page_title="ChatBot", page_icon="💬", layout="wide")

        # Initialize session variables
        self.initialize_session()

        # Header with subtle styling
        st.header("Hortifruti Chat")

        # Chat selection sidebar
        with st.sidebar:
            st.subheader("Chat Sessions")

            # Create a new chat
            new_chat_name = st.text_input("Create new chat:")
            if st.button("Create") and new_chat_name:
                if new_chat_name not in st.session_state.client_ids:
                    st.session_state.client_ids[new_chat_name] = str(uuid.uuid4())
                    st.session_state.chat_histories[new_chat_name] = []
                    st.session_state.last_heartbeats[new_chat_name] = time.time()
                st.session_state.active_chat = new_chat_name
                st.rerun()

            # List existing chats
            chat_options = list(st.session_state.client_ids.keys())
            if chat_options:
                selected_chat = st.selectbox(
                    "Select chat:",
                    chat_options,
                    index=chat_options.index(st.session_state.active_chat),
                )

                if selected_chat != st.session_state.active_chat:
                    st.session_state.active_chat = selected_chat
                    st.rerun()

                # Delete chat button
                if st.button("Delete this chat"):
                    chat_id = st.session_state.active_chat
                    self.chat_service.close(chat_id)

                    # Remove from session state
                    del st.session_state.client_ids[chat_id]
                    del st.session_state.chat_histories[chat_id]
                    del st.session_state.last_heartbeats[chat_id]

                    # Set active chat to first available or default
                    if st.session_state.client_ids:
                        st.session_state.active_chat = next(
                            iter(st.session_state.client_ids)
                        )
                    else:
                        st.session_state.active_chat = "default"
                        st.session_state.client_ids["default"] = str(uuid.uuid4())
                        st.session_state.chat_histories["default"] = []
                        st.session_state.last_heartbeats["default"] = time.time()

                    st.rerun()

        # Main chat area
        st.subheader(f"Chat: {st.session_state.active_chat}")
        st.markdown("---")

        active_chat = st.session_state.active_chat
        client_id = st.session_state.client_ids[active_chat]

        # Display chat messages for active chat
        chat_history = st.session_state.chat_histories[active_chat]
        for message in chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Chat input
        if prompt := st.chat_input("Type your message here..."):
            # Add user message to chat history
            st.session_state.chat_histories[active_chat].append(
                {"role": "user", "content": prompt}
            )

            # Display user message
            with st.chat_message("user"):
                st.write(prompt)

            # Get bot response using client_id for persistent connection
            print(f"Sending message to {client_id}")
            with st.chat_message("assistant"):
                with st.spinner(""):
                    bot_response = self.chat_service.send_message(
                        prompt, client_id=client_id
                    )
                print(f"Bot response: {bot_response}")
                st.write(bot_response)

            # Add bot response to chat history
            st.session_state.chat_histories[active_chat].append(
                {"role": "assistant", "content": bot_response}
            )

    def close(self):
        """Close all WebSocket connections on app shutdown"""
        for chat_id, client_id in st.session_state.client_ids.items():
            self.chat_service.close(chat_id)
