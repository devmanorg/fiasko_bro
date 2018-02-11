from setuptools import setup
from setuptools.command.install import install
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))


def load_requirements():
    return open(path.join(path.dirname(__file__), 'requirements.txt')).readlines()


class InstallWithCompile(install):
    def run(self):
        from babel.messages.frontend import compile_catalog
        compiler = compile_catalog(self.distribution)
        option_dict = self.distribution.get_option_dict('compile_catalog')
        compiler.domain = [option_dict['domain'][1]]
        compiler.directory = option_dict['directory'][1]
        compiler.run()
        super().run()


setup(
    name='Fiasko Bro',

    version='0.0.1',

    description='Automatic code validator',
    long_description='The project validates for common pitfalls',  # TODO: generate README

    url='https://github.com/devmanorg/fiasko_bro',

    license='MIT',

    # TODO: Author details
    # author='yourname',
    # author_email='your@address.com',

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

    # TODO: Keywords
    # keywords='sample setuptools development',

    packages=['fiasko_bro'],
    # since babel appears both in setup_requires and install_requires,
    # our package can't be instaled with python setup.py install command
    # see https://github.com/pypa/setuptools/issues/391
    setup_requires=['babel'],
    install_requires=load_requirements(),
    cmdclass = {
        'install': InstallWithCompile,
    },
    package_data={'': ['locale/*/*/*.mo', 'locale/*/*/*.po']},
)
