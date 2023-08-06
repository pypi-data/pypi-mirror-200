import os

import uvicorn
from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.middleware.cors import CORSMiddleware

from lndb_rest.routers import account, instance, introspection, run, file

port = int(os.getenv("PORT", 8000))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(account.router)
app.include_router(instance.router)
app.include_router(introspection.router)
app.include_router(run.router)
app.include_router(file.router)

client = TestClient(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
