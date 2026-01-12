import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# imports locaux (ne change pas ces fichiers)
from database import init_db

app = FastAPI(
    title="mati-connect",
    description="Serveur central mati-connect (cabinet médical)",
    version="1.0.0"
)

# ===============================
# CORS (important pour future app mobile)
# ===============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # plus tard on restreindra
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================
# ROUTES DE TEST (OBLIGATOIRES)
# ===============================
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

# ===============================
# INIT DATABASE
# ===============================
@app.on_event("startup")
def on_startup():
    init_db()

# ===============================
# LANCEMENT (RAILWAY COMPATIBLE)
# ===============================
if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )
