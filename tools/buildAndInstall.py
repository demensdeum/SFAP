from commands import run
import os

run("""
python -m mypy src\\SFAP
""")

os.chdir("src")

run("""
pip install .
python -m mypy --install-types SFAP
""")

