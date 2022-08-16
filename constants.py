from decouple import config

characters_url = 'https://swapi.dev/api/people'
planets_url = 'https://swapi.dev/api/planets'

csv_headers = [
    'Name',
    'Height',
    'Mass',
    'Hair Color',
    'Skin Color',
    'Eye Color',
    'Birth Year',
    'Gender',
    'HomeWorld',
    'Date'
]

REDIS_URL = config('REDIS_URL')

DB_NAME = config('DB_NAME')
DB_USER = config('DB_USER')
DB_PASS = config('DB_PASS')
DB_HOST = config('DB_HOST')
DB_PORT = config('DB_PORT')


DATABASE_URL = f"postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

THROTTLE_MINUTES = 0

