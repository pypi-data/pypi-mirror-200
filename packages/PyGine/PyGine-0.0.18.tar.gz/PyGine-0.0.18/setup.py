from setuptools import setup, find_packages


VERSION = '0.0.18'
DESCRIPTION = 'A simple 2D game engine'
LONG_DESCRIPTION = 'A simple 2D game engine working as unity but in python'

# Setting up
setup(
    name="PyGine",
    version=VERSION,
    author="PyGIne (Ronan.T)",
    author_email="<ronan.tremoureux@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pygame'],
    keywords=['python', 'game', 'engine', 'moteur', 'jeu', 'GameEngine','PyGine','PyGineGame',"pygame","componentGame","component","gameEngine","game","engine","2D","2DGame","2DGameEngine","2DGameEnginePython","2DGameEnginePygame","2DGameEnginePyGine","PyGineGameEngine","PyGineGameEnginePython","PyGineGameEnginePygame","PyGineGameEnginePyGine"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)