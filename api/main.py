from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api.routes import books, magazines, authors, chatbot, search
from utils.logger import setup_logging

# Initialize app
app = FastAPI(title="Library Chatbot API", version="1.0.0")
setup_logging()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(books.router, prefix="/api/books", tags=["books"])
app.include_router(magazines.router, prefix="/api/magazines", tags=["magazines"])
app.include_router(authors.router, prefix="/api/authors", tags=["authors"])
app.include_router(chatbot.router, prefix="/api/chat", tags=["chatbot"])
app.include_router(search.router, prefix="/api/search", tags=["search"])

# Serve frontend
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
