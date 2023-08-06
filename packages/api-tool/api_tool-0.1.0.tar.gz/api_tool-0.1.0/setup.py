from setuptools import setup, find_packages

setup(
    name='api_tool',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'api-tool=api_tool.__main__:main',
        ],
    },
)
