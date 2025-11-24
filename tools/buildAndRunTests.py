from commands import run
import os

commands = """
python ./tools/build.py
python ./src/main.py
"""

os.chdir("tests")
os.chdir("Weather")

delay = 10
browser_headless_mode = "False"

run(f"""
python ./Weather.py https://www.accuweather.com/ accuweather-weather.html {delay}  {browser_headless_mode}
python ./Weather.py https://www.google.com/search?q=weather google-weather.html {delay}  {browser_headless_mode}
python ./Weather.py https://www.bing.com/search?q=weather bing-weather.html {delay} {browser_headless_mode}
python ./Weather.py https://ya.ru/search/?text=weather yandex-weather.html {delay} {browser_headless_mode}
python ./Weather.py https://www.gismeteo.ru/ gismeteo-weather.html {delay} {browser_headless_mode}
""")
