from setuptools import find_packages, setup
from pathlib import Path

CURRENT_DIR = Path(__file__).parent

REQUIREMENTS_BASE_PATH = CURRENT_DIR / "requirements/base.txt"
REQUIREMENTS_BASE = REQUIREMENTS_BASE_PATH.read_text().splitlines()

setup(
    name='flask_augmentations',
    version='0.0.1',
    package_dir = {'': 'src'},
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS_BASE,
)