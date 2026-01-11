
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers import api

app = FastAPI(title="ResearchMate API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(api.router)

@app.get("/")
def read_root():
    return {"message": "ResearchMate Backend API is running (Refactored)"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
