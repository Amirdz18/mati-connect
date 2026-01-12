from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from database import SessionLocal, engine
from models import Base, Doctor, Message
from auth import hash_password, verify_password, create_token, decode_token
from pydantic import BaseModel
from datetime import datetime

Base.metadata.create_all(bind=engine)

app = FastAPI(title="mati-connect")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_doctor(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_token(token)
        doctor = db.query(Doctor).filter(Doctor.id == payload["id"]).first()
        if not doctor:
            raise HTTPException(status_code=401)
        return doctor
    except:
        raise HTTPException(status_code=401)

class RegisterSchema(BaseModel):
    email: str
    password: str
    full_name: str

class LoginSchema(BaseModel):
    email: str
    password: str

class MessageSchema(BaseModel):
    receiver_id: int
    content: str

@app.post("/register")
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    if db.query(Doctor).filter(Doctor.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    doctor = Doctor(
        email=data.email,
        password_hash=hash_password(data.password),
        full_name=data.full_name
    )
    db.add(doctor)
    db.commit()
    return {"message": "Compte créé"}

@app.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.email == data.email).first()
    if not doctor or not verify_password(data.password, doctor.password_hash):
        raise HTTPException(status_code=401, detail="Login incorrect")
    token = create_token({"id": doctor.id})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/messages")
def send_message(
    data: MessageSchema,
    doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    msg = Message(
        sender_id=doctor.id,
        receiver_id=data.receiver_id,
        content=data.content
    )
    db.add(msg)
    db.commit()
    return {"message": "Envoyé"}

@app.get("/messages")
def get_messages(
    doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    msgs = db.query(Message).filter(
        Message.receiver_id == doctor.id
    ).order_by(Message.created_at.desc()).all()

    return [
        {
            "from": m.sender_id,
            "content": m.content,
            "date": m.created_at
        }
        for m in msgs
    ]
