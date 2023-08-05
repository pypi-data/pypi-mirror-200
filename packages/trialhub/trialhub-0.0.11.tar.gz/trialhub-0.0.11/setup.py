import os
from setuptools import setup, find_packages

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname), "r", encoding="utf-8") as fh:
        return fh.read()
    
setup(
    name='trialhub',
    version='0.0.11',
    description='Helper modules for TrialHub project',
    author='FindMeCure team',
    author_email='ivo@findmecure.com',
    url='https://github.com/IvayloYosifov/trialhub-helpers',
    packages=['trialhub'],    
    package_data={'trialhub':['config.json']},
    install_requires=read("requirements.txt"),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
# py_modules=['vector_db', 'helper', 'azure_storage', 'pubmed_entrez', 'pubmed_download', 'open_ai'],