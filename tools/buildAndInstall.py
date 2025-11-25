from commands import run
import os

run("""
py -m mypy --strict --python-version 3.9 src/SFAP
""")

os.chdir("src")

run("""
pip install -e .
""")

