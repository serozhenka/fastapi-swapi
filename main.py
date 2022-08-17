from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_pagination import LimitOffsetPage, add_pagination, paginate
from tortoise.contrib.fastapi import register_tortoise

from constants import DATABASE_URL, THROTTLE_MINUTES
from models import CsvFile, CsvFile_Pydantic
from tasks import fetch_characters_create_csv
from utils import (
    update_last_fetch,
    minutes_since_last_fetch,
)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/csv_files", StaticFiles(directory="csv_files"), name="csv_files")
templates = Jinja2Templates(directory="templates")


async def get_by_filename_or_error(filename: str):
    if not await CsvFile.filter(filename=filename).count():
        raise HTTPException(status_code=404, detail=f"Csv File '{filename}' not found")
    return await CsvFile.get(filename=filename)


@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get('/fetches')
async def fetches_page(request: Request):
    return templates.TemplateResponse("fetches.html", {"request": request})


@app.get('/fetches/{filename}')
async def fetches_page(request: Request, file: CsvFile = Depends(get_by_filename_or_error)):
    return templates.TemplateResponse("fetch_detail.html", {
        "request": request,
        "filename": file.filename,
    })


@app.get('/fetches/{filename}/count')
async def fetches_page(request: Request, file: CsvFile = Depends(get_by_filename_or_error)):
    return templates.TemplateResponse("fetch_detail_value_count.html", {
        "request": request,
        "filename": file.filename,
    })


@app.get("/fetch/characters")
async def fetch_characters():
    if await minutes_since_last_fetch() >= THROTTLE_MINUTES:
        await update_last_fetch()
        fetch_characters_create_csv.delay()
        return {'status': 'success', 'detail': 'Fetch started'}
    return {'status': 'error', 'detail': 'Fetch declined. Too many requests.'}


@app.get("/fetch/since_last")
async def since_last_fetch_datetime():
    return {'status': 'success', 'minutes': await minutes_since_last_fetch()}


@app.get("/fetch/all", response_model=LimitOffsetPage[CsvFile_Pydantic])
async def all_fetches():
    fetches = await CsvFile.all()
    return paginate(fetches)


@app.get("/fetch/{filename}", response_model=CsvFile_Pydantic)
async def fetch_page(file: CsvFile = Depends(get_by_filename_or_error)):
    return await CsvFile.get(filename=file.filename)


add_pagination(app)

register_tortoise(
    app,
    db_url=DATABASE_URL,
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
