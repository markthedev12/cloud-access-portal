from fastapi import FastAPI

app = FastAPI(
    title="CloudAccess Portal API",
    description="An internal developer portal for secure IAM and cloud access requests.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"status": "online", "message": "Welcome to the CloudAccess Portal API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "backend-api"}