from setuptools import setup

setup(
    name='decpac',
    version='0.0.1',
    author='rendaw',
    license='MIT',
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
