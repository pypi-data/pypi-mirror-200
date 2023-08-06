from setuptools import setup, find_packages

with open("../README.md", "r") as fh:
    long_description = fh.read()

setup(    
    name="gamepandas",
    version="0.0.3",
    keywords=("payoff-table","pandas", "game-theory","nash"),
    description="A pandas extension package for payoff table utility in game theory.",
    long_description=long_description,
    long_description_content_type="text/markdown",   
    license="MIT Licence",

    url="https://github.com/Algebra-FUN/GamePandas",
    author="Algebra-FUN",
    author_email="algebra-fun@outlook.com",
  
    packages=find_packages(),
    include_package_data=True,
    platforms="linux",   
    install_requires=['numpy', 'pandas', 'scipy', 'IPython'],
    python_requires='>=3.8'
)