import csv
import requests

from datetime import datetime
from constants import csv_headers


def parse_and_format_date_str(date_string: str) -> str:
    edited = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    return edited.strftime('%Y-%m-%d')


def get_data_list_from_character(character: dict, planets: dict) -> list:
    return [
        character.get('name'),
        character.get('height'),
        character.get('mass'),
        character.get('hair_color'),
        character.get('skin_color'),
        character.get('eye_color'),
        character.get('birth_year'),
        character.get('gender'),
        planets.get(character.get('homeworld')),
        parse_and_format_date_str(character.get('edited')),
    ]


def fetch_characters(characters_url: str) -> list[dict]:
    characters = []
    while characters_url:
        response = requests.get(characters_url + "?page=4")
        characters_url = response.json().get('next')
        characters.extend(response.json()['results'])
        break
    return characters


def fetch_planets(planets_url: str) -> dict[str, str]:
    planets = {}
    while planets_url:
        response = requests.get(planets_url)
        planets_url = response.json().get('next')
        planets.update({
            planet.get('url'): planet.get('name')
            for planet in response.json()['results']
        })
    return planets


def write_characters_to_csv(characters: list, planets: dict) -> None:
    with open('csv.csv', 'w', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(csv_headers)

        for character in characters:
            row = get_data_list_from_character(character, planets)
            csv_writer.writerow(row)

