from setuptools import setup, find_packages

VERSION = '0.1.6' 
DESCRIPTION = 'Simple colored debug prints'
LONG_DESCRIPTION = 'Colored print functions like info, warn and error'

setup(
        name="colored_debug_prints", 
        version=VERSION,
        author="Leon",
        author_email="leonwagner09@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["colorama"],
        
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
