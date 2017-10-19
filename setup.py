from setuptools import setup

import elife_api_validator

setup(
    name='api-validator-python',
    version=elife_api_validator.__version__,
    description='Utility for accessing and validating eLife API JSON Schemas.',
    packages=['elife_api_validator'],
    package_data={
        'elife_api_validator/schemas': '*.json'
    },
    license='MIT',
    url='https://github.com/elifesciences/api-validator-python.git',
    maintainer='eLife Sciences Publications Ltd.',
    maintainer_email='tech-team@elifesciences.org',
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
    ]
)
