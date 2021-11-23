from setuptools import setup, find_packages

setup(
    name="edc",
    version="0.0.1",
    description="Package utilisé pour l'étude de cas Ekimetrics",
    author="Pauline BERBERI",
    packages=find_packages(), #où se situent les packages à importer : dans le dossier. remplace "find package in src"
)