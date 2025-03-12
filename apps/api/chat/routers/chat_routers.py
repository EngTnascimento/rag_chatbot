from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from chat.agents import RAGAgent
from libs.common.websocket import manager, MessageRequest
import logging

router = APIRouter(tags=["chat"])
logger = logging.getLogger(__name__)


def get_rag_agent():
    return RAGAgent()


rag_agent = RAGAgent()


@router.websocket("/ws/chat/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    connection_id = await manager.connect(websocket, user_id)
    print(f"Client connected: user_id={user_id}, connection_id={connection_id}")

    try:
        while True:
            print("Waiting for message...")
            # Receive message from client
            data = await websocket.receive_json()
            message = MessageRequest(**data)

            print(f"Message: {message}")
            # Process message and get response
            response = await rag_agent.chat(message.text, message.user_id)
            print(f"Answer: {response}")

            # Send response back to client
            await websocket.send_json({"answer": response})

    except WebSocketDisconnect:
        print(f"Client disconnected: user_id={user_id}")
    except Exception as e:
        print(f"Error processing message: {str(e)}")
        try:
            await websocket.send_json({"error": f"Failed to process message: {str(e)}"})
        except:
            pass  # Connection might be already closed
    finally:
        # Clean up
        await manager.disconnect(websocket, user_id)


@router.get("/connections")
async def get_connection_stats():
    """Get stats about active connections"""
    total = manager.get_connection_count()
    users = {
        user_id: len(connections)
        for user_id, connections in manager.active_connections.items()
    }

    return {"total_connections": total, "user_connections": users}


@router.get("/connections/{user_id}")
async def get_user_connections(user_id: str):
    """Get connection count for a specific user"""
    count = manager.get_connection_count(user_id)
    return {"user_id": user_id, "connection_count": count}
