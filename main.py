from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from tortoise.contrib.fastapi import register_tortoise

from constants import DATABASE_URL, THROTTLE_MINUTES
from models import CsvFile, LastFetch
from tasks import fetch_characters_create_csv
from utils import (
    update_last_fetch,
    minutes_since_last_fetch,
)


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/fetch/characters")
async def fetch_characters():
    if await minutes_since_last_fetch() >= THROTTLE_MINUTES:
        await update_last_fetch()
        fetch_characters_create_csv.delay()
        return {'status': 'success', 'detail': 'Fetch started'}
    return {'status': 'error', 'detail': 'Fetch declined. Too many requests'}


@app.get("/fetch/since_last")
async def since_last_fetch_datetime():
    return {'minutes': await minutes_since_last_fetch()}

register_tortoise(
    app,
    db_url=DATABASE_URL,
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


