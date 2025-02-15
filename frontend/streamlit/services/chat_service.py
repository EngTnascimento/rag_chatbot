import requests
import streamlit as st

class ChatService:
    def __init__(self):
        pass

    def send_message(self, message: str) -> str:
        try:
            response = requests.post(
                "http://localhost:8000/chat",
                json={"text": message},
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                return data["response"]
            else:
                return f"Error: {response.status_code}"
        except requests.exceptions.RequestException as e:
            return f"Connection Error: {str(e)}"

    def get_chat_history(self):
        return st.session_state.get("chat_history", [])
