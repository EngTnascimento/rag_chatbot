import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import router
from chat.routers.chat_routers import router as chat_router
from chat.routers.processor_routers import router as processor_router

# Create FastAPI instance
app = FastAPI(title="Chat API", description="API for chat services", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router)
app.include_router(processor_router)


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    # Run the application on port 800
    uvicorn.run("main:app", host="0.0.0.0", port=800, reload=True)
