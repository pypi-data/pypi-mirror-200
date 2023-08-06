from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = [
    "streamlit",
    'shillelagh==1.1.5',
    'shillelagh[gsheetsapi]'
]

setup(
    name="StreamHelper",
    version="0.3.0",
    author="Tao Xiang",
    author_email="tao.xiang@tum.de",
    description="A package of RL algorithms",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/leoxiang66/streamlit-apps/tree/toolkit",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
  "Programming Language :: Python :: 3.10",
  "License :: OSI Approved :: MIT License",
    ],
)