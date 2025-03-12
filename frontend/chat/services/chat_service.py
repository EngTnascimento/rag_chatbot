import streamlit as st
import websocket
import json
import threading
import time
import uuid
from urllib.parse import urljoin


class ChatService:
    def __init__(self, base_url="ws://api:8080"):
        self.base_url = base_url
        self.ws_connections = {}
        self.message_callbacks = {}
        self.responses = {}

    def _on_message(self, ws, message, client_id):
        """Handle incoming messages from the WebSocket"""
        try:
            data = json.loads(message)
            if "answer" in data:
                self.responses[client_id] = data["answer"]
            elif "error" in data:
                self.responses[client_id] = f"Error: {data['error']}"

            # Call any registered callbacks
            if client_id in self.message_callbacks:
                self.message_callbacks[client_id](data)
        except Exception as e:
            print(f"Error processing message: {str(e)}")
            self.responses[client_id] = f"Error processing response: {str(e)}"

    def _on_error(self, ws, error, client_id):
        """Handle WebSocket errors"""
        print(f"WebSocket error for client {client_id}: {error}")
        self.responses[client_id] = f"Connection error: {str(error)}"

    def _on_close(self, ws, close_status_code, close_msg, client_id):
        """Handle WebSocket connection closing"""
        print(f"WebSocket connection closed for client {client_id}")
        if client_id in self.ws_connections:
            del self.ws_connections[client_id]

    def _on_open(self, ws, client_id):
        """Handle WebSocket connection opening"""
        print(f"WebSocket connection opened for client {client_id}")

    def connect(self, client_id=None):
        print(f"Connecting {client_id}")
        """Establish a WebSocket connection"""
        if client_id is None:
            client_id = str(uuid.uuid4())

        if (
            client_id in self.ws_connections
            and self.ws_connections[client_id].sock
            and self.ws_connections[client_id].sock.connected
        ):
            return client_id  # Already connected

        # Generate WebSocket URL
        ws_url = urljoin(self.base_url, f"/ws/chat/{client_id}")

        # Create WebSocket connection
        ws = websocket.WebSocketApp(
            ws_url,
            on_open=lambda ws: self._on_open(ws, client_id),
            on_message=lambda ws, msg: self._on_message(ws, msg, client_id),
            on_error=lambda ws, err: self._on_error(ws, err, client_id),
            on_close=lambda ws, close_status_code, close_msg: self._on_close(
                ws, close_status_code, close_msg, client_id
            ),
        )

        # Start WebSocket connection in a separate thread
        thread = threading.Thread(target=ws.run_forever)
        thread.daemon = True
        thread.start()

        # Store the connection
        self.ws_connections[client_id] = ws
        self.responses[client_id] = None

        # Give the connection time to establish
        time.sleep(0.5)

        return client_id

    def send_message(self, message: str, client_id=None) -> str:
        """Send a message through the WebSocket and wait for response"""
        # Ensure we have a connection
        if client_id is None or client_id not in self.ws_connections:
            client_id = self.connect(client_id)

        # Reset previous response
        self.responses[client_id] = None

        # Send the message
        try:
            ws = self.ws_connections[client_id]
            ws.send(json.dumps({"text": message, "user_id": client_id}))

            # Wait for response with timeout
            start_time = time.time()
            while self.responses[client_id] is None:
                time.sleep(0.1)
                if time.time() - start_time > 30:  # 30-second timeout
                    return "Error: Response timeout"

            # Get the response
            response = self.responses[client_id]
            self.responses[client_id] = None

            # Update chat history
            self.update_chat_history(message, response, client_id)

            print(f"Response: {response}")

            return response

        except Exception as e:
            print(f"Error sending message: {str(e)}")
            return f"Error: {str(e)}"

    def get_chat_history(self, client_id=None):
        if "chat_histories" not in st.session_state:
            st.session_state.chat_histories = {}

        if client_id not in st.session_state.chat_histories:
            st.session_state.chat_histories[client_id] = []

        return st.session_state.chat_histories[client_id]

    def update_chat_history(self, message, response, client_id):
        history = self.get_chat_history(client_id)
        history.append({"message": message, "response": response})
        st.session_state.chat_histories[client_id] = history

    def close(self, client_id=None):
        """Close WebSocket connection"""
        if client_id is None:
            # Close all connections
            for cid, ws in list(self.ws_connections.items()):
                try:
                    ws.close()
                except:
                    pass
            self.ws_connections = {}
        elif client_id in self.ws_connections:
            # Close specific connection
            try:
                self.ws_connections[client_id].close()
            except:
                pass
            del self.ws_connections[client_id]

    def register_message_callback(self, client_id, callback):
        """Register a callback for incoming messages"""
        self.message_callbacks[client_id] = callback
