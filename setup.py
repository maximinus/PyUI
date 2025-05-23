from setuptools import setup, find_packages

setup(
    name="pyui",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "pyui": ["assets/**/*"],
    },
    install_requires=[],
    author="Chris Handy",
    author_email="maximinus@gmail.com",
    description="A Python UI library",
    long_description=open("LICENSE").read(),
    license="GPLv3",
    keywords="ui, python",
    url="https://github.com/maximinus/PyUI"
)
