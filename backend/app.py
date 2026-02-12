from fastapi import FastAPI
from routes.ocr_routes import router as ocr_router

app = FastAPI()

app.include_router(ocr_router)

@app.get("/")
def root():
    return {"status": "server running"}
