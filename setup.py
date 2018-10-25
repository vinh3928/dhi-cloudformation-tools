from os import path
from setuptools import setup, find_packages
from cfn import version


def get_long_description():
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, 'README.md'), encoding='utf-8') as file:
        long_description = file.read()
    return long_description


setup(
    name='cfn',
    version=version.__version__,
    description='DHI CloudFormation Tools',
    long_description=get_long_description(),
    url='https://github.com/DiceHoldingsInc/dhi-cloudformation-tools',
    author='DiceHoldingsInc',
    author_email='cloud.platform.engineering@dhigroupinc.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities'
    ],
    keywords='aws cloudformation deploy',
    project_urls={
        'Bug Reports': 'https://github.com/DiceHoldingsInc/dhi-cloudformation-tools/issues',
        'Source': 'https://github.com/DiceHoldingsInc/dhi-cloudformation-tools',
    },
    packages=find_packages(exclude=['code', 'infrastructure', 'tests']),
    install_requires=[
        'awscli >= 1.16',
        'botocore >= 1.12'
    ],
    python_requires='>=3',
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage']
    },
    entry_points={
        'console_scripts': [
            'cfn=cfn.main:main',
        ]
    },
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
)
