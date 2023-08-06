# command line: pip install -e . (use for development)
# command line: pip install .
# command line: python setup.py build
# command line: python setup.py install
# command line: python setup.py develop
# command line: python setup.py sdist

# upload to https://pypi.org
# python setup.py sdist bdist_wheel
# twine upload dist/*

import setuptools

from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    
    long_description = fh.read()


# read the contents of your README file
# from pathlib import Path
# this_directory = Path(__file__).parent
# long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="qsolve",
    version="0.1.9",
    author="Jan-Frederik Mennemann",
    author_email="jfmennemann@gmx.de",
    description="qsolve",
    # long_description=read('README.md'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    # license="MIT",
    keywords="ultracold atoms, simulations, Gross-Pitaevskii equation, thermal state sampling, time of flight",
    # url = "http://packages.python.org/an_example_pypi_project",
    url = "https://github.com/jfmennemann/qsolve",
    packages=find_packages(where="qsolve"),
    package_dir={"": "qsolve"},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 2 - Pre-Alpha",
        "Operating System :: POSIX :: Linux"
    ]
)
