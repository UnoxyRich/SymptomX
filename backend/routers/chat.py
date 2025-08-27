
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..models import ChatRequest, ChatResponse
from ..providers.logic import chat_reply, triage_message

router = APIRouter(tags=["chat"])

@router.post("/api/chat", response_model=ChatResponse)
def chat_http(req: ChatRequest):
    reply = chat_reply(req.message)
    return ChatResponse(reply=reply)

@router.websocket("/ws/chat")
async def chat_ws(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            msg = await ws.receive_text()
            reply = chat_reply(msg)
            await ws.send_text(reply)
    except WebSocketDisconnect:
        return
