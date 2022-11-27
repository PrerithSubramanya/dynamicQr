import uvicorn
from fastapi import FastAPI
from routes import router


description = """
This is a simple website to create dynamic QR codes and route to destined page whenever required

"""

app = FastAPI(
    title="Qlub's Dynamic Qr Station",
    description=description,
    version="0.01",
    contact={"name": "Prerith Subramanya", "email": "prerith.subramanya@qlub.io"},
)

app.include_router(router)
