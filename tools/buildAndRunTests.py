from commands import run
import os

run("""
python ./tools/buildAndInstall.py
python -m mypy --install-types
python -m mypy tests/Weather
""")

os.chdir("tests")
os.chdir("Weather")

delay = 2
browser_headless_mode = "True"

run(f"""
python ./Weather.py https://www.accuweather.com/ accuweather-weather.html {delay}  {browser_headless_mode}
python ./Weather.py https://www.google.com/search?q=weather google-weather.html {delay}  {browser_headless_mode}
python ./Weather.py https://www.bing.com/search?q=weather bing-weather.html {delay} {browser_headless_mode}
python ./Weather.py https://ya.ru/search/?text=weather yandex-weather.html {delay} {browser_headless_mode}
python ./Weather.py https://www.gismeteo.ru/ gismeteo-weather.html {delay} {browser_headless_mode}
""")
