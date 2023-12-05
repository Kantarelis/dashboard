from setuptools import setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="dashboard",
    version="0.1.0",
    description="A dashboard demo.",
    long_description="README.md",
    url="https://github.com/Kantarelis/dashboard",
    author="Spyros Kantarelis",
    author_email="spyrosscience@gmail.com",
    install_requires=requirements,
    include_package_data=True,
    packages=[
        "dashboard",
    ],
)
