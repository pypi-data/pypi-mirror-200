import setuptools
import os

try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = ''

setuptools.setup(
    name="HealthCheckIOAPI",
    version="1.0.1",
    author="Felix Hernandez",
    description="Simple Python Tooling to interact with Healthcheck.io projects.",
    packages=["healthcheckio"],
    install_requires=["requests"],
    url="https://github.com/basegodfelix/healthcheckioapi",
    long_description = long_description,
    long_description_context_type = 'text/markdown',
    license="MIT"
)