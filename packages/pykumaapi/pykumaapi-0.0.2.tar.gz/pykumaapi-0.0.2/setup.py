from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["certifi>=2022",
"charset-normalizer>=3",
"idna>=3",
"requests>=2.28",
"urllib3>=1.26"
]

setup(
    name="pykumaapi",
    version="0.0.2",
    author="Artur Kondakov",
    author_email="arthurkondakov@yandex.ru",
    description="A package to connect KUMA (SIEM)",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/arthurkondakov/pykumaapi/",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)