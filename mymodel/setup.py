from setuptools import find_packages, setup


REQUIREMENTS = [
    # "Pillow>=8.2.0",
    "numpy>=1.20.3",
    "albumentations>=1.0.0",
]

setup(
    name="mymodel",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
)
