from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'My first Python package'
LONG_DESCRIPTION = 'My first Python package with a slightly longer description'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="emailcrawl", 
        version="0.1",
        author="RagGar",
        author_email="<raghavgarg121212@gmail.com>",
        description="Scrap emails from websites",
        long_description="Scrap emails from websites",
        packages=find_packages(),
        install_requires=['requests-html','bs4','pandas'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)