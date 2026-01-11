from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.routers import records, import_excel
from app.database import engine, Base
# from app.models import record # IMPORTANT: Trebuie importat modelul pentru a fi "văzut" de Base
# from app.db.base import Base
# from app.db.session import engine

# IMPORTĂ TOATE MODELELE
from app.models.user import User
from app.models.record import Record
from app.models.audit_log import AuditLog

# Creează tabelele dacă nu există
Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(records.router, tags=["Records"])
app.include_router(import_excel.router, tags=["Import"])

@app.get("/")
def root():
    return RedirectResponse(url="/records")

