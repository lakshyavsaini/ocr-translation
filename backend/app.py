from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.ocr_routes import router as ocr_router

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # Local development
        "http://localhost:8000",      # Local backend
        "https://*.vercel.app",       # Vercel deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ocr_router)

@app.get("/")
def root():
    return {"status": "server running"}
