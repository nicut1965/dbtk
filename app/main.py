from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.routers import records, import_excel


app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(records.router, tags=["Records"])
app.include_router(import_excel.router, tags=["Import"])

@app.get("/")
def root():
    return RedirectResponse(url="/records")

