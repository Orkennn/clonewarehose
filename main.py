import uvicorn

from core.settings import settings
from api import router as router_v1
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = FastAPI()

app.include_router(router=router_v1, prefix=settings.api_prefix)


templates = Jinja2Templates(directory="templates")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return templates.TemplateResponse("error.html", {"request": request, "error": str(exc)})


@app.post("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

