import logging

import uvicorn
from fastapi import FastAPI

from src.api import router
from src.config import Config

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=Config.port)
