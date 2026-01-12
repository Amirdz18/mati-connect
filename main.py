from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# =========================
# APP
# =========================

app = FastAPI(
    title="mati-connect",
    description="Serveur central de communication médicale",
    version="1.0.0",
)

# =========================
# CORS (web + mobile)
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # à restreindre plus tard
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# ROUTES DE BASE (OBLIGATOIRES)
# =========================

@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "mati-connect",
        "message": "server online"
    }

@app.get("/health")
def health():
    return {"health": "ok"}

# =========================
# DÉMARRAGE (NE DOIT PAS CRASH)
# =========================

@app.on_event("startup")
def startup_event():
    print("🚀 mati-connect server started")

# =========================
# NOTE IMPORTANTE
# =========================
# ❌ PAS de uvicorn.run()
# ❌ PAS de if __name__ == "__main__"
# 👉 Railway lance le serveur avec la Start Command
