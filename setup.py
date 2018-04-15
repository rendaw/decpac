from setuptools import setup

GEN_version = '0.0.4'
READ_name = 'decpac'

setup(
    name=READ_name,
    version=GEN_version,
    author='rendaw',
    url='https://github.com/rendaw/decpac',
    download_url='https://github.com/rendaw/decpac/tarball/v{}'.format(
        GEN_version),
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
