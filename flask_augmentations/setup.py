from setuptools import find_packages, setup


REQUIREMENTS = [
    "Flask>=2.0.0",
    "requests>=2.25.0",
    "Pillow>=8.2.0",
]

setup(
    name="flask_augmentations",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
)
