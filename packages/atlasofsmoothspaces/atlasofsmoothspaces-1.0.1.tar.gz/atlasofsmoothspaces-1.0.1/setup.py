from setuptools import setup, find_packages

VERSION = '1.0.1' 
DESCRIPTION = 'Calculating Smoothness from Input Stream'
LONG_DESCRIPTION = 'Smoothness is calculated from an input stream. The input data format is midi.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="atlasofsmoothspaces", 
        version=VERSION,
        author="Leonhard horstmeyer",
        author_email="<leonhard.horstmeyer@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['smoothness', 'midi'],
        classifiers= [
            "Programming Language :: Python :: 3",
            "Operating System :: POSIX :: Linux"
        ]
)