from setuptools import setup

setup(
    name="huddu",
    version="1.1.11",
    packages=["huddu"],
    url="https://github.com/hudduapp/huddu-python",
    requires=["json", "requests", "pyjwt"],
    license="MIT",
    author="Joshua3212",
    author_email="hello@huddu.io",
    description="Python SDK for Huddu",
)
