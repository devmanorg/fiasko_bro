from setuptools import setup, find_packages
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

    version='0.0.1.1',

    description='Automatic code validator',
    long_description='The project validates for common pitfalls',  # TODO: generate README

    url='https://github.com/devmanorg/fiasko_bro',

    license='MIT',

    author='Ilya Lebedev',
    author_email='melevir@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Quality Assurance',
    ],

    keywords='static code analysis code quality',

    packages=find_packages(),
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
