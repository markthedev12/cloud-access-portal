from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import hashlib

from backend.database import get_db
from backend.models import User
from backend.schemas import UserCreate, UserResponse

app = FastAPI(
    title="CloudAccess Portal API",
    description="An internal developer portal for secure IAM and cloud access requests.",
    version="1.0.0"
)

# Simple helper function to hash passwords for now 
# (We'll upgrade this to bcrypt/Passlib later!)
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@app.get("/")
def read_root():
    return {"status": "online", "message": "Welcome to the CloudAccess Portal API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "backend-api"}

@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # 1. Check if user already exists by email
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered in the CloudAccess Portal"
        )
    
    # 2. Create the new user model instance
    hashed_pwd = hash_password(user.password)
    new_user = User(
        email=user.email,
        hashed_password=hashed_pwd,
        full_name=user.full_name
    )
    
    # 3. Add to session, commit to database, and refresh
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user