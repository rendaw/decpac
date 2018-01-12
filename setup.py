from setuptools import setup

setup(
    name='decpac',
    version='0.0.1',
    author='rendaw',
    url='https://github.com/rendaw/decpac',
    download_url='https://github.com/rendaw/decpac/tarball/v0.0.1',
    license='MIT',
    description='Arch Linux declarative package management',
    long_description=open('readme.md', 'r').read(),
    classifiers=[],
    py_modules=['decpac'],
    install_requires=[
        'luxem==0.0.2',
    ],
    entry_points={
        'console_scripts': [
            'decpac=decpac:main',
        ],
    },
)
