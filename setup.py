from setuptools import setup

GEN_version = '0.0.6'
READ_name = 'decpac'

setup(
    name=READ_name,
    version=GEN_version,
    author='rendaw',
    url='https://gitlab.com/rendaw/decpac',
    download_url='https://gitlab.com/rendaw/decpac/-/archive/v{v}/decpac-v{v}.tar.gz'.format(
        v=GEN_version),
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
