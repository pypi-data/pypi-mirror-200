from setuptools import setup, find_packages

VERSION = '3.0.0'
DESCRIPTION = "A Python3 package to Manage fonts and customize fonts in the terminal."
LONG_DESCRIPTION = "A Python3 package to Manage fonts and customize fonts in the terminal."

# Setting up
setup(
    name="pipfont",
    version=VERSION,
    author="ЕntchenBuilds",
    author_email="ЕntchenBuilds@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python'],
    classifiers=[
        "Operating System :: Microsoft :: Windows",
    ]
)