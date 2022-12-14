import asyncio
import utils

from celery import Celery, shared_task

from constants import (
    REDIS_URL,
    characters_url,
    planets_url,
)

app = Celery(broker=REDIS_URL)


@shared_task
def fetch_characters_create_csv():
    planets = utils.fetch_planets(planets_url)
    characters_generator = utils.fetch_characters(characters_url)
    filename = utils.write_characters_to_csv(characters_generator, planets)
    asyncio.get_event_loop().run_until_complete(utils.create_csv_file_model(filename))