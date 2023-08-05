import os
from pathlib import Path

from setuptools import find_packages, setup

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="django_dnoticias_services",
    version='1.0.97',
    url="https://www.dnoticias.pt/",
    author="Pedro Mendes",
    author_email="pedro.trabalho.uma@gmail.com",
    maintainer="Nélson Gomes",
    maintainer_email="ngoncalves@dnoticias.pt",
    license="MIT",
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'requests',
        'django',
        'python-keycloak',
        'mozilla-django-oidc'
    ],
    include_package_data=True,
    packages=find_packages(),
    data_files=[('dnoticias_services', [str(path) for path in Path('./dnoticias_services/templates').rglob('*')  if os.path.isfile(str(path))])]
)
