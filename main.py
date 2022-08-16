import utils

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from constants import characters_url, planets_url


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/fetch_characters")
async def fetch_characters():
    characters = utils.fetch_characters(characters_url)
    planets = utils.fetch_planets(planets_url)
    utils.write_characters_to_csv(characters, planets)

    return characters





