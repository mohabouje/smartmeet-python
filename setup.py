from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='smartmeet',
    version='0.0.1',
    description='A DSP framework to build voice enabled applications',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://bitbucket.org/smartmeet/smartmeet-research-python/',
    author='Mohammed Boujemaoui',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='audio, smart-speakers, vad, speech-recognition, speech-processing',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=requirements,
    entry_points={ 
        'console_scripts': [
        ],
    },
    project_urls={  
        'Bug Reports': '',
        'Funding': '',
        'Say Thanks!': '',
        'Source': '',
    },
)

