from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import database_module as db

# Initialize the FastAPI application
app = FastAPI(
    title="Facial Recognition Vector Engine",
    description="FastAPI gateway connecting the camera pipeline to the pgvector database.",
    version="1.0.0"
)

# Define the data structures for validation
class RegisterSchema(BaseModel):
    name: str
    embedding: list[float]

class IdentifySchema(BaseModel):
    embedding: list[float]


@app.get("/")
def root():
    """Simple health check endpoint."""
    return {"status": "online", "message": "Face Recognition API Server is running smoothly."}


@app.post("/register")
def register_face(data: RegisterSchema):
    """Web endpoint to register a new student's identity and vector."""
    if len(data.embedding) != 512:
        raise HTTPException(status_code=400, detail=f"Invalid embedding dimension. Expected 512, got {len(data.embedding)}")
    
    result = db.register_new_face(data.name, data.embedding)
    return {"status": "success", "response": result}


@app.post("/identify")
def identify_face(data: IdentifySchema):
    """Web endpoint to match a live camera vector against stored embeddings."""
    if len(data.embedding) != 512:
        raise HTTPException(status_code=400, detail=f"Invalid embedding dimension. Expected 512, got {len(data.embedding)}")
    
    result = db.identify_face(data.embedding)
    return {"status": "success", "response": result}