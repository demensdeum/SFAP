from commands import run
import os

run("""
py -m mypy src/SFAP
""")

os.chdir("src")

run("""
pip install -e .
py -m mypy --install-types
""")

