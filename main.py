import uvicorn
from fastapi import FastAPI

from core.settings import settings
from api import router as router_v1

app = FastAPI()

app.include_router(router=router_v1, prefix=settings.api_prefix)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)