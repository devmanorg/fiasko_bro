from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))


def load_requirements():
    return open(join(dirname(__file__), 'requirements.txt')).readlines()


setup(
    name='Fiasko Bro',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # http://packaging.python.org/en/latest/tutorial.html#version
    version='0.0.1',

    description='Automatic code validator',
    long_description='The project validates for common pitfalls',  # TODO: generate README

    # TODO: The project's main homepage.
    # url='https://github.com/whatever/whatever',

    # TODO: Author details
    # author='yourname',
    # author_email='your@address.com',

    # TODO: Choose your license
    # license='MIT',

    # See https://PyPI.python.org/PyPI?%3Aaction=list_classifiers
    # TODO: Classifiers
    # classifiers=[
    #     # How mature is this project? Common values are
    #     #   3 - Alpha
    #     #   4 - Beta
    #     #   5 - Production/Stable
    #     'Development Status :: 3 - Alpha',

        # # Indicate who your project is intended for
        # 'Intended Audience :: Developers',
        # 'Topic :: Software Development :: Build Tools',

        # # Pick your license as you wish (should match "license" above)
        # 'License :: OSI Approved :: MIT License',

    #     # Specify the Python versions you support here. In particular, ensure
    #     # that you indicate whether you support Python 2, Python 3 or both.
    #     'Programming Language :: Python :: 2.7',
    # ],

    # What does your project relate to?
    # keywords='sample setuptools development',

    packages=['fiasko_bro'],
    install_requires=load_requirements(),
)
