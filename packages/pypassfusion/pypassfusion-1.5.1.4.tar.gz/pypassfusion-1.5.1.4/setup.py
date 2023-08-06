from setuptools import setup, find_packages

VERSION = '1.5.1.4'
DESCRIPTION = 'The password generator Python app is a simple and efficient tool for creating strong and secure passwords'

# Setting up
setup(
    name="pypassfusion",
    version=VERSION,
    author="Amir Hossein Bonyadi",
    author_email="bonyadi.amirhosein@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['tk'],
    keywords=['python', 'password', 'generator', 'Passgenerator', 'pypassgenerator'],
    entry_points={
        'console_scripts': [
            'pyfusion=pypassfusion.main:main',
        ],
    },
    classifiers=[
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
    ]
)
