import setuptools

setuptools.setup(
    name = "vanVliet_ptnsPsychExperimentsGUI",
    version = "0.0.1",
    author = "I.v.Vliet",
    author_email = "ilonka.vanvliet@student.uva.nl",
    python_requires = ">=3.6",
    install_requires=[
        "matplotlib",   # version 3.8.4 used when making this
        "PIL",          # version pillow 10.3.0 used when making this
        "pandas",       # version 2.2.2 used when making this
    ],
    packages = setuptools.find_packages()
)