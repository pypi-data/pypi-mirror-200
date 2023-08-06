from setuptools import setup, find_packages

setup(
    name="gpt-react",
    version="0.1",
    packages=find_packages(),
    entry_points={"console_scripts": ["gpt-react = main:main"]},
    install_requires=["openai", "httpx"],
)
