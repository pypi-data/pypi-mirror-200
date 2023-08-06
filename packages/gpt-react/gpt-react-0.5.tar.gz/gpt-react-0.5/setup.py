from setuptools import setup, find_packages

setup(
    name="gpt-react",
    version="0.5",
    packages=find_packages(),
    entry_points={"console_scripts": ["gpt-react = react:main"]},
    install_requires=["openai", "httpx"],
)
